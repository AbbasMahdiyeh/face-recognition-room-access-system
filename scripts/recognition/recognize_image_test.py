"""
RecognitionEngine verification script.

This script verifies the complete recognition pipeline by
passing one image into RecognitionEngine.

RecognitionEngine internally coordinates:

- FaceEncoder
- FaceMatcher
- EmbeddingStorage

The test script is intentionally lightweight because
all recognition logic belongs inside RecognitionEngine.
"""

import sys
from pathlib import Path

import cv2

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.recognition.recognition_engine import RecognitionEngine


def main():
    """
    Verify the complete face recognition pipeline.
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
        print("Failed to load image.")
        return

    engine = RecognitionEngine(
        embeddings_root="data/embeddings",
        threshold=0.5,
    )

    result = engine.recognize(image)

    print("User:", result.user_name)
    print("Similarity:", result.similarity)
    print("Access:", result.access_granted)


if __name__ == "__main__":
    main()