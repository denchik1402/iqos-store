# -*- coding: utf-8 -*-
"""
Проверка публичного сайта iqos-store.ru (SEO, страницы, картинки).
Запуск: py audit_live.py
"""
from __future__ import annotations

import re
import ssl
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = 'https://iqos-store.ru'
TIMEOUT = 20
UA = 'Mozilla/5.0 (compatible; SiteAudit/1.0; +https://iqos-store.ru)'


def fetch(url: str, method: str = 'GET', retries: int = 3) -> tuple[int, str, dict]:
    req = urllib.request.Request(url, method=method, headers={'User-Agent': UA})
    ctx = ssl.create_default_context()
    last_err = ''
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
                body = r.read(500_000).decode('utf-8', errors='replace')
                return r.status, body, dict(r.headers)
        except urllib.error.HTTPError as e:
            body = e.read(300_000).decode('utf-8', errors='replace') if e.fp else ''
            return e.code, body, dict(e.headers)
        except Exception as e:
            last_err = str(e)
            if attempt + 1 < retries:
                import time
                time.sleep(1.5 * (attempt + 1))
    return 0, last_err, {}


def print_report(ok, warnings, errors):
    print('=' * 60)
    print('АУДИТ LIVE https://iqos-store.ru')
    print('=' * 60)
    for x in ok:
        print(f'  OK   {x}')
    for x in warnings:
        print(f'  WARN {x}')
    for x in errors:
        print(f'  ERR  {x}')
    print('-' * 60)
    print(f'Итого: {len(errors)} ошибок, {len(warnings)} предупреждений')


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    ok: list[str] = []

    for url in ('http://iqos-store.ru/robots.txt', f'{BASE}/robots.txt'):
        code, body, _ = fetch(url)
        if code == 200 and 'Sitemap:' in body and 'Disallow: /admin' in body:
            ok.append(f'robots.txt {url} -> 200')
        else:
            errors.append(f'robots.txt {url} -> {code}')

    code, sm_body, _ = fetch(f'{BASE}/sitemap.xml')
    if code != 200:
        errors.append(f'sitemap.xml -> {code}')
        print_report(ok, warnings, errors)
        return 1

    if 'https://iqos-store.ru/' not in sm_body or 'lilstore.ru' in sm_body:
        errors.append('sitemap: неверный домен или lilstore.ru в URL')
    else:
        ok.append('sitemap.xml домен iqos-store.ru OK')

    try:
        root = ET.fromstring(sm_body)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//sm:loc', ns) or root.findall('.//{*}loc')]
    except ET.ParseError as e:
        errors.append(f'sitemap parse error: {e}')
        urls = []

    ok.append(f'sitemap: {len(urls)} URL')

    code, home, _ = fetch(BASE + '/')
    if code != 200:
        errors.append(f'Главная -> {code}')
    else:
        ok.append('Главная -> 200')
        for tag, needle in (
            ('yandex-verification', 'f5f465a5a59bd8da'),
            ('google-site-verification', 'HQ9vRHnnwg'),
            ('canonical', 'iqos-store.ru'),
            ('schema.org', 'WebSite'),
        ):
            if needle.lower() in home.lower():
                ok.append(f'Главная: {tag}')
            else:
                errors.append(f'Главная: нет {tag} ({needle})')

    for q in ('iluma', '%D0%B8%D0%BB%D1%8E%D0%BC%D0%B0', '%D0%B0%D0%B9%D0%BA%D0%BE%D1%81'):
        code, body, _ = fetch(f'{BASE}/search?q={q}')
        if code == 200:
            ok.append(f'Поиск ?q={q} -> 200')
        else:
            errors.append(f'Поиск ?q={q} -> {code}')

    key_pages = [u for u in urls if '/product/' not in u]
    product_urls = [u for u in urls if '/product/' in u]
    sample = list(dict.fromkeys(key_pages + product_urls))

    broken_pages: list[str] = []
    broken_imgs: list[str] = []

    def check_page(url: str) -> tuple[str, int, list[str]]:
        c, body, _ = fetch(url)
        imgs = re.findall(r'(?:src|href)=["\'](/static/images/[^"\']+)["\']', body)
        imgs += re.findall(r'https://iqos-store\.ru/static/images/[^"\']+', body)
        bad = []
        for img in imgs[:8]:
            img_url = img if img.startswith('http') else BASE + img
            ic, _, _ = fetch(img_url)
            if ic != 200:
                bad.append(img_url)
        return url, c, bad

    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = [ex.submit(check_page, u) for u in sample]
        for fut in as_completed(futs):
            url, c, bad_imgs = fut.result()
            if c != 200:
                broken_pages.append(f'{url} -> {c}')
            broken_imgs.extend(bad_imgs)

    if broken_pages:
        errors.extend([f'Страница: {x}' for x in broken_pages[:20]])
    else:
        ok.append(f'Страниц проверено {len(sample)} — все 200')

    if broken_imgs:
        errors.extend([f'Битая картинка: {x}' for x in list(dict.fromkeys(broken_imgs))[:15]])
    else:
        ok.append('Картинки на проверенных страницах: OK')

    for path in ('/health', '/favicon.svg'):
        c, _, _ = fetch(BASE + path)
        if c == 200:
            ok.append(f'{path} -> 200')
        else:
            warnings.append(f'{path} -> {c}')

    print_report(ok, warnings, errors)
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
