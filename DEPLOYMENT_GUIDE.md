# Step-by-Step Deployment Guide for RunPod Serverless

This guide walks you through deploying the Sesame CSM 1B TTS API to RunPod serverless with load balancing.

## Prerequisites Checklist

- [ ] Docker installed on your local machine
- [ ] Docker Hub account (free tier works)
- [ ] RunPod account with credits
- [ ] Basic terminal/command line knowledge

## Step 1: Build the Docker Image

### 1.1 Navigate to Project Directory

```bash
cd /path/to/testfile
```

### 1.2 Build the Image

Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub username:

```bash
./deploy.sh YOUR_DOCKERHUB_USERNAME
```

Or manually:

```bash
docker build -t YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest .
```

### 1.3 Test Locally (Optional)

If you have a GPU locally:

```bash
docker run -p 8000:8000 --gpus all YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest
```

Then test:

```bash
python test_api.py http://localhost:8000
```

## Step 2: Push to Docker Hub

### 2.1 Login to Docker Hub

```bash
docker login
```

Enter your Docker Hub username and password when prompted.

### 2.2 Push the Image

```bash
docker push YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest
```

**Note**: This may take several minutes depending on your internet connection and image size.

## Step 3: Deploy to RunPod

### 3.1 Access RunPod Console

