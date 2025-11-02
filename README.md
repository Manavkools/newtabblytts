# Sesame CSM 1B Text-to-Speech API for RunPod Serverless

This repository contains a complete deployment setup for the Sesame CSM 1B text-to-speech model as a serverless API on RunPod with load balancing support.

## Overview

The Sesame CSM 1B model is a state-of-the-art text-to-speech model that converts text input into high-quality audio output. This deployment package makes it accessible via a REST API that can be deployed on RunPod's serverless infrastructure with automatic load balancing.

## Features

- ✅ FastAPI-based REST API
- ✅ Automatic model loading and caching
- ✅ GPU acceleration support
- ✅ Health check endpoints for RunPod
- ✅ Streaming audio response
- ✅ RunPod serverless handler compatibility
- ✅ Docker containerization
- ✅ Load balancing ready

## Project Structure

```
.
├── .github/
│   └── workflows/     # GitHub Actions CI/CD workflows
├── app.py              # FastAPI application with model inference
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker container configuration
├── .dockerignore      # Docker ignore patterns
├── README.md          # This file
├── GITHUB_DEPLOYMENT.md # GitHub deployment guide
└── test_api.py        # API testing script
```

## Prerequisites

1. **GitHub Account**: For repository hosting and deployment
2. **RunPod Account**: With credits for serverless deployments
3. **Local Docker** (optional): For building and testing the container locally

## Deployment Options

### Option 1: GitHub Integration (Recommended) ⭐

Deploy directly from GitHub to RunPod:

1. Push this repository to GitHub
2. Connect GitHub repository to RunPod
3. RunPod automatically builds and deploys

📖 See [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) for detailed instructions.

### Option 2: Docker Hub

Build and push Docker image, then import to RunPod:

1. Build Docker image locally
2. Push to Docker Hub
3. Import from Docker Registry on RunPod

📖 See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## Quick Start

### 1. Build Docker Image

```bash
# Build the image
docker build -t YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest .

# Test locally (optional)
docker run -p 8000:8000 --gpus all YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest
```

### 2. Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push the image
docker push YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest
```

### 3. Deploy to RunPod

1. **Log in to RunPod Console**: Navigate to [RunPod Console](https://www.runpod.io/console/serverless)

2. **Create New Serverless Endpoint**:
   - Click "New Endpoint" in the Serverless section
   - Select "Import from Docker Registry"
   - Enter your Docker image: `YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest`

3. **Configure Endpoint Settings**:
   - **Endpoint Name**: `sesame-csm-1b-tts` (or your preferred name)
   - **GPU Type**: Select based on model requirements (RTX 3090 or A100 recommended)
   - **Container Disk**: 20GB minimum (for model files)
   - **Max Workers**: Set based on expected load (e.g., 5-10 for production)
   - **Timeout**: 300 seconds
   - **Environment Variables**:
     - `PORT=8000`
     - `MODEL_NAME=saishah/sesame-csm-1b` (or your model path)
     - `DEVICE=cuda`

4. **Deploy**: Click "Create Endpoint" and wait for deployment

5. **Get Endpoint URL**: RunPod will provide an endpoint URL like:
   ```
   https://YOUR_ENDPOINT_ID.api.runpod.ai
   ```

## API Endpoints

### Health Check

```bash
GET /ping
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

### Generate Audio

```bash
POST /generate
```

**Request Body:**
```json
{
  "text": "Hello, this is a test message.",
  "language": "en",  // optional
  "temperature": 0.7  // optional, default 0.7
}
```

**Response:**
- Content-Type: `audio/wav`
- Streaming audio file

**Example using curl:**
```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello world!"}' \
     --output output.wav
```

### RunPod Handler (Serverless)

```bash
POST /run
```

**Request Body (RunPod Format):**
```json
{
  "input": {
    "text": "Hello, this is a test message.",
    "language": "en",
    "temperature": 0.7
  }
}
```

**Response:**
```json
{
  "output": {
    "audio_base64": "base64_encoded_audio_string",
    "audio_format": "wav",
    "text": "Hello, this is a test message."
  }
}
```

## Usage Examples

### Python Client

```python
import requests
import base64

endpoint_url = "https://YOUR_ENDPOINT_ID.api.runpod.ai"

# Generate audio
response = requests.post(
    f"{endpoint_url}/generate",
    json={"text": "This is a test of the Sesame CSM 1B model."}
)

if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("Audio saved to output.wav")
```

### JavaScript/Node.js Client

```javascript
const fetch = require('node-fetch');
const fs = require('fs');

async function generateAudio(text) {
  const response = await fetch('https://YOUR_ENDPOINT_ID.api.runpod.ai/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  
  const audioBuffer = await response.buffer();
  fs.writeFileSync('output.wav', audioBuffer);
}

generateAudio('Hello from Node.js!');
```

## Model Configuration

The model name can be configured via the `MODEL_NAME` environment variable. Default is `saishah/sesame-csm-1b`.

To use a different model:
1. Update the `MODEL_NAME` environment variable in RunPod endpoint settings
2. Or modify the Dockerfile `ENV MODEL_NAME=your-model-path`

## Troubleshooting

### Model Not Loading

- Check GPU availability in RunPod console
- Verify container disk space (model requires ~2-4GB)
- Check logs for specific error messages
- Ensure `MODEL_NAME` points to a valid HuggingFace model

### Out of Memory Errors

- Reduce batch size or text length
- Use a GPU with more VRAM (A100 recommended)
- Reduce the number of concurrent workers

### Slow Response Times

- Increase GPU allocation
- Enable model quantization (modify app.py)
- Use a faster GPU type (A100 > RTX 3090 > RTX 3080)

## Monitoring

RunPod provides built-in monitoring:
- Request metrics
- GPU utilization
- Response times
- Error rates

Access via the RunPod Console under your endpoint's "Metrics" tab.

## Cost Optimization

- Set appropriate max workers to avoid unnecessary GPU allocation
- Configure auto-scaling based on traffic patterns
- Use spot instances for non-critical workloads
- Monitor and adjust timeout settings

## Security

For production deployments:
1. Add API key authentication to endpoints
2. Implement rate limiting
3. Add request validation
4. Enable CORS restrictions if needed

## Support

- **RunPod Documentation**: [https://docs.runpod.io](https://docs.runpod.io)
- **RunPod Discord**: [https://discord.gg/runpod](https://discord.gg/runpod)
- **Model Repository**: Check HuggingFace for model-specific documentation

## License

Please refer to the model's license on HuggingFace for usage terms.

