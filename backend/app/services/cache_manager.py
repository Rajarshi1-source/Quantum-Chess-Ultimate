"""
Quantum Chess Ultimate - Cache Manager

In-memory caching for position evaluations and quantum measurements.
Provides a Redis-compatible interface for future migration.
"""

import time
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class CacheManager:
    """
    In-memory cache with TTL support.
    Drop-in replaceable with Redis when needed.
    """

    def __init__(self, default_ttl: int = 300):
        self._cache: dict[str, dict] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache. Returns None if expired or missing."""
        entry = self._cache.get(key)
        if entry is None:
            self.misses += 1
            return None

        if time.time() > entry["expires_at"]:
            del self._cache[key]
            self.misses += 1
            return None

        self.hits += 1
        return entry["value"]

    async def set(self, key: str, value: Any, ttl: int | None = None):
        """Set value in cache with TTL."""
        expires_at = time.time() + (ttl or self.default_ttl)
        self._cache[key] = {"value": value, "expires_at": expires_at}

    async def delete(self, key: str):
        """Delete a cache entry."""
        self._cache.pop(key, None)

    async def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
        self.hits = 0
        self.misses = 0

    async def cleanup(self):
        """Remove expired entries."""
        now = time.time()
        expired = [k for k, v in self._cache.items() if now > v["expires_at"]]
        for key in expired:
            del self._cache[key]

    def stats(self) -> dict:
        """Return cache statistics."""
        total = self.hits + self.misses
        return {
            "entries": len(self._cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hits / total, 2) if total > 0 else 0.0,
        }