1. Go to [https://www.runpod.io/console/serverless](https://www.runpod.io/console/serverless)
2. Log in to your RunPod account

### 3.2 Create New Serverless Endpoint

1. Click the **"New Endpoint"** button (top right)
2. Select **"Import from Docker Registry"**
3. Enter your Docker image name:
   ```
   YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest
   ```

### 3.3 Configure Endpoint Settings

#### Basic Settings:
- **Endpoint Name**: `sesame-csm-1b-tts` (or your preferred name)
- **Network Volume**: Optional - recommended if you want to cache model files (saves download time on cold starts)

#### GPU Configuration:
- **GPU Type**: 
  - **Recommended**: RTX 3090 (24GB) or A100 (40GB/80GB)
  - **Budget option**: RTX 3080 (10GB) - may have memory constraints
  - **Minimum**: RTX 3060 (12GB) - may be slower

#### Container Settings:
- **Container Disk**: 
  - **Minimum**: 20GB (for model files and dependencies)
  - **Recommended**: 25-30GB for buffer
- **Max Workers**: 
  - **Development**: 1-2 workers
  - **Production**: 5-10 workers (adjust based on traffic)
- **Idle Timeout**: 5 seconds (workers shut down after inactivity)
- **Flashboot**: Enabled (faster cold starts)

#### Environment Variables:
Add these in the environment variables section:

```
PORT=8000
MODEL_NAME=saishah/sesame-csm-1b
DEVICE=cuda
```

#### Expose HTTP Ports:
- **Port**: `8000`
- **Type**: HTTP

### 3.4 Review and Deploy

1. Review all settings
2. Click **"Create Endpoint"**
3. Wait for deployment (typically 2-5 minutes)

## Step 4: Get Your Endpoint URL

After deployment, RunPod will provide:

1. **Endpoint URL**: `https://YOUR_ENDPOINT_ID.api.runpod.ai`
2. **Endpoint ID**: Use this for API calls

Copy and save your endpoint URL - you'll need it for API calls!

## Step 5: Test Your Deployment

### 5.1 Health Check

```bash
curl https://YOUR_ENDPOINT_ID.api.runpod.ai/ping
```

Expected response:
```json
{"status":"ok"}
```

### 5.2 Test Audio Generation

```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, this is a test!"}' \
     --output test_audio.wav
```

### 5.3 Using Python Test Script

Update `test_api.py` with your endpoint URL, or pass it as argument:

```bash
python test_api.py https://YOUR_ENDPOINT_ID.api.runpod.ai
```

## Step 6: Configure Load Balancing (Optional)

RunPod serverless automatically provides load balancing when you set `Max Workers > 1`. The load balancer will:

- Distribute requests across workers
- Scale up workers based on demand
- Scale down workers during low traffic

### Load Balancing Configuration:

1. Go to your endpoint settings
2. Under "Scaling":
   - **Min Workers**: 0 (scale to zero when idle)
   - **Max Workers**: Your desired maximum (e.g., 10)
   - **Target Workers**: 2-3 (desired number during normal traffic)

## Step 7: Monitor Your Deployment

### 7.1 RunPod Console Metrics

1. Go to your endpoint in RunPod console
2. Click on **"Metrics"** tab
3. Monitor:
   - Request rate
   - Response times
   - GPU utilization
   - Worker count
   - Error rate

### 7.2 Check Logs

1. Click on **"Logs"** tab in your endpoint
2. View real-time logs for debugging
3. Look for any errors or warnings

## Common Issues and Solutions

### Issue: Model Not Loading

**Symptoms**: Health check returns 503, `/health` shows "Model not loaded"

**Solutions**:
1. Check GPU availability - ensure GPU type has enough VRAM
2. Increase container disk size (model files need ~2-4GB)
3. Check logs for specific error messages
4. Verify `MODEL_NAME` environment variable is correct

### Issue: Out of Memory

**Symptoms**: 500 errors, GPU OOM errors in logs

**Solutions**:
1. Use a GPU with more VRAM (A100 recommended)
2. Reduce text input length
3. Reduce number of concurrent workers
4. Enable model quantization (modify app.py)

### Issue: Slow Response Times

**Symptoms**: Requests taking >10 seconds

**Solutions**:
1. Use a faster GPU (A100 > RTX 3090 > RTX 3080)
2. Increase number of workers to handle concurrent requests
3. Check if model is loading on each request (should be cached)
4. Monitor GPU utilization - may need more workers

### Issue: Cold Start Delays

**Symptoms**: First request takes 30-60 seconds

**Solutions**:
1. Enable Flashboot in endpoint settings
2. Use Network Volume to cache model files
3. Keep minimum 1 worker (increase cost but eliminates cold starts)
4. Pre-warm endpoint with periodic health checks

### Issue: Docker Build Fails

**Solutions**:
1. Ensure Docker is running
2. Check internet connection for pulling base images
3. Verify Dockerfile syntax
4. Try building with `--no-cache` flag:
   ```bash
   docker build --no-cache -t YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest .
   ```

## Cost Estimation

### Typical Costs (approximate):

- **RTX 3090**: $0.29/hour per worker
- **A100 40GB**: $1.19/hour per worker
- **RTX 3080**: $0.24/hour per worker

### Cost Optimization Tips:

1. Set appropriate idle timeout (5 seconds recommended)
2. Scale to zero workers when idle (min workers = 0)
3. Use spot instances if available
4. Monitor and adjust max workers based on actual traffic
5. Consider using smaller GPU for development, larger for production

## Next Steps

1. **Add Authentication**: Implement API keys for production use
2. **Rate Limiting**: Add rate limiting to prevent abuse
3. **Caching**: Implement response caching for frequently used text
4. **Monitoring**: Set up external monitoring (e.g., Datadog, New Relic)
5. **CI/CD**: Automate deployments using GitHub Actions or similar

## Support Resources

- **RunPod Documentation**: [https://docs.runpod.io](https://docs.runpod.io)
- **RunPod Discord**: [https://discord.gg/runpod](https://discord.gg/runpod)
- **HuggingFace Model**: Search for "sesame-csm-1b" on HuggingFace

## Troubleshooting Checklist

If something doesn't work:

- [ ] Docker image builds successfully
- [ ] Docker image pushed to Docker Hub
- [ ] Endpoint created in RunPod
- [ ] Environment variables set correctly
- [ ] Port 8000 exposed
- [ ] GPU selected with sufficient VRAM
- [ ] Container disk size sufficient
- [ ] Health check returns OK
- [ ] Model loads successfully (check logs)
- [ ] Test request returns audio file

If all checkboxes are checked but still having issues, check the RunPod logs for specific error messages.

