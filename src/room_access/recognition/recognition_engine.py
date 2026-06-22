"""
Recognition engine module.

This module coordinates the full recognition workflow:

1. Generate an embedding from an input image.
2. Compare it with all stored authorized embeddings.
3. Return the best matching identity and access decision.

The RecognitionEngine does not know how images are captured.
It only receives an image frame and decides whether it matches
a known authorized user.
"""

from dataclasses import dataclass

import numpy as np

from room_access.recognition.face_encoder import FaceEncoder
from room_access.recognition.face_matcher import FaceMatcher
from room_access.storage.embedding_storage import EmbeddingStorage


@dataclass
class RecognitionResult:
    """
    Store the result of a face recognition attempt.
    """

    user_name: str | None
    similarity: float
    access_granted: bool
    bbox: tuple[int, int, int, int] | None


class RecognitionEngine:
    """
    Coordinate face encoding, matching, and access decision logic.
    """

    def __init__(
        self,
        embeddings_root: str,
        threshold: float = 0.5,
    ):
        """
        Initialize the components required for recognition.

        Parameters
        ----------
        embeddings_root
            Directory containing stored authorized user embeddings.

        threshold
            Minimum cosine similarity required to grant access.
        """

        self.encoder = FaceEncoder()
        self.matcher = FaceMatcher(threshold=threshold)
        self.storage = EmbeddingStorage(embeddings_root)

    def recognize(
        self,
        image: np.ndarray,
    ) -> RecognitionResult:
        """
        Recognize the largest detected face in an input image.

        The method compares the query embedding against all stored
        authorized embeddings and selects the user with the highest
        similarity score.
        """

        encoding_result = self.encoder.encode_largest_face_with_bbox(image)

        if encoding_result is None:
            return RecognitionResult(
                user_name=None,
                similarity=0.0,
                access_granted=False,
                bbox= None,
            )
        
        # Extract the embedding from the encoding result.
        # The bounding box will be used later for visualization.
        query_embedding = encoding_result.embedding

        best_user = None
        best_similarity = -1.0

        for embedding_path in self.storage.list_embeddings():
            user_name = embedding_path.stem

            stored_embedding = self.storage.load_embedding(user_name)

            if stored_embedding is None:
                continue

            similarity = self.matcher.cosine_similarity(
                query_embedding,
                stored_embedding,
            )

            # Keep only the closest authorized identity.
            # The final access decision should be based on the
            # strongest match rather than the first available match.
            if similarity > best_similarity:
                best_similarity = similarity
                best_user = user_name

        if best_user is None:
            return RecognitionResult(
                user_name=None,
                similarity=0.0,
                access_granted=False,
                bbox=encoding_result.bbox,
            )

        access_granted = best_similarity >= self.matcher.threshold

        return RecognitionResult(
            user_name=best_user,
            similarity=best_similarity,
            access_granted=access_granted,
            bbox=encoding_result.bbox,
        )