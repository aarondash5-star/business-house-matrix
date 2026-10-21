#!/usr/bin/env python3
"""Marketing Brain -> pre-existing Mac Reel Studio (no publishing).

Preflight is read-only. Rendering is opt-in, serialized by existing worker,
thermally gated, no local AI, no remote stock, and restricted to a media inbox.
"""
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time

BRAIN = Path(__file__).resolve().parent
INBOX = BRAIN / "media-inbox"
OUTBOX = BRAIN / "renders"
REEL = BRAIN.parent / "reel-studio" / "reel.py"
REEL_PYTHON = REEL.parent / ".venv" / "bin" / "python"
EXT = {".mp4",".mov",".mkv",".webm",".m4v",".jpg",".jpeg",".png",".webp"}
MAX_MEDIA = 12
MAX_FILE_BYTES = 1_000_000_000
MAX_TOTAL_BYTES = 2_000_000_000

def batch_paths(batch_id):
    if not isinstance(batch_id, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}",batch_id):
        raise ValueError("batch_id must be a 1-64 character safe identifier")
    return INBOX / batch_id, OUTBOX / batch_id

def scan(batch_id):
    src, dst = batch_paths(batch_id)
    if not src.is_dir() or src.is_symlink():
        raise RuntimeError("No approved media batch found; stage footage in isolated inbox")
    files = list(src.iterdir())
    if not files or len(files) > MAX_MEDIA:
        raise RuntimeError("Footage count must be 1 to 12")
    out = []
    total = 0
    for f in sorted(files):
        if f.is_symlink() or not f.is_file() or f.suffix.lower() not in EXT:
            raise RuntimeError("Only regular supported image/video files allowed; no links")
        size = f.stat().st_size
        if size < 100 or size > MAX_FILE_BYTES:
            raise RuntimeError("Media file outside allowed size range")
        total += size
        out.append({"filename":f.name,"bytes":size,"type":"video" if f.suffix.lower() in {".mp4",".mov",".mkv",".webm",".m4v"} else "image"})
    if total > MAX_TOTAL_BYTES:
        raise RuntimeError("Media batch too large")
    return {"batch_id":batch_id,"source":str(src),"destination":str(dst),
            "files":out,"total_bytes":total,"media_count":len(out),
            "publish_allowed":False}

def mac_temperature_c():
    # Mac Linux Apple SMC sensors can differ from coretemp; read both.
    temps = []
    for h in Path("/sys/class/hwmon").glob("hwmon*"):
        try:
            name = (h/"name").read_text().strip().lower()
            if not any(x in name for x in ("coretemp","applesmc","apple_smc","smc")):
                continue
            for val in h.glob("temp*_input"):
                t=float(val.read_text())/1000
                if 0 < t < 150:
                    temps.append(t)
        except (OSError, ValueError):
            continue
    return max(temps) if temps else None

def render(batch_id, brief, config):
    manifest = scan(batch_id)
    if not config.get("render_enabled",False):
        raise RuntimeError("Rendering not enabled; integration staged for controlled live test")
    if config.get("publish_enabled") or config.get("spend_enabled"):
        raise RuntimeError("Preview renderer rejects publishing/spend permissions")
    if not isinstance(brief,str) or not brief.strip() or len(brief)>140:
        raise ValueError("Brief must be nonempty and at most 140 characters")
    temp = mac_temperature_c()
    maximum = min(70.0, float(config.get("render_max_temp_c",68.0)))
    if temp is None or temp >= maximum:
        raise RuntimeError("Render blocked by thermal guard; no suitable sensor or too hot")
    if not REEL.is_file() or not REEL_PYTHON.is_file():
        raise RuntimeError("Original Reel Studio or its isolated Python environment missing")
    out=Path(manifest["destination"])
    if out.exists() and any(out.iterdir()):
        raise RuntimeError("Nonempty render destination; refuse overwrite")
    out.mkdir(mode=0o700,parents=True,exist_ok=True)
    cmd=[str(REEL_PYTHON),str(REEL),"--input",manifest["source"],
         "--output",str(out),"--brief",brief,
         "--seconds","12","--width","360","--no-ai"]
    # This entrypoint uses fixed arguments, no shell, no AI, no stock query.
    # Child processes inherit a new process group for bounded cleanup.
    proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                          text=True,start_new_session=True,
                          preexec_fn=lambda: os.nice(10))
    end = time.monotonic()+100
    while True:
        try:
            stdout,stderr=proc.communicate(timeout=min(2.0,max(0.1,end-time.monotonic())))
            break
        except subprocess.TimeoutExpired:
            measured=mac_temperature_c()
            if measured is None or measured >= maximum:
                os.killpg(proc.pid,signal.SIGKILL)
                proc.communicate()
                raise RuntimeError("Reel preview stopped by in-run thermal monitor")
            if time.monotonic()>=end:
                os.killpg(proc.pid,signal.SIGKILL)
                proc.communicate()
                raise RuntimeError("Reel preview timed out and process group was stopped")
    if proc.returncode:
        raise RuntimeError("Reel preview failed: exit "+str(proc.returncode)+" "+stderr[-180:])
    result=out/"report.json"
    if not result.is_file():
        raise RuntimeError("Renderer returned no preview manifest")
    data=json.loads(result.read_text())
    if data.get("status")!="preview_only_not_published" or not Path(data.get("movie","")).is_file():
        raise RuntimeError("Unexpected Reel Studio output; not certified")
    return {"state":"draft_preview_only","batch_id":batch_id,
            "video":data["movie"],"length":data.get("seconds"),
            "resolution":data.get("size"),"qa_required":True,
            "rights_check_required":True,"approved_to_publish":False,
            "auto_publish":False,"source_count":manifest["media_count"]}


def review(batch_id):
    """Read-only output QC; never converts a draft into publishing approval."""
    src,dst=batch_paths(batch_id)
    p=dst/"report.json"
    if not p.is_file() or p.is_symlink():
        raise RuntimeError("Preview report missing")
    report=json.loads(p.read_text())
    movie=dst/"reel_preview.mp4"
    if not movie.is_file() or movie.is_symlink():
        raise RuntimeError("Preview media missing")
    expected=movie.resolve()
    if Path(str(report.get("movie",""))).resolve()!=expected:
        raise RuntimeError("Preview report references unexpected output")
    checks={
        "preview_only":report.get("status")=="preview_only_not_published",
        "vertical":len(report.get("size",[]))==2 and report["size"][1]>report["size"][0],
        "has_video":bool(report.get("has_video",False)),
        "duration_sensible":isinstance(report.get("seconds"),(int,float)) and 4<=report["seconds"]<=60,
        "not_generic_outro":report.get("outro","").strip().upper() not in ("WATCH MORE","FOLLOW FOR MORE",""),
        "rights_verified":False, # independent licensing/asset consent QA must set separately
        "brand_reviewed":False,
    }
    return {"batch_id":batch_id,"checks":checks,
            "technical_checks_passed":all(checks[k] for k in ("preview_only","vertical","has_video","duration_sensible")),
            "state":"DRAFT_NEEDS_HUMAN_QA",
            "approved_to_publish":False,
            "publication_blocked":True,
            "video":str(movie),"source_dir":str(src)}

def preflight(batch_id):
    info=scan(batch_id)
    info["render_entrypoint_present"]=REEL.is_file()
    info["temperature_c"]=mac_temperature_c()
    info["state"]="awaiting_review_and_safe_render"
    return info
