"""
Fast startup script that uses cached embeddings and skips heavy initialization.
Use this for quick demos and testing.
"""
import os

# Performance optimizations
os.environ["DISABLE_VERTEX_EMBED"] = "1"  # Use fast hash-based embeddings
os.environ["LLM_DEBUG"] = "0"  # Reduce logging overhead

# Run main
from main import main
if __name__ == "__main__":
    main()
