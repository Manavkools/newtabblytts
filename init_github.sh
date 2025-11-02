#!/bin/bash

# Script to initialize and push to GitHub repository

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}${BLUE}GitHub Repository Initialization${NC}\n"

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    echo -e "${GREEN}✓ Git repository initialized${NC}\n"
fi

# Check if remote exists
if git remote | grep -q origin; then
    REMOTE_URL=$(git remote get-url origin)
    echo -e "GitHub remote already set: ${BLUE}$REMOTE_URL${NC}"
    read -p "Continue with this remote? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled"
        exit 0
    fi
else
    echo "No GitHub remote configured."
    read -p "Enter your GitHub repository URL (or username/repo-name): " REPO_INPUT
    
    if [[ $REPO_INPUT == *"http"* ]] || [[ $REPO_INPUT == *"git@"* ]]; then
        REPO_URL="$REPO_INPUT"
    else
        # Assume format: username/repo-name
        REPO_URL="https://github.com/$REPO_INPUT.git"
    fi
    
    git remote add origin "$REPO_URL"
    echo -e "${GREEN}✓ Added remote: $REPO_URL${NC}\n"
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "You have uncommitted changes."
    read -p "Commit them now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Initial commit: Sesame CSM 1B TTS API deployment"
        echo -e "${GREEN}✓ Changes committed${NC}\n"
    fi
else
    echo "No uncommitted changes."
    read -p "Create initial commit? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Initial commit: Sesame CSM 1B TTS API deployment"
        echo -e "${GREEN}✓ Initial commit created${NC}\n"
    fi
fi

# Determine default branch
DEFAULT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

# Check if branch exists
if ! git rev-parse --verify "$DEFAULT_BRANCH" >/dev/null 2>&1; then
    git checkout -b "$DEFAULT_BRANCH" 2>/dev/null || git branch "$DEFAULT_BRANCH"
fi

# Push to GitHub
echo "Pushing to GitHub..."
echo "Branch: $DEFAULT_BRANCH"
read -p "Continue? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push -u origin "$DEFAULT_BRANCH"
    echo ""
    echo -e "${GREEN}✓ Successfully pushed to GitHub!${NC}\n"
    
    REPO_NAME=$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')
    echo -e "${BOLD}Next steps:${NC}"
    echo "1. Go to: https://github.com/$REPO_NAME"
    echo "2. Set up GitHub Secrets (for CI/CD):"
    echo "   - Settings → Secrets → Actions"
    echo "   - Add DOCKERHUB_USERNAME"
    echo "   - Add DOCKERHUB_PASSWORD"
    echo ""
    echo "3. Deploy to RunPod:"
    echo "   - Go to: https://www.runpod.io/console/serverless"
    echo "   - Click 'New Endpoint'"
    echo "   - Select 'Connect GitHub Repository'"
    echo "   - Choose your repository: $REPO_NAME"
    echo ""
    echo "📖 See GITHUB_DEPLOYMENT.md for detailed instructions"
else
    echo "Push cancelled. You can push later with:"
    echo "  git push -u origin $DEFAULT_BRANCH"
fi

