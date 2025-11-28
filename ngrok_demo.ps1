#!/usr/bin/env pwsh
# Quick Ngrok Demo Setup
# Usage: .\ngrok_demo.ps1

Write-Host "🎯 Singapore Education Counselor - Quick Demo Setup" -ForegroundColor Cyan
Write-Host ""

# Check if ngrok is installed
if (-not (Get-Command ngrok -ErrorAction SilentlyContinue)) {
    Write-Host "❌ ngrok not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install ngrok:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://ngrok.com/download" -ForegroundColor Gray
    Write-Host "2. Extract ngrok.exe to a folder in your PATH" -ForegroundColor Gray
    Write-Host "3. Sign up for free account at: https://dashboard.ngrok.com/signup" -ForegroundColor Gray
    Write-Host "4. Get auth token from: https://dashboard.ngrok.com/get-started/your-authtoken" -ForegroundColor Gray
    Write-Host "5. Run: ngrok config add-authtoken YOUR_TOKEN" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

Write-Host "✅ ngrok found" -ForegroundColor Green
Write-Host ""

# Load environment
Write-Host "📋 Loading environment variables..." -ForegroundColor Yellow
.\load_env.ps1
Write-Host ""

# Start Streamlit in background
Write-Host "🚀 Starting Streamlit app..." -ForegroundColor Yellow
$streamlit = Start-Process -FilePath "streamlit" `
    -ArgumentList "run", "streamlit_app.py", "--server.port=8501" `
    -PassThru `
    -NoNewWindow

Write-Host "⏳ Waiting for Streamlit to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start ngrok tunnel
Write-Host ""
Write-Host "🌐 Creating public tunnel with ngrok..." -ForegroundColor Yellow
Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  📱 Your public URL will appear below" -ForegroundColor Green
Write-Host "  🔗 Share this URL with judges/testers" -ForegroundColor Green
Write-Host "  ⚠️  Press Ctrl+C to stop when done" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Run ngrok (blocks until Ctrl+C)
try {
    ngrok http 8501
} finally {
    # Cleanup on exit
    Write-Host ""
    Write-Host "🛑 Stopping services..." -ForegroundColor Yellow
    Stop-Process -Id $streamlit.Id -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Demo stopped" -ForegroundColor Green
}
