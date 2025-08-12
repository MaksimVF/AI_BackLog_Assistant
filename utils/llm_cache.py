


"""
LLM Response Caching System
"""

import time
import hashlib
import json
from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple
from collections import OrderedDict

class LRUCache:
    """Least Recently Used Cache implementation"""

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: OrderedDict[str, Tuple[float, Any]] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        """Get item from cache if it exists"""
        if key in self.cache:
            # Move to end to mark as recently used
            value = self.cache.pop(key)
            self.cache[key] = value
            return value[1]
        return None

    def set(self, key: str, value: Any) -> None:
        """Set item in cache, evicting least recently used if needed"""
        if key in self.cache:
            # Update existing item
            self.cache.move_to_end(key)
        else:
            # Add new item
            self.cache[key] = (time.time(), value)

        # Evict oldest items if over capacity
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def clear(self) -> None:
        """Clear the cache"""
        self.cache.clear()

class LLMResponseCache:
    """Cache for LLM responses"""

    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """
        Initialize LLM response cache

        Args:
            max_size: Maximum number of items to cache
            ttl: Time to live for cache items in seconds
        """
        self.cache = LRUCache(max_size)
        self.ttl = ttl

    def _generate_key(self, messages: list, model_name: str, **kwargs) -> str:
        """Generate a unique cache key from request parameters"""
        # Convert messages to a stable hashable format
        messages_str = json.dumps(messages, sort_keys=True)
        kwargs_str = json.dumps(kwargs, sort_keys=True)
        combined = f"{model_name}:{messages_str}:{kwargs_str}"

        # Generate SHA256 hash
        return hashlib.sha256(combined.encode()).hexdigest()

    def get_cached_response(self, messages: list, model_name: str, **kwargs) -> Optional[str]:
        """Get cached response if available and not expired"""
        key = self._generate_key(messages, model_name, **kwargs)
        cached = self.cache.get(key)

        if cached:
            timestamp, response = cached
            if time.time() - timestamp < self.ttl:
                return response

        return None

    def cache_response(self, messages: list, model_name: str, response: str, **kwargs) -> None:
        """Cache an LLM response"""
        key = self._generate_key(messages, model_name, **kwargs)
        self.cache.set(key, (time.time(), response))

    def clear(self) -> None:
        """Clear the cache"""
        self.cache.clear()

def llm_cache_decorator(ttl: int = 3600, max_size: int = 1000):
    """
    Decorator for caching LLM function calls

    Args:
        ttl: Time to live for cache items in seconds
        max_size: Maximum number of items to cache
    """
    cache = LLMResponseCache(max_size=max_size, ttl=ttl)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract relevant parameters for caching
            messages = kwargs.get('messages', [])
            model_name = kwargs.get('model_name', 'default')

            # Check cache first
            cached_response = cache.get_cached_response(messages, model_name, **kwargs)
            if cached_response is not None:
                return cached_response

            # Call the actual function
            response = func(*args, **kwargs)

            # Cache the response
            cache.cache_response(messages, model_name, response, **kwargs)

            return response

        return wrapper

    return decorator

# Global cache instance
global_llm_cache = LLMResponseCache(max_size=1000, ttl=3600)


