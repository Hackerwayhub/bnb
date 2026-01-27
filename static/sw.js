const CACHE_NAME = 'bnb-v2.0';
const OFFLINE_URL = '/offline/';

const urlsToCache = [
  '/',
  '/static/css/bootstrap.css',
  '/static/css/style.css',
  '/static/css/bnb.css',
  '/static/css/pwa.css',
  '/static/images/logo.png',
  '/static/images/android-chrome-192x192.png',
  '/static/images/android-chrome-512x512.png',
  '/static/js/jquery-3.4.1.min.js',
  '/static/js/bootstrap.js',
  '/static/js/custom.js'
];

// Install event
self.addEventListener('install', (event) => {
  console.log('🟢 Service Worker installing');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('📦 Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event
self.addEventListener('activate', (event) => {
  console.log('🟢 Service Worker activated');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Removing old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - Cache first, then network
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  // Skip API calls
  if (event.request.url.includes('/api/') ||
      event.request.url.includes('/admin/')) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        // Return cached response if found
        if (cachedResponse) {
          return cachedResponse;
        }

        // Otherwise fetch from network
        return fetch(event.request)
          .then((response) => {
            // Don't cache if not a valid response
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response to cache it
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });

            return response;
          })
          .catch(() => {
            // If offline and requesting HTML, return offline page
            if (event.request.headers.get('accept').includes('text/html')) {
              return caches.match(OFFLINE_URL);
            }
            // Otherwise return a fallback
            return new Response('You are offline. Please check your connection.');
          });
      })
  );
});

// Push notifications
self.addEventListener('push', (event) => {
  const options = {
    body: event.data?.text() || 'New update from BNBKE',
    icon: '/static/images/android-chrome-192x192.png',
    badge: '/static/images/badge.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '1'
    },
    actions: [
      {
        action: 'explore',
        title: 'Explore',
        icon: '/static/images/icon.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/static/images/icon.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('BNBKE', options)
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'explore') {
    clients.openWindow('/');
  } else {
    clients.openWindow('/');
  }
});