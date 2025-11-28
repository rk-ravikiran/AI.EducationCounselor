import json
import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.services.embedding_client import EmbeddingClient
import numpy as np



class VectorStore:
    def __init__(self, cache_dir: Optional[str] = None):
        self.embedding_client = EmbeddingClient()
        self._items: List[Dict[str, Any]] = []
        self._embeddings: List[List[float]] = []
        
        # Cache directory setup
        if cache_dir is None:
            cache_dir = os.path.join(os.getcwd(), ".vector_cache")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def _compute_cache_key(self, programs: List[Dict[str, Any]]) -> str:
        """Generate cache key based on program data hash."""
        # Sort programs for consistent hashing
        sorted_programs = sorted(programs, key=lambda p: p.get('program', ''))
        data_str = json.dumps(sorted_programs, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get path to cache file for given key."""
        return self.cache_dir / f"vectors_{cache_key}.json"
    
    def _load_from_cache(self, cache_key: str) -> bool:
        """Load embeddings from cache if available. Returns True if successful."""
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            return False
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            self._items = cached_data['items']
            self._embeddings = cached_data['embeddings']
            
            pass
            
            return True
        except Exception:
            pass
            return False
    
    def _save_to_cache(self, cache_key: str):
        """Save embeddings to cache."""
        cache_path = self._get_cache_path(cache_key)
        
        try:
            cache_data = {
                'items': self._items,
                'embeddings': self._embeddings
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            
            pass
        except Exception:
            pass

    def add_programs(self, programs: List[Dict[str, Any]], use_cache: bool = True):
        """
        Add programs to vector store with optional caching.
        
        Args:
            programs: List of program dictionaries
            use_cache: If True, attempts to load from cache or save to cache
        """
        if not programs:
            return
        
        cache_key = self._compute_cache_key(programs)
        
        # Try loading from cache first
        if use_cache and self._load_from_cache(cache_key):
            return
        
        # Generate embeddings (cache miss or disabled)
        pass
        
        texts = [f"{p.get('program','')} {' '.join(p.get('keywords', []))}" for p in programs]
        embs = self.embedding_client.embed(texts)
        self._items.extend(programs)
        self._embeddings.extend(embs)
        
        # Save to cache
        if use_cache:
            self._save_to_cache(cache_key)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self._items:
            return []
        q_emb = self.embedding_client.embed([query])[0]
        scores = [self.embedding_client.cosine(q_emb, e) for e in self._embeddings]
        ranked = sorted(zip(self._items, scores), key=lambda x: -x[1])[:top_k]
        return [
            {"program": item, "score": round(score, 4), "query": query}
            for item, score in ranked
        ]
