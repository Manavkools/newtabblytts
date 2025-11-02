# GitHub Quick Start Guide

Get your repository on GitHub and deploy to RunPod in 5 minutes!

## 🚀 Quick Setup

### Step 1: Initialize and Push to GitHub

```bash
# Run the automated script
./init_github.sh
```

This script will:
- Initialize git (if needed)
- Help you add GitHub remote
- Commit all files
- Push to GitHub

**Or manually:**

```bash
# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Sesame CSM 1B TTS API"

# Add GitHub remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/sesame-csm-1b-api.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Create GitHub Repository (if needed)

1. Go to https://github.com/new
2. Repository name: `sesame-csm-1b-api`
3. **Don't** initialize with README (we already have files)
4. Click "Create repository"
5. Copy the repository URL and use it in Step 1

### Step 3: Deploy to RunPod

RunPod builds directly from your GitHub repository - no Docker Hub needed!

### Step 4: Deploy to RunPod via GitHub

1. Go to [RunPod Console](https://www.runpod.io/console/serverless)
2. Click **"New Endpoint"**
3. Select **"Connect GitHub Repository"** or **"Build from Dockerfile"**
4. Authorize RunPod to access GitHub (if prompted)
5. Select your repository: `YOUR_USERNAME/sesame-csm-1b-api`
6. Configure:
   - Endpoint name: `sesame-csm-1b-tts`
   - GPU: RTX 3090 or A100
   - Container Disk: 25GB
   - Max Workers: 5
   - Port: 8000
7. Add Environment Variables:
   ```
   PORT=8000
   MODEL_NAME=saishah/sesame-csm-1b
   DEVICE=cuda
   ```
8. Click **"Create Endpoint"**
9. Wait 5-10 minutes for build and deployment

### Step 5: Test Your Deployment

```bash
# Replace YOUR_ENDPOINT_ID with your actual endpoint ID
curl https://YOUR_ENDPOINT_ID.api.runpod.ai/ping

# Generate audio
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello from GitHub!"}' \
     --output audio.wav
```

## ✅ Checklist

- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] GitHub Secrets configured (for CI/CD)
- [ ] RunPod endpoint created
- [ ] GitHub repository connected to RunPod
- [ ] Endpoint deployed and tested

## 📚 More Information

- **Detailed GitHub Guide**: See [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md)
- **General Deployment**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Quick Reference**: See [QUICK_START.md](QUICK_START.md)

## 🔄 Updating Your Deployment

After making changes:

```bash
git add .
git commit -m "Update API"
git push origin main
```

RunPod will automatically rebuild (if auto-redeploy enabled) or manually redeploy from console.

## 🆘 Troubleshooting

**Can't find "Connect GitHub Repository" option?**
- Try "Build from Dockerfile" option instead
- Or use "Import from Docker Registry" and use GitHub Actions to build

**Build fails?**
- Check RunPod logs
- Verify Dockerfile is in repository root
- Ensure all files are committed and pushed

**Need help?**
- Check [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) for detailed troubleshooting
- Join RunPod Discord: https://discord.gg/runpod

