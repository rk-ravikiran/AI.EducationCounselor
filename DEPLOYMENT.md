# Deployment Guide - Singapore Education Counselor

## Deployment Options for Hackathon Demo

### Option 1: Cloud Run (Recommended - Easiest)
**Best for:** Quick deployment, auto-scaling, serverless

#### Step 1: Create Dockerfile

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p .vector_cache exports

# Expose Streamlit port
EXPOSE 8080

# Set environment variable for Streamlit
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

#### Step 2: Create .dockerignore

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.env
.env.example
.git/
.gitignore
.vscode/
*.md
tests/
.vector_cache/
exports/
*.json.key
*_service_account.json
```

#### Step 3: Deploy to Cloud Run

```bash
# 1. Set your project
gcloud config set project gagenteducation

# 2. Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# 3. Build and deploy
gcloud run deploy edubuilder-demo \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_PROJECT_ID=gagenteducation \
  --set-env-vars GOOGLE_LOCATION=us-central1 \
  --set-env-vars MODEL_NAME=gemini-2.5-flash-lite \
  --set-env-vars DISABLE_VERTEX_EMBED=0 \
  --set-env-vars SUMMARY_LANG=en \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300
```

**Result:** Public URL like `https://edubuilder-demo-abc123-uc.a.run.app`

**Pros:** ✅ Serverless, ✅ Auto-scaling, ✅ HTTPS by default, ✅ No server management  
**Cons:** ❌ Cold start delays (~5-10s), ❌ Ephemeral storage (cache resets)

---

### Option 2: App Engine (Simpler Configuration)
**Best for:** Zero Docker knowledge, quick deploy

#### Step 1: Create app.yaml

```yaml
runtime: python311
entrypoint: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0

instance_class: F4
automatic_scaling:
  min_instances: 0
  max_instances: 3
  target_cpu_utilization: 0.6

env_variables:
  GOOGLE_PROJECT_ID: "gagenteducation"
  GOOGLE_LOCATION: "us-central1"
  MODEL_NAME: "gemini-2.5-flash-lite"
  DISABLE_VERTEX_EMBED: "0"
  SUMMARY_LANG: "en"
  LLM_DEBUG: "0"
```

#### Step 2: Deploy

```bash
gcloud app deploy app.yaml --project=gagenteducation
```

**Result:** URL like `https://gagenteducation.uc.r.appspot.com`

**Pros:** ✅ No Docker needed, ✅ Simple config, ✅ Persistent instances  
**Cons:** ❌ Less flexible than Cloud Run, ❌ Slower scaling

---

### Option 3: Vertex AI Workbench (For Judges to Test)
**Best for:** Interactive demo, code walkthrough

#### Deploy as Jupyter Notebook

```bash
# Create notebook instance
gcloud notebooks instances create edubuilder-demo \
  --project=gagenteducation \
  --location=us-central1-a \
  --machine-type=n1-standard-4 \
  --vm-image-project=deeplearning-platform-release \
  --vm-image-family=common-cpu
```

Upload your code and run in Jupyter for live demo.

---

### Option 4: Streamlit Community Cloud (Fastest - No GCP Needed)
**Best for:** Instant deployment, free hosting

#### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit for hackathon"
git remote add origin https://github.com/YOUR_USERNAME/edubuilder.git
git push -u origin main
```

#### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Connect GitHub repo
3. Add secrets in dashboard:

```toml
# .streamlit/secrets.toml (in Streamlit Cloud dashboard)
GOOGLE_APPLICATION_CREDENTIALS = """
{
  "type": "service_account",
  "project_id": "gagenteducation",
  ... paste full service account JSON ...
}
"""
GOOGLE_PROJECT_ID = "gagenteducation"
GOOGLE_LOCATION = "us-central1"
MODEL_NAME = "gemini-2.5-flash-lite"
GOOGLE_API_KEY = "your-api-key-here"
```

**Result:** URL like `https://edubuilder.streamlit.app`

