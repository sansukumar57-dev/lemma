"""Embedding provider selection."""

from __future__ import annotations

from functools import lru_cache

from app.core.config import settings
from app.core.embeddings.embeddings import Embedder
from app.core.embeddings.local_embedder import FastEmbedLocalEmbedder


def create_embedder() -> Embedder:
    return _create_embedder(
        settings.effective_embedding_provider(),
        settings.local_embedding_model,
        settings.fireworks_embedding_model,
        settings.embedding_dimension,
    )


@lru_cache(maxsize=8)
def _create_embedder(
    provider: str,
    local_model: str,
    fireworks_model: str,
    dimension: int,
) -> Embedder:
    if provider == "fireworks":
        from app.core.embeddings.fireworks_embedder import FireworksEmbedder

        return FireworksEmbedder(model=fireworks_model, dimension=dimension)
    return FastEmbedLocalEmbedder(model_name=local_model, dimension=dimension)
