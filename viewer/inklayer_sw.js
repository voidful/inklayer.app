'use strict';

const CACHE_VERSION = 'inklayer-pwa-v2';
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
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => cache.addAll(APP_SHELL)),
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
                key.startsWith('inklayer-pwa-') && key !== CACHE_VERSION,
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
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_VERSION);
      await cache.put(request, response.clone());
    }
    return response;
  } catch (_) {
    return (
      (await caches.match(request)) ||
      (await caches.match('./index.html')) ||
      (await caches.match('./offline.html'))
    );
  }
}

async function cacheFirstAsset(request) {
  const cached = await caches.match(request);
  if (cached) {
    return cached;
  }

  const response = await fetch(request);
  if (response.ok && shouldCache(request)) {
    const cache = await caches.open(CACHE_VERSION);
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
