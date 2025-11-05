# cURL Examples with RunPod Authentication

All requests require the `Authorization: Bearer` header with your RunPod API key.

## Get Your RunPod API Key

1. Go to: https://www.runpod.io/settings
2. Navigate to **API Keys**
3. Copy your API key

## Basic Structure

```bash
curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/ENDPOINT' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY' \
--header 'Content-Type: application/json' \
--data '{"json": "data"}'
```

## Quick Examples

### 1. Health Check (Ping)

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/ping' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY'
```

### 2. Generate Audio (Basic)

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/generate' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY' \
--header 'Content-Type: application/json' \
--data '{"text": "Hello world!"}' \
--output audio.wav
```

### 3. Generate Audio (With Options)

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/generate' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY' \
--header 'Content-Type: application/json' \
--data '{
    "text": "Hello world!",
    "language": "en",
    "temperature": 0.7
}' \
--output audio.wav
```

### 4. Health Check (Detailed)

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/health' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY'
```

### 5. Root Endpoint

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY'
```

### 6. RunPod Handler Format

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/run' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY' \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "text": "Hello from RunPod!",
        "language": "en",
        "temperature": 0.7
    }
}'
```

## Using Environment Variables

```bash
# Set your credentials
export RUNPOD_API_KEY="your-runpod-api-key-here"
export ENDPOINT_ID="oc4qjlw7gp8i5f"

# Health check
curl --location "https://${ENDPOINT_ID}.api.runpod.ai/ping" \
--header "Authorization: Bearer ${RUNPOD_API_KEY}"

# Generate audio
curl --location "https://${ENDPOINT_ID}.api.runpod.ai/generate" \
--header "Authorization: Bearer ${RUNPOD_API_KEY}" \
--header "Content-Type: application/json" \
--data '{"text": "Hello world!"}' \
--output audio.wav
```

## One-Liners (Copy & Paste)

Replace `YOUR_RUNPOD_API_KEY` with your actual key:

### Ping
```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/ping' --header 'Authorization: Bearer YOUR_RUNPOD_API_KEY'
```

### Generate Audio
```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/generate' --header 'Authorization: Bearer YOUR_RUNPOD_API_KEY' --header 'Content-Type: application/json' --data '{"text": "Hello world!"}' --output audio.wav
```

## Complete Test Script

Save as `test.sh`:

```bash
#!/bin/bash

# Set these variables
RUNPOD_API_KEY="your-runpod-api-key-here"
ENDPOINT_ID="oc4qjlw7gp8i5f"
BASE_URL="https://${ENDPOINT_ID}.api.runpod.ai"

echo "Testing endpoint: $BASE_URL"
echo ""

# Test 1: Ping
echo "1. Testing /ping..."
curl -s --location "${BASE_URL}/ping" \
--header "Authorization: Bearer ${RUNPOD_API_KEY}" | jq .
echo ""

# Test 2: Generate Audio
echo "2. Generating audio..."
curl --location "${BASE_URL}/generate" \
--header "Authorization: Bearer ${RUNPOD_API_KEY}" \
--header "Content-Type: application/json" \
--data '{"text": "This is a test of the Sesame CSM 1B API."}' \
--output test_audio.wav

if [ -f test_audio.wav ]; then
    echo "✓ Audio saved to test_audio.wav"
    echo "File size: $(ls -lh test_audio.wav | awk '{print $5}')"
else
    echo "✗ Audio generation failed"
fi
```

Make executable and run:
```bash
chmod +x test.sh
./test.sh
```

## Postman Import Format

Copy any of these into Postman's Import:

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/generate' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY' \
--header 'Content-Type: application/json' \
--data '{"text": "Hello world!"}'
```

## Important Notes

- ✅ **Required:** `Authorization: Bearer YOUR_RUNPOD_API_KEY` header
- ✅ Replace `YOUR_RUNPOD_API_KEY` with your actual API key
- ✅ Replace `oc4qjlw7gp8i5f` with your endpoint ID (if different)
- ✅ Get API key from: https://www.runpod.io/settings → API Keys
- ✅ Use `--output filename.wav` to save audio files

## Troubleshooting

**401 Unauthorized:**
- Check API key is correct
- Verify header format: `Authorization: Bearer YOUR_KEY` (space after "Bearer")
- Make sure API key has proper permissions in RunPod settings

**No response:**
- Check endpoint ID is correct
- Verify RunPod endpoint is running
- Check RunPod logs for errors

