"""
UserManager verification script.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.storage.user_manager import UserManager


def main():
    manager = UserManager()
    users = manager.list_users()

    print("Authorized Users")
    print("=" * 40)

    for user in users:
        embedding_status = "YES" if user["has_embedding"] else "NO"

        print(f"User: {user['user_name']}")
        print(f"Images: {user['image_count']}")
        print(f"Embedding: {embedding_status}")
        print("-" * 40)

    print("Total users:", len(users))


if __name__ == "__main__":
    main()