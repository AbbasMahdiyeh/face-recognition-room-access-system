"""
Dataset manager verification script.

This script validates that the DatasetManager can
discover authorized users from the dataset directory
structure.
"""

from room_access.storage.dataset_manager import DatasetManager


def main():
    """
    Create a dataset manager instance and print
    all discovered authorized users.
    """
    manager = DatasetManager(
        "data/authorized_faces"
    )

    users = manager.list_authorized_users()

    print("Authorized users:")

    for user in users:
        print("-", user)


if __name__ == "__main__":
    main()