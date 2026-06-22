"""
Recognition overlay verification script.

This script runs RecognitionEngine on one image, draws
the recognition overlay, and saves the annotated result.
"""

import sys
from pathlib import Path

import cv2

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.dashboard.display_overlay import draw_recognition_overlay
from room_access.recognition.recognition_engine import RecognitionEngine


def main():
    """
    Generate an annotated recognition image.
    """

    image_path = (
        project_root
        / "data"
        / "authorized_faces"
        / "abbas"
        / "abbas_01.jpg"
    )

    output_path = (
        project_root
        / "data"
        / "sample_images"
        / "recognition_overlay_test.jpg"
    )

    image = cv2.imread(str(image_path))

    if image is None:
        print("Failed to load image:", image_path)
        return

    engine = RecognitionEngine(
        embeddings_root="data/embeddings",
        threshold=0.5,
    )

    result = engine.recognize(image)

    annotated_image = draw_recognition_overlay(
        image,
        result,
    )

    cv2.imwrite(
        str(output_path),
        annotated_image,
    )

    print("Saved overlay image to:", output_path)


if __name__ == "__main__":
    main()