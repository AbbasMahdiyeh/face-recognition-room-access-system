"""
Laptop webcam verification script.

This script verifies that LaptopWebcamCamera can open
a webcam, read live frames, and display them with OpenCV.

Press 'q' to close the camera window.
"""

import sys
from pathlib import Path

import cv2

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.camera.laptop_webcam_camera import LaptopWebcamCamera


def main():
    """
    Open the laptop webcam and display live frames.
    """

    camera = LaptopWebcamCamera(camera_index=0)

    if not camera.open():
        print("Failed to open webcam.")
        return

    print("Webcam opened successfully.")
    print("Press 'q' to quit.")

    while True:
        frame = camera.read_frame()

        if frame is None:
            print("Failed to read frame.")
            break

        cv2.imshow("Laptop Webcam Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()