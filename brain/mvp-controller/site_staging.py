#!/usr/bin/env python3
"""Local-only, constrained website staging compiler; never deploys to production."""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile
from datetime import datetime, timezone

ROOT = Path(os.environ.get("BHM_AUTONOMY_HOME", Path(__file__).resolve().parent)).resolve()
INBOX = ROOT / "staging-inbox"
OUTPUT = ROOT / "staging-private"
SAFE = re.compile(r"^[a-z][a-z0-9_-]{1,39}$")
ROLES = {"sauna", "ice", "mud", "aloe", "yoga", "garden", "community", "private", "arrival", "texture"}
TYPES = {".jpg": b"\xff\xd8\xff", ".jpeg": b"\xff\xd8\xff", ".png": b"\x89PNG\r\n\x1a\n", ".webp": b"RIFF"}
MAX_SIZE = 180_000

def fail(message):
    raise ValueError(message)

def name(s):
    if not isinstance(s, str) or not SAFE.fullmatch(s):
        fail("Invalid fixed slug/manifest ID")
    return s

def txt(value, limit=300):
    if not isinstance(value, str) or not value.strip() or len(value) > limit or any(ord(c) < 32 for c in value if c not in "\n\t"):
        fail("Invalid bounded plain text")
    return value.strip()

def esc(v):
    return html.escape(v, quote=True)

