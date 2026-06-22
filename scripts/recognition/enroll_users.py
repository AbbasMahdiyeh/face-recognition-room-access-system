"""
Authorized user enrollment script.

This script reads all authorized users from the dataset,
generates face embeddings for their reference images, and
stores one embedding file per user.

At this stage, the script rebuilds embeddings for all users.
Later, we can optimize it to update only new or changed users.
"""

import sys
from pathlib import Path

import cv2
import numpy as np

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.recognition.face_encoder import FaceEncoder
from room_access.storage.dataset_manager import DatasetManager
from room_access.storage.embedding_storage import EmbeddingStorage


def main():
    """
    Enroll all authorized users by generating and storing embeddings.
    """

    dataset_manager = DatasetManager("data/authorized_faces")
    encoder = FaceEncoder()
    storage = EmbeddingStorage("data/embeddings")

    users = dataset_manager.list_authorized_users()

    for user in users:
        print("Enrolling user:", user)

        image_paths = dataset_manager.list_user_images(user)

        if not image_paths:
            print("  No supported images found.")
            continue

        embeddings = []

        for image_path in image_paths:
            image = cv2.imread(str(image_path))

            if image is None:
                print("  Failed to load:", image_path)
                continue

            embedding = encoder.encode_largest_face(image)

            if embedding is None:
                print("  No face detected in:", image_path)
                continue

            embeddings.append(embedding)

            print("  Encoded:", image_path)

        if not embeddings:
            print("  No valid embeddings generated.")
            continue

        # Average all embeddings for one user.
        # This creates a more stable representation when multiple
        # reference images are available for the same person.
        user_embedding = np.mean(
            embeddings,
            axis=0,
        )

        saved_path = storage.save_embedding(
            user,
            user_embedding,
        )

        print("  Saved embedding:", saved_path)


if __name__ == "__main__":
    main()