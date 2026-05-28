# -*- coding: utf-8 -*-
# Шаблон конфигурации. При первом запуске app.py создаётся config.py из этого файла.
# config.example.py — шаблон (можно хранить в git). config.py — ваши настройки (токены, ключи).

# Токен бота от @BotFather (для уведомлений о заказах и бота управления)
TELEGRAM_BOT_TOKEN = ''

# Username бота без @ (для плавающей кнопки на сайте, например: iluma_prime_bot)
TELEGRAM_BOT_USERNAME = ''

# ID чата для уведомлений (запасной вариант)
# По умолчанию: добавьте бота в группу и напишите /start или /set_notify — чат сохранится автоматически
TELEGRAM_CHAT_ID = ''

# ID пользователей Telegram с доступом к меню Boss/Admin (через запятую)
# Если не задано — доступ у всех, кто пишет боту
TELEGRAM_ADMIN_IDS = ''

# Секретный ключ администратора (полный доступ, в т.ч. удаление заказов): /admin
ADMIN_SECRET = ''

# Отдельный ключ роли «Босс» — тот же URL /admin, все права кроме удаления заказов
BOSS_SECRET = ''

# Секретный ключ для подписи сессий Flask.
# Рекомендуется: задать переменную окружения SECRET_KEY (не хранить в файле).
# Сгенерировать: py -c "import secrets; print(secrets.token_hex(24))"
SECRET_KEY = ''

# Кэширование: SimpleCache (память), FileSystemCache (файлы), RedisCache (Redis)
# CACHE_TYPE = 'FileSystemCache'  # для продакшена с несколькими воркерами
# CACHE_DIR = './cache'

# Админ по умолчанию (username без @)
TELEGRAM_DEFAULT_ADMIN = 'denchik1402'

# Путь к iluma.xlsx для расчёта прибыли (цены и себестоимость)
ILUMA_XLSX_PATH = r'c:\Users\Dubko\Desktop\iluma.xlsx'

# URL сайта для ссылок из бота (админка, маршруты)
# Для кнопки "Запустить приложение" (Web App) нужен HTTPS (например ngrok или хостинг)
SITE_URL = 'http://127.0.0.1:5000'

# Контакты на сайте (телефон, адрес для Яндекса/Google и страницы «Контакты»)
SITE_PHONE = '+7 (993) 596-82-25'
SITE_ADDRESS = 'Москва, Ленинградское шоссе, 16А'
SITE_CITY = 'Москва'

# Яндекс.Метрика: номер счётчика (только цифры) из https://metrika.yandex.ru
# Создайте счётчик для https://lilstore.ru и вставьте ID, например: 12345678
YANDEX_METRIKA_ID = ''

