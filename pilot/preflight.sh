#!/usr/bin/env bash
set -euo pipefail
fail=0
printf 'Business House Matrix — Open WebUI local-only pilot preflight\n'
for bin in docker openssl; do
  if command -v "$bin" >/dev/null 2>&1; then echo "OK: $bin present"; else echo "FAIL: $bin missing"; fail=1; fi
done
if ! command -v docker >/dev/null 2>&1; then exit 1; fi
if ! docker info >/dev/null 2>&1; then echo 'FAIL: Docker daemon inaccessible'; fail=1; fi
if ! docker compose version >/dev/null 2>&1; then echo 'FAIL: docker compose unavailable'; fail=1; fi
if [[ ! -f .env ]]; then echo 'FAIL: .env missing (copy from .env.example and edit)'; fail=1;
else
  if grep -Eq 'REPLACE_WITH|:main([[:space:]]|$)|:dev([[:space:]]|$)' .env; then echo 'FAIL: placeholders or floating image tag in .env'; fail=1; fi
  if ! grep -Eq '^WEBUI_SECRET_KEY=[0-9a-fA-F]{64}$' .env; then echo 'FAIL: WEBUI_SECRET_KEY must be 64 hex characters'; fail=1; fi
fi
if ((fail)); then echo 'STOP: resolve prerequisites'; exit 1; fi
if ! docker compose --env-file .env -f docker-compose.yml config -q; then echo 'FAIL: Compose config'; exit 1; fi
printf 'PASS: preflight checks. Verify published port is ONLY 127.0.0.1:3000 and backups are ready before starting.\n'
