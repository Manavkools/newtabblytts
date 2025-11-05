#!/bin/bash

# Script to add GitHub remote and push

set -e

echo "🚀 Pushing to GitHub..."
echo ""

# Get repository URL
if [ -z "$1" ]; then
    echo "Usage: ./push_to_github.sh YOUR_REPO_URL"
    echo ""
    echo "Examples:"
    echo "  ./push_to_github.sh https://github.com/username/sesame-csm-1b-api.git"
    echo "  ./push_to_github.sh username/sesame-csm-1b-api"
    echo ""
    read -p "Enter your GitHub repository URL: " REPO_URL
else
    REPO_URL="$1"
fi

# Handle short format (username/repo-name)
if [[ ! "$REPO_URL" == *"http"* ]] && [[ ! "$REPO_URL" == *"git@"* ]]; then
    REPO_URL="https://github.com/$REPO_URL.git"
fi

echo ""
echo "Adding remote: $REPO_URL"

# Add remote
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "Repository: $(echo $REPO_URL | sed 's/\.git$//')"
echo ""
echo "Next steps:"
echo "1. Set up GitHub Secrets for CI/CD (optional):"
echo "   - Go to: https://github.com/$(echo $REPO_URL | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/settings/secrets/actions"
echo "   - Add DOCKERHUB_USERNAME"
echo "   - Add DOCKERHUB_PASSWORD"
echo ""
echo "2. Deploy to RunPod:"
echo "   - Go to: https://www.runpod.io/console/serverless"
echo "   - Click 'New Endpoint' → 'Connect GitHub Repository'"
echo "   - Select your repository"
echo ""

