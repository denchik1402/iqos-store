# -*- coding: utf-8 -*-
"""
Импорт баннеров из banners_export.json в БД.
Запускать на проде: python3 import_banners.py [--replace]
  --replace  удалить существующие баннеры перед импортом (по умолчанию — добавить к имеющимся)
Требует banners_export.json в папке проекта.
"""
import json
import sqlite3
import os
import sys

DB_PATH = 'shop.db'
INPUT = 'banners_export.json'

def import_banners(replace=False):
    if not os.path.isfile(INPUT):
        print(f"Ошибка: {INPUT} не найден. Сначала выполните export_banners.py локально и закоммитьте файл.")
        return
    if not os.path.isfile(DB_PATH):
        print(f"Ошибка: {DB_PATH} не найден")
        return
    with open(INPUT, 'r', encoding='utf-8') as f:
        data = json.load(f)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if replace:
        cursor.execute("DELETE FROM banner")
        print("Удалены существующие баннеры")
    # Словарь product_name -> id для маппинга (регистронезависимый)
    cursor.execute("SELECT id, name FROM product")
    product_by_name = {row[1]: row[0] for row in cursor.fetchall()}
    product_by_name_lower = {k.lower(): v for k, v in product_by_name.items()}
    inserted = 0
    for item in data:
        product_id = None
        if item.get('product_name'):
            product_id = product_by_name.get(item['product_name']) or product_by_name_lower.get(item['product_name'].lower())
            if not product_id:
                print(f"  Пропуск: товар «{item['product_name']}» не найден в БД")
        button_url = item.get('button_url')
        if button_url in (None, '', 'None', 'none'):
            button_url = None
        cursor.execute("""
            INSERT INTO banner (image, title, subtitle, button_text, button_url,
                               product_id, badge_type, sort_order, is_active, ab_test_group)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item['image'],
            item['title'],
            item.get('subtitle'),
            item.get('button_text') or 'Купить сейчас',
            button_url,
            product_id,
            item.get('badge_type'),
            item.get('sort_order', 0),
            1 if item.get('is_active', True) else 0,
            item.get('ab_test_group'),
        ))
        inserted += 1
        print(f"  + {item['title']} ({item['image']})")
    conn.commit()
    conn.close()
    print(f"\nИмпортировано {inserted} баннеров")

if __name__ == '__main__':
    replace = '--replace' in sys.argv
    import_banners(replace=replace)
