/**
 * IQOS STORE — Luxury interactions: cursor, parallax, marquee, VIP form
 */
(function () {
    'use strict';

    var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var isTouch = window.matchMedia('(pointer: coarse)').matches;

    /* ── Custom cursor ── */
    function initCursor() {
        if (isTouch || prefersReduced) return;

        var dot = document.querySelector('.lux-cursor');
        var ring = document.querySelector('.lux-cursor-ring');
        if (!dot || !ring) return;

        document.body.classList.add('cursor-ready');

        var mx = -100, my = -100, rx = -100, ry = -100;

        function showCursor() {
            dot.style.opacity = '1';
            ring.style.opacity = '1';
        }

        function hideCursor() {
            dot.style.opacity = '0';
            ring.style.opacity = '0';
        }

        document.addEventListener('mousemove', function (e) {
            mx = e.clientX;
            my = e.clientY;
            showCursor();
        }, { passive: true });

        document.documentElement.addEventListener('mouseleave', hideCursor);
        document.documentElement.addEventListener('mouseenter', showCursor);

        document.addEventListener('mousedown', function () {
            document.body.classList.add('cursor-click');
        });
        document.addEventListener('mouseup', function () {
            document.body.classList.remove('cursor-click');
        });

        var hoverables = 'a, button, .lux-tile, .lux-strip-card, .lux-strip-arrow, input, .cart-widget-add, .nav-icon-btn';
        document.addEventListener('mouseover', function (e) {
            if (e.target.closest(hoverables)) {
                document.body.classList.add('cursor-hover');
            }
        });
        document.addEventListener('mouseout', function (e) {
            if (e.target.closest(hoverables)) {
                document.body.classList.remove('cursor-hover');
            }
        });

        function tick() {
            rx += (mx - rx) * 0.18;
            ry += (my - ry) * 0.18;
            dot.style.left = mx + 'px';
            dot.style.top = my + 'px';
            ring.style.left = rx + 'px';
            ring.style.top = ry + 'px';
            requestAnimationFrame(tick);
        }
        tick();
    }

    /* ── Parallax on scroll ── */
    function initParallax() {
        if (prefersReduced) return;

        var hero = document.querySelector('.lux-hero');
        var heroVideo = document.querySelector('.lux-hero-video');
        var heroContent = document.querySelector('.lux-hero-content');
        var parallaxEls = document.querySelectorAll('[data-parallax-speed]');

        function onScroll() {
            var scrollY = window.pageYOffset;

            if (hero && scrollY < window.innerHeight * 1.2) {
                var progress = scrollY / (window.innerHeight * 0.8);
                if (heroVideo) {
                    heroVideo.style.transform = 'scale(' + (1 + progress * 0.12) + ') translateY(' + (scrollY * 0.25) + 'px)';
                }
                if (heroContent) {
                    heroContent.style.transform = 'translateY(' + (scrollY * 0.35) + 'px)';
                    heroContent.style.opacity = String(Math.max(0, 1 - progress * 1.1));
                }
            }

            parallaxEls.forEach(function (el) {
                var speed = parseFloat(el.getAttribute('data-parallax-speed')) || 0.15;
                var rect = el.getBoundingClientRect();
                var center = rect.top + rect.height / 2 - window.innerHeight / 2;
                el.style.transform = 'translateY(' + (center * speed * -1) + 'px)';
            });
        }

        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    /* ── Infinite marquee duplicate ── */
    function initMarquees() {
        document.querySelectorAll('.lux-marquee-track').forEach(function (track) {
            var items = track.innerHTML;
            track.innerHTML = items + items;
        });
    }

    /* ── Horizontal strips with bottom arrows + drag scroll ── */
    function initLuxStrips() {
        document.querySelectorAll('.lux-strip').forEach(function (strip) {
            var viewport = strip.querySelector('.lux-strip-viewport');
            var nav = strip.querySelector('.lux-strip-nav');
            if (!viewport || !nav) return;

            var prev = nav.querySelector('.lux-strip-arrow--prev');
            var next = nav.querySelector('.lux-strip-arrow--next');

            function scrollStep() {
                var card = viewport.querySelector('.lux-strip-item');
                if (!card) return viewport.clientWidth * 0.85;
                var gap = parseFloat(getComputedStyle(viewport).gap) || 20;
                return card.offsetWidth + gap;
            }

            function updateArrows() {
                var maxScroll = viewport.scrollWidth - viewport.clientWidth - 2;
                if (prev) prev.disabled = viewport.scrollLeft <= 2;
                if (next) next.disabled = viewport.scrollLeft >= maxScroll;
            }

            if (prev) {
                prev.addEventListener('click', function () {
                    viewport.scrollBy({ left: -scrollStep(), behavior: 'smooth' });
                });
            }
            if (next) {
                next.addEventListener('click', function () {
                    viewport.scrollBy({ left: scrollStep(), behavior: 'smooth' });
                });
            }

            viewport.addEventListener('scroll', updateArrows, { passive: true });
            window.addEventListener('resize', updateArrows);
            updateArrows();

            if (isTouch) return;

            var dragging = false;
            var startX = 0;
            var startScroll = 0;
            var moved = false;

            function isInteractiveTarget(el) {
                return !!el.closest(
                    'button, input, textarea, select, label, .cart-widget-add, .favorite-btn, .add-to-cart-widget'
                );
            }

            viewport.addEventListener('mousedown', function (e) {
                if (e.button !== 0) return;
                if (isInteractiveTarget(e.target)) return;
                dragging = true;
                moved = false;
                startX = e.pageX;
                startScroll = viewport.scrollLeft;
                viewport.classList.add('is-dragging');
                e.preventDefault();
            }, true);

            window.addEventListener('mousemove', function (e) {
                if (!dragging) return;
                e.preventDefault();
                var dx = e.pageX - startX;
                if (Math.abs(dx) > 4) moved = true;
                viewport.scrollLeft = startScroll - dx * 1.15;
                updateArrows();
            });

            function endDrag() {
                if (!dragging) return;
                dragging = false;
                viewport.classList.remove('is-dragging');
            }

            window.addEventListener('mouseup', endDrag);
            viewport.addEventListener('mouseleave', endDrag);

            viewport.addEventListener('click', function (e) {
                if (!moved) return;
                var link = e.target.closest('a');
                if (link && viewport.contains(link)) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            }, true);

            viewport.addEventListener('dragstart', function (e) {
                e.preventDefault();
            });
        });
    }

    /* ── VIP subscription ── */
    function initVipForm() {
        var form = document.getElementById('luxVipForm');
        if (!form) return;

        var botUrl = form.getAttribute('data-bot-url') || 'https://t.me/iluma_prime_bot';

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var email = form.querySelector('input[type="email"]');
            if (email && !email.value.trim()) {
                email.focus();
                return;
            }
            try {
                localStorage.setItem('iqos_vip_subscribed', '1');
            } catch (err) { /* ignore */ }
            window.open(botUrl + '?start=vip_access', '_blank', 'noopener');
            form.reset();
        });
    }

    /* ── Reveal on scroll ── */
    function initReveal() {
        if (prefersReduced || !('IntersectionObserver' in window)) return;

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

        document.querySelectorAll('.lux-reveal').forEach(function (el) {
            observer.observe(el);
        });
    }

    function init() {
        initCursor();
        initParallax();
        initMarquees();
        initLuxStrips();
        initVipForm();
        initReveal();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
