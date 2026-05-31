const CACHE_NAME = 'lunar-data-pwa-v1';
const APP_SCOPE = '/LunarData/';
const APP_ORIGIN = self.location.origin;

const PRECACHE_URLS = [
  '/LunarData/',
  '/LunarData/index.html',
  '/LunarData/manifest.json',
  '/LunarData/ninestar.html',
  '/LunarData/assets/holidays.js',
  '/LunarData/assets/holidays.json',
  '/LunarData/assets/thai-buddhist-days.js',
  '/LunarData/assets/zodiac/rat.png',
  '/LunarData/assets/zodiac/ox.png',
  '/LunarData/assets/zodiac/tiger.png',
  '/LunarData/assets/zodiac/rabbit.png',
  '/LunarData/assets/zodiac/dragon.png',
  '/LunarData/assets/zodiac/snake.png',
  '/LunarData/assets/zodiac/horse.png',
  '/LunarData/assets/zodiac/sheep.png',
  '/LunarData/assets/zodiac/monkey.png',
  '/LunarData/assets/zodiac/rooster.png',
  '/LunarData/assets/zodiac/dog.png',
  '/LunarData/assets/zodiac/pig.png',
  '/LunarData/icons/icon-192.png',
  '/LunarData/icons/icon-512.png',
  '/LunarData/icons/icon-maskable-512.png',
  '/LunarData/icons/apple-touch-icon.png'
];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    await Promise.all(
      PRECACHE_URLS.map(async url => {
        try {
          await cache.add(url);
        } catch (error) {
          console.warn('Precache failed:', url, error);
        }
      })
    );
    self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys
        .filter(key => key !== CACHE_NAME)
        .map(key => caches.delete(key))
    );
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const request = event.request;

  if (request.method !== 'GET') {
    return;
  }

  const url = new URL(request.url);

  if (url.origin !== APP_ORIGIN) {
    return;
  }

  if (!url.pathname.startsWith(APP_SCOPE)) {
    return;
  }

  if (request.mode === 'navigate') {
    event.respondWith(handleNavigationRequest(request));
    return;
  }

  if (isStaleWhileRevalidateTarget(url)) {
    event.respondWith(handleStaleWhileRevalidate(event, request));
  }
});

async function handleNavigationRequest(request) {
  const cache = await caches.open(CACHE_NAME);
  const fallback = await cache.match('/LunarData/index.html');

  try {
    const response = await fetch(request);
    cache.put('/LunarData/index.html', response.clone());
    return response;
  } catch (error) {
    if (fallback) {
      return fallback;
    }
    throw error;
  }
}

async function handleStaleWhileRevalidate(event, request) {
  const cache = await caches.open(CACHE_NAME);
  const cacheKey = normalizeCacheKey(request.url);
  const cached = await cache.match(cacheKey);
  const networkPromise = fetch(request)
    .then(response => {
      if (response && response.ok) {
        cache.put(cacheKey, response.clone());
      }
      return response;
    })
    .catch(() => null);

  if (cached) {
    event.waitUntil(networkPromise);
    return cached;
  }

  const networkResponse = await networkPromise;
  if (networkResponse) {
    return networkResponse;
  }

  return Response.error();
}

function isStaleWhileRevalidateTarget(url) {
  if (/\.(?:css|js|json|png|jpg|jpeg|gif|svg|webp|ico)$/i.test(url.pathname)) {
    return true;
  }

  return false;
}

function normalizeCacheKey(rawUrl) {
  const url = new URL(rawUrl);
  url.hash = '';

  if (/\.(?:js|json|css|png|jpg|jpeg|gif|svg|webp|ico)$/i.test(url.pathname)) {
    url.search = '';
  }

  return url.toString();
}
