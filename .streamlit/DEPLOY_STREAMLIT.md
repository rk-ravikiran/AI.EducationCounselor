# Streamlit Cloud Deployment Guide

## Quick Deploy to Streamlit Cloud (FREE)

### Step 1: Push to GitHub

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Singapore Education Counselor - Google AI Hackathon"

# Create main branch
git branch -M main

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/edubuilder.git

# Push
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Go to:** https://share.streamlit.io/

2. **Sign in** with GitHub

3. **Click:** "New app"

4. **Configure:**
   - Repository: `YOUR_USERNAME/edubuilder`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

5. **Add Secrets** (click "Advanced settings" → "Secrets"):

Copy content from `.streamlit/secrets.toml.example`:

```toml
GOOGLE_PROJECT_ID = "gagenteducation"
GOOGLE_LOCATION = "us-central1"
GOOGLE_API_KEY = "your-api-key-here"
MODEL_NAME = "gemini-2.5-flash-lite"
DISABLE_VERTEX_EMBED = "1"
SUMMARY_LANG = "en"
LLM_DEBUG = "0"
```

6. **Click:** "Deploy"

7. **Wait:** 2-3 minutes for deployment

8. **Get URL:** `https://YOUR_APP.streamlit.app`

### Step 3: Share URL

Your app will be live at: `https://[your-app-name].streamlit.app`

Share this URL with hackathon judges!

---

## Update Deployed App

Any time you push to GitHub, Streamlit Cloud auto-redeploys:

```powershell
git add .
git commit -m "Update features"
git push
```

Wait 1-2 minutes for automatic redeployment.

---

## Troubleshooting

### "Module not found"
- Ensure `requirements.txt` includes all dependencies
- Check that imports work locally first

### "Secrets not found"
- Verify secrets are added in Streamlit Cloud dashboard
- Check spelling of secret keys
- Use `st.secrets["KEY_NAME"]` to access

### "App keeps restarting"
- Check logs in Streamlit Cloud dashboard
- Ensure service account credentials are valid
- Try setting `DISABLE_VERTEX_EMBED=1` to use fallback embeddings

---

## Cost

**FREE** - Streamlit Cloud Community plan includes:
- Unlimited public apps
- 1GB RAM
- 1 CPU
- Auto-scaling for moderate traffic

Perfect for hackathon demos! 🚀
