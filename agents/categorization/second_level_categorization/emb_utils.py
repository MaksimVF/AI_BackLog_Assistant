




"""
Embedding Utilities for Categorization
"""

import numpy as np
import random

# Mock embedding function for testing
def get_embedding(text: str) -> np.ndarray:
    """
    Generates a mock embedding for the given text.

    Args:
        text: Input text to embed

    Returns:
        Numpy array representing the embedding
    """
    # Create a random embedding vector for demonstration
    # In production, this would use a real embedding model
    random.seed(hash(text) % 4294967296)  # Seed based on text hash
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
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))




