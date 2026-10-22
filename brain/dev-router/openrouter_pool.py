"""Demand-only public discovery and routing; no credentials or prompt persistence."""
import decimal, fcntl, json, os, pathlib, re, signal, sqlite3, tempfile, time, urllib.request

CATALOG_URL = 'https://openrouter.ai/api/v1/models'
TTL = 900
QA_TTL = 7 * 86400
MODEL_ID = re.compile(r'^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+:free$')

def registry(base):
    try:
        raw = (pathlib.Path(base) / 'openrouter-reviewed.json').read_bytes()
        if len(raw) > 65536: return {}
        data = json.loads(raw)['models']
        return {k: v for k, v in data.items() if MODEL_ID.fullmatch(k)
                and v.get('license') in {'Apache-2.0', 'MIT', 'BSD-3-Clause'}
                and v.get('license_verified') is True
                and isinstance(v.get('license_source'), str)
                and v['license_source'].startswith('https://')}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return {}

def classify(prompt):
    words = set(re.findall(r'[a-z]+', prompt.lower()))
    if words & {'review', 'audit', 'vulnerability', 'vulnerabilities'}: return 'review'
    if words & {'reason', 'reasoning', 'prove', 'proof', 'mathematics', 'calculate'}: return 'reasoning'
    if words & {'brief', 'quick', 'short'}: return 'fast'
    return 'coding'

def zero_price(pricing):
    if not isinstance(pricing, dict) or not {'prompt', 'completion'} <= pricing.keys(): return False
    try:
        for value in pricing.values():
            if isinstance(value, bool) or not isinstance(value, (str, int, float)): return False
            n = decimal.Decimal(str(value))
            if not n.is_finite() or n != 0: return False
        return True
    except decimal.InvalidOperation:
        return False

def normalize(data):
    result = {}
    for item in data:
        if not isinstance(item, dict): continue
        model = item.get('id', '')
        arch = item.get('architecture') or {}
        if not isinstance(arch,dict): continue
        if not isinstance(model, str) or not MODEL_ID.fullmatch(model): continue
        if not zero_price(item.get('pricing')): continue
        if 'text' not in arch.get('input_modalities', []) or 'text' not in arch.get('output_modalities', []): continue
        context = item.get('context_length')
        if type(context) is not int or context < 4096: continue
        if 'max_tokens' not in item.get('supported_parameters', []): continue
        expiry = item.get('expiration_date')
        if expiry and (not isinstance(expiry, str) or expiry <= time.strftime('%Y-%m-%d', time.gmtime())): continue
        slug = item.get('canonical_slug')
        if not isinstance(slug, str) or len(slug) > 200: continue
        result[model] = {'canonical_slug': slug, 'context_length': context}
    return result

def _cached(path):
    try:
        raw = path.read_bytes()
        if len(raw) > 1048576: return None
        d = json.loads(raw)
        if type(d.get('fetched_at')) is not int or not 0 <= time.time() - d['fetched_at'] < TTL: return None
        if not isinstance(d.get('models'), dict): return None
        return d
    except (OSError, ValueError, TypeError): return None

def catalog(base, refresh=False):
    base = pathlib.Path(base)
    path = base / 'openrouter-catalog.json'
    cached = _cached(path)
    if cached is not None and not refresh: return cached
    with (base / 'openrouter-catalog.lock').open('a') as lock:
        try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise RuntimeError('OPENROUTER_DISCOVERY_BUSY')
        cached = _cached(path)
        if cached is not None and not refresh: return cached
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs): raise RuntimeError('CATALOG_REDIRECT_DENIED')
        def deadline(*args): raise TimeoutError('CATALOG_DEADLINE')
        old = signal.signal(signal.SIGALRM, deadline); signal.alarm(10)
        try:
            req = urllib.request.Request(CATALOG_URL, headers={'User-Agent': 'BusinessHouseMatrixDev/1.0'})
            with urllib.request.build_opener(NoRedirect()).open(req, timeout=6) as response:
                raw = response.read(8388609)
            if len(raw) > 8388608: raise RuntimeError('CATALOG_TOO_LARGE')
            items = json.loads(raw)['data']
            if not isinstance(items, list): raise RuntimeError('CATALOG_INVALID')
            d = {'fetched_at': int(time.time()), 'models': normalize(items)}
            with tempfile.NamedTemporaryFile(mode='w', dir=base, prefix='.openrouter-catalog-', delete=False) as f:
                temp = pathlib.Path(f.name); json.dump(d, f); f.flush(); os.fsync(f.fileno())
            os.replace(temp, path)
            return d
        finally: signal.alarm(0); signal.signal(signal.SIGALRM, old)

