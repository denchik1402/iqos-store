#!/usr/bin/env bash
# Открыть веб снаружи: firewall, nginx, SITE_URL, SSL, healthcheck
set -euo pipefail

APP_DIR="${APP_DIR:-/home/lilstore/iqos-store}"
SERVICE="${SERVICE:-iqos-store}"
DOMAIN="${DOMAIN:-iqos-store.ru}"
SITE_URL="https://${DOMAIN}"

echo "=== ensure_public_web: ${DOMAIN} ==="

if command -v ufw >/dev/null 2>&1; then
  ufw allow 22/tcp comment 'SSH' || true
  ufw allow 80/tcp comment 'HTTP' || true
  ufw allow 443/tcp comment 'HTTPS' || true
  ufw --force enable || true
  ufw status || true
fi

if [[ -f "${APP_DIR}/config.py" ]]; then
  if ! grep -qE "SITE_URL\s*=\s*['\"]${SITE_URL}['\"]" "${APP_DIR}/config.py"; then
    echo "WARN: SITE_URL в config.py должен быть ${SITE_URL}"
    if grep -qE "^SITE_URL\s*=" "${APP_DIR}/config.py"; then
      sed -i "s|^SITE_URL\s*=.*|SITE_URL = '${SITE_URL}'|" "${APP_DIR}/config.py"
      echo "SITE_URL исправлен на ${SITE_URL}"
      systemctl restart "${SERVICE}" || true
    fi
  fi
fi

systemctl enable nginx "${SERVICE}" 2>/dev/null || true
systemctl start nginx "${SERVICE}" || true

if [[ -f /etc/letsencrypt/live/${DOMAIN}/fullchain.pem ]]; then
  cp "${APP_DIR}/deploy/nginx-iqos-store.conf" /etc/nginx/sites-available/iqos-store
else
  cp "${APP_DIR}/deploy/nginx-iqos-store-http.conf" /etc/nginx/sites-available/iqos-store
fi
ln -sf /etc/nginx/sites-available/iqos-store /etc/nginx/sites-enabled/iqos-store
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

if [[ ! -f /etc/letsencrypt/live/${DOMAIN}/fullchain.pem ]]; then
  echo "SSL не найден — пробуем certbot..."
  certbot --nginx -d "${DOMAIN}" -d "www.${DOMAIN}" \
    --non-interactive --agree-tos --register-unsafely-without-email --redirect || true
  if [[ -f /etc/letsencrypt/live/${DOMAIN}/fullchain.pem ]]; then
    cp "${APP_DIR}/deploy/nginx-iqos-store.conf" /etc/nginx/sites-available/iqos-store
    nginx -t && systemctl reload nginx
  fi
fi

echo "--- локальные проверки ---"
curl -sf --max-time 10 "http://127.0.0.1:8000/health" >/dev/null && echo "OK gunicorn /health"
curl -sf --max-time 10 -H "Host: ${DOMAIN}" "http://127.0.0.1/robots.txt" | head -3
curl -sf --max-time 10 -H "Host: ${DOMAIN}" "http://127.0.0.1/" -o /dev/null && echo "OK nginx -> app"

if [[ -x /usr/local/bin/healthcheck-iqos-store.sh ]]; then
  /usr/local/bin/healthcheck-iqos-store.sh || true
fi

echo "=== ensure_public_web done ==="
