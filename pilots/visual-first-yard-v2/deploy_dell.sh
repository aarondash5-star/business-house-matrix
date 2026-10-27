#!/usr/bin/env bash
# Isolated Dell install only. Does NOT touch SSH MCP runtime or frozen game lanes.
set -euo pipefail
umask 077
ROOT=/var/lib/generic-linux-automator-exec/matrix-controller
FREEZE="$ROOT/docs/SHAADI_ART_LANES_OWNER_FREEZE.json"
REF="$ROOT/yard-certifications/drawing-e2e-20261027/target.png"
EXPECTED=7a02f3a72316378db5201c8fe38e0226ecaad8f1ab389ecd2f37fec6a65781f3
LIVE="$ROOT/yard-certifications/visual-first-v2"
python3 - "$FREEZE" "$REF" "$EXPECTED" <<'PY'
import sys,json,hashlib
from pathlib import Path
f,r,d=(Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3])
j=json.loads(f.read_text())
assert j['state']=='OWNER_FROZEN' and j['lane1']['frozen'] and j['lane2']['frozen']
assert j['allow']['new_art_jobs'] is False and j['release_authorized'] is False
assert hashlib.sha256(r.read_bytes()).hexdigest()==d, 'wrong benchmark fixture'
print('OWNER_FREEZE_AND_REFERENCE_VERIFIED')
PY
mkdir -p "$LIVE"
python3 -m venv "$LIVE/.venv"
"$LIVE/.venv/bin/python" -m pip install --disable-pip-version-check -r requirements.txt
# VTracer is an optional additional candidate and must never break the OpenCV path.
"$LIVE/.venv/bin/python" -m pip install --disable-pip-version-check -r requirements-optional.txt || echo 'VTracer unavailable; using OpenCV fallback'
"$LIVE/.venv/bin/python" -m unittest discover -v
"$LIVE/.venv/bin/python" -m visual_yard_v2 run --reference "$REF" --output "$LIVE/review" --freeze "$FREEZE" || status=$?
# Exit 2 means visual thresholds not met, keep saved preview; NOT installation failure.
[ "${status:-0}" = 2 ] || [ "${status:-0}" = 0 ] || exit "${status}"
[ -f "$LIVE/review/qa_receipt.json" ]
python3 - "$LIVE/review/qa_receipt.json" <<'PY'
import json,sys
j=json.load(open(sys.argv[1]));print('FINAL_VISUAL_STATUS',j['qa_outcome'],j.get('metrics',{}))
assert j['creative_certified'] is False and j['owner_approved'] is False
PY
# Existing private review-gallery service MAY serve this dedicated folder via a
# separately approved symlink. No changes to listener, tunnel, auth or service here.
echo 'ISOLATED_V2_BENCHMARK_COMPLETE_NO_PRODUCTION_MUTATIONS'
