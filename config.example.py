# -*- coding: utf-8 -*-
# Шаблон конфигурации. При первом запуске app.py создаётся config.py из этого файла.
# config.example.py — шаблон (можно хранить в git). config.py — ваши настройки (токены, ключи).

# Токен бота от @BotFather (тот же, что у my_shop — только для уведомлений о заказах)
TELEGRAM_BOT_TOKEN = ''

# False на проде: polling только на сервере my_shop. Не запускайте lilstore-bot здесь.
TELEGRAM_RUN_POLLING = False

# Username бота без @ (для плавающей кнопки на сайте, например: iluma_prime_bot)
TELEGRAM_BOT_USERNAME = ''

# Токен бота от @BotFather (тот же, что у my_shop — только для уведомлений о заказах)
TELEGRAM_BOT_TOKEN = ''

# ID чата для уведомлений о заказах (группа менеджеров).
# На iqos-store/lilsolid бот не запущен — укажите тот же chat_id, что в my_shop config.py
# или ID группы, куда добавлен @iluma_prime_bot (узнать: /set_notify в группе на my_shop).
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
SITE_URL = 'https://iqos-store.ru'

# Контакты на сайте (телефон, адрес для Яндекса/Google и страницы «Контакты»)
SITE_PHONE = '+7 (993) 596-82-25'
SITE_ADDRESS = 'Москва, Ленинградское шоссе, 16А'
SITE_CITY = 'Москва'

# Яндекс.Метрика — ОТДЕЛЬНЫЙ счётчик только для https://iqos-store.ru
# Создайте в https://metrika.yandex.ru → «Добавить счётчик» → домен iqos-store.ru
# Не используйте ID от lilstore.ru или lilsolid.ru
YANDEX_METRIKA_ID = ''

