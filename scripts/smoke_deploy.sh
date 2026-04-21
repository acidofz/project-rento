#!/usr/bin/env bash
# Быстрая проверка после деплоя (требует curl).
# Использование:
#   BASE_URL=https://your-domain.example uv run bash scripts/smoke_deploy.sh
# или:
#   BASE_URL=http://127.0.0.1:3000 bash scripts/smoke_deploy.sh

set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:3000}"
BASE_URL="${BASE_URL%/}"

echo "Smoke: BASE_URL=$BASE_URL"

curl -sfS "$BASE_URL/ping" >/dev/null
echo "OK  GET /ping"

curl -sfS "$BASE_URL/_health" >/dev/null
echo "OK  GET /_health"

curl -sfS "$BASE_URL/ready" >/dev/null
echo "OK  GET /ready"

for path in / /listings /health /terms /privacy /robots.txt; do
  code=$(curl -sS -o /dev/null -w "%{http_code}" "$BASE_URL$path")
  if [[ "$code" != "200" ]]; then
    echo "FAIL GET $path (HTTP $code)" >&2
    exit 1
  fi
  echo "OK  GET $path (HTTP $code)"
done

echo "Smoke finished successfully."
