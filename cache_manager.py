"""
Vector store cache management utility.
Usage: python cache_manager.py [clear|info|validate]
"""
import argparse
import json
import os
from pathlib import Path

CACHE_DIR = Path(".vector_cache")

def get_cache_files():
    """Get all cache files."""
    if not CACHE_DIR.exists():
        return []
    return list(CACHE_DIR.glob("vectors_*.json"))

def cache_info():
    """Display cache information."""
    cache_files = get_cache_files()
    
    if not cache_files:
        return
    
    total_size = 0
    for cache_file in cache_files:
        size = cache_file.stat().st_size
        total_size += size
        
        # Load and inspect cache
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                json.load(f)
        except Exception:
            pass
    
    pass

def clear_cache():
    """Clear all cache files."""
    cache_files = get_cache_files()
    
    if not cache_files:
        return

    for cache_file in cache_files:
        try:
            cache_file.unlink()
        except Exception as e:
            pass
    
    pass

def validate_cache():
    """Validate cache files for corruption."""
    cache_files = get_cache_files()
    
    if not cache_files:
        return

    valid_count = 0
    invalid_count = 0
    
    for cache_file in cache_files:
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate structure
            if not isinstance(data, dict):
                raise ValueError("Invalid cache structure")
            
            if 'items' not in data or 'embeddings' not in data:
                raise ValueError("Missing required keys")
            
            if len(data['items']) != len(data['embeddings']):
                raise ValueError("Items and embeddings length mismatch")
            
            valid_count += 1
        except Exception:
            invalid_count += 1
    
    pass

def main():
    parser = argparse.ArgumentParser(description="Vector store cache management")
    parser.add_argument(
        'command',
        choices=['info', 'clear', 'validate'],
        nargs='?',
        default='info',
        help='Command to execute (default: info)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'info':
        cache_info()
    elif args.command == 'clear':
        clear_cache()
    elif args.command == 'validate':
        validate_cache()

if __name__ == "__main__":
    main()
