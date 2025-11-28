# Google Custom Search API Setup Guide

The Web Search Agent uses Google's Custom Search JSON API to search Singapore university websites for real-time course information.

## Why Google Custom Search?

- ✅ **Respects robots.txt** - No scraping violations
- ✅ **Free tier** - 100 queries/day
- ✅ **Official API** - Reliable and fast
- ✅ **Targeted search** - Can restrict to specific domains

## Setup Steps

### 1. Get Google Custom Search API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services > Credentials**
3. Click **Create Credentials > API Key**
4. Copy the API key
5. (Optional) Restrict the key to "Custom Search API" for security

### 2. Create Custom Search Engine

1. Visit [Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/create)
2. Configure your search engine:
   - **Search engine name**: "Singapore Universities"
   - **What to search**: "Search specific sites"
   - **Sites to search** (add these one by one):
     ```
     nus.edu.sg
     ntu.edu.sg
     smu.edu.sg
     sit.singaporetech.edu.sg
     sp.edu.sg
     np.edu.sg
     tp.edu.sg
     rp.edu.sg
     nyp.edu.sg
     lasalle.edu.sg
     ```
3. Click **Create**
4. On the next page, copy your **Search Engine ID** (starts with a long alphanumeric string)

### 3. Enable Custom Search API

1. In [Google Cloud Console](https://console.cloud.google.com/)
2. Go to **APIs & Services > Library**
3. Search for "Custom Search API"
4. Click **Enable**

### 4. Configure Environment Variables

Add to your `.env` file:

```env
# Web Search Configuration
GOOGLE_CUSTOM_SEARCH_API_KEY=your_api_key_here
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id_here
```

### 5. Test the Agent

Run in Python:

```python
import os
os.environ["GOOGLE_CUSTOM_SEARCH_API_KEY"] = "your_key"
os.environ["GOOGLE_CUSTOM_SEARCH_ENGINE_ID"] = "your_id"

from src.agents.web_search_agent import WebSearchAgent
from src.agents.base import AgentContext

context = AgentContext(config={}, data_store={}, vector_store=None, genai_client=None)
agent = WebSearchAgent(context)

profile = {
    "interests": ["Artificial Intelligence"],
    "target_level": "degree"
}

result = agent.run(profile)
print(result)
```

## Quota Management

**Free Tier**: 100 queries/day

**Cost** (if you exceed):
- $5 per 1,000 queries
- First 100/day remain free

**Optimization**:
- Agent limits to 3 interests per profile (max 3 queries)
- Each query fetches 5 results
- Results are deduplicated

**Monthly cost** for 500 users:
- 500 users × 3 queries = 1,500 queries
- First 3,000 queries free (100/day × 30 days)
- **Total cost**: $0

## API Response Example

```json
{
  "agent": "web_search",
  "search_results": [
    {
      "title": "BSc Computer Science - NUS Computing",
      "link": "https://www.comp.nus.edu.sg/programmes/ug/cs/",
      "snippet": "The Bachelor of Computing in Computer Science...",
      "display_link": "www.comp.nus.edu.sg",
      "query": "Artificial Intelligence bachelor degree programme Singapore university 2025"
    }
  ],
  "queries_used": 3,
  "total_results_found": 12
}
```

## Alternative: Disable Web Search

If you don't want to set up Google Custom Search, the agent gracefully disables itself:

1. Don't set the environment variables
2. Agent will return:
   ```json
   {
     "agent": "web_search",
     "enabled": false,
     "message": "Web search disabled. Set API keys to enable."
   }
   ```

3. Other agents continue to work normally

## Troubleshooting

**"API key not valid"**
- Verify you enabled "Custom Search API" in Google Cloud Console
- Check that your API key is correct in `.env`

**"Invalid Value for cx parameter"**
- Your Search Engine ID is incorrect
- Get it from [Programmable Search Engine Control Panel](https://programmablesearchengine.google.com/controlpanel/all)

**"Quota exceeded"**
- You've used 100 free queries today
- Either wait until tomorrow or enable billing ($5/1000 queries)

## Best Practices

1. **Cache results** - Store search results temporarily to avoid repeat queries
2. **Limit queries** - Agent already limits to 3 interests per user
3. **Monitor quota** - Check usage in Google Cloud Console
4. **Set up billing alerts** - Get notified at $1, $5, $10 thresholds

---

**Need Help?**
- [Custom Search JSON API Documentation](https://developers.google.com/custom-search/v1/overview)
- [Pricing Details](https://developers.google.com/custom-search/v1/overview#pricing)
