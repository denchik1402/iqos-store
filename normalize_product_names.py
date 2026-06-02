#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Приводит названия всех товаров к единому стилю (IQOS, ILUMA, TEREA, LIL SOLID).
При изменении названия обновляет SEO-поля товара.

  python normalize_product_names.py
"""
import sys

from app import app
from extensions import db
from models import Product
from product_name_utils import normalize_product_name, normalize_description_brands
from seo_utils import generate_product_seo


def run() -> int:
    updated = 0
    with app.app_context():
        for product in Product.query.order_by(Product.id).all():
            new_name = normalize_product_name(product.name)
            new_desc = normalize_description_brands(product.description or '')
            changed = False
            if new_name and new_name != product.name:
                print(f'  {product.name!r} -> {new_name!r}')
                product.name = new_name
                changed = True
            if new_desc != (product.description or ''):
                product.description = new_desc or product.description
                changed = True
            if changed:
                seo = generate_product_seo(product)
                product.image_alt = seo['image_alt']
                product.meta_description = seo['meta_description']
                product.meta_keywords = seo['meta_keywords']
                updated += 1
        db.session.commit()
        print(f'\nОбновлено товаров: {updated}/{Product.query.count()}')
    return 0


if __name__ == '__main__':
    sys.exit(run())
