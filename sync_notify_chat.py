#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Синхронизировать TELEGRAM chat_id с my_shop (lilstore.ru)."""
import sys

sys.path.insert(0, 'TG')
from notify_sync import sync_notification_chat_to_local_db

if __name__ == '__main__':
    ok = sync_notification_chat_to_local_db()
    print('OK: chat_id синхронизирован с lilstore.ru' if ok else 'WARN: не удалось получить chat_id (проверьте TELEGRAM_BOT_TOKEN и /set_notify на my_shop)')
    sys.exit(0 if ok else 1)
