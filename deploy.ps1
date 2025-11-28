# Deploy to Google Cloud Run
# Usage: .\deploy.ps1

$ErrorActionPreference = "Stop"

Write-Host "🚀 Deploying Singapore Education Counselor to Cloud Run..." -ForegroundColor Cyan

# Configuration
$PROJECT_ID = "gagenteducation"
$REGION = "us-central1"
$SERVICE_NAME = "edubuilder-demo"

# Set project
Write-Host "📋 Setting GCP project..." -ForegroundColor Yellow
gcloud config set project $PROJECT_ID

# Enable required APIs
Write-Host "🔧 Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com  
gcloud services enable artifactregistry.googleapis.com
gcloud services enable aiplatform.googleapis.com

# Build and deploy
Write-Host "🏗️  Building and deploying..." -ForegroundColor Yellow
gcloud run deploy $SERVICE_NAME `
  --source . `
  --region $REGION `
  --platform managed `
  --allow-unauthenticated `
  --set-env-vars GOOGLE_PROJECT_ID=$PROJECT_ID `
  --set-env-vars GOOGLE_LOCATION=$REGION `
  --set-env-vars MODEL_NAME=gemini-2.5-flash-lite `
  --set-env-vars DISABLE_VERTEX_EMBED=0 `
  --set-env-vars SUMMARY_LANG=en `
  --set-env-vars LLM_DEBUG=0 `
  --memory 2Gi `
  --cpu 2 `
  --timeout 300 `
  --max-instances 3 `
  --min-instances 0

# Get service URL
Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Service URL:" -ForegroundColor Cyan
$url = gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)'
Write-Host $url -ForegroundColor White
Write-Host ""
Write-Host "📊 View logs:" -ForegroundColor Yellow
Write-Host "gcloud run logs tail $SERVICE_NAME --region $REGION" -ForegroundColor Gray
Write-Host ""
Write-Host "🔍 View in console:" -ForegroundColor Yellow
Write-Host "https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME?project=$PROJECT_ID" -ForegroundColor Gray
