#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SEO-контент: slug моделей, тексты категорий, статьи блога.
Запуск: python seed_seo_blog.py
"""
import sys
from datetime import datetime

from app import app
from extensions import db
from models import BlogPost, Category, DeviceModel
from seo_utils import (
    device_model_slug,
    generate_category_seo,
    generate_device_model_seo,
    normalize_device_model_name,
)

BLOG_POSTS = [
    {
        'slug': 'kak-vybrat-iqos-iluma',
        'title': 'Как выбрать IQOS ILUMA: One, Standart или Prime',
        'excerpt': 'Сравниваем три линейки IQOS Iluma i — компактность, автономность и для кого подходит каждая модель.',
        'cover_icon': 'fa-mobile-alt',
        'reading_minutes': 7,
        'meta_description': (
            'Как выбрать IQOS ILUMA: сравнение Iluma i One, Standart и Prime. '
            'Размер, батарея, цена — гайд LIL STORE для покупателей в Москве.'
        ),
        'meta_keywords': (
            'как выбрать IQOS ILUMA, Iluma i One vs Prime, IQOS ILUMA сравнение, '
            'какой IQOS купить, IQOS ILUMA гайд, LIL STORE'
        ),
        'content': '''
<div class="blog-lead">
<p>IQOS ILUMA — устройства без лезвия и без чистки. Все три модели используют стики TEREA и технологию SMARTCORE, но отличаются размером, автономностью и ценой. Разберём, какую выбрать именно вам.</p>
</div>

<h2 id="one">IQOS Iluma i One — компактный формат</h2>
<p><strong>Iluma i One</strong> — самый маленький и лёгкий вариант. Одно устройство без зарядного кейса, помещается в карман. Подходит тем, кто много в движении и не хочет носить габаритный аксессуар.</p>
<ul>
<li>Компактный корпус, минимальный вес</li>
<li>Одна сессия на заряд — нужно заряжать чаще</li>
<li>Оптимальная цена входа в линейку ILUMA</li>
</ul>
<p><a href="/catalog/iqos-iluma-i-one">Смотреть Iluma i One в каталоге →</a></p>

<h2 id="standart">IQOS Iluma i Standart — золотая середина</h2>
<p><strong>Iluma i Standart</strong> — сбалансированный вариант: больше батарея, удобный корпус, при этом не такой крупный, как Prime. Популярный выбор среди постоянных пользователей ILUMA.</p>
<ul>
<li>Увеличенная автономность по сравнению с One</li>
<li>Удобный хват, премиальные материалы</li>
<li>Широкий выбор цветов</li>
</ul>
<p><a href="/catalog/iqos-iluma-i-standart">Смотреть Iluma i Standart в каталоге →</a></p>

<h2 id="prime">IQOS Iluma i Prime — максимум возможностей</h2>
<p><strong>Iluma i Prime</strong> — топовая модель: самая ёмкая батарея, премиальный дизайн, расширенные материалы корпуса. Для тех, кто ценит автономность и статусный вид устройства.</p>
<ul>
<li>Максимальное время работы от одного заряда</li>
<li>Премиальные отделки и лимитированные цвета</li>
<li>Лучший выбор для ежедневного интенсивного использования</li>
</ul>
<p><a href="/catalog/iqos-iluma-i-prime">Смотреть Iluma i Prime в каталоге →</a></p>

<div class="blog-callout">
<h3>Краткая таблица</h3>
<table class="blog-table">
<thead><tr><th>Модель</th><th>Размер</th><th>Автономность</th><th>Кому подойдёт</th></tr></thead>
<tbody>
<tr><td>Iluma i One</td><td>Компактный</td><td>Базовая</td><td>Мобильность, первая покупка</td></tr>
<tr><td>Iluma i Standart</td><td>Средний</td><td>Хорошая</td><td>Ежедневное использование</td></tr>
<tr><td>Iluma i Prime</td><td>Крупный</td><td>Максимальная</td><td>Премиум, длительная работа</td></tr>
</tbody>
</table>
</div>

<h2>Что важно помнить</h2>
<p>Все модели ILUMA работают <strong>только со стиками TEREA</strong> — HEETS и Fiit к ним не подходят. В LIL STORE — только оригинальная продукция, бронь на сайте, доставка 1–2 дня по России.</p>
<p>Остались вопросы? Напишите в <a href="https://t.me/iluma_prime_bot" target="_blank" rel="noopener">Telegram @iluma_prime_bot</a> — поможем с выбором цвета и модели.</p>
''',
    },
    {
        'slug': 'terea-vs-heets',
        'title': 'TEREA vs HEETS: в чём разница и что выбрать',
        'excerpt': 'TEREA для ILUMA и HEETS для старых IQOS — совместимость, вкус, технология нагрева. Подробное сравнение.',
        'cover_icon': 'fa-exchange-alt',
        'reading_minutes': 6,
        'meta_description': (
            'TEREA vs HEETS: отличия стиков для IQOS ILUMA и классических IQOS/LIL. '
            'Совместимость, вкус, нагрев — сравнение от LIL STORE.'
        ),
        'meta_keywords': (
            'TEREA vs HEETS, чем отличаются TEREA от HEETS, стики TEREA, HEETS совместимость, '
            'TEREA для ILUMA, LIL STORE'
        ),
        'content': '''
<div class="blog-lead">
<p>TEREA и HEETS — оба формата нагреваемого табака, но они <strong>не взаимозаменяемы</strong>. Разберём ключевые отличия, чтобы вы не ошиблись с покупкой.</p>
</div>

<h2 id="devices">Для каких устройств</h2>
<div class="blog-callout blog-callout-info">
<ul>
<li><strong>TEREA</strong> — только для <strong>IQOS ILUMA</strong> (Iluma i One, Standart, Prime). Внутри стика есть металлический нагреваемый элемент.</li>
<li><strong>HEETS</strong> — для IQOS 3 DUOS, lil SOLID, LIL SOLID 3.0 и других устройств с лезвием. TEREA в них не работает.</li>
</ul>
</div>

<h2 id="tech">Технология нагрева</h2>
<p>IQOS ILUMA использует <strong>индукционный нагрев SMARTCORE</strong> — лезвие в устройстве не нужно, чистка не требуется. TEREA содержит встроенный металлический элемент, который нагревается изнутри.</p>
<p>Классические IQOS и LIL нагревают табак через <strong>лезвие</strong>, которое со временем загрязняется и требует обслуживания. HEETS рассчитаны именно на такой тип нагрева.</p>

<h2 id="taste">Вкус и ассортимент</h2>
<p>Линейки вкусов частично пересекаются по названиям (Amber, Yellow, Turquoise), но рецептуры разные — прямое сравнение «один в один» невозможно. TEREA часто даёт более чистый и стабильный вкус благодаря индукции.</p>
<p>У TEREA также есть линейка <strong>Pearl</strong> с капсулами (Purple Wave, Sun Pearl, Twilight Pearl и др.) — таких форматов у HEETS нет.</p>
<p><a href="/catalog/terea-sticks">Все вкусы TEREA в каталоге →</a></p>

<h2 id="table">Сравнительная таблица</h2>
<table class="blog-table">
<thead><tr><th></th><th>TEREA</th><th>HEETS</th></tr></thead>
<tbody>
<tr><td>Устройства</td><td>IQOS ILUMA</td><td>IQOS с лезвием, LIL SOLID</td></tr>
<tr><td>Нагрев</td><td>Индукция (SMARTCORE)</td><td>Контактное (лезвие)</td></tr>
<tr><td>Чистка устройства</td><td>Не нужна</td><td>Нужна периодически</td></tr>
<tr><td>Капсулы Pearl</td><td>Да</td><td>Нет</td></tr>
<tr><td>Стиков в блоке</td><td>20</td><td>20</td></tr>
</tbody>
</table>

<h2>Что выбрать</h2>
<p>Если у вас <strong>IQOS ILUMA</strong> — покупайте только TEREA. Если <strong>LIL SOLID или IQOS с лезвием</strong> — HEETS и совместимые стики.</p>
<p>В LIL STORE — оригинальные TEREA KZ и устройства ILUMA. Бронь на сайте, доставка 1–2 дня, оплата при получении.</p>
''',
    },
    {
        'slug': 'lil-solid-sravnenie',
        'title': 'LIL SOLID 3.0, Dual и 4.0: какая модель лучше',
        'excerpt': 'Сравниваем три поколения LIL SOLID — размер, батарея, совместимость со стиками и для кого подходит каждая модель.',
        'cover_icon': 'fa-bolt',
        'reading_minutes': 6,
        'meta_description': (
            'LIL SOLID 3.0 vs Dual vs 4.0: сравнение моделей, батареи и совместимости со стиками HEETS. '
            'Гайд по выбору LIL SOLID от LIL STORE.'
        ),
        'meta_keywords': (
            'LIL SOLID 3.0, LIL SOLID Dual, LIL SOLID 4.0, сравнение LIL SOLID, '
            'какой LIL SOLID купить, LIL STORE'
        ),
        'content': '''
<div class="blog-lead">
<p>LIL SOLID — доступная альтернатива IQOS с контактным нагревом через лезвие. В линейке три актуальные модели: <strong>3.0</strong>, <strong>Dual</strong> и <strong>4.0</strong>. Разберём отличия, чтобы выбрать подходящую.</p>
</div>

<h2 id="lil-30">LIL SOLID 3.0 — проверенная классика</h2>
<p>Базовая модель с зарядным кейсом. Надёжный формат «устройство + кейс», привычный всем пользователям IQOS 3 DUOS. Работает со стиками HEETS и совместимыми форматами.</p>
<ul>
<li>Компактный кейс на несколько сессий</li>
<li>Доступная цена входа в экосистему LIL</li>
<li>Периодическая чистка лезвия обязательна</li>
</ul>
<p><a href="/catalog/lil-solid-3-0">Смотреть LIL SOLID 3.0 в каталоге →</a></p>

<h2 id="dual">LIL SOLID Dual — два стика подряд</h2>
<p><strong>Dual</strong> — главное отличие: можно использовать <strong>два стика подряд</strong> без паузы на зарядку. Удобно, если вы привыкли к двум сессиям за один подход.</p>
<ul>
<li>Режим двойной сессии — редкая функция в сегменте</li>
<li>Увеличенная батарея по сравнению с 3.0</li>
<li>Те же стики HEETS, что и у остальных LIL</li>
</ul>
<p><a href="/catalog/lil-solid-dual">Смотреть LIL SOLID Dual в каталоге →</a></p>

<h2 id="lil-40">LIL SOLID 4.0 — новое поколение</h2>
<p>Самая свежая модель с обновлённым дизайном, улучшенной автономностью и более быстрой зарядкой. Подходит тем, кто хочет актуальное устройство с максимальным комфортом в линейке LIL.</p>
<ul>
<li>Обновлённый корпус и эргономика</li>
<li>Лучшая автономность в линейке</li>
<li>Быстрая зарядка кейса и держателя</li>
</ul>
<p><a href="/catalog/lil-solid-4-0">Смотреть LIL SOLID 4.0 в каталоге →</a></p>

<div class="blog-callout">
<h3>Краткое сравнение</h3>
<table class="blog-table">
<thead><tr><th>Модель</th><th>Особенность</th><th>Стики</th><th>Кому подойдёт</th></tr></thead>
<tbody>
<tr><td>LIL SOLID 3.0</td><td>Классический формат</td><td>HEETS</td><td>Первая покупка, бюджет</td></tr>
<tr><td>LIL SOLID Dual</td><td>2 стика подряд</td><td>HEETS</td><td>Интенсивное использование</td></tr>
<tr><td>LIL SOLID 4.0</td><td>Новое поколение</td><td>HEETS</td><td>Максимум автономности</td></tr>
</tbody>
</table>
</div>

<h2>Важно: LIL ≠ ILUMA</h2>
<p>Все модели LIL SOLID работают со <strong>стиками HEETS</strong>, а не TEREA. TEREA предназначены только для IQOS ILUMA. Если планируете перейти на ILUMA — смотрите наш гайд <a href="/blog/kak-vybrat-iqos-iluma">«Как выбрать IQOS ILUMA»</a>.</p>
<p><a href="/catalog/lil">Все устройства LIL в каталоге →</a></p>
''',
    },
    {
        'slug': 'luchshie-vkusu-terea',
        'title': 'Лучшие вкусы TEREA: полный гид по линейке',
        'excerpt': 'Amber, Yellow, Turquoise, Pearl и другие — разбираем вкусовую линейку TEREA и помогаем выбрать первый блок.',
        'cover_icon': 'fa-palette',
        'reading_minutes': 8,
        'meta_description': (
            'Лучшие вкусы TEREA: Amber, Yellow, Turquoise, Pearl и другие. '
            'Гид по выбору стиков TEREA для IQOS ILUMA от LIL STORE.'
        ),
        'meta_keywords': (
            'вкусы TEREA, TEREA Amber, TEREA Yellow, TEREA Turquoise, '
            'TEREA Pearl, какой TEREA выбрать, стики TEREA, LIL STORE'
        ),
        'content': '''
<div class="blog-lead">
<p>Линейка TEREA насчитывает десятки вкусов — от классического табака до фруктовых капсул Pearl. Разберём основные группы, чтобы вы быстро нашли свой вариант.</p>
</div>

<h2 id="classic">Классические табачные вкусы</h2>
<p>Для тех, кто привык к традиционному табаку без ярких добавок:</p>
<ul>
<li><strong>TEREA Amber</strong> — насыщенный, с лёгкими ореховыми нотами. Один из самых популярных вкусов.</li>
<li><strong>TEREA Yellow</strong> — более мягкий и лёгкий табак, хорош для ежедневного использования.</li>
<li><strong>TEREA Russet</strong> — глубокий, насыщенный вкус для опытных пользователей.</li>
<li><strong>TEREA Teak</strong> — сбалансированный табак с древесными оттенками.</li>
</ul>

<h2 id="fresh">Свежие и ментоловые</h2>
<p>Если нравится ощущение свежести и лёгкий холодок:</p>
<ul>
<li><strong>TEREA Turquoise</strong> — классика с ментолом, освежающий и чистый.</li>
<li><strong>TEREA Blue</strong> — мягкий ментол, менее интенсивный чем Turquoise.</li>
<li><strong>TEREA Green</strong> — ментол с мятными нотами.</li>
<li><strong>TEREA Silver</strong> — лёгкий свежий табак без сильного ментола.</li>
</ul>

<h2 id="pearl">Линейка Pearl — с капсулами</h2>
<p>Уникальная для TEREA серия с <strong>ароматической капсулой</strong> в фильтре. Нажимаете на капсулу — и вкус меняется:</p>
<ul>
<li><strong>Purple Wave Pearl</strong> — ягодные ноты после активации капсулы.</li>
<li><strong>Sun Pearl</strong> — тропический фруктовый аромат.</li>
<li><strong>Twilight Pearl</strong> — глубокие ягодные и фруктовые оттенки.</li>
</ul>
<p>Подробнее о технологии Pearl — в статье <a href="/blog/terea-pearl-kapsuly">«TEREA Pearl: что такое капсулы»</a>.</p>

<h2 id="choose">Как выбрать первый блок</h2>
<div class="blog-callout blog-callout-info">
<ul>
<li>Новичкам — <strong>Yellow</strong> или <strong>Silver</strong> (мягкие, нейтральные)</li>
<li>Любителям классики — <strong>Amber</strong> или <strong>Teak</strong></li>
<li>Фанатам ментола — <strong>Turquoise</strong> или <strong>Blue</strong></li>
<li>Хочется экспериментов — любой <strong>Pearl</strong></li>
</ul>
</div>
<p>В LIL STORE — оригинальные TEREA KZ, все вкусы в наличии. Можно заказать несколько блоков и найти свой.</p>
<p><a href="/catalog/terea-sticks">Все вкусы TEREA в каталоге →</a></p>
''',
    },
    {
        'slug': 'terea-pearl-kapsuly',
        'title': 'TEREA Pearl: что такое капсулы и какие вкусы попробовать',
        'excerpt': 'Разбираем линейку TEREA Pearl — технология ароматических капсул, отличия от обычных TEREA и топовые вкусы.',
        'cover_icon': 'fa-gem',
        'reading_minutes': 5,
        'meta_description': (
            'TEREA Pearl: что такое капсулы в стиках, как активировать, лучшие вкусы Purple Wave, '
            'Sun Pearl, Twilight Pearl. Гайд LIL STORE.'
        ),
        'meta_keywords': (
            'TEREA Pearl, TEREA капсулы, Purple Wave Pearl, Sun Pearl, Twilight Pearl, '
            'стики TEREA с капсулой, LIL STORE'
        ),
        'content': '''
<div class="blog-lead">
<p><strong>TEREA Pearl</strong> — особая линейка стиков с ароматической капсулой в фильтре. Это эксклюзив формата TEREA: у HEETS таких вкусов нет. Разберём, как это работает и что попробовать первым.</p>
</div>

<h2 id="how">Как работает капсула</h2>
<p>В фильтре каждого стика Pearl спрятана <strong>ароматическая капсула</strong>. Во время сессии вы можете нажать на фильтр — капсула лопается, и вкус меняется: добавляются фруктовые или ягодные ноты поверх базового табака.</p>
<p>Это даёт два вкуса в одном стике: сначала классический нагреваемый табак, затем — яркий аромат после активации.</p>

<h2 id="flavors">Популярные вкусы Pearl</h2>
<ul>
<li><strong>Purple Wave Pearl</strong> — один из бestseller'ов. Базовый табак + ягодный взрыв после капсулы. Яркий и запоминающийся.</li>
<li><strong>Sun Pearl</strong> — тропические фруктовые ноты. Лёгкий, летний характер.</li>
<li><strong>Twilight Pearl</strong> — глубокие ягодные оттенки, более насыщенный профиль.</li>
</ul>

<div class="blog-callout">
<h3>Pearl vs обычные TEREA</h3>
<table class="blog-table">
<thead><tr><th></th><th>Обычные TEREA</th><th>TEREA Pearl</th></tr></thead>
<tbody>
<tr><td>Капсула</td><td>Нет</td><td>Да, в фильтре</td></tr>
<tr><td>Вкус</td><td>Стабильный от начала до конца</td><td>Два этапа: табак → аромат</td></tr>
<tr><td>Для кого</td><td>Классика, ментол</td><td>Любители экспериментов</td></tr>
<tr><td>Устройство</td><td>IQOS ILUMA</td><td>IQOS ILUMA</td></tr>
</tbody>
</table>
</div>

<h2 id="tips">Советы по использованию</h2>
<ul>
<li>Активируйте капсулу в середине или конце сессии — так вы почувствуете оба вкуса.</li>
<li>Не нажимайте слишком сильно — достаточно лёгкого надавливания на фильтр.</li>
<li>Pearl совместимы только с <strong>IQOS ILUMA</strong> — как и все TEREA.</li>
</ul>
<p><a href="/catalog/terea-sticks">Купить TEREA Pearl в каталоге →</a></p>
''',
    },
    {
        'slug': 'iqos-iluma-vs-lil-solid',
        'title': 'IQOS ILUMA или LIL SOLID: что выбрать в 2026 году',
        'excerpt': 'Сравниваем две популярные экосистемы — технология нагрева, стики, цена, уход и кому что подойдёт.',
        'cover_icon': 'fa-balance-scale',
        'reading_minutes': 7,
        'meta_description': (
            'IQOS ILUMA vs LIL SOLID: сравнение технологий, стиков TEREA и HEETS, цены и ухода. '
            'Что выбрать — гайд LIL STORE.'
        ),
        'meta_keywords': (
            'IQOS ILUMA vs LIL SOLID, что лучше ILUMA или LIL, TEREA vs HEETS, '
            'сравнение IQOS и LIL, LIL STORE'
        ),
        'content': '''
<div class="blog-lead">
<p>Два главных игрока на рынке нагреваемого табака — <strong>IQOS ILUMA</strong> и <strong>LIL SOLID</strong>. Оба решают одну задачу, но принципиально по-разному. Поможем определиться.</p>
</div>

<h2 id="tech">Технология: индукция vs лезвие</h2>
<p><strong>IQOS ILUMA</strong> — индукционный нагрев SMARTCORE. Лезвия нет, чистка не нужна, устройство служит дольше без обслуживания. Стики TEREA содержат встроенный металлический элемент.</p>
<p><strong>LIL SOLID</strong> — классический контактный нагрев через лезвие (как у IQOS 3 DUOS). Лезвие нужно периодически чистить, но устройства дешевле.</p>

<h2 id="sticks">Стики: TEREA vs HEETS</h2>
<div class="blog-callout blog-callout-info">
<ul>
<li><strong>ILUMA</strong> → только <strong>TEREA</strong> (20 стиков в блоке)</li>
<li><strong>LIL SOLID</strong> → <strong>HEETS</strong> и совместимые форматы</li>
</ul>
<p>Стики <strong>не взаимозаменяемы</strong>. Подробнее — в статье <a href="/blog/terea-vs-heets">«TEREA vs HEETS»</a>.</p>
</div>

<h2 id="compare">Сравнительная таблица</h2>
<table class="blog-table">
<thead><tr><th></th><th>IQOS ILUMA</th><th>LIL SOLID</th></tr></thead>
<tbody>
<tr><td>Нагрев</td><td>Индукция (без лезвия)</td><td>Лезвие</td></tr>
<tr><td>Чистка</td><td>Не нужна</td><td>Раз в 1–2 недели</td></tr>
<tr><td>Стики</td><td>TEREA</td><td>HEETS</td></tr>
<tr><td>Цена устройства</td><td>Выше</td><td>Ниже</td></tr>
<tr><td>Капсулы Pearl</td><td>Да</td><td>Нет</td></tr>
<tr><td>Модели</td><td>One, Standart, Prime</td><td>3.0, Dual, 4.0</td></tr>
</tbody>
</table>

<h2 id="who">Кому что подойдёт</h2>
<p><strong>Выбирайте IQOS ILUMA, если:</strong></p>
<ul>
<li>Хотите устройство без обслуживания и чистки</li>
<li>Интересуют вкусы TEREA и линейка Pearl</li>
<li>Готовы инвестировать в премиальный опыт</li>
</ul>
<p><strong>Выбирайте LIL SOLID, если:</strong></p>
<ul>
<li>Нужен доступный вход в нагреваемый табак</li>
<li>Уже привыкли к HEETS</li>
<li>Не смущает периодическая чистка лезвия</li>
</ul>
<p><a href="/catalog/iqos-iluma">IQOS ILUMA в каталоге →</a> · <a href="/catalog/lil">LIL SOLID в каталоге →</a></p>
''',
    },
    {
        'slug': 'uhod-za-iqos-iluma',
        'title': 'Уход за IQOS ILUMA: зарядка, хранение и типичные ошибки',
        'excerpt': 'Как правильно заряжать ILUMA, можно ли мыть устройство и что делать, если стик не нагревается.',
        'cover_icon': 'fa-tools',
        'reading_minutes': 5,
        'meta_description': (
            'Уход за IQOS ILUMA: зарядка, хранение, чистка, типичные ошибки. '
            'Советы по эксплуатации Iluma i One, Standart, Prime от LIL STORE.'
        ),
        'meta_keywords': (
            'уход за IQOS ILUMA, как заряжать ILUMA, ILUMA не работает, '
            'чистка IQOS ILUMA, эксплуатация ILUMA, LIL STORE'
        ),
        'content': '''
<div class="blog-lead">
<p>IQOS ILUMA — одно из самых «беззаботных» устройств в линейке: нет лезвия, нет чистки. Но несколько простых правил помогут продлить срок службы и избежать проблем.</p>
</div>

<h2 id="charge">Зарядка</h2>
<ul>
<li>Используйте <strong>оригинальный кабель и адаптер</strong> (или качественный аналог 5V/2A).</li>
<li>Не заряжайте на солнце или рядом с нагревателями — перегрев сокращает ресурс батареи.</li>
<li>Для моделей с кейсом (Standart, Prime) заряжайте сначала кейс, затем вставляйте держатель.</li>
<li>Iluma i One заряжается напрямую — без кейса.</li>
</ul>

<h2 id="storage">Хранение</h2>
<ul>
<li>Храните при комнатной температуре (+15…+25 °C).</li>
<li>Избегайте влажности — устройство не водонепроницаемо.</li>
<li>Стики TEREA храните в сухом месте, в оригинальной упаковке.</li>
</ul>

<h2 id="clean">Нужна ли чистка?</h2>
<p><strong>Нет.</strong> Главное преимущество ILUMA — отсутствие лезвия. Не нужны палочки, щётки и спирт. Достаточно иногда протереть корпус сухой мягкой тканью.</p>
<div class="blog-callout blog-callout-info">
<p><strong>Важно:</strong> не мойте устройство водой и не погружайте в жидкость. Это приведёт к поломке.</p>
</div>

<h2 id="problems">Стик не нагревается — что проверить</h2>
<ul>
<li>Убедитесь, что используете <strong>TEREA</strong>, а не HEETS.</li>
<li>Стик вставлен до упора — металлический элемент должен быть внутри.</li>
<li>Батарея не разряжена — зарядите устройство.</li>
<li>Если проблема повторяется — напишите в <a href="https://t.me/iluma_prime_bot" target="_blank" rel="noopener">Telegram @iluma_prime_bot</a>.</li>
</ul>
<p><a href="/catalog/terea-sticks">Купить TEREA →</a> · <a href="/catalog/iqos-iluma">Устройства ILUMA →</a></p>
''',
    },
    {
        'slug': 'perehod-na-iluma',
        'title': 'Переход с IQOS на ILUMA: что нужно знать',
        'excerpt': 'Меняете классический IQOS или LIL на ILUMA? Рассказываем про новые стики TEREA, отличия в использовании и что делать со старым устройством.',
        'cover_icon': 'fa-arrow-right',
        'reading_minutes': 6,
        'meta_description': (
            'Переход с IQOS на ILUMA: что меняется, новые стики TEREA, отличия от HEETS. '
            'Гайд для пользователей классического IQOS и LIL SOLID от LIL STORE.'
        ),
        'meta_keywords': (
            'переход на IQOS ILUMA, с IQOS на ILUMA, TEREA вместо HEETS, '
            'обновить IQOS до ILUMA, LIL STORE'
        ),
        'content': '''
<div class="blog-lead">
<p>Решили перейти с классического IQOS или LIL SOLID на <strong>IQOS ILUMA</strong>? Это большой шаг вперёд — но есть несколько важных моментов, о которых стоит знать заранее.</p>
</div>

<h2 id="sticks">Главное: новые стики</h2>
<p>ILUMA работает <strong>только с TEREA</strong>. Все запасы HEETS, Fiit и других стиков для лезвийных устройств к ILUMA не подходят. Заранее закажите TEREA — в LIL STORE все вкусы в наличии.</p>
<p>Не переживайте: многие названия вкусов совпадают (Amber, Yellow, Turquoise), так что найти привычный профиль несложно. Подробное сравнение — в статье <a href="/blog/terea-vs-heets">«TEREA vs HEETS»</a>.</p>

<h2 id="diff">Что изменится в использовании</h2>
<ul>
<li><strong>Нет чистки</strong> — забудьте про палочки и щётки. ILUMA не имеет лезвия.</li>
<li><strong>Другой формат стика</strong> — TEREA чуть короче и имеет металлический элемент внутри.</li>
<li><strong>Тот же принцип</strong> — вставил стик, нажал кнопку, 14 секунд нагрев, ~6 минут сессия.</li>
<li><strong>Новые вкусы</strong> — линейка Pearl с капсулами доступна только для TEREA.</li>
</ul>

<h2 id="choose">Какую модель ILUMA выбрать</h2>
<p>Три варианта: <strong>One</strong> (компактный), <strong>Standart</strong> (сбалансированный), <strong>Prime</strong> (максимум автономности). Подробный разбор — в гайде <a href="/blog/kak-vybrat-iqos-iluma">«Как выбрать IQOS ILUMA»</a>.</p>

<div class="blog-callout">
<h3>Чек-лист перехода</h3>
<ul>
<li>☐ Выбрать модель ILUMA (One / Standart / Prime)</li>
<li>☐ Заказать 2–3 блока TEREA разных вкусов</li>
<li>☐ Зарядить новое устройство перед первой сессией</li>
<li>☐ Старые HEETS можно использовать в LIL SOLID или передать знакомым</li>
</ul>
</div>

<h2 id="buy">Где купить</h2>
<p>В LIL STORE — оригинальные устройства IQOS ILUMA и TEREA KZ. Бронь на сайте, доставка 1–2 дня по России, оплата при получении.</p>
<p><a href="/catalog/iqos-iluma">Устройства ILUMA →</a> · <a href="/catalog/terea-sticks">Стики TEREA →</a></p>
''',
    },
    {
        'slug': 'skolko-stoit-iqos-iluma',
        'title': 'Сколько стоит IQOS ILUMA: цены на устройства и стики TEREA',
        'excerpt': 'Актуальные цены на Iluma i One, Standart, Prime и блоки TEREA. Что входит в стоимость и как сэкономить при покупке.',
        'cover_icon': 'fa-ruble-sign',
        'reading_minutes': 4,
        'meta_description': (
            'Цены на IQOS ILUMA: Iluma i One, Standart, Prime и стики TEREA. '
            'Сколько стоит IQOS ILUMA и TEREA — актуальные цены LIL STORE.'
        ),
        'meta_keywords': (
            'сколько стоит IQOS ILUMA, цена ILUMA, цена TEREA, '
            'IQOS ILUMA цена Москва, купить ILUMA недорого, LIL STORE'
        ),
        'content': '''
<div class="blog-lead">
<p>Цены на IQOS ILUMA и стики TEREA зависят от модели и вкуса. Ниже — ориентиры по линейке. Актуальные цены всегда на сайте в каталоге.</p>
</div>

<h2 id="devices">Цены на устройства</h2>
<p>Стоимость зависит от модели:</p>
<ul>
<li><strong>Iluma i One</strong> — самый доступный вход в линейку ILUMA. Компактный формат без кейса.</li>
<li><strong>Iluma i Standart</strong> — средний сегмент, оптимальное соотношение цены и автономности.</li>
<li><strong>Iluma i Prime</strong> — топовая модель с максимальной батареей и премиальными материалами.</li>
</ul>
<p>Точные цены с учётом акций — на страницах моделей:</p>
<p><a href="/catalog/iqos-iluma-i-one">Iluma i One →</a> · <a href="/catalog/iqos-iluma-i-standart">Standart →</a> · <a href="/catalog/iqos-iluma-i-prime">Prime →</a></p>

<h2 id="terea">Цены на TEREA</h2>
<p>Блок TEREA содержит <strong>20 стиков</strong>. Цена блока зависит от вкуса — классические (Amber, Yellow) и Pearl могут немного отличаться. В LIL STORE — только оригинальные TEREA KZ.</p>
<p><a href="/catalog/terea-sticks">Все цены на TEREA в каталоге →</a></p>

<h2 id="save">Как сэкономить</h2>
<ul>
<li>Следите за <strong>акциями и скидками</strong> на главной странице — хиты и товары со скидкой обновляются регулярно.</li>
<li>Заказывайте несколько блоков TEREA за раз — экономите на доставке.</li>
<li>Iluma i One — лучший старт, если бюджет ограничен.</li>
</ul>

<div class="blog-callout blog-callout-info">
<p>В LIL STORE — бронь на сайте, доставка 1–2 дня по России, оплата при получении. Вопросы по ценам — в <a href="https://t.me/iluma_prime_bot" target="_blank" rel="noopener">Telegram @iluma_prime_bot</a>.</p>
</div>
''',
    },
]


def seed_device_model_slugs() -> int:
    updated = 0
    for dm in DeviceModel.query.all():
        name = normalize_device_model_name(dm.name)
        slug = device_model_slug(name)
        if dm.slug != slug:
            dm.slug = slug
            updated += 1
    return updated


def seed_category_seo_text() -> int:
    updated = 0
    for category in Category.query.all():
        seo = generate_category_seo(category)
        changed = False
        if seo.get('seo_text') and not (category.description or '').strip():
            category.description = seo['seo_text']
            changed = True
        if changed:
            updated += 1
    return updated


def seed_device_model_seo_text() -> int:
    updated = 0
    for dm in DeviceModel.query.all():
        seo = generate_device_model_seo(dm)
        if seo.get('seo_text') and not (dm.seo_text or '').strip():
            dm.seo_text = seo['seo_text']
            updated += 1
    return updated


def seed_blog_posts() -> int:
    created = 0
    now = datetime.utcnow()
    for data in BLOG_POSTS:
        if BlogPost.query.filter_by(slug=data['slug']).first():
            continue
        post = BlogPost(
            slug=data['slug'],
            title=data['title'],
            excerpt=data['excerpt'],
            content=data['content'].strip(),
            meta_description=data['meta_description'],
            meta_keywords=data['meta_keywords'],
            cover_icon=data.get('cover_icon', 'fa-book-open'),
            reading_minutes=data.get('reading_minutes', 5),
            is_published=True,
            created_at=now,
            updated_at=now,
        )
        db.session.add(post)
        created += 1
    return created


def main() -> int:
    with app.app_context():
        slugs = seed_device_model_slugs()
        cats = seed_category_seo_text()
        models = seed_device_model_seo_text()
        posts = seed_blog_posts()
        db.session.commit()
        print(f'Модели: slug обновлено {slugs}, seo_text {models}')
        print(f'Категории: seo_text {cats}')
        print(f'Блог: создано статей {posts}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
