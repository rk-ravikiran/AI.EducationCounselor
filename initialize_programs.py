"""
Script to load curated Singapore programs into vector store
Run this once to initialize the program database
"""
import json
import os
import sys

# Load environment for API keys
from dotenv import load_dotenv
load_dotenv()

from src.services.vector_store import VectorStore
from src.services.embedding_client import EmbeddingClient

def load_programs_to_vector_store():
    """Load curated programs into vector store with embeddings"""
    
    # Load programs from JSON
    try:
        with open('singapore_programs.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            programs_data = data['programs']
    except Exception as e:
        return False
    
    # Convert to format suitable for vector search
    searchable_programs = []
    for prog in programs_data:
        # Create rich text for embedding that captures all relevant info
        searchable_text = f"""
        Program: {prog['program_name']}
        Institution: {prog['institution']}
        Level: {prog['level']}
        Field: {prog['field']}
        Description: {prog['description']}
        Topics: {', '.join(prog['key_topics'])}
        Career Outcomes: {prog['career_outcomes']}
        Unique Features: {prog['unique_features']}
        Singapore Context: {prog['singapore_context']}
        """.strip()
        
        searchable_programs.append({
            'id': prog['id'],
            'program': prog['program_name'],
            'institution': prog['institution'],
            'level': prog['level'],
            'field': prog['field'],
            'keywords': prog['key_topics'],
            'searchable_text': searchable_text,
            'full_data': prog  # Store complete program data
        })
    
    vector_store = VectorStore(cache_dir=".vector_cache")
    try:
        # Add programs using their searchable text
        texts_for_embedding = [p['searchable_text'] for p in searchable_programs]
        embeddings = vector_store.embedding_client.embed(texts_for_embedding)
        
        # Store both items and embeddings
        vector_store._items = searchable_programs
        vector_store._embeddings = embeddings
    except Exception as e:
        return False
    try:
        cache_key = vector_store._compute_cache_key(searchable_programs)
        vector_store._save_to_cache(cache_key)
    except Exception as e:
        pass
    try:
        test_queries = [
            "artificial intelligence and machine learning programs",
            "finance and business programs",
            "cybersecurity diploma courses"
        ]
        
        for query in test_queries:
            results = vector_store.search(query, top_k=2)
    except Exception as e:
        pass
    
    return True

if __name__ == "__main__":
    success = load_programs_to_vector_store()
    sys.exit(0 if success else 1)
