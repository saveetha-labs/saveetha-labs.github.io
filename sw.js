/* Saveetha Labs service worker — offline-first for static pages */
const VERSION = 'sl-v1';
const CORE_CACHE = `sl-core-${VERSION}`;
const RUNTIME_CACHE = `sl-runtime-${VERSION}`;

const CORE_ASSETS = [
  '/',
  '/index.html',
  '/docs.html',
  '/repo/index.html',
  '/manifest.json',
  '/knowledgebase.txt',
  '/favicon-16x16.png',
  '/favicon-32x32.png',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/icon-maskable-512.png',
  '/icons/og-banner.png'
];

/* Install: precache the core shell */
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CORE_CACHE)
      .then((cache) => cache.addAll(CORE_ASSETS))
      .then(() => self.skipWaiting())
  );
});

/* Activate: clear old caches */
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k !== CORE_CACHE && k !== RUNTIME_CACHE).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

/* Fetch: core assets from cache-first, navigations network-first w/ offline fallback,
   API + CDN requests untouched (they manage their own caching/limits). */
self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;               // skip CDN / api.github.com / raw
  if (url.pathname.startsWith('/repo/') && url.search) return;   // explorer is URL-driven; don't cache param variants

  // HTML navigations: network-first, fall back to cache, then to offline shell
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(RUNTIME_CACHE).then((c) => c.put(req, copy));
          return res;
        })
        .catch(() =>
          caches.match(req).then((cached) => cached || caches.match('/index.html'))
        )
    );
    return;
  }

  // Static assets: cache-first, then network + populate runtime cache.
  // Offline + uncached → graceful empty response instead of an unhandled rejection.
  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req)
        .then((res) => {
          if (res.ok) {
            const copy = res.clone();
            caches.open(RUNTIME_CACHE).then((c) => c.put(req, copy));
          }
          return res;
        })
        .catch(() => new Response('', { status: 503, statusText: 'Offline' }));
    })
  );
});
