# CURL Examples for Sesame CSM 1B API

This guide provides curl examples for all API endpoints.

## Endpoint URL Format

Your RunPod endpoint URL format:
```
https://YOUR_ENDPOINT_ID.api.runpod.ai
```

Replace `YOUR_ENDPOINT_ID` with your actual endpoint ID from RunPod console.
Replace `YOUR_API_KEY` with your RunPod API key.

**Note:** Include the API key in the `X-API-Key` header for authentication.

## Health Check Endpoints

### Ping (Simple Health Check)

```bash
# Without API key (if RunPod handles it automatically)
curl https://YOUR_ENDPOINT_ID.api.runpod.ai/ping

# With API key
curl -H "X-API-Key: YOUR_API_KEY" \
     https://YOUR_ENDPOINT_ID.api.runpod.ai/ping
```

**Expected Response:**
```json
{"status":"ok"}
```

### Health Check (Detailed)

```bash
curl https://YOUR_ENDPOINT_ID.api.runpod.ai/health
```

**Expected Response (if healthy):**
```json
{
  "status": "healthy",
  "model": "saishah/sesame-csm-1b"
}
```

### Root Endpoint

```bash
curl https://YOUR_ENDPOINT_ID.api.runpod.ai/
```

**Expected Response:**
```json
{
  "service": "Sesame CSM 1B TTS API",
  "status": "running",
  "model_loaded": true
}
```

## Generate Audio Endpoint

### Basic Audio Generation

```bash
# With API key
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{"text": "Hello, this is a test message."}' \
     --output audio.wav
```

### With Language Option

```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{"text": "Hello world!", "language": "en"}' \
     --output audio.wav
```

### With Temperature Control

```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{"text": "Hello world!", "temperature": 0.7}"' \
     --output audio.wav
```

### Complete Example with All Options

```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{
       "text": "This is a complete example with all options.",
       "language": "en",
       "temperature": 0.7
     }' \
     --output complete_example.wav
```

## RunPod Handler Endpoint

This endpoint uses RunPod's serverless job format:

```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/run" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{
       "input": {
         "text": "Hello from RunPod handler!",
         "language": "en",
         "temperature": 0.7
       }
     }'
```

**Expected Response:**
```json
{
  "output": {
    "audio_base64": "UklGRiQAAABXQVZFZm10...",
    "audio_format": "wav",
    "text": "Hello from RunPod handler!"
  }
}
```

## Quick Copy-Paste Examples

### Simple Test

```bash
curl -H "X-API-Key: YOUR_API_KEY" \
     https://YOUR_ENDPOINT_ID.api.runpod.ai/ping
```

### Generate Audio

```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{"text": "Hello world!"}' \
     --output audio.wav
```

### Using Environment Variables

```bash
export ENDPOINT_ID="YOUR_ENDPOINT_ID"
export API_KEY="YOUR_API_KEY"

# Test health
curl -H "X-API-Key: ${API_KEY}" \
     "https://${ENDPOINT_ID}.api.runpod.ai/ping"

# Generate audio
curl -X POST "https://${ENDPOINT_ID}.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: ${API_KEY}" \
     -d '{"text": "Hello world!"}' \
     --output audio.wav
```

## Request Structure

### Generate Audio Request

```json
{
  "text": "Your text here",
  "language": "en",        // Optional
  "temperature": 0.7       // Optional, 0.0-2.0
}
```

### RunPod Handler Request

```json
{
  "input": {
    "text": "Your text here",
    "language": "en",      // Optional
    "temperature": 0.7     // Optional
  }
}
```

## Testing Your Endpoint

### Step 1: Get Your Endpoint ID

1. Go to [RunPod Console](https://www.runpod.io/console/serverless)
2. Find your endpoint
3. Copy the Endpoint ID (e.g., `abc123xyz`)
4. Your URL will be: `https://abc123xyz.api.runpod.ai`

### Step 2: Test Health Check

```bash
ENDPOINT_ID="YOUR_ENDPOINT_ID"
API_KEY="YOUR_API_KEY"
curl -H "X-API-Key: ${API_KEY}" \
     "https://${ENDPOINT_ID}.api.runpod.ai/ping"
```

### Step 3: Generate Audio

```bash
ENDPOINT_ID="YOUR_ENDPOINT_ID"
API_KEY="YOUR_API_KEY"
curl -X POST "https://${ENDPOINT_ID}.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: ${API_KEY}" \
     -d '{"text": "Hello, this is my first audio generation!"}' \
     --output my_first_audio.wav
```

### Step 4: Play Audio (macOS)

```bash
afplay my_first_audio.wav
```

### Step 4: Play Audio (Linux)

```bash
aplay my_first_audio.wav
# or
mpv my_first_audio.wav
```

## Common Issues

### Connection Refused / Timeout

- Endpoint may still be deploying (wait 5-10 minutes)
- Check RunPod console for endpoint status
- Verify endpoint ID is correct

### 503 Service Unavailable

- Model may still be loading (check logs in RunPod)
- Health check will show "unhealthy" until model loads
- Wait a few minutes and try again

### 404 Not Found

- Verify endpoint URL is correct
- Check endpoint is deployed and running
- Ensure you're using the correct endpoint ID

### Unauthorized / 401

- RunPod automatically handles authentication via your API key
- Make sure you're using the endpoint URL from RunPod console
- Check your RunPod account has access
