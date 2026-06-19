"""
EmbeddingStorage verification script.

This script verifies that embeddings can be saved
and loaded correctly using the EmbeddingStorage class.

A randomly generated NumPy array is used instead of
a real face embedding so that this test remains
independent from the AI recognition pipeline.
"""

import sys
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.storage.embedding_storage import EmbeddingStorage


def main():
    """
    Verify saving and loading of embeddings.
    """

    storage = EmbeddingStorage(
        "data/embeddings"
    )

    # Generate a fake 512-dimensional embedding.
    test_embedding = np.random.rand(512)

    # Save the embedding.
    saved_path = storage.save_embedding(
        "test_user",
        test_embedding,
    )

    print("Saved to:", saved_path)

    # Load the embedding.
    loaded_embedding = storage.load_embedding(
        "test_user"
    )

    if loaded_embedding is None:
        print("Failed to load embedding.")
        return

    print("Loaded embedding shape:", loaded_embedding.shape)

    if np.array_equal(test_embedding, loaded_embedding):
        print("Embedding verification: SUCCESS")
        print()

        print("Stored embeddings:")

        for embedding_path in storage.list_embeddings():
            print("-", embedding_path.name)

        print()

        print("Embedding exists:",
            storage.embedding_exists("test_user"))

        print()

        print("Cleaning up test data...")

        deleted = storage.delete_embedding(
            "test_user"
        )

        print("Deleted:", deleted)

        print()

        print("Embedding exists:",
            storage.embedding_exists("test_user"))
    else:
        print("Embedding verification: FAILED")


if __name__ == "__main__":
    main()