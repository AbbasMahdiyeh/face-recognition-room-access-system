"""
Web dashboard application.

Purpose
-------
Provide a browser-based management interface for the access-control system.

The web dashboard is designed for headless Raspberry Pi deployment,
where no monitor, keyboard, or desktop session is required.

Current features
----------------
- Live annotated camera stream
- Browser-based system dashboard

Planned extensions
------------------
- Web-based user enrollment
- User management
- Access statistics
- Event log viewer
"""

import cv2
from pathlib import Path
from flask import Flask, Response, render_template, jsonify
from room_access.camera.camera_factory import CameraFactory
from room_access.config.settings import Settings
from room_access.processing.frame_processor import FrameProcessor
from room_access.recognition.enrollment_manager import EnrollmentManager


class WebDashboardApp:
    """
    Run the access-control system through a browser interface.
    """

    def __init__(self):
        """
        Create the shared live access application.

        All AI, logging, LED, temperature, and overlay logic remains
        inside LiveAccessApp. This class only changes the output target
        from a desktop window to a web browser.
        """

        # Web mode uses the same camera and processing pipeline as desktop mode.
        # Only the output target changes: annotated frames are streamed to a browser
        # instead of being displayed with cv2.imshow().
        self.settings = Settings()

        self.camera = CameraFactory.create_camera(
            self.settings,
        )

        self.frame_processor = FrameProcessor(
            self.settings,
        )

        self.dataset_root = Path("data/authorized_faces")
        self.enrollment_manager = EnrollmentManager()

        self.enrollment_user_name = None
        self.enrollment_captured_count = 0
        self.enrollment_capture_count = self.settings.get(
            "enrollment",
            "capture_count",
            5,
        )
        self.latest_enrollment_frame = None

        self.enrollment_completed = False

        self.app = Flask(
            __name__,
            template_folder="../templates",
            static_folder="../static",
        )

        self.app.add_url_rule(
            "/",
            "index",
            self.index,
        )

        self.app.add_url_rule(
            "/video",
            "video",
            self.video,
        )

        self.app.add_url_rule("/enroll", "enroll", self.enroll)
        self.app.add_url_rule("/users", "users", self.users)
        self.app.add_url_rule("/stats", "stats", self.stats)
        self.app.add_url_rule("/logs", "logs", self.logs)
        self.app.add_url_rule("/health", "health", self.health)

        self.app.add_url_rule(
            "/enroll/<user_name>",
            "enroll_user",
            self.enroll_user,
        )

        self.app.add_url_rule(
            "/enroll-stream",
            "enroll_stream",
            self.enroll_stream,
        )

        self.app.add_url_rule(
            "/capture-enrollment",
            "capture_enrollment",
            self.capture_enrollment,
            methods=["POST"],
        )

    def index(self):
        """
        Render the web dashboard page.
        """

        return render_template("index.html")
    
    def enroll(self):
        """
        Placeholder page for future web-based user enrollment.
        """

        return render_template("enroll.html")


    def users(self):
        """
        Placeholder page for future web-based user management.
        """

        return render_template("users.html")


    def stats(self):
        """
        Placeholder page for future access statistics.
        """

        return render_template("stats.html")


    def logs(self):
        """
        Placeholder page for future event log viewer.
        """

        return render_template("logs.html")


    def health(self):
        """
        Placeholder page for future system health dashboard.
        """

        return render_template("health.html")

    def generate_frames(self):
        """
        Generate MJPEG frames for browser streaming.
        """

        if not self.camera.open():
            print("Failed to open camera.")
            return

        print("Web access-control stream started.")

        try:
            while True:
                frame = self.camera.read_frame()

                if frame is None:
                    print("Failed to read frame.")
                    break

                annotated_frame = self.frame_processor.process_frame(frame)

                success, buffer = cv2.imencode(
                    ".jpg",
                    annotated_frame,
                )

                if not success:
                    continue

                frame_bytes = buffer.tobytes()

                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n"
                    + frame_bytes
                    + b"\r\n"
                )

        finally:
            self.camera.release()

    def video(self):
        """
        Return the MJPEG video stream response.
        """

        return Response(
            self.generate_frames(),
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )

    def run(self):
        """
        Start the Flask web server.
        """

        print("Open in browser:")
        print("http://<raspberry-pi-ip>:5000")

        self.app.run(
            host="0.0.0.0",
            port=5000,
            threaded=True,
        )


    def enroll_user(self, user_name: str):
        """
        Render the web-based enrollment page for one user.
        """

        self.enrollment_user_name = user_name
        self.enrollment_captured_count = 0
        self.latest_enrollment_frame = None
        self.enrollment_completed = False

        user_dir = self.dataset_root / user_name
        user_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return render_template(
            "enroll.html",
            user_name=user_name,
            capture_count=self.enrollment_capture_count,
        )


    def generate_enrollment_frames(self):
        """
        Stream raw camera frames for web-based user enrollment.
        """

        if not self.camera.open():
            print("Failed to open camera.")
            return

        try:
            while True:
                frame = self.camera.read_frame()

                if frame is None:
                    break

                frame = cv2.resize(
                    frame,
                    (
                        self.settings.get("display", "width"),
                        self.settings.get("display", "height"),
                    ),
                )

                self.latest_enrollment_frame = frame.copy()

                success, buffer = cv2.imencode(
                    ".jpg",
                    frame,
                )

                if not success:
                    continue

                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n"
                    + buffer.tobytes()
                    + b"\r\n"
                )

        finally:
            self.camera.release()


    def enroll_stream(self):
        """
        Return the enrollment camera stream.
        """

        return Response(
            self.generate_enrollment_frames(),
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )


    def capture_enrollment(self):
        """
        Save the latest enrollment frame and generate embedding when complete.
        """

        if self.enrollment_user_name is None:
            return jsonify({"error": "No active enrollment user."}), 400

        if self.latest_enrollment_frame is None:
            return jsonify({"error": "No frame available yet."}), 400
        
        if self.enrollment_completed:
            return jsonify(
                {
                    "error": "Enrollment is already completed.",
                    "captured": self.enrollment_captured_count,
                    "target": self.enrollment_capture_count,
                    "completed": True,
                }
            ), 400

        user_dir = self.dataset_root / self.enrollment_user_name
        user_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.enrollment_captured_count += 1

        image_path = (
            user_dir
            / f"{self.enrollment_user_name}_{self.enrollment_captured_count:02d}.jpg"
        )

        cv2.imwrite(
            str(image_path),
            self.latest_enrollment_frame,
        )

        completed = self.enrollment_captured_count >= self.enrollment_capture_count

        embedding_path = None

        if completed:
            self.enrollment_completed = True

            embedding_path = self.enrollment_manager.enroll_user(
                self.enrollment_user_name,
            )

        return jsonify(
            {
                "captured": self.enrollment_captured_count,
                "target": self.enrollment_capture_count,
                "completed": completed,
                "embedding_path": str(embedding_path) if embedding_path else None,
            }
        )