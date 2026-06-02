#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Заполнение SEO-полей (image_alt, meta_description, meta_keywords) для товаров и категорий.

Использование:
  python fill_seo_meta.py           # только пустые поля
  python fill_seo_meta.py --force   # перезаписать все SEO-поля
"""
import argparse
import sys

from app import app
from extensions import db
from models import Category, Product
from seo_utils import generate_category_seo, generate_product_seo


def _should_set(current: str | None, force: bool) -> bool:
    return force or not (current or '').strip()


def fill_seo(force: bool = False) -> tuple[int, int]:
    categories_updated = 0
    products_updated = 0

    for category in Category.query.order_by(Category.id).all():
        seo = generate_category_seo(category)
        changed = False
        if _should_set(category.meta_description, force):
            category.meta_description = seo['meta_description']
            changed = True
        if _should_set(category.meta_keywords, force):
            category.meta_keywords = seo['meta_keywords']
            changed = True
        if changed:
            categories_updated += 1

    for product in Product.query.order_by(Product.id).all():
        seo = generate_product_seo(product)
        changed = False
        if _should_set(product.image_alt, force):
            product.image_alt = seo['image_alt']
            changed = True
        if _should_set(product.meta_description, force):
            product.meta_description = seo['meta_description']
            changed = True
        if _should_set(product.meta_keywords, force):
            product.meta_keywords = seo['meta_keywords']
            changed = True
        if changed:
            products_updated += 1

    db.session.commit()
    return categories_updated, products_updated


def main() -> int:
    parser = argparse.ArgumentParser(description='Fill SEO meta fields for products and categories')
    parser.add_argument('--force', action='store_true', help='Overwrite existing SEO values')
    args = parser.parse_args()

    with app.app_context():
        cats, prods = fill_seo(force=args.force)
        print(f'Updated categories: {cats}')
        print(f'Updated products: {prods}')
        total = Category.query.count()
        filled_c = Category.query.filter(Category.meta_description.isnot(None)).count()
        filled_p = Product.query.filter(Product.meta_description.isnot(None)).count()
        print(f'Categories with meta_description: {filled_c}/{total}')
        print(f'Products with meta_description: {filled_p}/{Product.query.count()}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
