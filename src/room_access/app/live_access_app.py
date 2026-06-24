"""
Live access-control application.

This module coordinates the full live access-control workflow:
camera input, face recognition, access decision, dashboard rendering,
event logging, and event image capture.

Scripts should only start this application; the main workflow belongs here.
"""

import time
from datetime import datetime

import cv2

from room_access.access_control.access_decision import AccessDecisionManager
from room_access.camera.laptop_webcam_camera import LaptopWebcamCamera
from room_access.dashboard.display_overlay import draw_recognition_overlay
from room_access.recognition.recognition_engine import RecognitionEngine
from room_access.storage.event_logger import EventLogger
from room_access.config.settings import Settings


class LiveAccessApp:
    """
    Run the real-time face recognition access-control system.
    """

    def __init__(self):
        """
        Initialize all long-lived application components once.

        The camera, recognition engine, decision manager, and logger are
        created here so they are not recreated for every video frame.
        """

        self.settings = Settings()
        self.camera = LaptopWebcamCamera()

        self.engine = RecognitionEngine(
            embeddings_root="data/embeddings",
            threshold=self.settings.get(
                "recognition",
                "threshold",
            ),
        )

        self.decision_manager = AccessDecisionManager()

        self.logger = EventLogger(
            log_path="data/logs/access_events.csv",
        )

        self.recognition_interval = self.settings.get(
            "recognition",
            "recognition_interval",
        )
        
        self.repeat_log_interval_seconds = self.settings.get(
            "logging",
            "repeat_log_interval_seconds",
        )

    def run(self):
        """
        Start the live recognition loop.
        """

        if not self.camera.open():
            print("Failed to open webcam.")
            return

        print("Real-time recognition started.")
        print("Press 'q' or 'Esc' to exit.")

        previous_time = time.time()
        fps = 0.0
        recognition_time_ms = 0.0

        frame_count = 0
        last_result = None

        last_log_time = 0.0
        last_logged_identity = None
        last_logged_access = None

        while True:
            frame = self.camera.read_frame()

            if frame is None:
                print("Failed to read frame.")
                break

            frame = cv2.resize(
                frame,
                (
                    self.settings.get("display", "width"),
                    self.settings.get("display", "height"),
                ),
            )

            frame_count += 1

            if frame_count % self.recognition_interval == 0 or last_result is None:
                # Measure only the AI recognition step.
                # This metric helps compare performance across laptop and Raspberry Pi.
                recognition_start_time = time.time()

                last_result = self.engine.recognize(frame)

                recognition_time_ms = (
                    time.time() - recognition_start_time
                ) * 1000

            current_time = time.time()
            elapsed_time = current_time - previous_time

            if elapsed_time > 0:
                fps = 1.0 / elapsed_time

            previous_time = current_time

            face_count = (
                1
                if last_result is not None and last_result.bbox is not None
                else 0
            )

            info_lines = [
                ("Camera", "Laptop Webcam"),
                ("FPS", f"{fps:.1f}"),
                ("Faces", str(face_count)),
                ("AI Time", f"{recognition_time_ms:.1f} ms"),
                ("Time", datetime.now().strftime("%H:%M:%S")),
                ("Temp", "-- °C"),
            ]

            annotated_frame = draw_recognition_overlay(
                frame,
                last_result,
                info_lines,
            )

            if last_result is not None:
                now = time.time()

                decision = self.decision_manager.decide(
                    user_name=last_result.user_name,
                    access_granted=last_result.access_granted,
                )

                current_identity = decision.user_name
                current_access = decision.access_granted

                identity_changed = (
                    current_identity != last_logged_identity
                    or current_access != last_logged_access
                )

                repeat_interval_passed = (
                    now - last_log_time >= self.repeat_log_interval_seconds
                )

                if identity_changed or repeat_interval_passed:
                    event_name = "granted" if current_access else "denied"

                    image_path = self.logger.save_event_image(
                        annotated_frame,
                        event_name,
                    )

                    self.logger.log_event(
                        user_name=current_identity,
                        access_granted=current_access,
                        similarity=last_result.similarity,
                        camera="Laptop Webcam",
                        fps=fps,
                        recognition_time_ms=recognition_time_ms,
                        temperature="--",
                        image_path=image_path,
                        reason=decision.reason,
                    )

                    last_logged_identity = current_identity
                    last_logged_access = current_access
                    last_log_time = now

            cv2.imshow(
                "Face Recognition",
                annotated_frame,
            )

            key = cv2.waitKey(30) & 0xFF

            if key == ord("q") or key == 27:
                break

        self.camera.release()
        cv2.destroyAllWindows()