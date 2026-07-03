"""
Frame processor.

Purpose
-------
Process one camera frame through the full access-control pipeline.

Why this exists
---------------
The project supports multiple output modes:

- Desktop window using cv2.imshow()
- Web dashboard using Flask MJPEG streaming

Both modes need the same AI, decision, logging, LED, temperature,
and overlay workflow.

This class keeps that shared workflow in one place so the logic is
not duplicated across desktop and web applications.
"""

import time
from datetime import datetime

import cv2

from room_access.access_control.access_decision import AccessDecisionManager
from room_access.dashboard.display_overlay import draw_recognition_overlay
from room_access.hardware.hardware_factory import HardwareFactory
from room_access.hardware.temperature_factory import TemperatureFactory
from room_access.recognition.recognition_engine import RecognitionEngine
from room_access.storage.event_logger import EventLogger


class FrameProcessor:
    """
    Process camera frames for access-control applications.
    """

    def __init__(
        self,
        settings,
    ):
        """
        Initialize long-lived processing components.
        """

        self.settings = settings

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

        self.led_controller = HardwareFactory.create_led_controller(
            self.settings,
        )

        self.temperature_sensor = (
            TemperatureFactory.create_temperature_sensor(
                self.settings,
            )
        )

        self.recognition_interval = self.settings.get(
            "recognition",
            "recognition_interval",
        )

        self.repeat_log_interval_seconds = self.settings.get(
            "logging",
            "repeat_log_interval_seconds",
        )

        self.previous_time = time.time()
        self.fps = 0.0
        self.recognition_time_ms = 0.0

        self.frame_count = 0
        self.last_result = None

        self.last_log_time = 0.0
        self.last_logged_identity = None
        self.last_logged_access = None

        self.camera_name = self.settings.get(
            "camera",
            "name",
            "Unknown Camera",
        )

    def process_frame(
        self,
        frame,
    ):
        """
        Process one frame and return the annotated frame.
        """

        frame = cv2.resize(
            frame,
            (
                self.settings.get("display", "width"),
                self.settings.get("display", "height"),
            ),
        )

        self.frame_count += 1

        if (
            self.frame_count % self.recognition_interval == 0
            or self.last_result is None
        ):
            recognition_start_time = time.time()

            self.last_result = self.engine.recognize(frame)

            self.recognition_time_ms = (
                time.time() - recognition_start_time
            ) * 1000

        current_time = time.time()
        elapsed_time = current_time - self.previous_time

        if elapsed_time > 0:
            self.fps = 1.0 / elapsed_time

        self.previous_time = current_time

        face_count = (
            1
            if self.last_result is not None
            and self.last_result.bbox is not None
            else 0
        )

        temperature = self.temperature_sensor.read_temperature()
        temperature_text = f"{temperature:.1f} C"

        info_lines = [
            ("Camera", self.camera_name),
            ("FPS", f"{self.fps:.1f}"),
            ("Faces", str(face_count)),
            ("AI Time", f"{self.recognition_time_ms:.1f} ms"),
            ("Time", datetime.now().strftime("%H:%M:%S")),
            ("Temp", temperature_text),
        ]

        annotated_frame = draw_recognition_overlay(
            frame,
            self.last_result,
            info_lines,
        )

        if self.last_result is not None:
            self._handle_access_event(
                annotated_frame=annotated_frame,
                temperature_text=temperature_text,
            )

        return annotated_frame

    def _handle_access_event(
        self,
        annotated_frame,
        temperature_text: str,
    ):
        """
        Handle access decision, LED feedback, and event logging.
        """
        if self.last_result is None:
            return
        
        now = time.time()

        decision = self.decision_manager.decide(
            user_name=self.last_result.user_name,
            access_granted=self.last_result.access_granted,
        )

        current_identity = decision.user_name
        current_access = decision.access_granted

        self.led_controller.show_access_result(
            access_granted=current_access,
        )

        identity_changed = (
            current_identity != self.last_logged_identity
            or current_access != self.last_logged_access
        )

        repeat_interval_passed = (
            now - self.last_log_time >= self.repeat_log_interval_seconds
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
                similarity=self.last_result.similarity,
                fps=self.fps,
                recognition_time_ms=self.recognition_time_ms,
                temperature=temperature_text,
                image_path=image_path,
                reason=decision.reason,
                camera=self.camera_name,
            )

            self.last_logged_identity = current_identity
            self.last_logged_access = current_access
            self.last_log_time = now