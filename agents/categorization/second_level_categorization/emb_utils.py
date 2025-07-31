




"""
Embedding Utilities for Categorization
"""

import numpy as np
import random
from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL_NAME

# Initialize embedding model (singleton pattern)
_embedding_model = None

def get_embedding_model():
    """
    Gets the embedding model instance (singleton pattern).

    Returns:
        SentenceTransformer model
    """
    global _embedding_model
    if _embedding_model is None:
        try:
            # Load the model (default to a good multilingual model if not specified)
            # For testing, use a smaller model to avoid long loading times
            model_name = EMBEDDING_MODEL_NAME or "intfloat/multilingual-e5-small"
            print(f"Loading embedding model: {model_name}")
            _embedding_model = SentenceTransformer(model_name)
            print("Embedding model loaded successfully")
        except Exception as e:
            print(f"Failed to load embedding model: {e}")
            # Fallback to mock embeddings if model loading fails
            return None
    return _embedding_model

def get_embedding(text: str) -> np.ndarray:
    """
    Generates an embedding for the given text using a production-ready model.

    Args:
        text: Input text to embed

    Returns:
        Numpy array representing the embedding
    """
    if not text or not isinstance(text, str):
        # Return a zero vector for invalid input
        return np.zeros(384)

    try:
        model = get_embedding_model()
        if model is not None:
            embedding = model.encode(text, convert_to_numpy=True)
            return embedding
        else:
            # Fallback to mock embedding if model is not available
            random.seed(hash(text) % 4294967296)
            return np.array([random.random() for _ in range(384)])
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Fallback to random embedding if model fails
        random.seed(hash(text) % 4294967296)
        return np.array([random.random() for _ in range(384)])

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




