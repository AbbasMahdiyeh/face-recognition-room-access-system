"""
Dashboard theme configuration.

This module centralizes all visual styling used by the
dashboard. Keeping colors and drawing parameters here
makes it easy to update the application's appearance
without modifying drawing logic.
"""

# ==========================
# Colors (OpenCV uses BGR)
# ==========================

AUTHORIZED_COLOR = (80, 180, 80)

UNAUTHORIZED_COLOR = (80, 80, 220)

TEXT_COLOR = (255, 255, 255)

SYSTEM_INFO_COLOR = (0, 215, 255)

BACKGROUND_COLOR = (35, 35, 35)


# ==========================
# Drawing parameters
# ==========================

LINE_THICKNESS = 3

CORNER_LENGTH = 35

FONT_SCALE = 0.65

FONT_THICKNESS = 2

STATUS_BAR_HEIGHT = 65