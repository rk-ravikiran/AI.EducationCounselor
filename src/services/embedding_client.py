from typing import List, Optional
import hashlib, os

try:
    from vertexai.preview.language_models import TextEmbeddingModel  # type: ignore
    _VERTEX_AVAILABLE = True
except Exception:
    _VERTEX_AVAILABLE = False

import numpy as np

class EmbeddingClient:
    def __init__(self, model_name: str = "text-embedding-004"):
        self.model_name = model_name
        self._model = None
        # Allow tests or constrained environments to disable Vertex embeddings
        if _VERTEX_AVAILABLE and not self._env_disabled():
            try:
                self._model = TextEmbeddingModel.from_pretrained(model_name)
            except Exception:
                self._model = None

    def embed(self, texts: List[str]) -> List[List[float]]:
        if self._model:
            try:
                embeddings = self._model.get_embeddings(texts)
                return [e.values for e in embeddings]
            except Exception:
                pass
        # Fallback: deterministic hash-based pseudo-embedding (not semantic, for offline demo)
        return [self._fallback_embed(t) for t in texts]

    def _fallback_embed(self, text: str) -> List[float]:
        h = hashlib.sha256(text.encode("utf-8")).digest()
        arr = np.frombuffer(h, dtype=np.uint8)[:32] / 255.0
        return arr.tolist()

    @staticmethod
    def cosine(a: List[float], b: List[float]) -> float:
        va, vb = np.array(a), np.array(b)
        if va.size == 0 or vb.size == 0:
            return 0.0
        # Guard against dimension mismatch between fallback and vertex embeddings
        if va.shape != vb.shape:
            return 0.0
        denom = np.linalg.norm(va) * np.linalg.norm(vb)
        if denom == 0:
            return 0.0
        return float(np.dot(va, vb) / denom)

    @staticmethod
    def _env_disabled() -> bool:
        val = os.getenv("DISABLE_VERTEX_EMBED", "0").lower()
        return val in ("1", "true", "yes")
