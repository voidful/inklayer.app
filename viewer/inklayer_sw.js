'use strict';

// Each build stamps its own BUILD (tool/build_web_app.sh,
// tool/build_web_viewer.sh), so a release replaces the cached code instead
// of serving the last one. Caches are named for this worker's scope (/app/,
// /viewer/), so the app and the viewer on one site keep theirs apart.
const BUILD = '20261113071519';
const SCOPE = new URL(self.registration.scope).pathname;
const CACHE_PREFIX = `inklayer-pwa-${SCOPE}`;
const CACHE_VERSION = `${CACHE_PREFIX}${BUILD}`;
const APP_SHELL = [
  './',
  './index.html',
  './manifest.json',
  './offline.html',
  './privacy.html',
  './privacy/',
  './privacy/index.html',
  './privacy.zh-TW.html',
  './support.html',
  './support/',
  './support/index.html',
  './support.zh-TW.html',
  './favicon.png',
  './icons/Icon-192.png',
  './icons/Icon-512.png',
  './icons/Icon-maskable-192.png',
  './icons/Icon-maskable-512.png',
];

self.addEventListener('install', (event) => {
  // Pages a build leaves out (the app and the viewer link to the site's own
  // legal pages) are skipped rather than failing the install.
  event.waitUntil(
    caches
      .open(CACHE_VERSION)
      .then((cache) =>
        Promise.all(APP_SHELL.map((url) => cache.add(url).catch(() => {}))),
      ),
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter(
              (key) =>
                (key.startsWith(CACHE_PREFIX) && key !== CACHE_VERSION) ||
                // Caches from before they were named for their scope.
                /^inklayer-pwa-v\d+$/.test(key),
            )
            .map((key) => caches.delete(key)),
        ),
      )
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') {
    return;
  }

  if (request.mode === 'navigate') {
    event.respondWith(networkFirstPage(request));
    return;
  }

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) {
    return;
  }

  event.respondWith(cacheFirstAsset(request));
});

async function networkFirstPage(request) {
  const cache = await caches.open(CACHE_VERSION);
  try {
    const response = await fetch(request);
    if (response.ok) {
      await cache.put(request, response.clone());
    }
    return response;
  } catch (_) {
    return (
      (await cache.match(request)) ||
      (await cache.match('./index.html')) ||
      (await cache.match('./offline.html'))
    );
  }
}

async function cacheFirstAsset(request) {
  const cache = await caches.open(CACHE_VERSION);
  const cached = await cache.match(request);
  if (cached) {
    return cached;
  }

  const response = await fetch(request);
  if (response.ok && shouldCache(request)) {
    await cache.put(request, response.clone());
  }
  return response;
}

function shouldCache(request) {
  const url = new URL(request.url);
  return (
    ['font', 'image', 'script', 'style'].includes(request.destination) ||
    url.pathname.endsWith('.json') ||
    url.pathname.endsWith('.wasm')
  );
}
