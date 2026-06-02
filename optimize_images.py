#!/usr/bin/env python
"""Создаёт WebP-варианты изображений (400w / 800w / 1200w). Запуск: python optimize_images.py"""
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

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
# method=4 — быстрее method=6, размер файла чуть больше, визуально не отличить
WEBP_METHOD = 4
MAX_WORKERS = min(4, os.cpu_count() or 2)


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
    img.save(dest_path, 'WEBP', quality=QUALITY, method=WEBP_METHOD)


def _outdated_variants(src_path, folder, rel_inner, widths):
    mtime = os.path.getmtime(src_path)
    pending = []
    for width in widths:
        out_path = os.path.join(STATIC, 'images', folder, variant_rel_path(rel_inner, width))
        if not os.path.isfile(out_path) or os.path.getmtime(out_path) < mtime:
            pending.append(width)
    return pending


def _process_file_job(folder, rel_inner, widths):
    src_path = os.path.join(STATIC, 'images', folder, rel_inner)
    pending = _outdated_variants(src_path, folder, rel_inner, widths)
    if not pending:
        return {'created': 0, 'skipped': len(widths), 'errors': 0, 'messages': []}

    created = 0
    skipped = len(widths) - len(pending)
    messages = []
    try:
        with Image.open(src_path) as img:
            img = _prepare_image(img)
            for width in pending:
                out_path = os.path.join(STATIC, 'images', folder, variant_rel_path(rel_inner, width))
                resized = _resize(img, width)
                _save_webp(resized, out_path)
                created += 1
                messages.append(
                    f"OK: {folder}/{rel_inner} -> {os.path.relpath(out_path, ROOT)}"
                )
    except Exception as exc:
        return {'created': created, 'skipped': skipped, 'errors': 1, 'messages': [f'Ошибка {folder}/{rel_inner}: {exc}']}

    return {'created': created, 'skipped': skipped, 'errors': 0, 'messages': messages}


def _collect_jobs(folder, widths):
    base = os.path.join(STATIC, 'images', folder)
    if not os.path.isdir(base):
        return []
    jobs = []
    for dirpath, _, filenames in os.walk(base):
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in IMAGE_EXTENSIONS or is_variant_filename(name):
                continue
            full = os.path.join(dirpath, name)
            rel_inner = os.path.relpath(full, base).replace('\\', '/')
            jobs.append((folder, rel_inner, widths))
    return jobs


def main():
    stats = {'created': 0, 'skipped': 0, 'errors': 0}
    jobs = _collect_jobs('products', PRODUCT_WIDTHS) + _collect_jobs('banners', BANNER_WIDTHS)
    if not jobs:
        print('Нет изображений для обработки.')
        return 0

    workers = min(MAX_WORKERS, len(jobs))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_process_file_job, *job) for job in jobs]
        for future in as_completed(futures):
            result = future.result()
            stats['created'] += result['created']
            stats['skipped'] += result['skipped']
            stats['errors'] += result['errors']
            for line in result['messages']:
                print(line)

    print(
        f"Готово. Создано: {stats['created']}, "
        f"пропущено (актуальны): {stats['skipped']}, ошибок: {stats['errors']}"
    )
    return 0 if stats['errors'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
