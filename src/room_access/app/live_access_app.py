"""
Desktop live access-control application.

Purpose
-------
Run the real-time access-control system with a desktop OpenCV window.

Architecture
------------
This class is responsible only for desktop display.

The shared AI pipeline is handled by FrameProcessor:
camera frame
    -> FrameProcessor
    -> annotated frame
    -> cv2.imshow()

Why this exists
---------------
The project supports multiple output modes.

Desktop mode uses OpenCV windows.
Web mode streams the same annotated frames to a browser.

Both modes reuse the same processing pipeline, which prevents
duplicated recognition, logging, LED, and temperature logic.
"""


import cv2
from room_access.camera.camera_factory import CameraFactory
from room_access.config.settings import Settings
from room_access.processing.frame_processor import FrameProcessor


class LiveAccessApp:
    """
    Run the desktop version of the access-control system.
    """

    def __init__(self):
        """
        Initialize shared settings, camera backend, and frame processor.

        Camera selection is handled by CameraFactory.
        FrameProcessor owns the AI, access decision, logging,
        LED feedback, temperature, and overlay pipeline.
        """

        self.settings = Settings()
        self.camera = CameraFactory.create_camera(
            self.settings,
        )

        self.frame_processor = FrameProcessor(
            self.settings,
        )

    def run(self):
        """
        Start the desktop OpenCV live-view loop.

        This method only handles:
        - reading frames from the camera
        - sending frames to FrameProcessor
        - displaying annotated frames with cv2.imshow()
        """

        if not self.camera.open():
            print("Failed to open webcam.")
            return

        print("Real-time recognition started.")
        print("Press 'q' or 'Esc' to exit.")

        while True:
            frame = self.camera.read_frame()

            if frame is None:
                print("Failed to read frame.")
                break

            annotated_frame = self.frame_processor.process_frame(frame)

            cv2.imshow(
                "Face Recognition",
                annotated_frame,
            )

            key = cv2.waitKey(30) & 0xFF

            if key == ord("q") or key == 27:
                break

        self.camera.release()
        cv2.destroyAllWindows()