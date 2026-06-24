"""
Main command-line entry point for the face recognition access system.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.app.enrollment_app import EnrollmentApp
from room_access.app.live_access_app import LiveAccessApp
from room_access.recognition.enrollment_manager import EnrollmentManager


def main():
    """
    Run the selected application mode.
    """

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py live")
        print("  python main.py enroll <user_name>")
        print("  python main.py enroll-all")
        return

    command = sys.argv[1]

    if command == "live":
        app = LiveAccessApp()
        app.run()

    elif command == "enroll":
        if len(sys.argv) < 3:
            print("Usage: python main.py enroll <user_name>")
            return

        user_name = sys.argv[2]

        app = EnrollmentApp(
            capture_count=5,
        )

        app.run(user_name)

    elif command == "enroll-all":
        manager = EnrollmentManager()
        saved_paths = manager.enroll_all_users()

        print("Enrollment completed.")
        print("Saved embeddings:")

        for path in saved_paths:
            print("-", path)

    else:
        print("Unknown command:", command)


if __name__ == "__main__":
    main()