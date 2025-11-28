"""
Direct Google Custom Search API test to diagnose the issue
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")

pass
pass
pass
pass
pass
pass

# Test 1: Simple query
query = "Computer Science NUS"
url = "https://www.googleapis.com/customsearch/v1"
params = {
    "key": api_key,
    "cx": search_engine_id,
    "q": query,
    "num": 5
}

pass
pass
pass
pass

try:
    response = requests.get(url, params=params, timeout=10)
    pass
    pass
    
    if response.status_code == 200:
        data = response.json()
        
        pass
        pass
        pass
        pass
        
        items = data.get("items", [])
        if items:
            pass
            pass
            for i, item in enumerate(items[:3], 1):
                pass
                pass
                pass
                pass
        else:
            pass
            pass
            pass
            pass
            pass
            pass
            
    else:
        pass
        pass
        
except Exception as e:
    pass
    import traceback
    traceback.print_exc()

pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
