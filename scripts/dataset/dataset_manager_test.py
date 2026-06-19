"""
Dataset manager verification script.

This script validates that the DatasetManager can
discover authorized users from the dataset directory
structure.
"""

"""
Dataset manager verification script.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.storage.dataset_manager import DatasetManager


def main():
    """
    Create a dataset manager instance and print
    all discovered authorized users with their available image files.
    """
    manager = DatasetManager(
        "data/authorized_faces"
    )

    users = manager.list_authorized_users()

    print("Authorized users:")

    for user in users:
        print("-", user)

        image_paths = manager.list_user_images(user)

        for image_path in image_paths:
            print("  Image:", image_path)

        image_count = manager.count_user_images(user)
        print("  Total images:", image_count)

        unsupported_images = manager.list_unsupported_images(user)

    for unsupported_image in unsupported_images:
        print("  Unsupported image:", unsupported_image)


if __name__ == "__main__":
    main()