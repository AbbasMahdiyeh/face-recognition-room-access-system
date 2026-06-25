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
from room_access.storage.user_manager import UserManager
from room_access.storage.statistics_manager import StatisticsManager


def main():
    """
    Run the selected application mode.
    """

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py live")
        print("  python main.py enroll <user_name>")
        print("  python main.py enroll-all")
        print("  python main.py users")
        print("  python main.py delete-user <user_name>")
        print("  python main.py stats")
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

    elif command == "users":
        manager = UserManager()

        users = manager.list_users()

        print()
        print("=" * 50)
        print("Authorized Users")
        print("=" * 50)

        for user in users:
            embedding = (
                "YES"
                if user["has_embedding"]
                else "NO"
            )

            print(f"User: {user['user_name']}")
            print(f"Images: {user['image_count']}")
            print(f"Embedding: {embedding}")
            print("-" * 50)

        print(f"Total users: {len(users)}")

    elif command == "delete-user":
        if len(sys.argv) < 3:
            print("Usage: python main.py delete-user <user_name>")
            return

        user_name = sys.argv[2]

        manager = UserManager()
        deleted = manager.delete_user(user_name)

        if deleted:
            print(f"User deleted: {user_name}")
        else:
            print(f"User not found: {user_name}")

    elif command == "stats":
        manager = StatisticsManager()
        summary = manager.get_summary()

        print()
        print("=" * 50)
        print("Access Statistics")
        print("=" * 50)
        print(f"Total Events   : {summary['total_events']}")
        print(f"Access Granted : {summary['granted']}")
        print(f"Access Denied  : {summary['denied']}")

        last_event = summary["last_event"]

        if last_event is not None:
            print("-" * 50)
            print("Last Event")
            print(f"Time   : {last_event['timestamp']}")
            print(f"User   : {last_event['user_name']}")
            print(f"Access : {last_event['access_granted']}")
            print(f"Reason : {last_event.get('reason', '')}")

        print("=" * 50)

    else:
        print("Unknown command:", command)


if __name__ == "__main__":
    main()