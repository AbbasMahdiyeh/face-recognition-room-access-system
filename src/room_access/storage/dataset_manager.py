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

SUPPORTED_IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
)

UNSUPPORTED_IMAGE_EXTENSIONS = (
    ".heic",
    ".heif",
)

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

    def list_user_images(self, user_name: str) -> list[Path]:
        """
        Return all supported image files for one authorized user.

        The current dataset policy supports JPG, JPEG, and PNG files.
        HEIC/HEIF files are intentionally not loaded at this stage because
        standard OpenCV installations may not read them reliably.

        If HEIC support becomes necessary later, we will add a dedicated
        conversion step instead of silently mixing unsupported files into
        the recognition pipeline.
        """

        user_folder = self.dataset_root / user_name

        if not user_folder.exists():
            return []

        image_paths = []

        for item in user_folder.iterdir():
            if item.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
                image_paths.append(item)

        return sorted(image_paths)
    
    def count_user_images(self, user_name: str) -> int:

        """
        Count how many reference images are available for one user.

        This is useful for validating whether an authorized user has
        enough face images before entering the recognition pipeline.
        """

        return len(self.list_user_images(user_name))
    
    def list_unsupported_images(self, user_name: str) -> list[Path]:
        """
        Return unsupported image files found for one authorized user.

        This helps detect dataset problems early. For example, many modern
        phones save photos as HEIC/HEIF, but our current OpenCV-based
        pipeline expects JPG, JPEG, or PNG files.
        """

        user_folder = self.dataset_root / user_name

        if not user_folder.exists():
            return []

        unsupported_paths = []

        for item in user_folder.iterdir():
            if item.suffix.lower() in UNSUPPORTED_IMAGE_EXTENSIONS:
                unsupported_paths.append(item)

        return sorted(unsupported_paths)