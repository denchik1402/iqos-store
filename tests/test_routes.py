# -*- coding: utf-8 -*-
"""Тесты маршрутов и API."""
import pytest


def test_index(client, app_ctx):
    """Главная страница возвращает 200."""
    r = client.get('/')
    assert r.status_code == 200
    assert b'\xd0\x90\xd0\x99\xd0\x9a\xd0\x9e\xd0\xa1 \xd0\xa1\xd0\xa2\xd0\x9e\xd0\xa0' in r.data or b'IQOS' in r.data


def test_catalog(client, app_ctx):
    """Каталог возвращает 200."""
    r = client.get('/catalog')
    assert r.status_code == 200


def test_catalog_404(client, app_ctx):
    """Несуществующая категория — 404."""
    r = client.get('/catalog/nonexistent-category')
    assert r.status_code == 404


def test_blog(client, app_ctx):
    """Блог — 200."""
    r = client.get('/blog')
    assert r.status_code == 200


def test_catalog_model_slug(client, app_ctx):
    """ЧПУ модели устройства — 200 или 404 если slug ещё не создан."""
    r = client.get('/catalog/iqos-iluma-i-one')
    assert r.status_code in (200, 404)


def test_search_empty(client, app_ctx):
    """Поиск без запроса — 200."""
    r = client.get('/search')
    assert r.status_code == 200


def test_search_with_query(client, app_ctx):
    """Поиск с запросом — 200."""
    r = client.get('/search?q=IQOS')
    assert r.status_code == 200


def test_search_special_chars(client, app_ctx):
    """Поиск со спецсимволами LIKE — не падает."""
    r = client.get('/search?q=%25%5C_')
    assert r.status_code == 200


def test_about(client, app_ctx):
    """О магазине — 200."""
    r = client.get('/about')
    assert r.status_code == 200


def test_contacts(client, app_ctx):
    """Контакты — 200."""
    r = client.get('/contacts')
    assert r.status_code == 200


def test_delivery(client, app_ctx):
    """Доставка — 200."""
    r = client.get('/delivery')
    assert r.status_code == 200


def test_faq(client, app_ctx):
    """FAQ — 200."""
    r = client.get('/faq')
    assert r.status_code == 200


def test_health(client, app_ctx):
    """Health check — 200."""
    r = client.get('/health')
    assert r.status_code == 200
    assert b'ok' in r.data


def test_robots(client, app_ctx):
    """robots.txt — 200."""
    r = client.get('/robots.txt')
    assert r.status_code == 200
    assert b'Sitemap' in r.data
    assert b'Disallow: /banner-click' in r.data


def test_sitemap(client, app_ctx):
    """sitemap.xml — 200."""
    r = client.get('/sitemap.xml')
    assert r.status_code == 200
    assert b'<?xml' in r.data or b'urlset' in r.data


def test_manifest(client, app_ctx):
    """manifest.json — 200, валидная структура."""
    r = client.get('/manifest.json')
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('name') == 'АЙКОС СТОР'
    assert 'start_url' in data
    assert 'icons' in data


def test_404_page(client, app_ctx):
    """Страница 404 — кастомная."""
    r = client.get('/nonexistent-page-xyz')
    assert r.status_code == 404
    assert b'404' in r.data
