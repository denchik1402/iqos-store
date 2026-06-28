/* Service Worker — iqos-store.ru (не кэшируем favicon) */
const CACHE_NAME = 'iqos-store-v3';

function isFaviconRequest(url) {
  return /^\/favicon\.(ico|png|svg)$/.test(url.pathname);
}

self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== self.location.origin) return;

  if (isFaviconRequest(url)) {
    e.respondWith(fetch(e.request, { cache: 'reload' }));
    return;
  }

  const isNav = e.request.mode === 'navigate' || e.request.destination === 'document';
  const fetchOpts = isNav ? { cache: 'reload' } : {};
  e.respondWith(
    fetch(e.request, fetchOpts).then((res) => {
      const clone = res.clone();
      if (res.ok && !url.pathname.startsWith('/admin') && !isNav && !isFaviconRequest(url)) {
        caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
      }
      return res;
    }).catch(() => caches.match(e.request))
  );
});
