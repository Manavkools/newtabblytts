# Quick Start Guide

## 🚀 Deploy in 5 Minutes

### 1. Build & Push Docker Image

```bash
# Replace YOUR_DOCKERHUB_USERNAME with your actual username
./deploy.sh YOUR_DOCKERHUB_USERNAME

# Or manually:
docker build -t YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest .
docker push YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest
```

### 2. Deploy to RunPod

1. Go to [RunPod Serverless Console](https://www.runpod.io/console/serverless)
2. Click "New Endpoint"
3. Select "Import from Docker Registry"
4. Enter: `YOUR_DOCKERHUB_USERNAME/sesame-csm-1b-api:latest`
5. Configure:
   - GPU: RTX 3090 or A100 (recommended)
   - Container Disk: 25GB
   - Max Workers: 5
   - Port: 8000
   - Environment Variables:
     ```
     PORT=8000
     MODEL_NAME=saishah/sesame-csm-1b
     DEVICE=cuda
     ```
6. Click "Create Endpoint"

### 3. Test Your API

```bash
# Get your endpoint URL from RunPod (format: https://ENDPOINT_ID.api.runpod.ai)

# Health check
curl https://YOUR_ENDPOINT_ID.api.runpod.ai/ping

# Generate audio
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello world!"}' \
     --output audio.wav
```

### 4. Use in Your Code

**Python:**
```python
import requests

response = requests.post(
    "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate",
    json={"text": "Your text here"}
)

with open("output.wav", "wb") as f:
    f.write(response.content)
```

**JavaScript:**
```javascript
const response = await fetch('https://YOUR_ENDPOINT_ID.api.runpod.ai/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'Your text here' })
});

const audioBlob = await response.blob();
// Use audioBlob as needed
```

## 📋 API Endpoints

- `GET /ping` - Health check
- `GET /health` - Detailed health status
- `POST /generate` - Generate audio from text
- `POST /run` - RunPod serverless handler format

## 📝 Request Format

```json
{
  "text": "Your text to convert to speech",
  "language": "en",  // optional
  "temperature": 0.7  // optional, 0.0-2.0
}
```

## 🔧 Troubleshooting

- **503 Error**: Model not loaded - check GPU/disk space
- **Slow responses**: Use faster GPU or increase workers
- **Out of memory**: Use GPU with more VRAM (A100)

For detailed help, see `DEPLOYMENT_GUIDE.md` and `README.md`.

