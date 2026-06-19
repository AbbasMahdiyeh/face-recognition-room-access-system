"""
Face encoding module.

This module converts face images into numerical embeddings
using InsightFace / ArcFace.

The FaceEncoder is responsible only for:
- loading the InsightFace model
- detecting faces in an image
- extracting face embeddings

It does not decide whether access is granted or denied.
That responsibility will belong to another component.
"""

import numpy as np
from insightface.app import FaceAnalysis


class FaceEncoder:
    """
    Generate face embeddings from input images.
    """

    def __init__(self):
        """
        Initialize the InsightFace analysis pipeline.

        ctx_id=-1 forces CPU mode. This keeps the project compatible
        with normal laptops and Raspberry Pi devices without requiring GPU.
        """

        self.app = FaceAnalysis(name="buffalo_l")
        self.app.prepare(ctx_id=-1)

    def _face_area(self, face) -> float:
        """
        Calculate the area of a detected face bounding box.

        The largest detected face is assumed to belong to the
        primary user standing closest to the camera.

        Parameters
        ----------
        face
            Face object returned by InsightFace.

        Returns
        -------
        float
            Area of the face bounding box in pixels.
        """

        width = face.bbox[2] - face.bbox[0]
        height = face.bbox[3] - face.bbox[1]

        return width * height

    def encode_largest_face(self, image) -> np.ndarray | None:
        """
        Detect faces in an image and return the embedding of the largest face.

        If no face is detected, return None.

        When multiple faces are found, the largest face is selected because
        in an access-control scenario the main user is usually closest to
        the camera.
        """

        faces = self.app.get(image)

        if not faces:
            return None

        largest_face = max(
            faces,
            key=self._face_area,
        )

        return largest_face.embedding