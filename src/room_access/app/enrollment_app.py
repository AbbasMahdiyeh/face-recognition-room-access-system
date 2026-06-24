"""
Camera-based user enrollment application.

This module captures reference face images from the webcam
and then generates the user's authorized embedding.

It is separate from LiveAccessApp because enrollment and
real-time access control are two different application modes.
"""

from pathlib import Path

import cv2

from room_access.camera.laptop_webcam_camera import LaptopWebcamCamera
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

        capture_count defines how many reference images will be
        collected for each user. Multiple images improve recognition
        stability under different poses and lighting conditions.
        """

        self.dataset_root = Path(dataset_root)
        self.capture_count = capture_count
        self.camera = LaptopWebcamCamera()
        self.enrollment_manager = EnrollmentManager()

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
            print("Failed to open webcam.")
            return

        print(f"Enrollment started for user: {user_name}")
        print("Press 'c' to capture an image.")
        print("Press 'q' or 'Esc' to cancel.")

        captured_count = 0

        while captured_count < self.capture_count:
            frame = self.camera.read_frame()

            if frame is None:
                print("Failed to read frame.")
                break

            display_frame = frame.copy()

            cv2.putText(
                display_frame,
                f"User: {user_name}",
                (30, 40),
                cv2.FONT_HERSHEY_DUPLEX,
                0.9,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                display_frame,
                f"Captured: {captured_count}/{self.capture_count}",
                (30, 80),
                cv2.FONT_HERSHEY_DUPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                display_frame,
                "Press C to capture | Q/Esc to cancel",
                (30, 120),
                cv2.FONT_HERSHEY_DUPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.imshow(
                "User Enrollment",
                display_frame,
            )

            key = cv2.waitKey(30) & 0xFF

            if key == ord("c"):
                image_path = user_dir / f"{user_name}_{captured_count + 1:02d}.jpg"

                cv2.imwrite(
                    str(image_path),
                    frame,
                )

                captured_count += 1
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