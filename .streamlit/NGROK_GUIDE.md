# Ngrok Quick Demo Guide

## Instant Public Demo with Ngrok

Perfect for live presentations when you want to show your app running on your machine.

### Prerequisites

1. **Install ngrok:**
   - Download: https://ngrok.com/download
   - Extract `ngrok.exe` to a folder
   - Add to PATH or place in project folder

2. **Sign up (free):**
   - Create account: https://dashboard.ngrok.com/signup
   - Get auth token: https://dashboard.ngrok.com/get-started/your-authtoken

3. **Configure:**
   ```powershell
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

---

## Option A: Automated Script (Recommended)

```powershell
# One-command demo launch
.\ngrok_demo.ps1
```

This will:
1. Load environment variables
2. Start Streamlit app locally
3. Create public ngrok tunnel
4. Display public URL to share

**Press Ctrl+C when done to stop everything**

---

## Option B: Manual Steps

### Terminal 1: Start Streamlit
```powershell
.\load_env.ps1
streamlit run streamlit_app.py
```

### Terminal 2: Start ngrok
```powershell
ngrok http 8501
```

**Copy the public URL** (looks like `https://abc123.ngrok.io`) and share it!

---

## What Judges Will See

- ✅ Full working demo with real-time processing
- ✅ Singapore-specific counseling recommendations
- ✅ All 9 agents working together
- ✅ Professional Streamlit UI
- ✅ LLM-generated summaries

---

## Pros & Cons

### Pros
✅ **Instant** - No deployment needed
✅ **Live** - Runs on your machine with full control
✅ **Debug-friendly** - See logs in real-time
✅ **FREE** - ngrok free tier is sufficient
✅ **Flexible** - Can demo code changes immediately

### Cons
❌ **Temporary** - URL expires when you close ngrok
❌ **Dependent** - Requires your machine to stay on
❌ **Network** - Needs stable internet
❌ **Limited** - Free tier has bandwidth limits

---

## Usage Tips

### For Hackathon Presentation:

1. **Before your slot:**
   ```powershell
   .\ngrok_demo.ps1
   ```

2. **Copy the public URL** (e.g., `https://abc123.ngrok.io`)

3. **Share URL** with judges via:
   - Chat
   - QR code (ngrok dashboard shows one)
   - Presentation slides

4. **Demo live** while talking through features

5. **Stop when done:**
   - Press `Ctrl+C`

### For Testing Before Demo:

```powershell
# Test that ngrok works
.\ngrok_demo.ps1

# Try accessing from your phone/another device
# Make sure demo profile loads quickly
```

---

## Troubleshooting

### "ngrok: command not found"
```powershell
# Download and extract ngrok
# Then either:
# Option 1: Add to PATH
# Option 2: Copy ngrok.exe to project folder
```

### "Tunnel not found"
- Ensure you configured auth token: `ngrok config add-authtoken YOUR_TOKEN`

### "Too many connections"
- Free tier allows ~40 connections/minute
- Sufficient for hackathon judging

### Streamlit won't start
```powershell
.\load_env.ps1
python -m streamlit run streamlit_app.py
```

---

## Bandwidth Usage

Typical hackathon demo: **~50 MB total**
- Initial load: ~5 MB
- Per query: ~1-2 MB
- 10 demo queries = ~20 MB

Free tier limit: **1 GB/month** ✅

---

## Security Note

Ngrok creates a **temporary public URL** that anyone can access. After your demo:
- Press `Ctrl+C` to close the tunnel
- URL becomes invalid immediately
- No one can access your app anymore

---

## Alternative: Ngrok Custom Domain (Optional)

If you have ngrok Pro ($8/month):
```powershell
ngrok http 8501 --domain=edubuilder-demo.ngrok.app
```

Gets you a **permanent URL** instead of random one.

---

## When to Use Ngrok vs Cloud Deploy

| Scenario | Use Ngrok | Use Cloud Run |
|----------|-----------|---------------|
| Live presentation with you present | ✅ | |
| Judges test at different times | | ✅ |
| Want to show code updates live | ✅ | |
| Need 24/7 availability | | ✅ |
| Testing before deploying | ✅ | |
| Professional impression | | ✅ |

**Recommendation:** Use both!
- Ngrok for live demo during presentation
- Cloud Run for judges to test later
