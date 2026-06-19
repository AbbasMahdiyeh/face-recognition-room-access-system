"""
InsightFace verification script.

This script checks whether InsightFace can load its model,
detect a face in an authorized dataset image, and generate
a face embedding.

At this stage, we only test the AI model. Recognition and
access decisions will be implemented later in src/.
"""

from pathlib import Path
import sys

import cv2
from insightface.app import FaceAnalysis


project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))


def main():
    """
    Load one authorized face image and generate its embedding.
    """

    image_path = project_root / "data" / "authorized_faces" / "abbas" / "abbas_01.jpg"

    image = cv2.imread(str(image_path))

    if image is None:
        print("Failed to load image:", image_path)
        return

    print("Image loaded:", image_path)
    print("Image shape:", image.shape)

    # FaceAnalysis is InsightFace's high-level pipeline.
    # It performs face detection, face alignment, and embedding extraction.
    app = FaceAnalysis(name="buffalo_l")

    # ctx_id=-1 means CPU mode.
    # This is important because we want the project to work on a laptop
    # and later on Raspberry Pi without requiring a GPU.
    app.prepare(ctx_id=-1)

    faces = app.get(image)

    print("Detected faces:", len(faces))

    if not faces:
        print("No face detected.")
        return

    face = faces[0]

    embedding = face.embedding

    print("Embedding shape:", embedding.shape)
    print("First 5 embedding values:", embedding[:5])


if __name__ == "__main__":
    main()