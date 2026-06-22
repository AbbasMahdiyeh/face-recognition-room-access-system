"""
Status bar drawing utilities.

This module is responsible for drawing the access status
bar at the bottom of the video frame.

It does not perform recognition and is independent from
the recognition pipeline.
"""

import cv2

from room_access.dashboard.theme import (
    TEXT_COLOR,
    STATUS_BAR_HEIGHT,
)



def draw_status_bar(
    image,
    text: str,
    color: tuple[int, int, int],
):
    """
    Draw the access status bar.

    Parameters
    ----------
    image
        Image to draw on.

    text
        Status message such as ACCESS GRANTED.

    color
        Background color of the status bar.
    """

    height, width = image.shape[:2]

    cv2.rectangle(
        image,
        (0, height - STATUS_BAR_HEIGHT),
        (width, height),
        color,
        -1,
    )

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0
    thickness = 2

    text_size, _ = cv2.getTextSize(
        text,
        font,
        font_scale,
        thickness,
    )

    text_width, text_height = text_size

    text_x = (width - text_width) // 2
    text_y = height - (STATUS_BAR_HEIGHT - text_height) // 2

    cv2.putText(
        image,
        text,
        (text_x, text_y),
        font,
        font_scale,
        TEXT_COLOR,
        thickness,
    )