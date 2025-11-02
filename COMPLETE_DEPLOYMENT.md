# Complete End-to-End Deployment Guide

This guide will help you deploy the Sesame CSM 1B API to RunPod completely, from start to finish.

## Quick Start: Automated Deployment

Run this single command to do everything automatically:

```bash
./auto_deploy.sh
```

This script will:
1. ✅ Check if Docker is installed (install if needed on macOS)
2. ✅ Build the Docker image
3. ✅ Push to Docker Hub
4. ✅ Provide RunPod deployment instructions

## What You Need

Before starting, make sure you have:

- [ ] **Docker Hub account** (free) - https://hub.docker.com/signup
- [ ] **RunPod account** with credits - https://www.runpod.io/signup
- [ ] **Internet connection** (for downloading images and pushing)

## Step-by-Step Automated Deployment

### Option 1: Fully Automated (Recommended)

```bash
# Run the automated deployment script
./auto_deploy.sh
```

The script will guide you through:
- Docker installation (if needed)
- Docker Hub login
- Building the Docker image
- Pushing to Docker Hub
- RunPod deployment instructions

### Option 2: Manual Step-by-Step

If you prefer manual control:

#### 1. Install Docker (if needed)

**macOS:**
```bash
brew install --cask docker
open -a Docker
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (optional)
sudo usermod -aG docker $USER
```

#### 2. Build Docker Image

```bash
# Login to Docker Hub
docker login

# Build the image (replace YOUR_USERNAME)
docker build -t YOUR_USERNAME/sesame-csm-1b-api:latest .

# Push to Docker Hub
docker push YOUR_USERNAME/sesame-csm-1b-api:latest
```

#### 3. Deploy on RunPod

1. Go to: https://www.runpod.io/console/serverless
2. Click "New Endpoint"
3. Select "Import from Docker Registry"
4. Enter: `YOUR_USERNAME/sesame-csm-1b-api:latest`
5. Configure:
   - **GPU Type**: RTX 3090 or A100
   - **Container Disk**: 25GB
   - **Max Workers**: 5
   - **Port**: 8000
6. Add Environment Variables:
   - `PORT=8000`
   - `MODEL_NAME=saishah/sesame-csm-1b`
   - `DEVICE=cuda`
7. Click "Create Endpoint"
8. Wait 2-5 minutes for deployment

## Verifying Deployment

Once deployed, test your endpoint:

```bash
# Replace YOUR_ENDPOINT_ID with your actual endpoint ID
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, this is a test!"}' \
     --output test_audio.wav

# Play the audio (macOS)
afplay test_audio.wav
```

Or use the test script:

```bash
python3 test_api.py https://YOUR_ENDPOINT_ID.api.runpod.ai
```

## Environment Variables

You can set these before running `auto_deploy.sh`:

```bash
export DOCKERHUB_USERNAME="your_username"
export DOCKERHUB_PASSWORD="your_password"  # Optional, will prompt if not set
```

## Troubleshooting

### Docker Not Starting

**macOS:**
```bash
# Start Docker Desktop
open -a Docker

# Or via command line
brew services start docker
```

**Linux:**
```bash
sudo systemctl start docker
```

### Build Fails

- Check internet connection
- Ensure Docker has enough disk space (need ~10GB free)
- Try rebuilding: `docker build --no-cache -t YOUR_USERNAME/sesame-csm-1b-api:latest .`

### Push Fails

- Verify Docker Hub credentials: `docker login`
- Check internet connection
- Ensure you have permissions on the Docker Hub repository

### RunPod Deployment Issues

- Verify GPU selection has enough VRAM (RTX 3090 or A100 recommended)
- Increase container disk size if model fails to load
- Check RunPod logs for specific errors
- Ensure port 8000 is exposed

## What Happens During Deployment

1. **Docker Build** (5-15 minutes)
   - Downloads base Python image
   - Installs system dependencies
   - Installs Python packages
   - Copies application code

2. **Docker Push** (5-10 minutes)
   - Uploads image to Docker Hub
   - Image size: ~2-5 GB

3. **RunPod Deployment** (2-5 minutes)
   - RunPod pulls image from Docker Hub
   - Starts container on GPU
   - Downloads model (~1-2 GB)
   - Model initialization

## Cost Estimation

**RunPod Pricing** (approximate):
- RTX 3090: $0.29/hour per worker
- A100 40GB: $1.19/hour per worker
- RTX 3080: $0.24/hour per worker

**With auto-scaling:**
- Idle: $0 (scales to zero workers)
- Active: Pay only for active workers
- Typical cost: $5-20/day for moderate usage

## Next Steps

After successful deployment:

1. ✅ Test your endpoint with sample requests
2. 📊 Monitor metrics in RunPod console
3. 🔧 Adjust worker count based on traffic
4. 🔒 Add API authentication for production
5. 📈 Set up monitoring/alerting

## Support

- **RunPod Docs**: https://docs.runpod.io
- **RunPod Discord**: https://discord.gg/runpod
- **Docker Docs**: https://docs.docker.com

## Scripts Available

- `auto_deploy.sh` - Complete automated deployment
- `deploy.sh` - Docker build and push only
- `deploy_to_runpod.py` - Python deployment script
- `test_api.py` - Test your deployed endpoint

Run `./auto_deploy.sh` to get started! 🚀

