#!/usr/bin/env python
"""Создаёт WebP-варианты изображений (400w / 800w / 1200w). Запуск: python optimize_images.py"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(ROOT, 'static')

try:
    from PIL import Image
except ImportError:
    print('Установите Pillow: pip install Pillow')
    sys.exit(1)

from image_utils import (
    BANNER_WIDTHS,
    IMAGE_EXTENSIONS,
    PRODUCT_WIDTHS,
    is_variant_filename,
    variant_rel_path,
)

QUALITY = 82


def _prepare_image(img):
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        return img.convert('RGBA')
    if img.mode != 'RGB':
        return img.convert('RGB')
    return img


def _resize(img, max_width):
    w, h = img.size
    if w <= max_width:
        return img.copy()
    ratio = max_width / float(w)
    return img.resize((max_width, max(1, int(h * ratio))), Image.Resampling.LANCZOS)


def _save_webp(img, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    img.save(dest_path, 'WEBP', quality=QUALITY, method=6)


def _process_file(src_path, folder, rel_inner, widths, stats):
    mtime = os.path.getmtime(src_path)
    try:
        with Image.open(src_path) as img:
            img = _prepare_image(img)
            for width in widths:
                out_rel = variant_rel_path(rel_inner, width)
                out_path = os.path.join(STATIC, 'images', folder, out_rel)
                if os.path.isfile(out_path) and os.path.getmtime(out_path) >= mtime:
                    stats['skipped'] += 1
                    continue
                resized = _resize(img, width)
                _save_webp(resized, out_path)
                stats['created'] += 1
                print('OK:', f'{folder}/{rel_inner}', '->', os.path.relpath(out_path, ROOT))
    except Exception as exc:
        stats['errors'] += 1
        print('Ошибка', f'{folder}/{rel_inner}', ':', exc)


def _walk_folder(folder, widths, stats):
    base = os.path.join(STATIC, 'images', folder)
    if not os.path.isdir(base):
        return
    for dirpath, _, filenames in os.walk(base):
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in IMAGE_EXTENSIONS or is_variant_filename(name):
                continue
            full = os.path.join(dirpath, name)
            rel_inner = os.path.relpath(full, base).replace('\\', '/')
            _process_file(full, folder, rel_inner, widths, stats)


def main():
    stats = {'created': 0, 'skipped': 0, 'errors': 0}
    _walk_folder('products', PRODUCT_WIDTHS, stats)
    _walk_folder('banners', BANNER_WIDTHS, stats)
    print(
        f"Готово. Создано: {stats['created']}, "
        f"пропущено (актуальны): {stats['skipped']}, ошибок: {stats['errors']}"
    )
    return 0 if stats['errors'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
