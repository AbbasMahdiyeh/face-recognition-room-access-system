"""
Real-time face recognition verification script.

This script captures live frames from the laptop webcam,
runs the recognition pipeline, draws the visual overlay,
and displays the result in real time.

Press 'q' to exit.
"""

import sys
import time
from datetime import datetime
from pathlib import Path
import cv2

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.camera.laptop_webcam_camera import LaptopWebcamCamera
from room_access.dashboard.display_overlay import draw_recognition_overlay
from room_access.recognition.recognition_engine import RecognitionEngine


def main():
    """
    Run the complete real-time face recognition pipeline.
    """

    camera = LaptopWebcamCamera()

    if not camera.open():
        print("Failed to open webcam.")
        return

    engine = RecognitionEngine(
        embeddings_root="data/embeddings",
        threshold=0.5,
    )

    print("Real-time recognition started.")
    print("Press 'q' to exit.")

    previous_time = time.time()
    fps = 0.0

    frame_count = 0
    recognition_interval = 20
    last_result = None

    while True:

        frame = camera.read_frame()

        if frame is None:
            print("Failed to read frame.")
            break

        frame = cv2.resize(frame, (1280, 720))
        
        frame_count += 1

        # Running the AI model on every frame is expensive on CPU.
        # We only run recognition every N frames and reuse the latest
        # result in between to keep the video stream responsive.
        if frame_count % recognition_interval == 0 or last_result is None:
            last_result = engine.recognize(frame)

        current_time = time.time()
        elapsed_time = current_time - previous_time

        if elapsed_time > 0:
            fps = 1.0 / elapsed_time

        previous_time = current_time

        face_count = 1 if last_result is not None and last_result.bbox is not None else 0

        info_lines = [
            ("Camera", "Laptop Webcam"),
            ("FPS", f"{fps:.1f}"),
            ("Faces", str(face_count)),
            ("Time", datetime.now().strftime("%H:%M:%S")),
            ("Temp", "-- °C"),
        ]

        annotated_frame = draw_recognition_overlay(
            frame,
            last_result,
            info_lines,
        )

        cv2.imshow(
            "Face Recognition",
            annotated_frame,
        )

        key = cv2.waitKey(30) & 0xFF

        if key == ord("q") or key == 27:
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()