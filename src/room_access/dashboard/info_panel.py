import cv2

from room_access.dashboard.components import draw_info_icon
from room_access.dashboard.theme import (
    BACKGROUND_COLOR,
    BORDER_COLOR,
    SYSTEM_INFO_COLOR,
    TEXT_COLOR,
)


def draw_info_panel(
    image,
    info_lines: list[tuple[str, str]],
):
    height, width = image.shape[:2]

    x1 = 20
    y1 = 20
    x2 = width - 20
    y2 = 170

    cv2.rectangle(image, (x1, y1), (x2, y2), BACKGROUND_COLOR, -1)
    cv2.rectangle(image, (x1, y1), (x2, y2), BORDER_COLOR, 1)

    cv2.putText(
        image,
        "AI ACCESS CONTROL",
        (x1 + 35, y1 + 45),
        cv2.FONT_HERSHEY_DUPLEX,
        1.0,
        TEXT_COLOR,
        2,
    )

    section_y = y1 + 105
    section_width = (x2 - x1) // len(info_lines)

    for index, (label, value) in enumerate(info_lines):
        section_x = x1 + index * section_width

        if index > 0:
            cv2.line(
                image,
                (section_x, y1 + 75),
                (section_x, y2 - 25),
                BORDER_COLOR,
                1,
            )

        icon_type = label.lower().replace(" ", "_")
        if icon_type in ("room_temp", "temp"):
            icon_type = "temperature"

        draw_info_icon(
            image,
            icon_type,
            (section_x + 45, section_y),
            SYSTEM_INFO_COLOR,
            scale=1.0,
        )

        cv2.putText(
            image,
            label,
            (section_x + 85, section_y - 12),
            cv2.FONT_HERSHEY_DUPLEX,
            0.65,
            TEXT_COLOR,
            1,
        )

        cv2.putText(
            image,
            value,
            (section_x + 85, section_y + 25),
            cv2.FONT_HERSHEY_DUPLEX,
            0.65,
            SYSTEM_INFO_COLOR,
            1,
        )