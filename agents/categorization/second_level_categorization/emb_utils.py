"""
Embedding Utilities for Categorization
"""

import numpy as np
import random
import time
from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL_NAME
import threading

# Cache management
_cache_lock = threading.Lock()
_cache_max_size = 1000  # Maximum number of embeddings to cache

# Initialize embedding model (singleton pattern)
_embedding_model = None
_model_load_time = 0
_model_cache = {}  # Simple cache for embeddings

def get_embedding_model():
    """
    Gets the embedding model instance (singleton pattern) with caching.

    Returns:
        SentenceTransformer model
    """
    global _embedding_model, _model_load_time
    if _embedding_model is None:
        try:
            # Load the model (default to a good multilingual model if not specified)
            # For testing, use a smaller model to avoid long loading times
            model_name = EMBEDDING_MODEL_NAME or "intfloat/multilingual-e5-small"
            print(f"Loading embedding model: {model_name}")

            start_time = time.time()
            _embedding_model = SentenceTransformer(model_name)
            _model_load_time = time.time() - start_time

            print(f"Embedding model loaded successfully in {_model_load_time:.2f} seconds")
        except Exception as e:
            print(f"Failed to load embedding model: {e}")
            # Fallback to mock embeddings if model loading fails
            return None
    return _embedding_model

def manage_cache_size():
    """
    Manage the cache size to prevent memory issues.
    """
    global _model_cache
    with _cache_lock:
        if len(_model_cache) > _cache_max_size:
            # Remove random entries to make space
            keys_to_remove = list(_model_cache.keys())[:len(_model_cache) - _cache_max_size + 100]
            for key in keys_to_remove:
                del _model_cache[key]

def clear_embedding_cache():
    """
    Clear the embedding cache.
    """
    global _model_cache
    with _cache_lock:
        _model_cache.clear()

def get_embedding(text: str) -> np.ndarray:
    """
    Generates an embedding for the given text using a production-ready model with caching.

    Args:
        text: Input text to embed

    Returns:
        Numpy array representing the embedding
    """
    if not text or not isinstance(text, str):
        # Return a zero vector for invalid input
        return np.zeros(384)

    # Check cache first (thread-safe)
    global _model_cache
    with _cache_lock:
        if text in _model_cache:
            return _model_cache[text]

    try:
        model = get_embedding_model()
        if model is not None:
            embedding = model.encode(text, convert_to_numpy=True)
            # Cache the embedding (thread-safe)
            with _cache_lock:
                _model_cache[text] = embedding
                manage_cache_size()
            return embedding
        else:
            # Fallback to mock embedding if model is not available
            random.seed(hash(text) % 4294967296)
            mock_embedding = np.array([random.random() for _ in range(384)])
            with _cache_lock:
                _model_cache[text] = mock_embedding
                manage_cache_size()
            return mock_embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Fallback to random embedding if model fails
        random.seed(hash(text) % 4294967296)
        fallback_embedding = np.array([random.random() for _ in range(384)])
        with _cache_lock:
            _model_cache[text] = fallback_embedding
            manage_cache_size()
        return fallback_embedding

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Computes cosine similarity between two vectors.

    Args:
        a: First vector
        b: Second vector

    Returns:
        Cosine similarity score (0-1)
    """
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
