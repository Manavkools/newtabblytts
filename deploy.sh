#!/bin/bash

# Deployment script for Sesame CSM 1B API to RunPod
# Usage: ./deploy.sh YOUR_DOCKERHUB_USERNAME

set -e

DOCKERHUB_USERNAME=${1:-"your_dockerhub_username"}
IMAGE_NAME="sesame-csm-1b-api"
VERSION=${2:-"latest"}
FULL_IMAGE_NAME="${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${VERSION}"

echo "🚀 Building Docker image..."
docker build -t "${FULL_IMAGE_NAME}" .

echo "✅ Build complete!"
echo ""
echo "📦 To push to Docker Hub, run:"
echo "   docker push ${FULL_IMAGE_NAME}"
echo ""
echo "🧪 To test locally, run:"
echo "   docker run -p 8000:8000 --gpus all ${FULL_IMAGE_NAME}"
echo ""
echo "🌐 After pushing, deploy to RunPod:"
echo "   1. Go to https://www.runpod.io/console/serverless"
echo "   2. Click 'New Endpoint'"
echo "   3. Select 'Import from Docker Registry'"
echo "   4. Enter: ${FULL_IMAGE_NAME}"
echo "   5. Configure GPU and workers"
echo "   6. Deploy!"

# Optional: auto-push if DOCKER_PASSWORD is set
if [ -n "$DOCKER_PASSWORD" ]; then
    echo ""
    echo "🔐 Docker password detected, pushing to Docker Hub..."
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
    docker push "${FULL_IMAGE_NAME}"
    echo "✅ Pushed to Docker Hub!"
fi

