"""
Dataset management utilities.

This module is responsible for discovering and
organizing authorized face datasets used by the
access control system.
"""

from pathlib import Path


class DatasetManager:
    """
    Manage authorized user datasets.
    """

    def __init__(self, dataset_root: str):
        self.dataset_root = Path(dataset_root)

    def list_authorized_users(self):
        """
        Return all authorized user names based on
        folder names inside the dataset directory.
        """

        users = []

        for item in self.dataset_root.iterdir():
            if item.is_dir():
                users.append(item.name)

        return sorted(users)