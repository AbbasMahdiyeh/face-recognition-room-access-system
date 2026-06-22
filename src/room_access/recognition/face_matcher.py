"""
Face matching module.

This module compares face embeddings and decides whether
two embeddings are similar enough to belong to the same person.

FaceMatcher does not generate embeddings.
It only compares embeddings that were already produced by FaceEncoder.
"""

import numpy as np


class FaceMatcher:
    """
    Compare face embeddings using cosine similarity.
    """

    def __init__(self, threshold: float = 0.5):
        """
        Store the similarity threshold used for matching.

        Threshold defines the minimum cosine similarity required
        for two embeddings to be considered the same person.

        If cosine similarity is greater than or equal to this
        threshold, two embeddings are considered a match.

        Examples
        --------
        Similarity = 0.95
        Threshold = 0.80
        Result = Match (True)

        Similarity = 0.62
        Threshold = 0.80
        Result = No Match (False)

        Higher thresholds make the system more strict,
        while lower thresholds make it more tolerant.
        """

        self.threshold = threshold

    def cosine_similarity(
        self,
        embedding_a: np.ndarray,
        embedding_b: np.ndarray,
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.

        Cosine similarity measures the angle between two vectors.
        For face embeddings, higher similarity usually means the
        two faces are more likely to belong to the same person.
        """

        numerator = np.dot(
            embedding_a,
            embedding_b,
        )

        denominator = (
            np.linalg.norm(embedding_a) *
            np.linalg.norm(embedding_b)
        )

        if denominator == 0:
            return 0.0

        return float(numerator / denominator)
    
    def is_match(
        self,
        embedding_a: np.ndarray,
        embedding_b: np.ndarray,
    ) -> bool:
        """
        Decide whether two embeddings belong to the same person.
        """

        similarity = self.cosine_similarity(
            embedding_a,
            embedding_b,
        )

        return similarity >= self.threshold