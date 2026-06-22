"""
FaceEncoder verification script.

This script verifies that the project-level FaceEncoder
can generate a real ArcFace embedding from an authorized
dataset image.

The script intentionally uses FaceEncoder instead of calling
InsightFace directly. This keeps all InsightFace-specific
logic isolated inside src/room_access/recognition/face_encoder.py.
"""

import sys
from pathlib import Path

import cv2

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.recognition.face_encoder import FaceEncoder


def main():
    """
    Load one authorized face image and generate its embedding
    using the project's FaceEncoder abstraction.
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

    print("Image loaded:", image_path)
    print("Image shape:", image.shape)

    encoder = FaceEncoder()

    embedding = encoder.encode_largest_face(image)

    if embedding is None:
        print("No face embedding generated.")
        return

    print("Embedding shape:", embedding.shape)
    print("First 10 embedding values:", embedding[:10])


if __name__ == "__main__":
    main()