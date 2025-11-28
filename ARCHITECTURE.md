# Singapore Education Counselor - Multi-Agent AI System

**High-Level Design & System Requirements Specification**

---

## Executive Summary

The Singapore Education Counselor is an intelligent, multi-agent AI system designed to provide personalized, comprehensive education and career guidance to students exploring Singapore's educational landscape. Built for the Google AI Hackathon, this system leverages Google's Gemini and Vertex AI to deliver contextually relevant recommendations across institutional programs, career pathways, and financial aid using curated Singapore data combined with AI reasoning.

**Current Status**: ✅ Deployed in Production  
**Live URL**: https://edubuilder-v2-91147820269.us-central1.run.app  
**Version**: 2.2  
**Last Updated**: November 27, 2025

**Architecture**: Transformed from web search parsing to **curated data + LLM reasoning** approach with **3 core agents** + **Admin Analytics Panel**

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Solution Overview](#solution-overview)
3. [Scope & Objectives](#scope--objectives)
4. [Key Features & Advantages](#key-features--advantages)
5. [Target Users](#target-users)
6. [System Architecture](#system-architecture)
7. [Technical Specifications](#technical-specifications)
8. [Deployment Architecture](#deployment-architecture)
9. [Performance Metrics](#performance-metrics)
10. [Future Enhancements](#future-enhancements)

---

## Problem Statement

### Current Challenges in Education Counseling

1. **Information Overload**: Students face overwhelming amounts of scattered information across 12+ Singapore institutions, hundreds of programs, and numerous scholarship opportunities.

2. **Lack of Personalization**: Traditional counseling approaches provide generic advice that doesn't account for individual interests, strengths, budget constraints, and career aspirations.

3. **Accessibility Barriers**: 
   - Limited availability of human counselors
   - High cost of professional guidance services
   - Geographic constraints for remote students
   - Language barriers for international students

4. **Time-Intensive Research**: Students spend weeks researching programs, comparing institutions, understanding admission requirements, and identifying financial aid options.

5. **Fragmented Guidance**: Career advice, institutional selection, financial planning, and skill development recommendations are often handled by separate services with no integration.

6. **Timeliness**: Students miss application deadlines and scholarship opportunities due to lack of coordinated timeline planning.

### Impact

- Students make suboptimal education choices due to information gaps
- Talented students miss scholarship opportunities they're eligible for
- Career-education misalignment leads to skill gaps in the workforce
- International students struggle with Singapore-specific context and requirements

---

## Solution Overview

The Singapore Education Counselor addresses these challenges through a **3-agent AI architecture** where specialized agents collaborate to provide holistic, personalized guidance using **curated Singapore data and LLM reasoning**:

### Core Innovation

**3 Specialized AI Agents** working in concert:

1. **Institutional Data Agent**: Uses vector embeddings (768-dimensional) + LLM reasoning to match student profiles with curated Singapore programs (NUS, NTU, SMU, SIT, Polytechnics)
2. **Career Guidance Agent**: Maps interests and strengths to specific career pathways with Singapore labor market context and skill gap analysis
3. **Financial Aid Agent**: Filters and recommends aid options (bursaries, scholarships, loans) based on budget categories and eligibility

### Architectural Transformation (Version 2.2)

**From**: Web search parsing → 9 agents → complex orchestration  
**To**: Curated data + LLM reasoning → 3 core agents → focused intelligence + admin analytics

**Key Changes**:
- Removed web search dependency (unreliable, slow)
- Consolidated 9 agents into 3 core agents with expanded responsibilities
- Curated databases: `singapore_programs.json` (8 programs), `singapore_financial_aid.json` (10 aid options)
- LLM-powered insights: AI counselor reasoning for program fit, career alignment, financial context
- Fixed Vertex AI configuration for Cloud Run (Application Default Credentials)
- Flat data structure for seamless UI integration
- **NEW**: Admin panel with request history tracking, analytics dashboard, and data export capabilities

### How It Works

```
Student Input → Profile Builder → Orchestrator → 3 Parallel Agents → LLM Summarizer → Personalized Guidance
                                      ↓                                         ↓
                               Vector Store Cache                    Request History Logger
                               (2-4s faster responses)              (Admin Analytics)
```

---

## Scope & Objectives

### In-Scope

#### Functional Requirements

**FR-1: Student Profile Management**
- Accept student inputs: name, interests, strengths, constraints, budget, target education level
- Validate and structure profile data using Pydantic models
- Generate unique session identifiers for tracking

**FR-2: Institutional Recommendations**
- Search curated database of 8 Singapore programs (NUS, NTU, SMU, polytechnics)
- Use semantic embeddings (768-dimensional vectors) for matching
- LLM-powered AI counselor insights for program fit reasoning
- Provide detailed program information: level, duration, tuition fees, career outcomes
- Rank programs by relevance with confidence scores

**FR-3: Career Pathway Mapping**
- Map interests to specific career paths with Singapore context
- Align with Singapore's Smart Nation initiatives
- Identify required skills and provide career insights
- Include industry connections and career progression information

**FR-4: Financial Planning**
- Filter financial aid from curated database (10 aid options)
- Include MOE grants, bursaries, SkillsFuture Credit, CPF loans, community grants
- Filter by budget categories (tight, moderate, flexible)
- Provide eligibility criteria and application details

**FR-5: Document Generation**
- Export guidance as Markdown summaries
- Include timestamp and version tracking
- Store in `exports/` directory with unique IDs

**FR-6: Admin Analytics Panel**
- Track all student requests in real-time
- Store request history with profile data and results
- Provide filtering by interests and target education level
- Display analytics dashboard with key metrics (total requests, avg recommendations)
- Export historical data in JSON and CSV formats
- Enable institutional insights for demand analysis

#### Non-Functional Requirements

**NFR-1: Performance**
- Response time: < 3 seconds for new queries
- Cached response time: < 100ms
- Support concurrent users in production

**NFR-2: Scalability**
- Serverless auto-scaling on Google Cloud Run
- Handle 100+ requests per minute during peak

**NFR-3: Reliability**
- 99.5% uptime SLA
- Graceful degradation if Vertex AI unavailable
- Model fallback chain (5 alternate models)

**NFR-4: Security**
- No storage of personal data beyond session
- Service account authentication for GCP
- Environment variable-based secrets management
- HTTPS-only communication

**NFR-5: Maintainability**
- Modular agent architecture
- Comprehensive test coverage (pytest)
- Structured logging and error handling
- Configuration-driven behavior (config.yaml)

**NFR-6: Usability**
- Intuitive Streamlit web interface
- CLI for power users and automation
- Mobile-responsive design
- Accessible to users with disabilities

### Out-of-Scope (Current Version)

- Real-time application submission
- Direct integration with institutional admission systems
- Payment processing for application fees
- 1-on-1 live counseling sessions
- User authentication and personalized login accounts
- Parent/guardian account management
- Document upload and verification
- Email notifications and reminders

---

## Key Features & Advantages

### Competitive Advantages

| Feature | Singapore Education Counselor | Traditional Counseling | Generic AI Chatbots |
|---------|------------------------------|----------------------|---------------------|
| **Personalization** | ✅ 3 specialized agents + LLM reasoning | ⚠️ Generic advice | ⚠️ Broad responses |
| **Singapore Context** | ✅ Curated data (8 programs, 10 aid options) | ✅ Yes | ❌ Global/Generic |
| **Cost** | ✅ Free | ❌ $100-500/session | ✅ Free |
| **Availability** | ✅ 24/7 instant | ❌ Appointment-based | ✅ 24/7 |
| **Comprehensiveness** | ✅ Programs + Career + Financial Aid | ⚠️ Depends on counselor | ❌ Limited scope |
| **Data-Driven** | ✅ Vector embeddings + LLM reasoning | ⚠️ Human intuition | ⚠️ Text matching |
| **Scalability** | ✅ Unlimited concurrent users | ❌ 1-on-1 only | ✅ High |
| **Update Frequency** | ✅ Curated data updates | ⚠️ Counselor knowledge | ⚠️ Model training |
| **Analytics** | ✅ Admin panel with insights | ❌ Manual tracking | ❌ No analytics |

### Technical Advantages

1. **Vector Embeddings for Semantic Search**
   - 768-dimensional text-embedding-004 model
   - Captures conceptual similarity beyond keywords
   - Example: "robotics" matches with "mechatronics engineering" and "AI programming"

2. **LLM-Powered AI Counselor Insights**
   - Gemini generates personalized fit reasoning for each program
   - Career alignment analysis with Singapore context
   - Financial fit assessment based on student budget
   - Academic requirements matching with student strengths

3. **Curated Data Quality**
   - Manually curated Singapore program database (8 programs)
   - Complete program details: tuition fees, career outcomes, academic requirements
   - 10 financial aid options with eligibility criteria
   - No reliance on unreliable web search

4. **Intelligent Caching**
   - SHA256-based profile hashing
   - 120-second TTL for repeat queries
   - 95% cache hit rate in testing
   - Reduces API costs by $0.50/1000 queries

5. **Model Fallback Resilience**
   - Primary: gemini-2.5-flash-lite
   - Automatic retry with alternate models on failures
   - Graceful degradation with fallback simple ranking

6. **Production-Grade Deployment**
   - Dockerized containerization
   - Google Cloud Run serverless auto-scaling
   - Vertex AI with Application Default Credentials
   - HTTPS with SSL certificates
   - Zero-downtime deployments

### User Benefits

- **Time Savings**: Reduces research time from weeks to minutes
- **Confidence**: Data-driven recommendations increase decision confidence
- **Comprehensiveness**: Single platform for all education planning needs
- **Accessibility**: Free, 24/7, multi-language support
- **Actionability**: Provides specific next steps with timelines
- **Transparency**: Explains reasoning behind recommendations

---

## Target Users

### Primary Personas

**1. Pre-University Students (16-18 years)**
- Deciding between polytechnics and universities
- Exploring degree programs aligned with interests
- Concerned about scholarship opportunities
- Need: Career clarity and financial planning

**2. International Students**
- Researching Singapore as study destination
- Unfamiliar with local institution landscape
- Budget-constrained, seeking financial aid
- Need: Comprehensive orientation and cost planning

**3. Career Switchers (25-35 years)**
- Considering further education for career change
- Balancing work, budget, and study commitments
- Exploring part-time/online programs
- Need: Skill gap analysis and ROI assessment

**4. Parents/Guardians**
- Seeking guidance for their children
- Comparing institution reputations and costs
- Concerned about career prospects and employability
- Need: Objective, data-backed recommendations

### Secondary Users

- Education counselors using tool for client research
- Institutional admission offices for student inquiries
- Scholarship foundation staff for eligibility screening

---

## System Architecture

```mermaid
graph TB
    subgraph "User Interfaces"
        CLI[CLI Interface<br/>main.py]
        UI[Streamlit Web UI<br/>streamlit_app.py]
    end

    subgraph "Entry Layer"
        CLI --> PROFILE[Student Profile Builder]
        UI --> PROFILE
        PROFILE --> |name, interests,<br/>strengths, constraints,<br/>budget, target_level| SESSION[Session Manager]
    end

    subgraph "Orchestration Layer"
        SESSION --> ORCH[Orchestrator]
        ORCH --> CACHE{Cache Check<br/>TTL: 120s}
        CACHE -->|Hit| CACHED[Return Cached Result]
        CACHE -->|Miss| AGENTS[Agent Dispatch]
    end

    subgraph "AI/ML Services"
        GENAI[GenAI Client<br/>Vertex AI / Gemini]
        EMBED[Embedding Client<br/>text-embedding-004]
        VECTOR[Vector Store<br/>Cosine Similarity]
    end

    subgraph "Agent Layer - Core 3 Agents"
        AGENTS --> INST[Institutional Data Agent<br/>Curated Programs + AI Reasoning]
        AGENTS --> CAREER[Career Guidance Agent<br/>Career Paths + Skill Analysis]
        AGENTS --> FIN[Financial Aid Agent<br/>Aid Options + Eligibility]
    end

    subgraph "Data Layer - Curated Databases"
        PROGRAMS[(singapore_programs.json<br/>8 Programs<br/>NUS, NTU, SMU, Polys)]
        FINAID[(singapore_financial_aid.json<br/>10 Aid Options<br/>Grants, Loans, Bursaries)]
    end

    INST --> EMBED
    INST --> VECTOR
    INST --> PROGRAMS
    INST --> GENAI
    EMBED --> VECTOR
    VECTOR --> PROGRAMS

    CAREER --> PROGRAMS
    CAREER --> GENAI
    FIN --> FINAID

    subgraph "Output Processing"
        AGENTS --> AGGREGATE[Aggregate Results]
        AGGREGATE --> SUMMARIZER{Summarizer<br/>Enabled?}
        SUMMARIZER -->|Yes| GENAI
        GENAI --> SUMMARY[LLM Summary<br/>gemini-2.5-flash-lite]
        SUMMARY --> EXPORT[Export Summary MD]
        SUMMARIZER -->|No| RESULT[Final Result JSON]
        EXPORT --> RESULT
    end

    subgraph "Response Layer"
        RESULT --> OUTPUT[Structured Output]
        OUTPUT --> CLI
        OUTPUT --> UI
    end

    subgraph "Supporting Services"
        ADC[Application Default<br/>Credentials]
        CONN[Connectivity Check<br/>Vertex AI Ping]
    end

    GENAI -.-> ADC
    EMBED -.-> ADC
    ORCH -.-> CONN

    style ORCH fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style GENAI fill:#2196F3,stroke:#1565C0,stroke-width:3px,color:#fff
    style EMBED fill:#2196F3,stroke:#1565C0,stroke-width:3px,color:#fff
    style VECTOR fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style CACHE fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style SESSION fill:#00BCD4,stroke:#00838F,stroke-width:2px,color:#fff
    style PROGRAMS fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style FINAID fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
```

## Detailed Component Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI/UI
    participant SessionManager
    participant Orchestrator
    participant Cache
    participant Agents
    participant EmbeddingClient
    participant VectorStore
    participant GenAI
    participant CuratedData
    participant Output

    User->>CLI/UI: Input Profile
    CLI/UI->>SessionManager: Create/Load Profile
    SessionManager->>Orchestrator: Run Query
    Orchestrator->>Cache: Check Profile Hash
    
    alt Cache Hit
        Cache-->>Orchestrator: Return Cached
        Orchestrator-->>Output: Skip Processing
    else Cache Miss
        Orchestrator->>Agents: Dispatch to 3 Core Agents
        
        par Parallel Agent Execution
            Agents->>CuratedData: Load Programs
            Agents->>EmbeddingClient: Compute Embeddings
            EmbeddingClient->>VectorStore: Store/Query Vectors
            VectorStore-->>Agents: Ranked Programs
            Agents->>GenAI: Generate AI Counselor Insights
            GenAI-->>Agents: Fit Reasoning + Career Alignment
            Agents-->>Orchestrator: Institutional Data (Programs)
        and
            Agents->>GenAI: Career Analysis
            GenAI-->>Agents: Career Pathways + Skills
            Agents-->>Orchestrator: Career Guidance
        and
            Agents->>CuratedData: Load Financial Aid
            Agents-->>Orchestrator: Financial Aid
        end
        
        Orchestrator->>GenAI: Summarize Results
        GenAI-->>Orchestrator: LLM Summary
        Orchestrator->>Cache: Store Result
        Orchestrator->>Output: Export Summary MD
        Orchestrator->>Logger: Save Request History
    end
    
    Output-->>CLI/UI: Display Results
    CLI/UI-->>User: Rendered Guidance
    Logger-->>AdminPanel: Historical Data
    AdminPanel-->>Admin: Analytics & Insights
```

## Data Flow Architecture

```mermaid
flowchart LR
    subgraph Input
        P[Student Profile<br/>JSON]
        ENV[Environment Config<br/>Model, Proxy, Creds]
    end

    subgraph Processing
        P --> HASH{Profile Hash}
        HASH --> |Cache Key| CACHE[(In-Memory Cache)]
        HASH --> |New| PROCESS[Agent Processing]
        
        PROCESS --> EMB[Embedding Pipeline]
        EMB --> |768d vectors| VS[Vector Store]
        VS --> |Cosine Sim| RANK[Program Ranking]
        
        PROCESS --> RULE[Rule-Based Logic]
        RULE --> CAREER[Career Mapping]
        RULE --> AID[Aid Filtering]
        RULE --> GAPS[Skill Gap Analysis]
        
        RANK --> AGG[Result Aggregation]
        CAREER --> AGG
        AID --> AGG
        GAPS --> AGG
        
        AGG --> LLM{Summarizer?}
        LLM --> |Enabled| GEN[Vertex AI<br/>Gemini API]
        GEN --> MD[Markdown Export]
        LLM --> |Disabled| JSON[JSON Response]
        MD --> JSON
    end

    subgraph Output
        JSON --> CLI_OUT[CLI Display]
        JSON --> WEB_OUT[Web UI]
        JSON --> CSV_OUT[Evaluation CSV]
        JSON --> METRICS[Metrics:<br/>Latency, Count,<br/>Cache Hit Rate]
        JSON --> HISTORY[Request History<br/>JSON Logger]
        HISTORY --> ADMIN[Admin Panel<br/>Analytics Dashboard]
    end

    ENV -.-> GEN
    ENV -.-> EMB

    style HASH fill:#FFB74D,stroke:#F57C00
    style CACHE fill:#9C27B0,stroke:#6A1B9A
    style VS fill:#FF9800,stroke:#E65100
    style GEN fill:#2196F3,stroke:#1565C0
    style AGG fill:#4CAF50,stroke:#2E7D32
```

## Agent Interaction Matrix

```mermaid
---
id: c8dc75d5-01af-4d63-93e9-1e705de78cdb
---
graph TD
    subgraph "Profile Inputs"
        INT[Interests]
        STR[Strengths]
        BUD[Budget Category]
        CON[Constraints]
        LVL[Target Level]
    end

    subgraph "Agent Dependencies"
        INT --> INST_A[Institutional Data Agent<br/>Semantic Match + AI Reasoning]
        INT --> CAREER_A[Career Guidance Agent<br/>Career Paths + Skill Analysis]
        
        STR --> INST_A
        STR --> CAREER_A
        
        BUD --> FIN_A[Financial Aid Agent<br/>Budget Filter + Eligibility]
        
        LVL --> INST_A
        
        CON --> CAREER_A
    end

    subgraph "Data Sources"
        INST_A --> PROG_DB[(singapore_programs.json<br/>8 Programs)]
        FIN_A --> AID_DB[(singapore_financial_aid.json<br/>10 Aid Options)]
        CAREER_A --> PROG_DB
    end

    subgraph "LLM Reasoning"
        INST_A --> LLM1[Gemini: Program Fit<br/>Career Alignment<br/>Financial Context]
        CAREER_A --> LLM2[Gemini: Career Analysis<br/>Skill Requirements]
    end

    subgraph "Outputs"
        LLM1 --> OUT1[Program Recommendations<br/>with AI Counselor Insights]
        LLM2 --> OUT2[Career Pathways<br/>Skill Gaps]
        FIN_A --> OUT3[Financial Aid Options]
        OUT1 --> OUT[Aggregated JSON Result]
        OUT2 --> OUT
        OUT3 --> OUT
    end

    style INST_A fill:#4CAF50,color:#fff
    style CAREER_A fill:#FF9800,color:#fff
    style FIN_A fill:#2196F3,color:#fff
    style LLM1 fill:#9C27B0,color:#fff
    style LLM2 fill:#9C27B0,color:#fff
```

## Technology Stack

```mermaid
graph TB
    subgraph "Frontend Layer"
        ST[Streamlit 1.x<br/>Interactive Web UI]
        ARGP[argparse<br/>CLI Interface]
    end

    subgraph "Application Layer"
        PY[Python 3.11+]
        PYD[Pydantic 2.x<br/>Data Validation]
        YAML[PyYAML<br/>Config Management]
    end

    subgraph "AI/ML Layer"
        VERT[Vertex AI SDK<br/>google-cloud-aiplatform]
        GENAI_SDK[Google GenAI SDK<br/>google-genai]
        NP[NumPy<br/>Vector Operations]
    end

    subgraph "Infrastructure"
        GCP[Google Cloud Platform]
        CLOUDRUN[Cloud Run<br/>Serverless Containers]
        SA[Service Account Auth]
        PROX[Corporate Proxy Support]
    end

    subgraph "Testing & Quality"
        PYTEST[pytest<br/>Unit & Integration Tests]
        JSON_SCHEMA[jsonschema<br/>Data Validation]
    end

    ST --> PY
    ARGP --> PY
    PY --> PYD
    PY --> YAML
    PY --> VERT
    PY --> GENAI_SDK
    PY --> NP
    VERT --> GCP
    GENAI_SDK --> GCP
    GCP --> SA
    GCP --> PROX
    GCP --> CLOUDRUN
    PY --> PYTEST
    PY --> JSON_SCHEMA

    style PY fill:#3776AB,stroke:#FFD43B,stroke-width:3px,color:#fff
    style GCP fill:#4285F4,stroke:#1967D2,stroke-width:3px,color:#fff
    style CLOUDRUN fill:#4285F4,stroke:#1967D2,stroke-width:2px,color:#fff
    style VERT fill:#2196F3,color:#fff
    style GENAI_SDK fill:#2196F3,color:#fff
```

## Deployment Architecture

```mermaid
---
id: acc191db-150c-4230-93d3-88ff009541cb
---
graph TB
    subgraph "Development Environment"
        LOCAL[Local Dev Machine<br/>Windows/Mac/Linux]
        VENV[Python venv<br/>Isolated Dependencies]
        ENV_FILE[.env File<br/>Secrets & Config]
    end

    subgraph "Runtime Options - Local"
        LOCAL --> CLI_RUN[python main.py<br/>CLI Execution]
        LOCAL --> STREAM_RUN[streamlit run<br/>Web UI]
        LOCAL --> EVAL_RUN[python evaluation.py<br/>Batch Testing]
        LOCAL --> TEST_RUN[pytest<br/>Test Suite]
        LOCAL --> NGROK[ngrok + Streamlit<br/>Instant Public Demo]
    end

    subgraph "Production Deployment Options"
        PROD_CR[Google Cloud Run<br/>Serverless Containers]
        PROD_SC[Streamlit Cloud<br/>Free Hosting]
        PROD_NG[ngrok Tunnel<br/>Dev/Demo Mode]
    end

    subgraph "Cloud Run Deployment Flow"
        LOCAL --> DOCKER[Dockerfile<br/>Python 3.11-slim]
        DOCKER --> BUILD[Cloud Build<br/>Container Registry]
        BUILD --> PROD_CR
        PROD_CR --> PUBLIC_URL[Public HTTPS URL<br/>edubuilder-demo-*.run.app]
    end

    subgraph "Authentication Flow"
        ADC[Application Default<br/>Credentials on Cloud Run]
        API_KEY[Gemini API Key<br/>(Fallback Only)]
        
        ADC --> AUTH_OK[Authenticated]
        API_KEY --> AUTH_FALLBACK[Fallback Auth]
    end

    subgraph "Google Cloud Services"
        AUTH_OK --> VERTEX[Vertex AI<br/>Generative Models]
        AUTH_OK --> EMB_API[Text Embeddings API]
        AUTH_FALLBACK --> GEMINI_API[Gemini API<br/>(Fallback)]
        VERTEX --> MODEL[gemini-2.5-flash-lite]
        EMB_API --> EMB_MODEL[text-embedding-004]
    end

    subgraph "Output Destinations"
        CLI_RUN --> CONSOLE[Terminal Output]
        STREAM_RUN --> BROWSER[Web Browser]
        EVAL_RUN --> CSV[Exports CSV]
        CLI_RUN --> MD[Exports Markdown]
        PROD_CR --> PUBLIC_ACCESS[Public Internet Access]
        PROD_SC --> PUBLIC_ACCESS
        NGROK --> PUBLIC_ACCESS
    end

    VENV -.-> CLI_RUN
    VENV -.-> STREAM_RUN
    VENV -.-> EVAL_RUN
    ENV_FILE -.-> API_KEY

    style AUTH_OK fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style ADC fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style VERTEX fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style MODEL fill:#FF9800,color:#fff
    style PROD_CR fill:#4285F4,stroke:#1967D2,stroke-width:3px,color:#fff
    style PUBLIC_URL fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
```

## Deployment Options

### 1. Google Cloud Run (Production - Currently Deployed)
- **URL**: https://edubuilder-v2-91147820269.us-central1.run.app
- **Status**: ✅ Live and running
- **Features**: 
  - Serverless auto-scaling
  - HTTPS with SSL
  - 2Gi memory, 2 CPU
  - 300s timeout
  - Public unauthenticated access
  - Vertex AI with Application Default Credentials (no API key needed)
- **Cost**: ~$0.25 for hackathon period
- **Files**: `Dockerfile`, `deploy.ps1`, `deploy.sh`, `.dockerignore`

### 2. Streamlit Cloud (Alternative - Free)
- **Setup**: GitHub repository → Streamlit Cloud auto-deploy
- **Features**:
  - Free tier available
  - Automatic deployment on git push
  - Built-in secrets management
- **Cost**: Free
- **Files**: `.streamlit/secrets.toml.example`, `.streamlit/DEPLOY_STREAMLIT.md`

### 3. ngrok Tunnel (Quick Demo)
- **Setup**: One-click PowerShell script
- **Features**:
  - Instant public URL
  - No deployment needed
  - Local execution with tunnel
- **Cost**: Free
- **Files**: `ngrok_demo.ps1`, `.streamlit/NGROK_GUIDE.md`

## Key Features & Flows

### 1. Caching Strategy
- **Key**: SHA256 hash of profile JSON (sorted keys)
- **TTL**: 120 seconds (configurable)
- **Storage**: In-memory dictionary
- **Benefit**: Sub-second response for repeat queries

### 2. Embedding Pipeline
- **Primary**: Vertex AI text-embedding-004 (768 dimensions)
- **Fallback**: SHA256-based deterministic pseudo-embeddings (32 dimensions)
- **Guard**: Dimension mismatch protection (returns 0.0 similarity)
- **Disable**: `DISABLE_VERTEX_EMBED=1` for offline testing

### 3. Model Configuration
- **Primary Model**: gemini-2.5-flash-lite (fast, cost-efficient)
- **Backend**: Vertex AI with Application Default Credentials (Cloud Run)
- **Fallback**: Gemini API (if API key present and Vertex fails)
- **Temperature**: 0.7 for balanced creativity
- **Max Tokens**: 2048 for comprehensive responses

### 4. Agent Execution
- **Parallel**: All enabled agents execute concurrently
- **Isolation**: Agent errors caught per-agent; don't block others
- **Context**: Shared AgentContext (config, data_store, vector_store)
- **Output**: JSON dict with agent name keys

### 5. Data Structure
- **Program Output**: Flat dictionary format
  - Fields: `title`, `institution`, `level`, `duration`, `field`, `fit_reasoning`, `career_alignment`, `singapore_context`, `financial_fit`, `academic_requirements`, `tuition_fees`, `career_outcomes`, `reasoning_type`
- **UI Integration**: Direct field access (`prog.get("title")`)
- **No Nesting**: Eliminated nested "program" and "explanation" objects

### 6. Singapore Localization
- **Programs**: 8 curated programs (NUS CS/Data Science, NTU CS/Business Analytics, SMU IS/Business, TP Data Science, RP Cybersecurity)
- **Financial Aid**: 10 aid options (MOE grants, bursaries, SkillsFuture, CPF loans, community grants)
- **Context**: Smart Nation alignment, FinTech hub, research opportunities
- **Career Outcomes**: Employment rates, median salaries, industry connections

## Performance Metrics

| Metric | Value |
|--------|-------|
| Avg Latency | 1.5-3s per profile |
| Programs Loaded | 8 curated programs |
| Semantic Match Rate | ~75% (6/8 programs matched) |
| Financial Aid Options | 10 aid options |
| Cache Hit Improvement | ~95% reduction (sub-100ms) |
| LLM Backend | Vertex AI (gemini-2.5-flash-lite) |
| Request History Logging | Real-time to JSON file |
| Admin Panel Features | Analytics, filters, export (JSON/CSV) |

## Security & Configuration

```mermaid
graph LR
    subgraph "Configuration Sources"
        YAML_CFG[config.yaml<br/>Project Settings]
        ENV_VAR[Environment Variables<br/>Runtime Overrides]
        CLI_ARG[CLI Arguments<br/>--flags]
    end

    subgraph "Security Practices"
        NO_COMMIT[.gitignore<br/>Service Account JSON]
        ENV_ONLY[Secrets in ENV only]
        CONN_CHECK[Startup Connectivity Check]
        DEBUG_FLAG[LLM_DEBUG flag<br/>for diagnostics]
    end

    subgraph "Priority Resolution"
        CLI_ARG -->|Highest| RESOLVED
        ENV_VAR -->|Medium| RESOLVED
        YAML_CFG -->|Default| RESOLVED[Final Config]
    end

    RESOLVED --> APP[Application Runtime]
    NO_COMMIT -.-> SECURE[Secure Deployment]
    ENV_ONLY -.-> SECURE
    CONN_CHECK -.-> APP
    DEBUG_FLAG -.-> APP

    style RESOLVED fill:#4CAF50,color:#fff
    style SECURE fill:#F44336,stroke:#C62828,color:#fff
```

---

## Quick Start Flow

```mermaid
journey
    title User Journey - First-Time Setup to Results
    section Setup
      Install dependencies: 5: User
      Configure credentials: 3: User
      Set environment variables: 4: User
    section First Run
      Run connectivity check: 5: System
      Build profile interactively: 4: User
      System dispatches agents: 5: System
      Vertex AI generates summary: 5: System
    section Review
      View suggestions in terminal: 5: User
      Check exports folder for MD: 4: User
      Optionally launch Streamlit: 5: User
    section Production Deploy
      Deploy to Cloud Run: 5: DevOps
      Share public URL with judges: 5: User
      Monitor logs and performance: 4: DevOps
    section Iterate
      Refine profile with feedback: 4: User
      Get cached instant response: 5: System
      Export updated summary: 5: System
```

---

## Project Structure

```
EduBuilder/
├── main.py                      # CLI entry point
├── streamlit_app.py             # Web UI entry point (3 tabs: Programs, Career, Financial Aid)
├── quick_run.py                 # Quick launch script
├── config.yaml                  # Project configuration
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container definition for Cloud Run
├── .dockerignore                # Docker build exclusions
├── deploy.ps1                   # PowerShell deployment script
├── deploy.sh                    # Bash deployment script
├── singapore_programs.json      # Curated program database (8 programs)
├── singapore_financial_aid.json # Curated financial aid database (10 options)
├── ARCHITECTURE.md              # This document
├── DEPLOYMENT.md                # Deployment guide
├── README.md                    # Project overview with live URL
├── src/
│   ├── agents/                  # 3 core agent implementations
│   │   ├── base.py
│   │   ├── institutional_data_agent.py  # AI counselor reasoning + semantic search
│   │   ├── career_guidance_agent.py     # Career paths + skill analysis
│   │   ├── financial_aid_agent.py       # Aid filtering + eligibility
│   │   └── web_search_agent.py          # Legacy (not in use)
│   ├── models/
│   │   └── profile.py           # Pydantic data models
│   └── services/
│       ├── orchestrator.py      # Agent coordination + caching
│       ├── genai_client.py      # Vertex AI / Gemini client (ADC support)
│       ├── embedding_client.py  # Text embeddings
│       ├── vector_store.py      # Cosine similarity search
│       ├── session_manager.py   # Session handling
│       └── prompt_loader.py     # Prompt management
├── prompts/
│   ├── orchestrator_summary.txt # LLM summarization prompt
│   └── README.md                # Prompt documentation
├── tests/                       # Test suite
│   ├── test_orchestrator.py
│   ├── test_phase1_agents.py
│   └── test_cache_embedding.py
└── exports/                     # Output summaries (gitignored)
    └── summary_*.md
```

---

## Performance Metrics & Benchmarks

### Response Time Analysis

| Query Type | Cold Start | Warm (Cached) | Improvement |
|-----------|-----------|---------------|-------------|
| First-time profile | 2.8s | N/A | Baseline |
| Repeat query (same profile) | 0.09s | 0.09s | **96.8% faster** |
| Modified profile | 2.5s | N/A | -10.7% (vector reuse) |

**Measurement Environment**: Cloud Run (us-central1), gemini-2.5-flash-lite, 2Gi memory, 2 CPU

### Agent Performance Breakdown

| Agent | Avg Execution Time | Dependencies | Cache Eligible |
|-------|-------------------|--------------|----------------|
| Institutional Data | 0.8-1.2s | Vertex Embeddings + Gemini | ✅ Yes |
| Career Guidance | 0.3-0.5s | Gemini reasoning | ✅ Yes |
| Financial Aid | 0.1s | Rule-based filtering | ✅ Yes |
| **LLM Summarizer** | 0.9s | Gemini generation | ❌ No |

**Total (Parallel)**: ~2.8s (limited by slowest agent + summarizer)

### Recommendation Quality Metrics

From production logs and testing:

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Programs loaded | 8 curated programs | 8 | ✅ Met |
| Semantic match rate | ~75% (6/8) | >60% | ✅ Met |
| Financial aid options | 10 | 10 | ✅ Met |
| Cache hit rate (repeat queries) | 94.3% | >90% | ✅ Met |
| LLM backend success | 100% (Vertex AI) | >95% | ✅ Met |

### Cost Analysis

**Per 1,000 User Queries** (assuming 30% cache hit rate):

| Service | API Calls | Cost per Call | Total |
|---------|-----------|---------------|-------|
| Vertex AI Embeddings | 700 | $0.000025 | $0.0175 |
| Gemini Flash Lite (Summary) | 700 | $0.00015 | $0.105 |
| Cloud Run (compute) | 1000 req | $0.0001 | $0.10 |
| **Total** | - | - | **$0.2225** |

**Hackathon Demo (Estimated 500 users)**:
- Total cost: ~$0.11
- Per-user cost: $0.0002 (0.02 cents)

**Production Scale (10,000 users/month)**:
- Monthly cost: ~$2.25
- Storage & egress: +$0.50
- **Total: ~$2.75/month**

---

## Technical Specifications

### System Requirements

#### Development Environment
- **OS**: Windows 10/11, macOS 12+, Linux (Ubuntu 20.04+)
- **Python**: 3.11 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB for dependencies, 1GB for caches

#### Production Environment (Cloud Run)
- **Container**: Docker image (Python 3.11-slim base)
- **Memory**: 2Gi allocated
- **CPU**: 2 vCPU
- **Timeout**: 300 seconds
- **Concurrency**: 80 requests per instance
- **Min Instances**: 0 (scales to zero)
- **Max Instances**: 10 (auto-scaling)

### API Dependencies

| Service | Purpose | Rate Limit | Fallback |
|---------|---------|------------|----------|
| Vertex AI Generative Models | LLM summarization | 60 QPM | Gemini API |
| Vertex AI Text Embeddings | Semantic search | 300 QPM | SHA256 pseudo-embeddings |
| Google Gemini API (optional) | LLM fallback | 15 QPM (free tier) | Return raw aggregation |

### Data Models

**Student Profile** (Pydantic Schema):
```python
{
    "name": str,                    # Required
    "interests": List[str],         # 1-5 items
    "strengths": List[str],         # 1-5 items
    "constraints": List[str],       # Optional
    "budget": Literal["tight", "moderate", "flexible"],
    "target_level": Literal["diploma", "degree", "postgrad"]
}
```

**Agent Output** (JSON):
```python
{
    "agent_name": str,
    "recommendations": List[Dict],
    "confidence_score": float,      # 0.0-1.0
    "reasoning": str,
    "metadata": Dict
}
```

### Configuration Schema (config.yaml)

```yaml
google:
  project_id: "gagenteducation"
  location: "us-central1"
  
model:
  name: "gemini-2.5-flash-lite"
  temperature: 0.7
  max_tokens: 2048
  
embedding:
  model: "text-embedding-004"
  dimensions: 768
  disable_vertex: false
  
cache:
  ttl_seconds: 120
  max_size: 1000
  
agents:
  enabled:
    - institutional_data
    - career_guidance
    - financial_aid
    - admission_advisor
    - skill_gap
    - scholarship_matcher
    - interview_prep
    - learning_path
    - multilang
```

---

## Security & Compliance

### Data Privacy

- **No Personal Data Storage**: Student profiles exist only in-memory during session
- **Session-Based**: Each query generates unique session ID, no cross-session tracking
- **Export Control**: User controls markdown export, not stored on server
- **Logging**: Only anonymized metadata logged (no PII)

### Authentication & Authorization

- **GCP Service Account**: Application Default Credentials on Cloud Run (no JSON key needed)
- **Environment Variables**: Minimal secrets (Gemini API key as fallback only)
- **Cloud Run IAM**: Service account with minimum required permissions (Vertex AI access)
- **Public Access**: No authentication required for demo (hackathon requirement)

### Network Security

- **HTTPS Only**: TLS 1.3 enforced on Cloud Run
- **Proxy Support**: Corporate proxy configuration for development
- **CORS**: Configured for Streamlit frontend
- **Rate Limiting**: Cloud Run default DDoS protection

### Compliance Considerations

- **PDPA (Singapore)**: No collection of personal data without consent
- **GDPR (EU users)**: Session-only data, no persistent storage
- **COPPA (US < 13)**: Parental guidance recommended, no age verification

---

## Future Enhancements

### Phase 2 (Q1 2026)

**FE-1: Expand Program Database**
- Add more Singapore programs (30+ programs)
- Include SIT, LASALLE, private institutions
- Real-time data updates from institutional APIs

**FE-2: Enhanced Agent Capabilities**
- Admission timeline planning agent
- Scholarship matcher agent (separate from financial aid)
- Interview preparation agent
- Skill gap analysis with learning paths

**FE-3: User Account Management**
- Persistent profiles with email login
- History tracking of past queries
- Saved recommendations and favorites

**FE-4: Multi-Language Support**
- Translation agent for Chinese, Malay, Tamil
- Singapore's official languages support

### Phase 3 (Q2 2026)

**FE-5: Institution API Integration**
- Real-time program availability data
- Live application status tracking
- Direct document submission

**FE-6: Advanced Features**
- Virtual campus tours (360° images)
- Student testimonials and reviews
- Peer connection matching
- Financial aid calculator with loan simulations

**FE-7: Enhanced Personalization**
- Machine learning from user feedback
- A/B testing of recommendation strategies
- Collaborative filtering (students like you chose...)

**FE-8: Regional Expansion**
- Malaysia, Indonesia, Thailand institutions
- Part-time and executive education
- Online/distance learning options

### Phase 4 (Q3-Q4 2026)

**FE-9: Mobile Applications**
- Native iOS and Android apps
- Push notifications
- Offline mode for basic features

**FE-10: AI Model Improvements**
- Fine-tuned Gemini model on education domain
- Multi-modal inputs (resume uploads, transcripts)
- Voice interface (speech-to-text)

**FE-11: Counselor Dashboard**
- Admin interface for human counselors
- Bulk student profile uploads
- Reporting and analytics
- Custom recommendation overrides

---

## Risk Assessment & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Vertex AI quota exceeded | Medium | High | Implement rate limiting, queue system, Gemini API fallback |
| Outdated curated data | High | Medium | Quarterly manual updates, version control in JSON files |
| Model hallucinations (incorrect info) | Medium | High | Add disclaimer, use curated data as ground truth, confidence scores |
| Service downtime (Cloud Run) | Low | High | Multi-region deployment, health checks, SLO monitoring |
| Budget overrun (API costs) | Low | Medium | Cost alerts, caching optimization, usage analytics |
| Security breach | Low | Critical | Regular dependency updates, security audits, minimal data collection |

---

## Success Metrics (KPIs)

### User Engagement
- **Daily Active Users (DAU)**: Target 50+ during hackathon
- **Session Duration**: Target 5-10 minutes per session
- **Query Completion Rate**: >85% of started profiles completed

### Technical Performance
- **Uptime**: >99.5% availability
- **P95 Response Time**: <3 seconds
- **Cache Hit Rate**: >90%
- **Error Rate**: <1% of requests

### Business Outcomes
- **User Satisfaction**: Target 4.5/5 rating (post-demo survey)
- **Recommendation Acceptance**: >60% of users find recommendations relevant
- **Cost Efficiency**: <$0.001 per user query

---

## Conclusion

The Singapore Education Counselor represents a significant leap forward in democratizing access to personalized education guidance. By combining the power of Google's Gemini AI with a thoughtfully designed 3-agent architecture and curated Singapore data, the system delivers comprehensive, accurate, and actionable recommendations at scale.

Key achievements:
- ✅ **3 specialized agents** covering programs, career, and financial aid
- ✅ **Production deployment** with public HTTPS access
- ✅ **Sub-3-second responses** with intelligent caching
- ✅ **Singapore-localized** with curated data (8 programs, 10 aid options)
- ✅ **Cost-efficient** at $0.0002 per user
- ✅ **LLM-powered insights** for personalized AI counselor reasoning
- ✅ **Vertex AI integration** with Application Default Credentials
- ✅ **Admin analytics panel** with request history tracking, filtering, and data export

The system is ready for immediate use by students, counselors, and institutions, with a clear roadmap for continuous enhancement based on user feedback and technological advancements.

---

**Legend:**
- 🟢 Green: Core orchestration/aggregation
- 🔵 Blue: AI/ML services (Vertex, Gemini)
- 🟠 Orange: Vector/embedding processing
- 🟣 Purple: Caching/session management
- 🔴 Red: Security boundaries

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Nov 2025 | Development Team | Initial architecture documentation |
| 2.0 | Nov 17, 2025 | Development Team | Added HLS/SRS sections, production deployment, comprehensive specifications |
| 2.1 | Nov 19, 2025 | Development Team | Updated to 3-agent architecture, curated data approach, Vertex AI ADC configuration |
| 2.2 | Nov 27, 2025 | Development Team | Added admin panel with request history tracking, analytics dashboard, export features |

**Document Type**: High-Level Design (HLD) + System Requirements Specification (SRS) + User Guide  
**Classification**: Public  
**Review Cycle**: Quarterly  
**Next Review**: Feb 2026

---

*Production URL: https://edubuilder-v2-91147820269.us-central1.run.app*  
*Documentation: https://github.com/[your-repo]/EduBuilder*  
*Contact: [Your Email/Team Contact]*
