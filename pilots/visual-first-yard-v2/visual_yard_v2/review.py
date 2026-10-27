"""Static owner gallery. Displays actual output and QA results; accepts NO approval."""
from __future__ import annotations
import html,json
from pathlib import Path

PAGE='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Visual Yard V2 — Independent Test</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{background:#101922;color:#edf5f9;font:15px/1.5 system-ui;margin:0}main{max-width:1280px;margin:auto;padding:clamp(12px,3vw,25px)}h1{font-size:24px}h2{font-size:18px}section{background:#192735;border:1px solid #334d62;border-radius:14px;padding:15px;margin:16px 0}.imgs{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px}.imgs figure{margin:0}.imgs img{width:100%;background:white;border-radius:7px;display:block}.imgs figcaption{padding:6px;font-size:13px}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:7px}.metric{padding:13px;border:1px solid #405d72;border-radius:9px}.metric strong{display:block;font-size:25px}.warn{color:#ffc37e}a{color:#89cef6}
</style></head><body><main><h1>Visual-First Yard V2 · 2D tracing benchmark</h1><p>Reference image → open-source vector tracing → independent pixel QA → owner visual review. This is <strong>tracing</strong>, not a generative artistic redraw.</p>
<section><h2>Execution verdict</h2><p class="warn" id="verdict">No creative certification or owner approval.</p><div id="metrics" class="stats"></div><p><a href="qa_receipt.json">View machine-readable QA receipt</a> · <a href="result.svg">Open editable SVG</a></p></section>
<section><h2>Actual images</h2><div class="imgs"><figure><img src="reference.png" alt="Input reference"><figcaption>Input pixels (held from model)</figcaption></figure><figure><img src="result.png" alt="Traced worker output"><figcaption>Editable tracing output, rasterized</figcaption></figure><figure><img src="difference.png" alt="Pixel difference"><figcaption>Independent pixel difference</figcaption></figure></div></section>
<section><h2>Owner review</h2><p class="warn">Technical metrics do not certify facial likeness, design artistry, 3D rigging or game readiness. This page is read-only; no approval or production activation is possible.</p></section></main><script>
fetch('qa_receipt.json',{cache:'no-store'}).then(r=>r.json()).then(d=>{const m=d.metrics||{};document.getElementById('verdict').textContent=d.qa_outcome+' · '+(d.best_engine||'no renderer')+' · no creative certification';document.getElementById('metrics').innerHTML=Object.entries(m).map(([k,v])=>'<div class="metric">'+k.replace(/_/g,' ')+'<strong>'+v+'%</strong></div>').join('')}).catch(()=>{document.getElementById('verdict').textContent='Receipt missing: FAIL CLOSED'})
</script></body></html>'''

def make_review(reference: str|Path, output: str|Path):
    o=Path(output)
    ref=Path(reference)
    (o/'reference.png').write_bytes(ref.read_bytes())
    (o/'index.html').write_text(PAGE,encoding='utf-8')
