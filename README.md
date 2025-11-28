# Singapore Education Counselor – Multi-Agent Google AI Hackathon Project

This project implements a modular, multi-agent architecture to provide career and education guidance for students exploring Singapore institutions. It leverages Google AI (Gemini), and is structured for rapid iteration during a hackathon.

## 🌐 Live Demo
**Public URL:** https://edubuilder-demo-91147820269.us-central1.run.app

## Core Goals

1. Aggregate institutional program data (placeholder JSON now; can extend via APIs/web scraping).
2. Provide career pathway suggestions based on interests/strengths.
3. Surface financial aid options and application planning timelines.
4. Summarize multi-agent output into concise actionable guidance using an LLM.

## Architecture Overview

```
StudentProfile → Orchestrator → [9 Specialized Agents] → Aggregated Results → LLM Summary (via structured prompts)
```

### Key Components

| Component | Purpose |
|-----------|---------|
| `src/models/profile.py` | Pydantic model for student profile input |
| `src/agents/*` | 9 domain agents (institutional, career, financial, admission, skill gap, scholarship, interview, learning path, multilang) |
| `src/services/orchestrator.py` | Coordinates agent execution and LLM summarization |
| `src/services/genai_client.py` | Unified client for Vertex AI + Gemini API with fallbacks |
| `src/services/prompt_loader.py` | Loads and formats structured prompt templates |
| `src/services/vector_store.py` | In-memory vector similarity search for program matching |
| `src/services/embedding_client.py` | Text embedding via Vertex AI (text-embedding-004) |
| `prompts/*` | Structured LLM prompt templates with Singapore context |
| `config.yaml` | Project configuration (models, agents, settings) |
| `main.py` | Enriched program catalog with 12+ Singapore institutions |

### Agent Suite

**Core Agents:**
- **InstitutionalDataAgent**: Vector similarity search across program catalog
- **CareerGuidanceAgent**: Career pathway mapping based on interests
- **FinancialAidAgent**: Budget-based financial aid recommendations
- **AdmissionAdvisorAgent**: Singapore-specific application timelines & requirements

**Phase 1 Extensions (Singapore-focused):**
- **SkillGapAgent**: Identifies skill gaps with NUS/NTU/SkillsFuture resources
- **ScholarshipMatcherAgent**: MOE, ASEAN, NUS scholarships with eligibility scoring
- **InterviewPrepAgent**: Mock questions with Smart Nation & MAS context
- **LearningPathAgent**: Prerequisite-based learning sequences
- **MultiLangAgent**: Translation support (Mandarin, Tamil, Malay)

## Setup

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Configure Environment Variables

**Option A: Using .env file (Recommended)**

1. Copy the example file:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` with your credentials:
   ```env
   GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service_account.json
   GOOGLE_PROJECT_ID=your-project-id
   GOOGLE_API_KEY=your_api_key_here  # Optional fallback
   ```

3. Load environment variables:
   ```powershell
   .\load_env.ps1
   ```

**Option B: Set manually in PowerShell**

```powershell
# Service Account (Vertex AI) - Primary method
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\service_account.json"
$env:GOOGLE_PROJECT_ID="your-project-id"
$env:GOOGLE_LOCATION="us-central1"

# Gemini API Key (fallback)
$env:GOOGLE_API_KEY="your_api_key_here"

# Model override
$env:MODEL_NAME="gemini-2.5-flash-lite"

# Enable debug logging
$env:LLM_DEBUG="1"
```

### 3. Verify Setup

```powershell
# Check authentication
python -c "import os; print('✓ Service account:', os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))"

