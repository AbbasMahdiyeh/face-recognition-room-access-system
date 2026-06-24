"""
Enrollment management module.

This module handles the process of enrolling authorized users.

Enrollment means converting one or more reference face images
into a stored embedding that can later be used for recognition.
"""

import cv2
import numpy as np

from room_access.recognition.face_encoder import FaceEncoder
from room_access.storage.dataset_manager import DatasetManager
from room_access.storage.embedding_storage import EmbeddingStorage


class EnrollmentManager:
    """
    Create and update authorized user embeddings from reference images.
    """

    def __init__(
        self,
        dataset_root: str = "data/authorized_faces",
        embeddings_root: str = "data/embeddings",
    ):
        """
        Initialize enrollment dependencies.

        DatasetManager is responsible for finding authorized user images.
        FaceEncoder converts each valid face image into an embedding.
        EmbeddingStorage stores the final user embedding on disk.
        """

        self.dataset_manager = DatasetManager(dataset_root)
        self.encoder = FaceEncoder()
        self.storage = EmbeddingStorage(embeddings_root)

    def enroll_user(
        self,
        user_name: str,
    ) -> str | None:
        """
        Generate and store an embedding for one authorized user.

        Multiple reference images are averaged into one embedding.
        This makes recognition more stable against lighting, pose,
        and facial expression differences.
        """

        image_paths = self.dataset_manager.list_user_images(user_name)

        if not image_paths:
            print(f"No images found for user: {user_name}")
            return None

        embeddings = []

        for image_path in image_paths:
            image = cv2.imread(str(image_path))

            if image is None:
                print(f"Failed to load image: {image_path}")
                continue

            embedding = self.encoder.encode_largest_face(image)

            if embedding is None:
                print(f"No face detected in image: {image_path}")
                continue

            embeddings.append(embedding)

        if not embeddings:
            print(f"No valid face embeddings generated for user: {user_name}")
            return None

        user_embedding = np.mean(
            embeddings,
            axis=0,
        )

        saved_path = self.storage.save_embedding(
            user_name,
            user_embedding,
        )

        return str(saved_path)

    def enroll_all_users(self) -> list[str]:
        """
        Enroll all users found in the authorized faces dataset.
        """

        saved_paths = []

        users = self.dataset_manager.list_authorized_users()

        for user_name in users:
            saved_path = self.enroll_user(user_name)

            if saved_path is not None:
                saved_paths.append(saved_path)

        return saved_paths