def read_manifest(project, manifest_id):
    name(project); name(manifest_id)
    p = INBOX / project / (manifest_id + ".json")
    if p.is_symlink() or not p.is_file() or p.stat().st_size > MAX_SIZE:
        fail("Missing/unsafe manifest")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("project") != project or data.get("version") != 1:
        fail("Project/version mismatch")
    if data.get("publish") is not False or data.get("spend") is not False:
        fail("Production and spend must be explicitly false")
    pages = data.get("pages")
    if not isinstance(pages, list) or not 1 <= len(pages) <= 12:
        fail("Expected 1-12 pages")
    slugs = []
    for page in pages:
        if not isinstance(page, dict): fail("Page must be object")
        slug = name(page.get("slug"))
        if slug in slugs: fail("Duplicate slug")
        slugs.append(slug)
        for f, limit in (("title", 90), ("eyebrow", 75), ("headline", 110), ("summary", 600)):
            txt(page.get(f), limit)
        hero = page.get("hero")
        if not isinstance(hero, dict) or hero.get("role") not in ROLES:
            fail("Hero role missing")
        txt(hero.get("label"), 110)
        sections = page.get("sections")
        if not isinstance(sections, list) or not 1 <= len(sections) <= 10:
            fail("Expected 1-10 sections")
        for section in sections:
            if not isinstance(section, dict) or section.get("role") not in ROLES:
                fail("Invalid section")
            txt(section.get("title"), 100)
            txt(section.get("text"), 850)
            txt(section.get("image_label"), 110)
        cta = page.get("cta")
        if not isinstance(cta, dict):
            fail("Missing CTA")
        txt(cta.get("label"), 65)
        name(cta.get("target"))
    if "home" not in slugs or any(p["cta"]["target"] not in slugs for p in pages):
        fail("No homepage or CTA target missing")
    asset_map = data.get("assets", {})
    if not isinstance(asset_map, dict) or len(asset_map) > 24: fail("Unsafe assets")
    for role, item in asset_map.items():
        if role not in ROLES or not isinstance(item, dict): fail("Unknown asset role")
        asset = item.get("filename")
        if not isinstance(asset, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{2,60}\.(jpg|jpeg|png|webp)", asset):
            fail("Unsafe local asset path")
        if item.get("rights_verified") is not True:
            fail("Rights must be independently verified before asset use")
        txt(item.get("source"), 350)
        txt(item.get("license"), 180)
        f = INBOX / project / "assets" / asset
        if f.is_symlink() or not f.is_file() or f.stat().st_size > 6_000_000:
            fail("Missing/unsafe asset")
        if not f.read_bytes()[:len(TYPES[f.suffix])].startswith(TYPES[f.suffix]):
            fail("File signature mismatch")
    return data, p

CSS = """
:root{--pine:#25483d;--moss:#365a46;--sand:#eee8db;--cream:#faf7f0;--ink:#253128;--muted:#667367;--accent:#bd8452;--line:#dbddd4}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:var(--cream);font:16px/1.55 system-ui,-apple-system,sans-serif}
a{color:inherit}a:focus-visible{outline:3px solid #bd8452;outline-offset:4px}
header{position:sticky;top:0;z-index:5;background:#faf7f0f5;border-bottom:1px solid var(--line)}
.wrap{width:min(1120px,calc(100% - 36px));margin:auto}.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px 0;flex-wrap:wrap}
.brand{text-decoration:none;font:bold 21px Georgia,serif;letter-spacing:.08em}.links{display:flex;gap:16px;flex-wrap:wrap}.links a{text-decoration:none;font-size:.84rem}.links a[aria-current=page]{text-decoration:underline;text-underline-offset:5px}
.pill{display:inline-block;border-radius:100px;padding:12px 21px;text-decoration:none;background:var(--pine);color:white;font-weight:650}
.hero{display:grid;grid-template-columns:1.05fr .95fr;gap:24px;align-items:center;padding:42px 0 38px}.eyebrow{color:var(--moss);font-size:.75rem;letter-spacing:.14em;text-transform:uppercase;font-weight:800}
h1,h2{font-family:Georgia,serif;line-height:1.1;font-weight:500}h1{font-size:clamp(2.65rem,6.2vw,5.1rem);margin:14px 0 22px}h2{font-size:clamp(1.75rem,3.2vw,2.7rem);margin:0 0 16px}
.intro{max-width:550px;color:#54645b;font-size:1.08rem}.photo{min-height:245px;position:relative;border-radius:18px;display:flex;align-items:end;overflow:hidden;padding:16px;color:#fff;background:linear-gradient(137deg,#506b58,#203b35 70%);isolation:isolate}
.photo::before{content:'';position:absolute;inset:9% 9% 20%;border:1px solid #ffffff63;border-radius:180px 180px 18px 18px;opacity:.55;z-index:-1}
.photo[data-role=ice]{background:linear-gradient(140deg,#7899a2,#1e4454)}.photo[data-role=mud]{background:linear-gradient(140deg,#9d795b,#483e33)}
.photo[data-role=aloe]{background:linear-gradient(140deg,#91a16b,#3d614e)}.photo[data-role=yoga]{background:linear-gradient(140deg,#c1a67c,#5f654a)}
.photo[data-role=garden]{background:linear-gradient(140deg,#8b9c6d,#254438)}.photo[data-role=arrival]{background:linear-gradient(140deg,#b39c79,#496453)}
.photo[data-role=community]{background:linear-gradient(140deg,#ae8970,#586d5a)}.photo[data-role=private]{background:linear-gradient(140deg,#9a8b81,#2e4a45)}
.photo figcaption{font-size:.78rem;max-width:100%;background:#172b27c9;border-radius:9px;padding:9px 12px;backdrop-filter:blur(3px)}
.photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}
.sections{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;padding:28px 0 55px}
.tile{border:1px solid var(--line);background:#fff;border-radius:18px;overflow:hidden}
.tile .photo{border-radius:0;min-height:185px}.tile .copy{padding:24px}.tile p{color:var(--muted);margin:0}
.action{padding:34px;background:var(--sand);border-radius:18px;margin-bottom:65px;display:flex;align-items:center;justify-content:space-between;gap:25px;flex-wrap:wrap}
footer{border-top:1px solid var(--line);padding:28px 0 85px;font-size:.85rem;color:var(--muted)}
.demo{position:fixed;bottom:0;z-index:10;background:#213a30;color:#fff;width:100%;font-size:.76rem;text-align:center;padding:10px}
@media(max-width:700px){.wrap{width:min(100% - 28px,560px)}.hero{grid-template-columns:1fr;padding:24px 0}.hero .photo{min-height:300px;order:-1}
.sections{grid-template-columns:1fr;gap:16px}.links{max-width:100%;overflow-x:auto;flex-wrap:nowrap}.links a{white-space:nowrap}
.nav{align-items:start;gap:8px}.pill{padding:11px 16px}h1{font-size:clamp(2.4rem,10vw,3.5rem)}
.action{margin-bottom:85px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""
def photo(role, label, assets):
    safe = esc(label)
    item = assets.get(role)
    if item:
        f = esc("assets/" + item["filename"])
        inside = '<img src="' + f + '" alt="' + safe + '" loading="lazy"/>'
        cap = esc("Source: " + item["source"] + " · " + item["license"])
    else:
        inside = ""
        cap = "IMAGE PLACEHOLDER · " + safe + " · replace with rights-cleared photograph"
    return '<figure class="photo" data-role="' + esc(role) + '" role="group" aria-label="' + safe + '">' + inside + '<figcaption>' + cap + '</figcaption></figure>'

def render(page, pages, assets):
    def link(slug): return "index.html" if slug == "home" else esc(slug) + ".html"
    nav = "".join('<a ' + ('aria-current="page" ' if p["slug"]==page["slug"] else '') + 'href="'+link(p["slug"])+'">'+esc(p["title"])+'</a>' for p in pages[:7])
    cells = ""
    for s in page["sections"]:
        cells += '<article class="tile">'+photo(s["role"],s["image_label"],assets)+'<div class="copy"><h2>'+esc(s["title"])+'</h2><p>'+esc(s["text"])+'</p></div></article>'
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
      '<meta name="robots" content="noindex,nofollow,noarchive"><meta http-equiv="Content-Security-Policy" content="default-src &#39;none&#39;; img-src &#39;self&#39; data:; style-src &#39;self&#39;; base-uri &#39;none&#39;; form-action &#39;none&#39;">'
      '<title>'+esc(page["title"])+' — Moksha design preview</title><link rel="stylesheet" href="style.css"></head><body>'
      '<header><div class="wrap nav"><a class="brand" href="index.html">MOKSHA</a><nav class="links" aria-label="Page navigation">'+nav+'</nav></div></header>'
      '<main class="wrap"><div class="hero"><div><p class="eyebrow">'+esc(page["eyebrow"])+'</p><h1>'+esc(page["headline"])+'</h1><p class="intro">'+esc(page["summary"])+'</p>'
      '<a class="pill" href="'+link(page["cta"]["target"])+'">'+esc(page["cta"]["label"])+'</a></div>'
      +photo(page["hero"]["role"],page["hero"]["label"],assets)+'</div><div class="sections">'+cells+'</div>'
      '<section class="action"><div><p class="eyebrow">Discover the ritual</p><h2>Find your next Moksha experience.</h2></div><a class="pill" href="experiences.html">Explore rituals</a></section></main>'
      '<footer><div class="wrap">Moksha Wellness · Arambol, Goa · Private design preview only</div></footer>'
      '<div class="demo">PRIVATE STAGING — CONCEPT / PLACEHOLDERS ONLY · NO LIVE BOOKINGS OR PAYMENTS</div></body></html>')

def build(project, manifest_id):
    manifest, src = read_manifest(project, manifest_id)
    digest = hashlib.sha256(src.read_bytes()).hexdigest()[:16]
    parent = OUTPUT / project
    parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    parent.chmod(0o700)
    target = parent / digest
    if target.exists():
        receipt = json.loads((target / "receipt.json").read_text())
        return dict(receipt, deduplicated=True)
    temp = Path(tempfile.mkdtemp(prefix=".stage-", dir=parent))
    try:
        (temp / "style.css").write_text(CSS, encoding="utf-8")
        (temp / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
        (temp / "assets").mkdir(mode=0o700)
        for item in manifest.get("assets", {}).values():
            filename=item["filename"]
            shutil.copyfile(INBOX/project/"assets"/filename, temp/"assets"/filename)
        files=[]
        for p in manifest["pages"]:
            filename="index.html" if p["slug"] == "home" else p["slug"]+".html"
            (temp / filename).write_text(render(p, manifest["pages"], manifest.get("assets", {})), encoding="utf-8")
            files.append(filename)
        problems=[]
        for filename in files:
            s=(temp/filename).read_text()
            for bad in ("<script", "<form", "http://", "https://", "href=\"/"):
                if bad in s: problems.append(filename+":"+bad)
            for dest in re.findall(r'href="([^"]+)"',s):
                if dest!="style.css" and not (temp/dest).is_file(): problems.append("missing_link:"+dest)
            if 'noindex,nofollow' not in s: problems.append("robots_missing:"+filename)
        if problems: fail("Staging QA failed:"+str(problems))
        receipt={"project":project,"manifest_id":manifest_id,"sha256_prefix":digest,
          "state":"private_preview_ready","files":files,"pages":len(files),
          "placeholder_roles":sorted(ROLES-set(manifest.get("assets",{}))),
          "local_path":str(target),"external_services":False,"server_started":False,
          "publication":False,"spend":False,"nonindexed":True,"qa_passed":True,
          "created_utc":datetime.now(timezone.utc).isoformat()}
        (temp/"receipt.json").write_text(json.dumps(receipt,indent=2))
        for f in temp.rglob("*"):
            if f.is_file(): f.chmod(0o600)
        temp.chmod(0o700)
        temp.rename(target)
        return receipt
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("command",choices=("validate","build"))
    parser.add_argument("project")
    parser.add_argument("manifest_id")
    args=parser.parse_args()
    if args.command=="validate":
        data,_=read_manifest(args.project,args.manifest_id)
        print(json.dumps({"valid":True,"pages":len(data["pages"]),"publish":False,"spend":False}))
    else:
        print(json.dumps(build(args.project,args.manifest_id),indent=2))

if __name__=="__main__":
    main()