**Pros:** ✅ FREE, ✅ Instant, ✅ Auto-redeploys on git push, ✅ No GCP setup  
**Cons:** ❌ Public (anyone can see), ❌ Resource limits (1GB RAM)

---

## Recommended Approach for Your Hackathon

### **Use Cloud Run (Option 1)**

**Why:**
- Professional deployment on Google Cloud (shows technical depth)
- Scalable for multiple judges testing simultaneously
- Works with your existing service account
- Public URL without authentication
- Easy to take down after hackathon

### Quick Deploy Steps:

1. **Create the Dockerfile** (I'll provide complete file below)
2. **Update streamlit_app.py** to use environment variables
3. **Deploy with one command**
4. **Share the public URL** with judges

---

## Security Considerations

### For Public Demo:

```python
# Add rate limiting to streamlit_app.py
import time
from collections import defaultdict

# Simple rate limiter
request_count = defaultdict(list)

def rate_limit(session_id, max_requests=10, window=60):
    """Limit to 10 requests per minute per session"""
    now = time.time()
    request_count[session_id] = [t for t in request_count[session_id] if now - t < window]
    
    if len(request_count[session_id]) >= max_requests:
        return False
    
    request_count[session_id].append(now)
    return True
```

### Protect API Keys:

**Option A: Use Secret Manager (Recommended)**

```bash
# Store API key in Secret Manager
gcloud secrets create gemini-api-key \
  --data-file=- <<< "your-api-key-here"

# Deploy with secret
gcloud run deploy edubuilder-demo \
  --source . \
  --set-secrets GOOGLE_API_KEY=gemini-api-key:latest
```

**Option B: Service Account Only**

Remove `GOOGLE_API_KEY` from environment and rely only on service account.

---

## Cost Estimation

### Cloud Run (Recommended)

- **Free tier:** 2 million requests/month
- **Estimated cost for hackathon:** $0-5
  - 50 demo sessions × 3 minutes each = 2.5 hours
  - ~$0.10/hour = **$0.25 total**

### Streamlit Cloud

- **Free tier:** Unlimited for public apps
- **Cost:** $0 ✅

---

## Pre-Deployment Checklist

- [ ] Test locally: `streamlit run streamlit_app.py`
- [ ] Verify all agents work without errors
- [ ] Check LLM summaries generate properly
- [ ] Test with sample student profiles
- [ ] Prepare demo script/walkthrough
- [ ] Create short demo video (2-3 min)
- [ ] Have backup plan (local demo if cloud fails)

---

## Demo Best Practices

### 1. Pre-load Cache
```bash
# Generate vector cache before demo
python -c "from main import load_programs; from src.services.vector_store import VectorStore; vs = VectorStore(); vs.add_programs(load_programs())"
```

### 2. Create Sample Profiles
```python
# Add to streamlit_app.py
DEMO_PROFILES = {
    "AI Enthusiast": {"interests": ["AI", "Machine Learning"], ...},
    "Finance Student": {"interests": ["Finance", "Economics"], ...},
    "Robotics Engineer": {"interests": ["Robotics", "Automation"], ...}
}
```

### 3. Add Performance Metrics
```python
# Show processing time in UI
with st.spinner("Processing..."):
    start = time.time()
    results = orchestrator.run(profile)
    st.info(f"⚡ Processed in {time.time() - start:.2f}s")
```

---

## Troubleshooting

### "Service account not found"
- Ensure service account JSON is in Secret Manager or mounted
- Check IAM permissions for Cloud Run service account

### "Cold start too slow"
- Set `--min-instances 1` to keep one instance warm
- Use `--cpu-boost` flag for faster startup

### "Out of memory"
- Increase to `--memory 2Gi`
- Disable vector embeddings: `DISABLE_VERTEX_EMBED=1`

---

## Next Steps

Would you like me to:
1. ✅ Create the complete Dockerfile?
2. ✅ Update streamlit_app.py for cloud deployment?
3. ✅ Generate deployment commands for Cloud Run?
4. ✅ Set up Secret Manager for API keys?

Let me know which deployment option you prefer!
