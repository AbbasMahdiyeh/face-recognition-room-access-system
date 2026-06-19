"""
Dataset management utilities.

This module is responsible for discovering and organizing
authorized face datasets used by the access control system.

In this project, each authorized user is represented by one
folder inside the dataset root directory.

Example:

data/authorized_faces/
├── abbas/
│   ├── abbas_01.jpg
│   └── abbas_02.jpg
└── sadegh/
    ├── sadegh_01.jpg
    └── sadegh_02.jpg
"""

from pathlib import Path


class DatasetManager:
    """
    Manage authorized user datasets.

    The DatasetManager does not perform face recognition.
    Its only responsibility is to understand the dataset
    folder structure and provide clean access to user data
    """

    def __init__(self, dataset_root: str):
        """
        Store the root path of the authorized faces dataset.
        """

        self.dataset_root = Path(dataset_root)

    def list_authorized_users(self):
        """
        Return all authorized user names.

        Each folder inside the dataset root is treated as one
        authorized user. The returned list is sorted to make the
        result predictable across different operating systems.
        """

        users = []

        for item in self.dataset_root.iterdir():
            if item.is_dir():
                users.append(item.name)

        return sorted(users)

    def list_user_images(self, user_name: str):
        """
        Return all image files for one authorized user.

        This method will later be used by the face recognition
        pipeline to load training/reference images for each
        authorized person.
        """

        user_folder = self.dataset_root / user_name

        if not user_folder.exists():
            return []

        image_extensions = ("*.jpg", "*.jpeg", "*.png")

        image_paths = []

        for extension in image_extensions:
            image_paths.extend(user_folder.glob(extension))

        return sorted(image_paths)
    
    def count_user_images(self, user_name: str) -> int:

        """
        Count how many reference images are available for one user.

        This is useful for validating whether an authorized user has
        enough face images before entering the recognition pipeline.
        """

        return len(self.list_user_images(user_name))