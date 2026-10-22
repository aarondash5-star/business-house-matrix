#!/bin/sh
# Gate E candidate QA — self-hosted/local, offline, no hosted CI dependency.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
export PYTHONDONTWRITEBYTECODE=1
export PYTHONNOUSERSITE=1
cd "$ROOT"
echo "Gate E candidate source: $(git rev-parse HEAD)"
exec /usr/bin/python3 -B -m unittest discover -s brain/dev-operator/tests -p 'test_*.py' -v
