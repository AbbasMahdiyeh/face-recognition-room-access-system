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
from dataclasses import dataclass

import numpy as np
from insightface.app import FaceAnalysis

@dataclass
class FaceEncodingResult:
    """
    Store the output of face encoding.

    The embedding is used for recognition, while the bounding
    box is used later for drawing visual feedback on the image.
    """

    embedding: np.ndarray
    bbox: tuple[int, int, int, int]


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
    
    def encode_largest_face_with_bbox(
        self,
        image,
    ) -> FaceEncodingResult | None:
        """
        Detect the largest face and return both its embedding and bounding box.

        Returning the bounding box is important for visual feedback.
        The UI layer will use it to draw a green or red rectangle
        around the recognized face.
        """

        faces = self.app.get(image)

        if not faces:
            return None

        largest_face = max(
            faces,
            key=self._face_area,
        )

        x1, y1, x2, y2 = map(
            int,
            largest_face.bbox,
        )

        return FaceEncodingResult(
            embedding=largest_face.embedding,
            bbox=(x1, y1, x2, y2),
        )

    def encode_largest_face(self, image) -> np.ndarray | None:
        """
        Detect faces in an image and return the embedding of the largest face.

        If no face is detected, return None.

        This method keeps the public API simple for components that only
        need the embedding and do not need visual information such as bbox.
        
        When multiple faces are found, the largest face is selected because
        in an access-control scenario the main user is usually closest to
        the camera.
        """

        result = self.encode_largest_face_with_bbox(image)

        if result is None:
            return None

        return result.embedding