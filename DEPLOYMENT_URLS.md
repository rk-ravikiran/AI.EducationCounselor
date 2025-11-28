# EduBuilder Deployment URLs

## Production Deployments

### Version 1.0 (Original)
- **URL**: https://edubuilder-demo-91147820269.us-central1.run.app
- **Service**: `edubuilder-demo`
- **Branch**: `version-1`
- **Features**:
  - 9 core agents (no web search)
  - Basic text input UI
  - Vector store for embeddings
  - Session management

### Version 2.0 (Latest) ⭐
- **URL**: https://edubuilder-v2-91147820269.us-central1.run.app
- **Service**: `edubuilder-v2`
- **Branch**: `version-2`
- **New Features**:
  - ✅ Web Search Agent (Google Custom Search API)
  - ✅ Interactive autocomplete UI
  - ✅ Multi-select dropdowns for interests/strengths
  - ✅ Tabbed results display
  - ✅ Real-time university course data
  - ✅ Enhanced UX with emojis and better formatting

## Git Branches

- `version-1`: Baseline (commit: a5e2100)
- `version-2`: Latest with web search + interactive UI (commit: 721777f)

## API Configuration

### Required for Version 2.0:
```env
GOOGLE_API_KEY=<your_gemini_api_key>
GOOGLE_CUSTOM_SEARCH_API_KEY=<your_search_api_key>
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=25644d89499424009
```

### Version 1.0 only needs:
```env
GOOGLE_API_KEY=<your_gemini_api_key>
```

## Testing

Both versions are publicly accessible and ready for demo.

### Test Web Search (Version 2.0 only):
1. Visit: https://edubuilder-v2-91147820269.us-central1.run.app
2. Select interests from dropdown (e.g., "Artificial Intelligence")
3. Click "Generate Guidance"
4. Check the "Web Search Results" tab for real-time university data

## Rollback Instructions

If Version 2.0 has issues, Version 1.0 remains available:
```bash
# Traffic is already split - no rollback needed
# Both versions run independently

# To delete Version 2.0 if needed:
gcloud run services delete edubuilder-v2 --region us-central1
```

## Cost Monitoring

- **Cloud Run**: Both services on free tier (first 2M requests/month free)
- **Google Custom Search**: 100 queries/day free (Version 2.0 only)
- **Gemini API**: Free tier applies to both

## For Google AI Hackathon

**Demo URL**: https://edubuilder-v2-91147820269.us-central1.run.app

**Key Features to Highlight**:
1. Multi-agent orchestration (10 specialized agents)
2. Real-time web search integration
3. Interactive, user-friendly UI
4. Singapore education system expertise
5. Vector embeddings for institutional data
6. Session management for multi-turn conversations
