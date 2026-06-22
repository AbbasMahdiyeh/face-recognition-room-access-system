"""
FaceMatcher verification script.

This script verifies that FaceMatcher can compare
two numerical embeddings using cosine similarity.

We use manually created NumPy arrays here so the test
remains independent from InsightFace.
"""

import sys
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.recognition.face_matcher import FaceMatcher


def main():
    """
    Compare simple test embeddings.
    """

    matcher = FaceMatcher()

    embedding_a = np.array([1.0, 0.0, 0.0])
    embedding_b = np.array([1.0, 0.0, 0.0])
    embedding_c = np.array([0.0, 1.0, 0.0])

    similarity_ab = matcher.cosine_similarity(
        embedding_a,
        embedding_b,
    )

    similarity_ac = matcher.cosine_similarity(
        embedding_a,
        embedding_c,
    )

    print("\nCosine Similarity Tests")
    print("-----------------------")
    print("Similarity A-B:", similarity_ab)
    print("Similarity A-C:", similarity_ac)

    print("A-B is match:", matcher.is_match(embedding_a, embedding_b))
    print("A-C is match:", matcher.is_match(embedding_a, embedding_c))


    # Use different similarity thresholds to verify that
    # the final access decision changes while the cosine
    # similarity score itself remains identical.
    
    strict_matcher = FaceMatcher(
        threshold=0.9
    )

    loose_matcher = FaceMatcher(
        threshold=0.1
    )
    
    print("\nThreshold Tests")
    print("----------------")
    print("Strict matcher A-C:", strict_matcher.is_match(embedding_a, embedding_c))
    print("Loose matcher A-C:", loose_matcher.is_match(embedding_a, embedding_c))


if __name__ == "__main__":
    main()