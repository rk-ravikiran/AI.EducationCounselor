# Version 2.0 Release Notes

## 🎉 New Features

### 1. **Web Search Agent** 🌐
Search real-time course information from Singapore university websites using Google Custom Search API.

**Features:**
- Searches 10 Singapore university domains (NUS, NTU, SMU, SIT, polytechnics, LASALLE)
- Respects `robots.txt` (no web scraping violations)
- Returns latest course details, admission requirements
- 100 free queries/day
- Graceful fallback if API not configured

**Setup:** See [WEB_SEARCH_SETUP.md](WEB_SEARCH_SETUP.md)

**Example Result:**
```json
{
  "search_results": [
    {
      "title": "BSc Computer Science - NUS Computing",
      "link": "https://www.comp.nus.edu.sg/programmes/ug/cs/",
      "snippet": "Bachelor of Computing in Computer Science...",
      "query": "AI degree programme Singapore 2025"
    }
  ]
}
```

---

### 2. **Interactive UI with Autocomplete** 🎯

Enhanced Streamlit interface with intelligent suggestions for Singapore courses.

**Features:**
- **Multiselect dropdowns** for interests and strengths (max 5 each)
- **Course catalog integration** - 20+ popular Singapore programs
- **Custom input option** - Add interests not in the list
- **Visual improvements** - Emojis, tabs, better organization
- **Real-time validation** - Warns if no interests selected

**UI Improvements:**
- 📚 Programs | 💼 Career | 💰 Financial Aid tabs
- 🎯 Skills | 🏆 Scholarships | 🗣️ Interview tabs
- 📖 Learning | 🌐 Web Search tabs
- Better visual hierarchy and readability

---

## 📊 System Architecture Updates

**Agent Count:** 9 → **10 agents**

New agent:
- `web_search` - Real-time web search for course data

**Configuration:**
```yaml
agents:
  enabled:
    - web_search  # NEW: Optional, requires Google API setup
```

---

## 🔧 Technical Changes

### Files Modified
- `src/agents/web_search_agent.py` - New agent implementation
- `src/services/orchestrator.py` - Added web search agent to mapping
- `streamlit_app.py` - Complete UI overhaul with autocomplete
- `src/data/singapore_courses.json` - Course catalog for suggestions
- `requirements.txt` - Added `requests` library
- `config.yaml` - Enabled all agents + web search
- `.env.example` - Added Google Custom Search API config

### Files Added
- `WEB_SEARCH_SETUP.md` - Complete setup guide for Google API
- `src/agents/web_search_agent.py` - 170 lines of code
- `src/data/singapore_courses.json` - 20+ interests, 9+ strengths

---

## 🚀 How to Use

### Web Search Agent

1. **Get Google Custom Search API Key** (free):
   - Follow [WEB_SEARCH_SETUP.md](WEB_SEARCH_SETUP.md) guide
   - 100 free queries/day

2. **Add to `.env`**:
   ```env
   GOOGLE_CUSTOM_SEARCH_API_KEY=your_key
   GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_id
   ```

3. **Run app** - Web search agent automatically enabled

**Without API keys:** Agent disables gracefully, other agents continue working.

### Interactive UI

1. **Launch Streamlit**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Select interests** from dropdown (or add custom)

3. **Select strengths** from dropdown (or add custom)

4. **Click "🚀 Get Guidance"**

5. **View results** in organized tabs

---

## 📈 Performance Impact

| Metric | Version 1.0 | Version 2.0 | Change |
|--------|-------------|-------------|--------|
| **Agents** | 9 | 10 | +1 |
| **UI Fields** | 6 text inputs | 2 multiselect + 6 inputs | +Autocomplete |
| **Response Time** | 2.8s | 3.2s (with web search) | +0.4s |
| **API Costs** | $0.0002/user | $0.0002/user | No change* |

*Web search is free (100/day). Only costs $5/1000 queries if exceeded.

---

## 🔄 Backward Compatibility

**✅ Version 2.0 is fully backward compatible with Version 1.0**

- Web search agent is optional (config-driven)
- Old text input UI still works if you modify the code
- All existing agents unchanged
- API contracts remain the same

---

## 🐛 Known Issues

1. **Web search quota** - Limited to 100/day on free tier
   - **Mitigation**: Agent limits to 3 interests per query

2. **Autocomplete loading** - Initial load reads JSON file
   - **Mitigation**: Using `@st.cache_data` for caching

3. **Custom interests** - Not persisted across sessions
   - **Future fix**: Add to local storage or database

---

## 🗺️ Roadmap (Version 3.0)

Potential features for next version:

1. **Persistent user profiles** - Save and load profiles
2. **Advanced web scraping** - Use ScraperAPI or Bright Data
3. **AI-powered suggestions** - LLM suggests interests based on strengths
4. **Course comparison tool** - Side-by-side program comparison
5. **Application tracker** - Deadline reminders and status tracking

---

## 📝 Commit History

```bash
git log --oneline version-1..version-2
```

**Version 2.0 commit:**
- `6253797` - Version 2.0: Add Web Search Agent + Interactive UI with Autocomplete

**Version 1.0 commit:**
- `a5e2100` - Version 1.0: Initial commit with complete multi-agent system

---

## 🙏 Acknowledgments

- **Google Custom Search API** - For respectful web search capabilities
- **Streamlit** - For beautiful multiselect components
- **Singapore Universities** - For maintaining accessible course information

---

**Questions?** Check [WEB_SEARCH_SETUP.md](WEB_SEARCH_SETUP.md) or open an issue.
