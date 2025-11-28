# Proxy Configuration Guide

## Problem

Infosys corporate proxy (`blrproxy.ad.infosys.com:80`) blocks Google Cloud API connections, causing:
- Vertex AI: 503 connection errors
- Gemini API: Server disconnection
- Embedding API: Timeout failures

## Solution

**Use project-level proxy configuration via `.env` file** (NOT global environment variables)

## Configuration Options

### Option 1: No Proxy (Recommended for Google AI)

```env
# .env file
# Proxy disabled - Google Cloud APIs work directly
# HTTP_PROXY=http://blrproxy.ad.infosys.com:80   # Commented out
# HTTPS_PROXY=http://blrproxy.ad.infosys.com:80  # Commented out
```

**Use when:**
- Working with Google Cloud APIs (Vertex AI, Gemini)
- Running hackathon demo
- Local development

**Pros:** ✅ Fast, ✅ Reliable, ✅ No connection issues  
**Cons:** ❌ May not access some internal Infosys resources

### Option 2: Selective Proxy with NO_PROXY

```env
# Enable proxy for most traffic
HTTP_PROXY=http://blrproxy.ad.infosys.com:80
HTTPS_PROXY=http://blrproxy.ad.infosys.com:80

# Bypass proxy for Google services
NO_PROXY=.googleapis.com,.google.com,generativelanguage.googleapis.com,aiplatform.googleapis.com
```

**Use when:**
- Need both internal resources AND Google Cloud
- Production environment with mixed requirements

**Pros:** ✅ Access to both internal/external  
**Cons:** ❌ More complex, ❌ May still have issues

### Option 3: Global Proxy (Not Recommended)

```powershell
# Set at User level (persists across sessions)
[Environment]::SetEnvironmentVariable('HTTP_PROXY', 'http://blrproxy.ad.infosys.com:80', 'User')
[Environment]::SetEnvironmentVariable('HTTPS_PROXY', 'http://blrproxy.ad.infosys.com:80', 'User')
```

**Use when:**
- ALL applications need proxy
- Company policy requires it

**Pros:** ✅ Affects all apps  
**Cons:** ❌ Breaks Google Cloud, ❌ Hard to troubleshoot, ❌ Not portable

## How to Check Current Settings

```powershell
# Check project-level (after loading .env)
.\load_env.ps1
Write-Host "HTTP_PROXY: $env:HTTP_PROXY"
Write-Host "HTTPS_PROXY: $env:HTTPS_PROXY"

# Check user-level (global)
[Environment]::GetEnvironmentVariable('HTTP_PROXY', 'User')

# Check system-level
[Environment]::GetEnvironmentVariable('HTTP_PROXY', 'Machine')
```

## How to Remove Global Proxy

If you accidentally set global proxy:

```powershell
# Remove User-level proxy
[Environment]::SetEnvironmentVariable('HTTP_PROXY', $null, 'User')
[Environment]::SetEnvironmentVariable('HTTPS_PROXY', $null, 'User')

# Remove System-level proxy (requires admin)
[Environment]::SetEnvironmentVariable('HTTP_PROXY', $null, 'Machine')
[Environment]::SetEnvironmentVariable('HTTPS_PROXY', $null, 'Machine')

# Restart PowerShell for changes to take effect
```

## Best Practice Workflow

### For Hackathon Development

1. **Keep proxy disabled in `.env`**
   ```env
   # HTTP_PROXY=...  # Commented out
   # HTTPS_PROXY=... # Commented out
   ```

2. **Load environment per session**
   ```powershell
   cd C:\Ravi\EduBuilder
   .\load_env.ps1
   python main.py
   ```

3. **Verify connectivity before demo**
   ```powershell
   python -c "from src.services.genai_client import GenAIClient; c = GenAIClient('gemini-2.5-flash-lite'); print('OK' if c.backend else 'FAILED')"
   ```

### For Production Deployment

1. **Use NO_PROXY bypass list**
2. **Configure at container/service level** (not global)
3. **Monitor connection failures and adjust**

## Troubleshooting

### "503 failed to connect to all addresses"
- ✅ Disable proxy in `.env`
- ✅ Reload with `.\load_env.ps1`
- ✅ Verify: `Write-Host $env:HTTP_PROXY` (should be empty)

### "LLM summary unavailable"
- ✅ Check credentials: `Test-Path $env:GOOGLE_APPLICATION_CREDENTIALS`
- ✅ Check API key: `Write-Host $env:GOOGLE_API_KEY.Length` (should be >30)
- ✅ Disable proxy (see above)

### "Gemini fallback error"
- ✅ Ensure API key is set and valid
- ✅ Disable proxy completely
- ✅ Check firewall/antivirus isn't blocking

## Current Configuration Status

Run this to see your current setup:

```powershell
Write-Host "=== Current Configuration ===" -ForegroundColor Cyan
Write-Host "Session HTTP_PROXY: $env:HTTP_PROXY"
Write-Host "Session HTTPS_PROXY: $env:HTTPS_PROXY"
Write-Host "User HTTP_PROXY: $([Environment]::GetEnvironmentVariable('HTTP_PROXY', 'User'))"
Write-Host "Machine HTTP_PROXY: $([Environment]::GetEnvironmentVariable('HTTP_PROXY', 'Machine'))"
Write-Host "`nRecommendation: All should be empty for Google Cloud to work"
```

## References

- Google Cloud Proxy Docs: https://cloud.google.com/functions/docs/networking/network-settings
- Python requests proxy: https://docs.python-requests.org/en/latest/user/advanced/#proxies
- Environment variable precedence: Process > User > Machine
