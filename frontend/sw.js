// ParseWiz Service Worker
const CACHE_VERSION = 'v1'
const CACHE_NAME = `parsewiz-${CACHE_VERSION}`

// Static assets to cache on install
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/styles.css',
    '/app.js',
    '/manifest.json',
    '/favicon.svg',
    '/favicon-16x16.png',
    '/favicon-32x32.png',
    '/apple-touch-icon.png',
    '/icon-192x192.png',
    '/icon-512x512.png'
]

// Install event - cache static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[SW] Caching static assets')
                return cache.addAll(STATIC_ASSETS)
            })
            .then(() => {
                // Skip waiting to activate immediately
                return self.skipWaiting()
            })
            .catch((error) => {
                console.error('[SW] Failed to cache static assets:', error)
            })
    )
})

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames
                        .filter((name) => name.startsWith('parsewiz-') && name !== CACHE_NAME)
                        .map((name) => {
                            console.log('[SW] Deleting old cache:', name)
                            return caches.delete(name)
                        })
                )
            })
            .then(() => {
                // Take control of all clients immediately
                return self.clients.claim()
            })
    )
})

// Fetch event - serve from cache or network
self.addEventListener('fetch', (event) => {
    const { request } = event
    const url = new URL(request.url)

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return
    }

    // Skip cross-origin requests (analytics, etc.)
    if (url.origin !== location.origin) {
        return
    }

    // API requests - network first, no cache
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(request)
                .catch(() => {
                    // Return offline error for API requests
                    return new Response(
                        JSON.stringify({
                            error: 'You are offline. Please check your connection and try again.'
                        }),
                        {
                            status: 503,
                            headers: { 'Content-Type': 'application/json' }
                        }
                    )
                })
        )
        return
    }

    // Static assets - cache first, then network
    event.respondWith(
        caches.match(request)
            .then((cachedResponse) => {
                if (cachedResponse) {
                    // Return cached version and update cache in background
                    event.waitUntil(
                        fetch(request)
                            .then((networkResponse) => {
                                if (networkResponse && networkResponse.status === 200) {
                                    caches.open(CACHE_NAME)
                                        .then((cache) => cache.put(request, networkResponse))
                                }
                            })
                            .catch(() => {
                                // Network failed, but we have cache - that's fine
                            })
                    )
                    return cachedResponse
                }

                // Not in cache - fetch from network
                return fetch(request)
                    .then((networkResponse) => {
                        // Cache successful responses
                        if (networkResponse && networkResponse.status === 200) {
                            const responseClone = networkResponse.clone()
                            caches.open(CACHE_NAME)
                                .then((cache) => cache.put(request, responseClone))
                        }
                        return networkResponse
                    })
                    .catch(() => {
                        // Network failed and not in cache
                        // For navigation requests, return the cached index.html
                        if (request.mode === 'navigate') {
                            return caches.match('/index.html')
                        }
                        return new Response('Offline', { status: 503 })
                    })
            })
    )
})

// Handle messages from the main thread
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting()
    }
})