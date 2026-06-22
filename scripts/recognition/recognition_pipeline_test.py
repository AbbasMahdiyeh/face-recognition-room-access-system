"""
Recognition pipeline verification script.

This script connects three core components:

- FaceEncoder: generates a 512-dimensional face embedding
- EmbeddingStorage: saves and loads embeddings from disk
- FaceMatcher: compares embeddings using cosine similarity

This script verifies the interaction between the
individual recognition components before introducing
RecognitionEngine.

Unlike recognize_image_test.py, this test directly
connects FaceEncoder, EmbeddingStorage, and FaceMatcher
to validate their integration.

The goal is to verify that a real face image can be encoded,
stored, loaded, and matched against itself.
"""

import sys
from pathlib import Path

import cv2

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.recognition.face_encoder import FaceEncoder
from room_access.recognition.face_matcher import FaceMatcher
from room_access.storage.embedding_storage import EmbeddingStorage


def main():
    """
    Run a minimal end-to-end recognition pipeline test.
    """

    image_path = (
        project_root
        / "data"
        / "authorized_faces"
        / "abbas"
        / "abbas_01.jpg"
    )

    image = cv2.imread(str(image_path))

    if image is None:
        print("Failed to load image:", image_path)
        return

    encoder = FaceEncoder()
    storage = EmbeddingStorage("data/embeddings")
    matcher = FaceMatcher(threshold=0.5)

    embedding = encoder.encode_largest_face(image)

    if embedding is None:
        print("No face embedding generated.")
        return

    saved_path = storage.save_embedding(
        "abbas",
        embedding,
    )

    print("Embedding saved to:", saved_path)

    stored_embedding = storage.load_embedding("abbas")

    if stored_embedding is None:
        print("Failed to load stored embedding.")
        return

    similarity = matcher.cosine_similarity(
        embedding,
        stored_embedding,
    )

    is_match = matcher.is_match(
        embedding,
        stored_embedding,
    )

    print("Similarity:", similarity)
    print("Is match:", is_match)


if __name__ == "__main__":
    main()