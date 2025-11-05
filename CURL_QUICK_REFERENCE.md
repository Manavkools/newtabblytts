# Quick CURL Reference

## Basic Structure (with API Key)

```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{"text": "Your text here"}' \
     --output audio.wav
```

## Common Commands

### 1. Health Check (with API Key)
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
     https://YOUR_ENDPOINT_ID.api.runpod.ai/ping
```

### 2. Generate Audio (Basic with API Key)
```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{"text": "Hello world!"}' \
     --output audio.wav
```

### 3. Generate Audio (With Options and API Key)
```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{
       "text": "Hello world!",
       "language": "en",
       "temperature": 0.7
     }' \
     --output audio.wav
```

## Complete Examples with API Key

### Using Environment Variables
```bash
export ENDPOINT_ID="YOUR_ENDPOINT_ID"
export API_KEY="YOUR_API_KEY"

# Health check
curl -H "X-API-Key: ${API_KEY}" \
     "https://${ENDPOINT_ID}.api.runpod.ai/ping"

# Generate audio
curl -X POST "https://${ENDPOINT_ID}.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: ${API_KEY}" \
     -d '{"text": "Hello world!"}' \
     --output audio.wav
```

### One-liner with API Key
```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{"text": "Hello world!"}' \
     --output audio.wav
```

## JSON Request Body Structure

```json
{
  "text": "Your text to convert to speech",
  "language": "en",        // Optional
  "temperature": 0.7       // Optional (0.0-2.0)
}
```

## Notes

- Replace `YOUR_ENDPOINT_ID` with your actual RunPod endpoint ID
- Replace `YOUR_API_KEY` with your RunPod API key
- API key goes in the `X-API-Key` header
- Audio is returned as a WAV file
- Use `--output filename.wav` to save the audio file

