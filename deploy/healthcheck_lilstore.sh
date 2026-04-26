#!/usr/bin/env bash
# Auto-heal check for LIL STORE (site + sitemap + local gunicorn)

set -u

SITE_URL="https://lilstore.ru"
SITE_ENDPOINTS=(
  "/"
  "/sitemap.xml"
  "/robots.txt"
)
LOCAL_ENDPOINT="http://127.0.0.1:8000/health"
LOG_TAG="lilstore-healthcheck"

ok=1
reasons=()

check_url() {
  local url="$1"
  local code
  code="$(curl -L -sS -o /dev/null -w "%{http_code}" --max-time 10 "$url" || echo "000")"
  if [[ "$code" != "200" ]]; then
    ok=0
    reasons+=("$url:$code")
  fi
}

for path in "${SITE_ENDPOINTS[@]}"; do
  check_url "${SITE_URL}${path}"
done

check_url "${LOCAL_ENDPOINT}"

if [[ "$ok" -eq 1 ]]; then
  logger -t "$LOG_TAG" "OK: site endpoints healthy"
  exit 0
fi

logger -t "$LOG_TAG" "FAIL: ${reasons[*]} -> restarting lilstore and nginx"
systemctl restart lilstore nginx || true
sleep 4

# Re-check after restart
ok=1
reasons=()
for path in "${SITE_ENDPOINTS[@]}"; do
  check_url "${SITE_URL}${path}"
done
check_url "${LOCAL_ENDPOINT}"

if [[ "$ok" -eq 1 ]]; then
  logger -t "$LOG_TAG" "RECOVERED: endpoints healthy after restart"
  exit 0
fi

logger -t "$LOG_TAG" "CRITICAL: still failing after restart: ${reasons[*]}"
exit 1
