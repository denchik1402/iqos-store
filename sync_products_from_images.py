# -*- coding: utf-8 -*-
"""Импорт товаров с путями к фото из static/images/products (Devices/, Sticks/)."""
import json
import os
from datetime import datetime

from app import app, db
from models import Category, Product
from full_update import STICKS, DEVICES, IMAGE_MAP, slugify
from assign_product_models import detect_model
from assign_product_colors import detect_color


def sync_products():
    categories = [
        ('IQOS ILUMA', 'iqos-iluma', 'Устройства IQOS ILUMA'),
        ('Стики TEREA', 'terea-sticks', 'Стики для IQOS ILUMA'),
        ('LIL', 'lil', 'Устройства LIL'),
    ]
    cat_ids = {}
    for name, slug, desc in categories:
        cat = Category.query.filter_by(slug=slug).first()
        if not cat:
            cat = Category(name=name, slug=slug, description=desc, created_at=datetime.utcnow())
            db.session.add(cat)
            db.session.flush()
        cat_ids[slug] = cat.id

    db.session.query(Product).delete()
    db.session.commit()

    def resolve_image(name, fallback):
        if name in IMAGE_MAP:
            return IMAGE_MAP[name]
        lower = name.lower()
        for key, path in IMAGE_MAP.items():
            if key.lower() == lower:
                return path
        return fallback

    def add_item(item, cat_slug, is_device=False):
        slug = slugify(item['name'])
        img = resolve_image(item['name'], item.get('image'))
        if img and not os.path.isfile(os.path.join('static/images/products', img.replace('/', os.sep))):
            print(f'  [WARN] файл не найден: {item["name"]} -> {img}')
        extra = json.dumps(item['images']) if item.get('images') else None
        model_val = detect_model(item['name'], item.get('description', '')) if is_device else None
        color_val = detect_color(item['name'], item.get('description', '')) if is_device else None
        p = Product(
            name=item['name'],
            slug=slug,
            price=item['price'],
            description=item['description'],
            image=img,
            images=extra,
            category_id=cat_ids[cat_slug],
            in_stock=True,
            model=model_val,
            color=color_val,
            created_at=datetime.utcnow(),
        )
        db.session.add(p)

    for stick in STICKS:
        add_item(stick, 'terea-sticks')

    for device in DEVICES:
        cat_slug = 'iqos-iluma' if 'IQOS' in device['name'] or 'Iqos' in device['name'] else 'lil'
        add_item(device, cat_slug, is_device=True)

    db.session.commit()
    print(f'Импортировано товаров: {Product.query.count()}')


if __name__ == '__main__':
    with app.app_context():
        sync_products()
    from update_product_galleries import update_galleries
    update_galleries()
    with app.app_context():
        from app import populate_promo_and_hits
        populate_promo_and_hits()
    print('Готово: товары привязаны к фото в static/images/products/')
