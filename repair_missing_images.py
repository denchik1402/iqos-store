# -*- coding: utf-8 -*-
"""
Исправление битых путей к картинкам товаров и генерация обложек блога.
Запуск на сервере:
  python3 repair_missing_images.py
"""
from __future__ import annotations

import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_DIR = os.path.join(ROOT, 'static', 'images', 'products')
COVERS_DIR = os.path.join(ROOT, 'static', 'images', 'blog', 'covers')

# Обложки блога ← файл товара (относительно static/images/products/)
BLOG_COVER_SOURCES = {
    'terea.webp': 'Sticks/Terea Purple Wave KZ/cr13289_h208450_pmi_switzerland_terea_3_quarter_right_single_mauve_wave_angle-1-600x600-1.png',
    'lil-solid.webp': 'Devices/lil SOLID 3.0 Чёрный/64bd6e61-7833-4c03-acd3-34cb9b0a7b88.800x600.png',
    'iqos-iluma.webp': 'Devices/IQOS Iluma i Standart Midnight Black/iqos_iluma_i_midnight_black.webp',
    'iqos-iluma-seletti.webp': 'Devices/Iqos Iluma i Standart Seletti/iqos_iluma_seletti.webp',
    'lil-solid-dual.png': 'Devices/lil SOLID DUAL Чёрный Титан/9c489a07101e290c762e07d9760629c8.png',
}


def _product_file(rel: str) -> str:
    return os.path.join(PRODUCTS_DIR, rel.replace('/', os.sep))


def _resolve_from_map(name: str, image_map: dict) -> str | None:
    if name in image_map:
        return image_map[name]
    lower = name.lower()
    for key, path in image_map.items():
        if key.lower() == lower:
            return path
    return None


def fix_product_images() -> int:
    from app import app, db
    from models import Product
    from full_update import IMAGE_MAP

    updated = 0
    with app.app_context():
        for product in Product.query.all():
            current = (product.image or '').strip()
            if current and os.path.isfile(_product_file(current)):
                continue
            fixed = _resolve_from_map(product.name, IMAGE_MAP)
            if not fixed:
                print(f'  [WARN] нет в IMAGE_MAP: {product.name!r}')
                continue
            if not os.path.isfile(_product_file(fixed)):
                print(f'  [WARN] файл не на диске: {product.name!r} -> {fixed}')
                continue
            if product.image != fixed:
                print(f'  OK product: {product.name!r} -> {fixed}')
                product.image = fixed
                updated += 1
        if updated:
            db.session.commit()
    return updated


def _save_cover_webp(src_path: str, dest_path: str, width: int = 800) -> None:
    from PIL import Image

    img = Image.open(src_path)
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        img = img.convert('RGBA')
    else:
        img = img.convert('RGB')
    w, h = img.size
    if w > width:
        ratio = width / float(w)
        img = img.resize((width, max(1, int(h * ratio))), Image.Resampling.LANCZOS)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    ext = os.path.splitext(dest_path)[1].lower()
    if ext == '.webp':
        img.save(dest_path, 'WEBP', quality=85, method=4)
    else:
        img.save(dest_path, 'PNG', optimize=True)


def ensure_blog_covers() -> int:
    created = 0
    os.makedirs(COVERS_DIR, exist_ok=True)
    for cover_name, product_rel in BLOG_COVER_SOURCES.items():
        dest = os.path.join(COVERS_DIR, cover_name)
        if os.path.isfile(dest):
            continue
        src = _product_file(product_rel)
        if not os.path.isfile(src):
            print(f'  [WARN] источник обложки не найден: {cover_name} <- {product_rel}')
            continue
        try:
            if cover_name.endswith('.webp'):
                _save_cover_webp(src, dest)
            else:
                shutil.copy2(src, dest)
            print(f'  OK cover: {cover_name}')
            created += 1
        except Exception as e:
            print(f'  [ERR] {cover_name}: {e}')
    return created


def main() -> int:
    print('=== repair_missing_images ===')
    print('--- товары ---')
    n_products = fix_product_images()
    print(f'Обновлено товаров: {n_products}')
    print('--- обложки блога ---')
    n_covers = ensure_blog_covers()
    print(f'Создано обложек: {n_covers}')
    print('=== done ===')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
