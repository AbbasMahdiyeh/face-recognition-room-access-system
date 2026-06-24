"""
EnrollmentManager verification script.

This script verifies that EnrollmentManager can generate
and store embeddings for users in the authorized dataset.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.recognition.enrollment_manager import EnrollmentManager


def main():
    """
    Enroll all authorized users.
    """

    manager = EnrollmentManager(
        dataset_root="data/authorized_faces",
        embeddings_root="data/embeddings",
    )

    saved_paths = manager.enroll_all_users()

    print("Enrollment completed.")
    print("Saved embeddings:")

    for path in saved_paths:
        print("-", path)


if __name__ == "__main__":
    main()