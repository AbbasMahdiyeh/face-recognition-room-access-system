"""
Camera-based user enrollment application.

This module captures reference face images from the camera and then
generates the user's authorized embedding.

Enrollment is separate from live access control because registering
users and verifying access are two different application modes.
"""

from pathlib import Path

import cv2

from room_access.camera.camera_factory import CameraFactory
from room_access.config.settings import Settings
from room_access.recognition.enrollment_manager import EnrollmentManager


class EnrollmentApp:
    """
    Capture face images and enroll a new authorized user.
    """

    def __init__(
        self,
        dataset_root: str = "data/authorized_faces",
        capture_count: int = 5,
    ):
        """
        Initialize the enrollment application.
        """

        self.dataset_root = Path(dataset_root)
        self.capture_count = capture_count
        self.settings = Settings()
        self.camera = CameraFactory.create_camera(self.settings)
        self.enrollment_manager = EnrollmentManager()

    def _draw_enrollment_overlay(
        self,
        frame,
        user_name: str,
        captured_count: int,
        message: str = "",
    ):
        """
        Draw enrollment instructions and progress on the camera frame.
        """

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (0, 0),
            (frame.shape[1], 155),
            (2, 6, 23),
            -1,
        )

        cv2.addWeighted(
            overlay,
            0.82,
            frame,
            0.18,
            0,
            frame,
        )

        # Draw a subtle face-position guide in the center of the frame.
        # This helps the user keep their face in a stable position during
        # enrollment, which improves the quality of the captured images.
        guide_width = 420
        guide_height = 520

        center_x = frame.shape[1] // 2
        center_y = frame.shape[0] // 2 + 40

        top_left = (
            center_x - guide_width // 2,
            center_y - guide_height // 2,
        )

        bottom_right = (
            center_x + guide_width // 2,
            center_y + guide_height // 2,
        )

        cv2.rectangle(
            frame,
            top_left,
            bottom_right,
            (34, 211, 238),
            2,
        )


        cv2.putText(
            frame,
            "User Enrollment",
            (30, 38),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (34, 211, 238),
            2,
        )

        cv2.putText(
            frame,
            f"User: {user_name}",
            (30, 76),
            cv2.FONT_HERSHEY_DUPLEX,
            0.75,
            (241, 245, 249),
            2,
        )

        cv2.putText(
            frame,
            f"Captured: {captured_count}/{self.capture_count}",
            (30, 112),
            cv2.FONT_HERSHEY_DUPLEX,
            0.75,
            (241, 245, 249),
            2,
        )

        cv2.putText(
            frame,
            "C: capture   |   Q / Esc: cancel",
            (30, 140),
            cv2.FONT_HERSHEY_DUPLEX,
            0.55,
            (148, 163, 184),
            1,
        )

        cv2.putText(
            frame,
            "Keep your face inside the guide rectangle",
            (30, 165),
            cv2.FONT_HERSHEY_DUPLEX,
            0.55,
            (148, 163, 184),
            1,
        )

        if message:
            cv2.rectangle(
                frame,
                (30, frame.shape[0] - 78),
                (frame.shape[1] - 30, frame.shape[0] - 25),
                (20, 83, 45),
                -1,
            )

            cv2.rectangle(
                frame,
                (30, frame.shape[0] - 78),
                (frame.shape[1] - 30, frame.shape[0] - 25),
                (34, 197, 94),
                2,
            )

            cv2.putText(
                frame,
                message,
                (52, frame.shape[0] - 43),
                cv2.FONT_HERSHEY_DUPLEX,
                0.65,
                (220, 252, 231),
                2,
            )

        return frame

    def run(
        self,
        user_name: str,
    ):
        """
        Capture reference images for one user and create their embedding.
        """

        user_dir = self.dataset_root / user_name
        user_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.camera.open():
            print("Failed to open camera.")
            return

        print(f"Enrollment started for user: {user_name}")
        print("Press 'c' to capture an image.")
        print("Press 'q' or 'Esc' to cancel.")

        captured_count = 0
        message = ""

        while captured_count < self.capture_count:
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

            display_frame = self._draw_enrollment_overlay(
                frame.copy(),
                user_name,
                captured_count,
                message,
            )

            cv2.imshow(
                "Face Recognition Room Access System - User Enrollment",
                display_frame,
            )

            key = cv2.waitKey(30) & 0xFF
            message = ""

            if key == ord("c"):
                image_path = user_dir / f"{user_name}_{captured_count + 1:02d}.jpg"

                cv2.imwrite(
                    str(image_path),
                    frame,
                )

                captured_count += 1
                message = f"Captured image {captured_count}/{self.capture_count}"

                print("Captured:", image_path)

            if key == ord("q") or key == 27:
                print("Enrollment cancelled.")
                break

        self.camera.release()
        cv2.destroyAllWindows()

        if captured_count == self.capture_count:
            saved_path = self.enrollment_manager.enroll_user(user_name)

            if saved_path is None:
                print("Enrollment failed.")
                return

            print("Enrollment completed.")
            print("Saved embedding:", saved_path)
        else:
            print("Not enough images captured. Embedding was not created.")