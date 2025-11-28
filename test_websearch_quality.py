import os
import requests
import json

# Use environment variables for credentials to avoid committing secrets
GOOGLE_CUSTOM_SEARCH_API_KEY = os.environ.get('GOOGLE_CUSTOM_SEARCH_API_KEY')
GOOGLE_CUSTOM_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_CUSTOM_SEARCH_ENGINE_ID')

if not GOOGLE_CUSTOM_SEARCH_API_KEY or not GOOGLE_CUSTOM_SEARCH_ENGINE_ID:
    raise RuntimeError(
        'Please configure GOOGLE_CUSTOM_SEARCH_API_KEY and GOOGLE_CUSTOM_SEARCH_ENGINE_ID as environment variables before running this test.'
    )

# Test what Google Custom Search returns
r = requests.get('https://www.googleapis.com/customsearch/v1', params={
    'key': GOOGLE_CUSTOM_SEARCH_API_KEY,
    'cx': GOOGLE_CUSTOM_SEARCH_ENGINE_ID,
    'q': 'computer science bachelor degree Singapore university 2025',
    'num': 5
})

results = r.json().get('items', [])
