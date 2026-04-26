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
APP_DIR="/home/lilstore/my_shop"

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

notify_telegram() {
  local level="$1"
  local text="$2"
  python3 - "$APP_DIR" "$level" "$text" <<'PY'
import os
import sys
import urllib.parse
import urllib.request
import importlib.util

app_dir, level, text = sys.argv[1], sys.argv[2], sys.argv[3]
cfg_path = os.path.join(app_dir, "config.py")
if not os.path.exists(cfg_path):
    sys.exit(0)

spec = importlib.util.spec_from_file_location("lilstore_config", cfg_path)
if not spec or not spec.loader:
    sys.exit(0)
cfg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cfg)

token = getattr(cfg, "TELEGRAM_BOT_TOKEN", "") or ""
chat_id = getattr(cfg, "TELEGRAM_CHAT_ID", "") or ""
if not token or not chat_id:
    sys.exit(0)

prefix = {"FAIL": "⚠️", "RECOVERED": "✅", "CRITICAL": "🚨"}.get(level, "ℹ️")
msg = f"{prefix} LIL STORE healthcheck [{level}]\n{text}"
url = f"https://api.telegram.org/bot{token}/sendMessage"
data = urllib.parse.urlencode({"chat_id": str(chat_id), "text": msg}).encode("utf-8")
try:
    urllib.request.urlopen(url, data=data, timeout=8).read()
except Exception:
    pass
PY
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
notify_telegram "FAIL" "Проблема с endpoint: ${reasons[*]}\nАвтоперезапуск lilstore + nginx"
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
  notify_telegram "RECOVERED" "Сайт восстановлен после автоперезапуска.\nПроверка: ${SITE_URL}"
  exit 0
fi

logger -t "$LOG_TAG" "CRITICAL: still failing after restart: ${reasons[*]}"
notify_telegram "CRITICAL" "Сайт не восстановился после перезапуска.\nПроблемные endpoint: ${reasons[*]}"
exit 1
