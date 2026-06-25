"""
User manager.

Purpose
-------
Provide a centralized interface for managing all authorized users.

Why this exists
---------------
As the project grows, user-related operations such as listing,
deleting, updating and validating users should not be scattered
across the application.

This class becomes the single source of truth for all authorized
user data stored on disk.

Architecture
------------
Application
      ↓
UserManager
      ↓
Authorized Faces
      ↓
Embeddings

Future extensions
-----------------
- Delete users
- Rename users
- Update user images
- Rebuild embeddings
- Export user information
"""

from pathlib import Path


class UserManager:
    """
    Manage authorized user information stored on disk.
    """

    def __init__(
        self,
        dataset_root: str = "data/authorized_faces",
        embeddings_root: str = "data/embeddings",
    ):
        self.dataset_root = Path(dataset_root)
        self.embeddings_root = Path(embeddings_root)

    def list_users(self) -> list[dict]:
        """
        Return basic information for all authorized users.
        """

        users = []

        if not self.dataset_root.exists():
            return users

        for user_dir in sorted(self.dataset_root.iterdir()):
            if not user_dir.is_dir():
                continue

            user_name = user_dir.name

            image_count = len(
                list(user_dir.glob("*.jpg"))
                + list(user_dir.glob("*.jpeg"))
                + list(user_dir.glob("*.png"))
            )

            embedding_path = self.embeddings_root / f"{user_name}.npy"

            users.append(
                {
                    "user_name": user_name,
                    "image_count": image_count,
                    "has_embedding": embedding_path.exists(),
                }
            )

        return users