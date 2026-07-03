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
from room_access.app.health_check import HealthCheck
from room_access.app.web_dashboard_app import WebDashboardApp

from room_access.app.version import (
    AI_ENGINE,
    COMPUTER_VISION,
    DEVELOPER,
    GITHUB,
    LANGUAGE,
    LICENSE,
    PLATFORM,
    PROGRAM,
    PROJECT_NAME,
    SPECIALIZATION,
    STATUS,
    UNIVERSITY,
    VERSION,
)


def print_usage():
    """
    Print the command-line usage guide.
    """

    print()
    print("=" * 70)
    print("Face Recognition Room Access System")
    print("Command Line Interface")
    print("=" * 70)
    print()
    print("Usage:")
    print("    python main.py <command>")
    print()
    print("Commands:")
    print("    live            Start desktop live access system")
    print("    web             Start browser-based live dashboard")
    print("    enroll          Register a new authorized user")
    print("    enroll-all      Rebuild embeddings for all users")
    print("    users           List all authorized users")
    print("    delete-user     Delete an authorized user")
    print("    stats           Display access statistics")
    print("    version         Display project information")
    print("    check           Run system health check")
    print()
    print("Examples:")
    print("    python main.py live")
    print("    python main.py web")
    print("    python main.py enroll abbas")
    print("    python main.py users")
    print("    python main.py stats")
    print("    python main.py version")
    print("    python main.py check")
    print()
    print("=" * 70)

def main():
    """
    Run the selected application mode.
    """

    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "live":
        app = LiveAccessApp()
        app.run()

    elif command == "web":
        app = WebDashboardApp()
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

    elif command == "version":
        print()
        print("=" * 70)
        print(PROJECT_NAME.center(70))
        print("=" * 70)

        print(f"{'Version':18}: {VERSION}")
        print(f"{'Status':18}: {STATUS}")

        print("-" * 70)

        print(f"{'Developer':18}: {DEVELOPER}")
        print(f"{'University':18}: {UNIVERSITY}")
        print(f"{'Program':18}: {PROGRAM}")
        print(f"{'Specialization':18}: {SPECIALIZATION}")

        print("-" * 70)

        print(f"{'AI Engine':18}: {AI_ENGINE}")
        print(f"{'Computer Vision':18}: {COMPUTER_VISION}")
        print(f"{'Language':18}: {LANGUAGE}")
        print(f"{'Platform':18}: {PLATFORM}")

        print("-" * 70)

        print(f"{'License':18}: {LICENSE}")
        print(f"{'GitHub':18}: {GITHUB}")

        print("=" * 70)
        print()

        print("Available Commands")
        print("-" * 70)

        print("  live            Start desktop live access system")
        print("  web             Start browser-based live dashboard")
        print("  enroll          Register a new authorized user")
        print("  enroll-all      Rebuild embeddings for all users")
        print("  users           List all authorized users")
        print("  delete-user     Remove an authorized user")
        print("  stats           Show access statistics")
        print("  version         Show project information")

        print("=" * 70)

    elif command == "check":
        checker = HealthCheck()
        results = checker.run()

        print()
        print("=" * 70)
        print("System Health Check")
        print("=" * 70)

        all_ok = True

        for key, value in results.items():
            if isinstance(value, bool):
                status = "OK" if value else "MISSING"

                if not value and key != "is_raspberry_pi":
                    all_ok = False

                print(f"{key:30}: {status}")
            else:
                print(f"{key:30}: {value}")

        print("-" * 70)

        if all_ok:
            print("System Status                 : READY")
        else:
            print("System Status                 : WARNING")

        print("=" * 70)

    else:
        print("Unknown command:", command)
        print_usage()


if __name__ == "__main__":
    main()