def connect(db):
    c = sqlite3.connect(db, timeout=5)
    c.execute('CREATE TABLE IF NOT EXISTS openrouter_model_health(model TEXT PRIMARY KEY, canonical_slug TEXT, qa_pass INTEGER DEFAULT 0, qa_at INTEGER DEFAULT 0, provenance TEXT, latency_ms REAL DEFAULT 0, successes INTEGER DEFAULT 0, failures INTEGER DEFAULT 0, cooldown_until INTEGER DEFAULT 0)')
    c.commit()
    return c

def mark_qa(base, db, model, passed, provenance, latency_ms=0):
    if model not in registry(base): raise RuntimeError('MODEL_LICENSE_NOT_REVIEWED')
    current = catalog(base)['models'].get(model)
    if not current: raise RuntimeError('MODEL_NOT_FREE_OR_AVAILABLE')
    if current['canonical_slug'] != registry(base)[model].get('canonical_slug'): raise RuntimeError('MODEL_LICENSE_REVISION_REVIEW_REQUIRED')
    with connect(db) as c:
        c.execute('INSERT INTO openrouter_model_health(model,canonical_slug,qa_pass,qa_at,provenance,latency_ms,cooldown_until) VALUES(?,?,?,?,?,?,?) ON CONFLICT(model) DO UPDATE SET canonical_slug=excluded.canonical_slug,qa_pass=excluded.qa_pass,qa_at=excluded.qa_at,provenance=excluded.provenance,latency_ms=excluded.latency_ms,cooldown_until=excluded.cooldown_until',
                  (model,current['canonical_slug'],int(passed),int(time.time()),provenance,float(latency_ms),0 if passed else int(time.time())+900))

def record(db, model, passed, latency_ms):
    with connect(db) as c:
        c.execute('UPDATE openrouter_model_health SET successes=successes+?,failures=failures+?,latency_ms=CASE WHEN latency_ms=0 THEN ? ELSE 0.7*latency_ms+0.3*? END,cooldown_until=? WHERE model=?',
                  (int(passed),int(not passed),latency_ms,latency_ms,0 if passed else int(time.time())+900,model))

def describe(base, db, profile='coding', refresh=False):
    approved = registry(base); discovered = catalog(base, refresh)['models']; result = []
    with connect(db) as c:
        health = {r[0]:r[1:] for r in c.execute('SELECT model,canonical_slug,qa_pass,qa_at,latency_ms,successes,failures,cooldown_until FROM openrouter_model_health')}
    now = int(time.time())
    for model, metadata in discovered.items():
        state = 'license_review_pending'; score = 99999
        if model in approved:
            state = 'qa_pending'; h = health.get(model)
            if metadata['canonical_slug'] != approved[model].get('canonical_slug'): state = 'license_revision_review_pending'
            elif h and h[6] > now: state = 'model_cooldown'
            elif h and h[0] == metadata['canonical_slug'] and h[1] == 1 and 0 <= now-h[2] < QA_TTL:
                state = 'model_cooldown' if h[6] > now else 'ready'
                rank = approved[model].get('preference', {}).get(profile)
                if type(rank) is not int: state = 'profile_not_supported'
                else: score = rank + min(h[3]/1000,10 if profile=='fast' else 2) + 5*h[5]/max(1,h[4]+h[5])
        result.append({'model':model,'state':state,'score':round(score,3)})
    return sorted(result, key=lambda x:(x['score'],x['model']))

def select(base, db, profile):
    for row in describe(base, db, profile):
        if row['state'] == 'ready': return row['model']
    raise RuntimeError('NO_QUALIFIED_FREE_OPENROUTER_MODEL')

def next_probe(base, db, profile):
    approved=registry(base)
    rows=[r for r in describe(base,db,profile) if r['model'] in approved
          and r['state'] in {'ready','qa_pending'}
          and type(approved[r['model']].get('preference',{}).get(profile)) is int]
    rows.sort(key=lambda r:(approved[r['model']]['preference'][profile],r['model']))
    if rows and rows[0]['state']=='qa_pending': return rows[0]['model']
    return None
