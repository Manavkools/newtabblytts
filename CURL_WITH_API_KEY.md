# CURL Examples with API Key

Quick reference for using curl with API key authentication.

## Format

Always include the API key in the `X-API-Key` header:

```bash
-H "X-API-Key: YOUR_API_KEY"
```

## Quick Examples

### 1. Health Check
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
     https://YOUR_ENDPOINT_ID.api.runpod.ai/ping
```

### 2. Generate Audio (Basic)
```bash
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{"text": "Hello world!"}' \
     --output audio.wav
```

### 3. Generate Audio (Full Example)
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

## Using Environment Variables

```bash
# Set your credentials
export ENDPOINT_ID="YOUR_ENDPOINT_ID"
export API_KEY="YOUR_API_KEY"

# Use them in curl commands
curl -H "X-API-Key: ${API_KEY}" \
     "https://${ENDPOINT_ID}.api.runpod.ai/ping"

curl -X POST "https://${ENDPOINT_ID}.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: ${API_KEY}" \
     -d '{"text": "Hello world!"}' \
     --output audio.wav
```

## Complete Test Script

```bash
#!/bin/bash

ENDPOINT_ID="YOUR_ENDPOINT_ID"
API_KEY="YOUR_API_KEY"

# Test ping
echo "Testing /ping..."
curl -H "X-API-Key: ${API_KEY}" \
     "https://${ENDPOINT_ID}.api.runpod.ai/ping"

echo ""
echo "Generating audio..."
curl -X POST "https://${ENDPOINT_ID}.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: ${API_KEY}" \
     -d '{"text": "This is a test!"}' \
     --output test.wav

echo "Audio saved to test.wav"
```

## Request Structure

```bash
curl -X POST "URL" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY" \
     -d '{"json": "data"}' \
     --output file.wav
```

## Where to Get Your API Key

1. Go to [RunPod Console](https://www.runpod.io/console/settings/api-keys)
2. Create or copy your API key
3. Use it in the `X-API-Key` header

