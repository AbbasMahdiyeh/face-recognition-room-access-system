"""
Dataset image loading verification script.

This script verifies that authorized user image paths
can be loaded into memory using OpenCV.

At this stage, we are not performing face recognition yet.
The goal is only to confirm that dataset images can be
discovered and loaded correctly.
"""

import sys
from pathlib import Path

import cv2

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.storage.dataset_manager import DatasetManager


def main():
    """
    Load all authorized user images and print their properties.
    """

    manager = DatasetManager("data/authorized_faces")

    users = manager.list_authorized_users()

    for user in users:
        print("User:", user)

        image_paths = manager.list_user_images(user)

        for image_path in image_paths:
            image = cv2.imread(str(image_path))

            if image is None:
                print("  Failed to load:", image_path)
                continue

            print("  Loaded:", image_path)
            print("  Shape:", image.shape)
            print("  Dtype:", image.dtype)

            # Convert the loaded image to grayscale before detection.
            # Haar Cascade detectors analyze intensity patterns, so color
            # information is not required at this stage.
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Build the path to OpenCV's built-in Haar Cascade model.
            # We avoid cv2.data.haarcascades here because some editors
            # cannot statically detect that dynamic OpenCV attribute.
            cascade_path = (
                Path(cv2.__file__).parent
                / "data"
                / "haarcascade_frontalface_default.xml"
            )

            face_detector = cv2.CascadeClassifier(str(cascade_path))

            # Run face detection on the authorized user's reference image.
            # This verifies that each dataset image actually contains a
            # detectable face before it enters the recognition pipeline.
            faces = face_detector.detectMultiScale(
                gray_image,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
            )

            print("  Detected faces:", len(faces))


if __name__ == "__main__":
    main()