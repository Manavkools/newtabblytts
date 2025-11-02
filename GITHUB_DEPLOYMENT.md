# GitHub Deployment Guide for RunPod

This guide walks you through setting up your GitHub repository and deploying to RunPod using GitHub integration.

## Prerequisites

- GitHub account
- RunPod account with credits

## Step 1: Create GitHub Repository

### Option 1: Using GitHub Web Interface

1. Go to [GitHub](https://github.com/new)
2. Repository name: `sesame-csm-1b-api` (or your preferred name)
3. Description: "Sesame CSM 1B Text-to-Speech API for RunPod Serverless"
4. Choose **Public** or **Private**
5. **Do NOT** initialize with README (we already have one)
6. Click "Create repository"

### Option 2: Using Command Line

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Sesame CSM 1B TTS API"

# Add GitHub remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Deploy Directly to RunPod

RunPod will build directly from your GitHub repository using the Dockerfile - no Docker Hub needed!

## Step 3: Deploy to RunPod via GitHub Integration

### Direct GitHub Integration (Recommended)

1. **Log in to RunPod Console**
   - Go to [RunPod Console](https://www.runpod.io/console/serverless)

2. **Create New Endpoint**
   - Click **"New Endpoint"**
   - Select **"Connect GitHub Repository"** (if available)
   - OR select **"Build from Dockerfile"** and connect GitHub

3. **Select Your Repository**
   - Authorize RunPod to access GitHub (if needed)
   - Select your repository: `YOUR_USERNAME/sesame-csm-1b-api`
   - Select branch: `main` or `master`

4. **Configure Endpoint**
   - **Endpoint Name**: `sesame-csm-1b-tts`
   - **Dockerfile Path**: `./Dockerfile` (default)
   - **GPU Type**: RTX 3090 or A100
   - **Container Disk**: 25 GB
   - **Max Workers**: 5
   - **Port**: 8000

5. **Environment Variables**
   Add these in the environment variables section:
   ```
   PORT=8000
   MODEL_NAME=saishah/sesame-csm-1b
   DEVICE=cuda
   ```

6. **Deploy**
   - Click **"Create Endpoint"**
   - RunPod will build from your GitHub repository
   - Wait 5-10 minutes for first build


## Step 4: Auto-Deploy on Git Push (Optional)

To enable automatic redeployment when you push code:

1. **Set Up RunPod Webhook** (if supported)
   - In RunPod endpoint settings, enable auto-redeploy
   - Add GitHub webhook URL

2. **Or Use GitHub Actions**
   - The included workflow will rebuild image on push
   - Manually redeploy endpoint on RunPod (or use API)

## Step 5: Verify Deployment

```bash
# Replace YOUR_ENDPOINT_ID with your actual endpoint ID
curl https://YOUR_ENDPOINT_ID.api.runpod.ai/ping

# Test audio generation
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello from GitHub deployment!"}' \
     --output test_audio.wav
```

## GitHub Repository Structure

Your repository should have this structure:

```
sesame-csm-1b-api/
├── .github/
│   └── workflows/
│       ├── build.yml              # CI/CD workflow
│       └── runpod-deploy.yml      # Deployment workflow
├── app.py                         # FastAPI application
├── Dockerfile                     # Docker configuration
├── requirements.txt               # Python dependencies
├── .dockerignore                  # Docker ignore patterns
├── .gitignore                     # Git ignore patterns
├── README.md                      # Project documentation
├── DEPLOYMENT_GUIDE.md            # Deployment instructions
├── GITHUB_DEPLOYMENT.md           # This file
└── test_api.py                    # API testing script
```

## Continuous Integration Setup

The repository includes GitHub Actions workflows:

### Build Workflow (`.github/workflows/build.yml`)

- Automatically builds Docker image on push
- Pushes to Docker Hub
- Triggers on:
  - Push to `main`/`master` branch
  - Tag creation (e.g., `v1.0.0`)
  - Pull requests (builds but doesn't push)

### Deploy Workflow (`.github/workflows/runpod-deploy.yml`)

- Manual deployment trigger
- Can be extended with RunPod API integration

## Updating Your Deployment

### Method 1: Automatic (if auto-redeploy enabled)

1. Make changes to your code
2. Commit and push:
   ```bash
   git add .
   git commit -m "Update API"
   git push origin main
   ```
3. RunPod will automatically rebuild and redeploy

### Method 2: Manual

1. Push changes to GitHub
2. Go to RunPod Console
3. Find your endpoint
4. Click **"Redeploy"** or **"Rebuild"**

## Troubleshooting

### GitHub Actions Build Fails

- Check Actions tab for error logs
- Verify Dockerfile syntax is correct
- Ensure all dependencies are in requirements.txt

### RunPod Build Fails

- Check RunPod logs for error messages
- Verify Dockerfile is in repository root
- Ensure all dependencies are in requirements.txt
- Check container disk size (increase if needed)

### Deployment Not Updating

- Verify you're pushing to correct branch
- Check if auto-redeploy is enabled
- Manually trigger redeploy from RunPod console

## Benefits of GitHub Integration

✅ **Version Control**: Track all changes to your deployment
✅ **CI/CD**: Automatic builds on code changes
✅ **Collaboration**: Multiple developers can contribute
✅ **Rollback**: Easy to revert to previous versions
✅ **Documentation**: Code and docs in one place
✅ **Automation**: Less manual work for deployments

## Next Steps

1. ✅ Push your code to GitHub
2. ✅ Set up GitHub secrets (for CI/CD)
3. ✅ Connect repository to RunPod
4. ✅ Configure endpoint settings
5. ✅ Deploy and test
6. ✅ Set up monitoring and alerts

## Resources

- **GitHub Docs**: https://docs.github.com
- **RunPod Docs**: https://docs.runpod.io
- **GitHub Actions**: https://github.com/features/actions
- **RunPod GitHub Integration**: Check RunPod console for latest features

## Support

For issues:
- Check GitHub Actions logs
- Review RunPod deployment logs
- Consult RunPod Discord: https://discord.gg/runpod

