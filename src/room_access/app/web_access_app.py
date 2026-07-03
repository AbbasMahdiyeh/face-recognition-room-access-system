"""
Web access-control application.

Purpose
-------
Provide a browser-based live view for the access-control system.

Why this exists
---------------
Raspberry Pi deployments are often headless and do not have a
desktop display available. The desktop version uses cv2.imshow(),
but that requires an active graphical session.

This web application reuses the same LiveAccessApp pipeline and
streams the final annotated frames to a browser as an MJPEG stream.
"""

import cv2
from flask import Flask, Response, render_template
from room_access.camera.camera_factory import CameraFactory
from room_access.config.settings import Settings
from room_access.processing.frame_processor import FrameProcessor


class WebAccessApp:
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

    def index(self):
        """
        Render the web dashboard page.
        """

        return render_template("index.html")

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