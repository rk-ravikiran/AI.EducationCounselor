#!/bin/bash
# Deploy to Google Cloud Run
# Usage: ./deploy.sh

set -e  # Exit on error

echo "🚀 Deploying Singapore Education Counselor to Cloud Run..."

# Configuration
PROJECT_ID="gagenteducation"
REGION="us-central1"
SERVICE_NAME="edubuilder-demo"

# Set project
echo "📋 Setting GCP project..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable aiplatform.googleapis.com

# Build and deploy
echo "🏗️  Building and deploying..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_PROJECT_ID=$PROJECT_ID \
  --set-env-vars GOOGLE_LOCATION=$REGION \
  --set-env-vars MODEL_NAME=gemini-2.5-flash-lite \
  --set-env-vars DISABLE_VERTEX_EMBED=0 \
  --set-env-vars SUMMARY_LANG=en \
  --set-env-vars LLM_DEBUG=0 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 3 \
  --min-instances 0

# Get service URL
echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Service URL:"
gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)'
echo ""
echo "📊 View logs:"
echo "gcloud run logs tail $SERVICE_NAME --region $REGION"
echo ""
echo "🔍 View in console:"
echo "https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME?project=$PROJECT_ID"