# Test connectivity
python main.py
```

### Authentication Methods

The system uses **two-tier authentication** with automatic fallback:

1. **Primary: Service Account (Vertex AI)**
   - Requires: `GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_PROJECT_ID`
   - Best for: Production, server deployments, hackathon demos
   - Get it: [Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts) → Create Service Account → Download JSON key

2. **Fallback: Gemini API Key**
   - Requires: `GOOGLE_API_KEY`
   - Best for: Quick testing, local development
   - Get it: [Google AI Studio](https://aistudio.google.com/app/apikey)

## Running the Demo

```powershell
python main.py
```

Interactive mode (build profile via prompts):
```powershell
python main.py --interactive
```

Disable LLM summary (for offline runs):
```powershell
python main.py --no-summary
```

Save profile after run:
```powershell
python main.py --save-profile my_profile.json
```

Load and refine:
```powershell
python main.py --load-profile my_profile.json --refine "add ai and low budget"
```

Launch Streamlit UI:
```powershell
streamlit run streamlit_app.py
```

You will see each agent's structured output plus a summary (if LLM available). If the summary returns the fallback text, ensure credentials/API key are set.

## Customization

### Agent Configuration
- Enable/disable agents via `config.yaml` under `agents.enabled`
- All 9 agents enabled by default for comprehensive counseling

### Prompt Engineering
- **Structured Prompts**: All LLM interactions use templates from `prompts/` directory
- **Orchestrator Summary**: Edit `prompts/orchestrator_summary.txt` for customized guidance format
- **Translation**: Modify `prompts/translation.txt` for language-specific adaptations
- **Adding Prompts**: Create new `.txt` files in `prompts/` and use `load_prompt("template_name", var=value)`
- See `prompts/README.md` for detailed documentation

### Data & Settings
- **Program Catalog**: 12+ Singapore programs in `main.py` (NUS, NTU, SMU, polytechnics, etc.)
- **Scholarships**: MOE, ASEAN, NUS scholarships in `src/agents/scholarship_matcher_agent.py`
- **Skill Matrix**: AI/Finance/Design/Robotics domains in `src/agents/skill_gap_agent.py`
- **Vector Store**: Enabled by default for semantic program matching
- **Cache**: 120s TTL for profile results (configurable in `config.yaml`)

### Profile Management
- Save profiles: `--save-profile profile.json`
- Load profiles: `--load-profile profile.json`
- Refine profiles: `--refine "add ai interest and low budget"`
- Session history maintained across refinements

### UI Options
- **CLI**: `python main.py` (default, quick testing)
- **Interactive**: `python main.py --interactive` (guided questionnaire)
- **Streamlit**: `streamlit run streamlit_app.py` (web UI demo)

## Singapore Localization Features

All agents are customized for Singapore education context:

- **Academic Calendar**: Aug-Sep intake, Mar-Apr deadlines
- **Institutions**: NUS, NTU, SMU, SUTD, SIT, SUSS, polytechnics
- **Government Initiatives**: MOE, SkillsFuture, Smart Nation, MAS FinTech
- **Scholarships**: MOE Tuition Grant, ASEAN, NUS Global Merit, SkillsFuture
- **Interview Topics**: Smart Nation projects, MAS regulations, multicultural UX
- **Learning Resources**: NTU/NUS tracks, SkillsFuture courses, local certifications

## Hackathon Differentiation

**Implemented High-Impact Features:**
✅ 9-agent orchestration with specialized domains  
✅ Vector similarity search for intelligent program matching  
✅ Singapore-specific localization (scholarships, timelines, institutions)  
✅ Structured prompt engineering with separate template files  
✅ Comprehensive evaluation metrics (CSV export)  
✅ Caching & session management for performance  
✅ Multi-language support (translation agent)  
✅ Interactive architecture diagrams (Mermaid)  

**Potential Extensions:**
- Real-time web scraping from university portals
- Persistent vector store (ChromaDB, Pinecone)
- Cost/latency logging and analytics
- Dockerization for cloud deployment

## Testing

Run unit tests:
```powershell
pytest -q
```

## Folder Structure

```
EduBuilder/
├── prompts/                        # Structured LLM prompt templates
│   ├── README.md                   # Prompt documentation
│   ├── orchestrator_summary.txt    # Main counseling summary prompt
│   └── translation.txt             # Multi-language translation prompt
├── src/
│   ├── agents/                     # 9 specialized agents
│   │   ├── base.py
│   │   ├── institutional_data_agent.py
│   │   ├── career_guidance_agent.py
│   │   ├── financial_aid_agent.py
│   │   ├── admission_advisor_agent.py
│   │   ├── skill_gap_agent.py
│   │   ├── scholarship_matcher_agent.py
│   │   ├── interview_prep_agent.py
│   │   ├── learning_path_agent.py
│   │   └── multilang_agent.py
│   ├── services/                   # Core services
│   │   ├── orchestrator.py         # Agent coordination
│   │   ├── genai_client.py         # LLM client (Vertex + Gemini)
│   │   ├── embedding_client.py     # Text embeddings
│   │   ├── vector_store.py         # Similarity search
│   │   ├── session_manager.py      # Session tracking
│   │   └── prompt_loader.py        # Prompt template loader
│   ├── models/
│   │   └── profile.py              # StudentProfile Pydantic model
│   └── data/                       # Legacy (data now in main.py)
├── tests/                          # Unit tests (12 tests)
│   ├── test_phase1_agents.py
│   ├── test_orchestrator.py
│   └── test_new_features.py
├── exports/                        # Generated summaries & evaluations
├── main.py                         # CLI entry point (enriched program data)
├── streamlit_app.py                # Streamlit web UI
├── evaluation.py                   # Batch evaluation script
├── config.yaml                     # Configuration
├── requirements.txt                # Python dependencies
├── ARCHITECTURE.md                 # Interactive architecture diagrams
└── README.md                       # This file
```

## Hackathon Pitch Points

1. Personalized, multi-perspective guidance (academic, financial, admissions).
2. Modular agents allow fast feature expansion.
3. AI summarization converts raw structured outputs into actionable narrative.
4. Clear path to real data integration and scalability (BigQuery, Storage, vector DB).

## Next Steps (Suggested)
| Priority | Enhancement |
|----------|-------------|
| High | Real institutional API/data ingestion |
| High | Advanced semantic reranking (hybrid keyword + vector) |
| Medium | BigQuery persistent program and profile storage |
| Medium | Conversation-based iterative planning (LLM chat) |
| Low | Deployment (Cloud Run / App Engine) |

---
Feel free to request any of the enhancements and they can be scaffolded quickly.
