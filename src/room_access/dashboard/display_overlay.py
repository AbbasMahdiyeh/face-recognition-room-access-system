"""
Display overlay utilities.

This module draws recognition results on image frames.

It is responsible only for visualization:
- drawing face bounding boxes
- showing the recognized user name
- showing access status text

It does not perform recognition or make access decisions.
"""

import cv2

from room_access.recognition.recognition_engine import RecognitionResult

from room_access.dashboard.theme import (
    AUTHORIZED_COLOR,
    UNAUTHORIZED_COLOR,
    TEXT_COLOR,
    LINE_THICKNESS,
    CORNER_LENGTH,
    FONT_SCALE,
    FONT_THICKNESS,
)
from room_access.dashboard.status_bar import draw_status_bar
from room_access.dashboard.info_panel import draw_info_panel

def draw_corner_box(
    image,
    bbox: tuple[int, int, int, int],
    color: tuple[int, int, int],
    thickness = LINE_THICKNESS,
    corner_length = CORNER_LENGTH ,
):
    """
    Draw a modern corner-style bounding box.

    Corner boxes look cleaner than full rectangles and keep
    the face area less visually cluttered.
    """

    x1, y1, x2, y2 = bbox

    # Top-left corner
    cv2.line(image, (x1, y1), (x1 + corner_length, y1), color, thickness)
    cv2.line(image, (x1, y1), (x1, y1 + corner_length), color, thickness)

    # Top-right corner
    cv2.line(image, (x2, y1), (x2 - corner_length, y1), color, thickness)
    cv2.line(image, (x2, y1), (x2, y1 + corner_length), color, thickness)

    # Bottom-left corner
    cv2.line(image, (x1, y2), (x1 + corner_length, y2), color, thickness)
    cv2.line(image, (x1, y2), (x1, y2 - corner_length), color, thickness)

    # Bottom-right corner
    cv2.line(image, (x2, y2), (x2 - corner_length, y2), color, thickness)
    cv2.line(image, (x2, y2), (x2, y2 - corner_length), color, thickness)


def draw_filled_label(
    image,
    text: str,
    bbox: tuple[int, int, int, int],
    color: tuple[int, int, int],
):
    """
    Draw a centered label above the face bounding box.

    Centering the label makes the overlay look cleaner and
    keeps the identity information visually connected to the face.
    """

    x1, y1, x2, _ = bbox

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = FONT_SCALE
    thickness = FONT_THICKNESS
    padding_x = 12
    padding_y = 8

    text_size, _ = cv2.getTextSize(
        text,
        font,
        font_scale,
        thickness,
    )

    text_width, text_height = text_size
    face_center_x = (x1 + x2) // 2

    label_width = text_width + padding_x * 2
    label_height = text_height + padding_y * 2

    label_x1 = face_center_x - label_width // 2
    label_y1 = max(y1 - label_height - 8, 0)
    label_x2 = label_x1 + label_width
    label_y2 = label_y1 + label_height

    cv2.rectangle(
        image,
        (label_x1, label_y1),
        (label_x2, label_y2),
        color,
        -1,
    )

    cv2.putText(
        image,
        text,
        (label_x1 + padding_x, label_y2 - padding_y),
        font,
        font_scale,
        TEXT_COLOR,
        thickness,
    )

def draw_recognition_overlay(
    image,
    result: RecognitionResult,
    info_lines: list[tuple[str, str]] | None = None,
):
    """
    Draw visual feedback for a recognition result.

    Green indicates granted access.
    Red indicates denied access or an unknown user.
    """

    annotated_image = image.copy()

    if result.access_granted:
        color = AUTHORIZED_COLOR
        user_label = result.user_name or "Unknown"
        access_label = "ACCESS GRANTED"
    else:
        color = UNAUTHORIZED_COLOR
        user_label = "Unknown"
        access_label = "ACCESS DENIED"

    bbox = result.bbox

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        label_text = (
            f"{user_label.upper()} | AUTHORIZED"
            if result.access_granted
            else "UNKNOWN | UNAUTHORIZED"
        )

        draw_corner_box(
            annotated_image,
            bbox,
            color,
        )

        draw_filled_label(
            annotated_image,
            label_text,
            bbox,
            color,
        )

        if info_lines is None:
            info_lines = [
                ("Camera", "Laptop Webcam"),
                ("FPS", "--"),
                ("Faces", "0"),
                ("Time", "--:--:--"),
                ("Temp", "-- °C"),
            ]

        draw_info_panel(
            annotated_image,
            info_lines,
        )

        draw_status_bar(
            annotated_image,
            access_label,
            color,
            result.access_granted,
        )

    return annotated_image