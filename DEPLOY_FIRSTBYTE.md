# iqos-store.ru — деплой на FirstByte

Полная пошаговая инструкция для **двух сайтов** (iqos + lilsolid): [`../DEPLOY_TWO_SITES.md`](../DEPLOY_TWO_SITES.md)

Кратко для этого проекта:

| Параметр | Значение |
|----------|----------|
| Домен | `iqos-store.ru` |
| IP сервера | `178.253.44.52` |
| DNS | Selectel → A `@` и `www` → `178.253.44.52` |
| Путь | `/home/lilstore/iqos-store` |
| systemd | `iqos-store` |
| Порт gunicorn | `127.0.0.1:8000` |
| Telegram polling | **выключен** (`TELEGRAM_RUN_POLLING = False`) |

## Быстрый старт

```bash
ssh root@178.253.44.52
export GITHUB_REPO="https://github.com/denchik1402/iqos-store.git"
# после git clone:
bash /home/lilstore/iqos-store/deploy/bootstrap_server.sh
nano /home/lilstore/iqos-store/config.py
certbot --nginx -d iqos-store.ru -d www.iqos-store.ru
```

GitHub Secrets в репозитории `iqos-store`: `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY`.

Push в `main` → автодеплой.
