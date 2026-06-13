# -*- coding: utf-8 -*-
"""
Полный аудит iqos-store: БД, картинки, SEO.
Запуск на сервере:
  cd /home/lilstore/iqos-store && source venv/bin/activate && python3 audit_site.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from urllib.parse import urljoin

ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(ROOT, 'static')
IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg')


def _blog_cover_path(cover: str) -> str:
    path = (cover or '').strip().lstrip('/')
    if not path:
        return ''
    if path.startswith('images/'):
        return path
    if path.startswith('products/') or path.startswith('blog/'):
        return f'images/{path}'
    return f'images/blog/{path}'


def _product_image_path(img: str) -> str:
    if not img:
        return ''
    if img.startswith('images/'):
        return img
    return f'images/products/{img.replace(chr(92), "/")}'


def main() -> int:
    sys.path.insert(0, ROOT)
    from app import app, db
    from models import Product, Category, DeviceModel, BlogPost, Banner, HomeBlock

    errors: list[str] = []
    warnings: list[str] = []
    ok_lines: list[str] = []

    with app.app_context():
        try:
            import config
            site_url = getattr(config, 'SITE_URL', '') or ''
            yandex_id = getattr(config, 'YANDEX_METRIKA_ID', '') or ''
        except ImportError:
            site_url = ''
            yandex_id = ''

        if site_url != 'https://iqos-store.ru':
            errors.append(f'SITE_URL={site_url!r} — должно быть https://iqos-store.ru')
        else:
            ok_lines.append(f'SITE_URL OK: {site_url}')

        if not yandex_id or not str(yandex_id).isdigit():
            warnings.append('YANDEX_METRIKA_ID не задан — создайте счётчик в metrika.yandex.ru для этого домена')
        elif site_url == 'https://iqos-store.ru' and str(yandex_id) == '109480691':
            errors.append('YANDEX_METRIKA_ID=109480691 — это счётчик lilstore.ru, нужен отдельный для iqos-store.ru')
        else:
            ok_lines.append(f'YANDEX_METRIKA_ID: {yandex_id}')

        products = Product.query.all()
        categories = Category.query.all()
        slugs_seen: set[str] = set()

        ok_lines.append(f'Товаров в БД: {len(products)}, категорий: {len(categories)}')

        missing_images = 0
        missing_seo = 0
        bad_price = 0

        for p in products:
            slug = p.get_url_slug()
            if slug in slugs_seen:
                warnings.append(f'Дублирующийся slug: {slug} ({p.name})')
            slugs_seen.add(slug)

            if not p.slug:
                warnings.append(f'Товар без slug в БД: id={p.id} {p.name!r}')
            if p.price is None or p.price <= 0:
                bad_price += 1
                errors.append(f'Некорректная цена: id={p.id} {p.name!r} price={p.price}')
            if not p.category_id:
                errors.append(f'Товар без категории: id={p.id} {p.name!r}')

            imgs = p.all_images
            if not imgs:
                missing_images += 1
                warnings.append(f'Нет изображений: id={p.id} {p.name!r}')
            else:
                for img in imgs:
                    rel = _product_image_path(img)
                    if not os.path.isfile(os.path.join(STATIC, rel.replace('/', os.sep))):
                        missing_images += 1
                        errors.append(f'Битая картинка: {p.name!r} -> {img}')

            if not (p.meta_description or '').strip():
                missing_seo += 1
            if not (p.meta_keywords or '').strip():
                missing_seo += 1

        for cat in categories:
            if not (cat.meta_description or '').strip():
                warnings.append(f'Категория без meta_description: {cat.name}')
            if cat.image:
                rel = f'images/categories/{cat.image}' if '/' not in cat.image else cat.image
                if not os.path.isfile(os.path.join(STATIC, rel.replace('/', os.sep))):
                    errors.append(f'Битая картинка категории: {cat.name} -> {cat.image}')

        for dm in DeviceModel.query.all():
            if not (dm.meta_description or '').strip():
                warnings.append(f'Модель без meta_description: {dm.name}')

        for post in BlogPost.query.filter_by(is_published=True).all():
            if not (post.meta_description or '').strip():
                warnings.append(f'Блог без meta_description: {post.slug}')
            if post.cover_image:
                rel = _blog_cover_path(post.cover_image)
                if rel and not os.path.isfile(os.path.join(STATIC, rel.replace('/', os.sep))):
                    errors.append(f'Битая обложка блога: {post.slug} -> {post.cover_image}')

        for b in Banner.query.filter_by(is_active=True).all():
            if b.image:
                rel = f'images/banners/{b.image}' if '/' not in b.image else b.image
                if not os.path.isfile(os.path.join(STATIC, rel.replace('/', os.sep))):
                    errors.append(f'Битый баннер: id={b.id} -> {b.image}')

        for hb in HomeBlock.query.filter_by(is_active=True).all():
            if hb.image:
                rel = f'images/banners/{hb.image}' if '/' not in hb.image else hb.image
                if not os.path.isfile(os.path.join(STATIC, rel.replace('/', os.sep))):
                    errors.append(f'Битый home block: {hb.title} -> {hb.image}')

        # SEO files
        robots_path = os.path.join(ROOT, 'robots.txt')
        if os.path.isfile(robots_path):
            ok_lines.append('robots.txt в корне репозитория: OK')
        else:
            warnings.append('robots.txt в корне репо отсутствует (nginx отдаёт inline)')

        base_html = os.path.join(ROOT, 'templates', 'base.html')
        if os.path.isfile(base_html):
            html = open(base_html, encoding='utf-8').read()
            if 'yandex-verification' not in html:
                errors.append('Нет yandex-verification в base.html')
            elif 'f5f465a5a59bd8da' not in html:
                warnings.append('yandex-verification в base.html — проверьте код для iqos-store.ru')
            else:
                ok_lines.append('yandex-verification в шаблоне: OK')
            if 'google-site-verification' not in html:
                warnings.append('Нет google-site-verification в base.html')
            else:
                ok_lines.append('google-site-verification в шаблоне: OK')

        in_stock = Product.query.filter_by(in_stock=True).count()
        ok_lines.append(f'В наличии (sitemap): {in_stock} товаров')
        if missing_seo:
            warnings.append(f'Товаров с неполным SEO: ~{missing_seo // 2}+ записей meta')

    print('=' * 60)
    print('АУДИТ iqos-store.ru (локальный: БД + файлы)')
    print('=' * 60)
    for line in ok_lines:
        print(f'  OK  {line}')
    for line in warnings:
        print(f'  WARN  {line}')
    for line in errors:
        print(f'  ERR  {line}')

    print('-' * 60)
    print(f'Итого: {len(errors)} ошибок, {len(warnings)} предупреждений')
    if errors:
        print('Запустите: python3 fix_product_images.py && python3 fill_seo_meta.py --refresh-keywords')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
