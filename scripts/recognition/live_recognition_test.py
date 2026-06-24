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
from room_access.storage.event_logger import EventLogger


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

    logger = EventLogger(
    log_path="data/logs/access_events.csv"
)

    print("Real-time recognition started.")
    print("Press 'q' to exit.")

    previous_time = time.time()
    fps = 0.0

    frame_count = 0
    recognition_interval = 20
    last_result = None

    last_log_time = 0.0
    log_interval_seconds = 3.0
    recognition_time_ms = 0.0

    last_logged_identity = None
    last_logged_access = None
    repeat_log_interval_seconds = 10.0

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
            # Measure only the recognition step, not camera reading or UI drawing.
            # This helps us understand how expensive the AI pipeline is on each device.
            recognition_start_time = time.time()

            last_result = engine.recognize(frame)

            recognition_time_ms = (
                time.time() - recognition_start_time
            ) * 1000

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
            ("AI Time", f"{recognition_time_ms:.1f} ms"),
            ("Temp", "-- °C"),
        ]

        annotated_frame = draw_recognition_overlay(
            frame,
            last_result,
            info_lines,
        )

        if last_result is not None:
            now = time.time()

            current_identity = last_result.user_name or "Unknown"
            current_access = last_result.access_granted

            identity_changed = (
                current_identity != last_logged_identity
                or current_access != last_logged_access
            )

            repeat_interval_passed = (
                now - last_log_time >= repeat_log_interval_seconds
            )

            if identity_changed or repeat_interval_passed:

                event_name = (
                    "granted"
                    if current_access
                    else "denied"
                )
                
                image_path = logger.save_event_image(
                    annotated_frame,
                    event_name,
                )
                print("Saved event image:", image_path)

                logger.log_event(
                    user_name=current_identity if current_access else "Unknown",
                    access_granted=current_access,
                    similarity=last_result.similarity,
                    camera="Laptop Webcam",
                    fps=fps,
                    recognition_time_ms=recognition_time_ms,
                    temperature="--",
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

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()