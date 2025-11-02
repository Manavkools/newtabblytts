# RunPod Authentication Guide

## Important: RunPod Load Balancer Authentication

RunPod's load balancer requires authentication for **ALL requests** using the `Authorization: Bearer` header with your RunPod API key. This happens **before** requests reach your application.

## How to Get Your RunPod API Key

1. Go to [RunPod Settings](https://www.runpod.io/settings)
2. Navigate to **API Keys** section
3. Click **Create API Key** or copy existing key
4. Save it securely - you'll need it for all requests

## Using Authentication in Requests

### cURL Examples

**All requests must include the Authorization header:**

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/ping' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY'
```

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/generate' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY' \
--header 'Content-Type: application/json' \
--data '{
    "text": "Hello world!"
}'
```

### Postman Setup

**Method 1: Import cURL**
```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/generate' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY' \
--header 'Content-Type: application/json' \
--data '{"text": "Hello!"}'
```

**Method 2: Manual Setup**
1. **Headers:**
   - `Authorization` = `Bearer YOUR_RUNPOD_API_KEY`
   - `Content-Type` = `application/json`
2. **Body (raw JSON):**
```json
{
    "text": "Hello world!"
}
```

## Complete Examples

### 1. Health Check (Ping)

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/ping' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY'
```

**Expected Response:**
```json
{"status":"ok"}
```

### 2. Generate Audio

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/generate' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY' \
--header 'Content-Type: application/json' \
--data '{
    "text": "Hello from RunPod!"
}' \
--output audio.wav
```

### 3. Generate Audio (Full Options)

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

## Using Environment Variables

```bash
export RUNPOD_API_KEY="your-runpod-api-key-here"
export ENDPOINT_ID="oc4qjlw7gp8i5f"

# Ping
curl --location "https://${ENDPOINT_ID}.api.runpod.ai/ping" \
--header "Authorization: Bearer ${RUNPOD_API_KEY}"

# Generate
curl --location "https://${ENDPOINT_ID}.api.runpod.ai/generate" \
--header "Authorization: Bearer ${RUNPOD_API_KEY}" \
--header "Content-Type: application/json" \
--data '{"text": "Hello!"}' \
--output audio.wav
```

## Postman Environment Setup

1. Create new environment in Postman
2. Add variables:
   - `runpod_api_key` = `YOUR_RUNPOD_API_KEY`
   - `endpoint_id` = `oc4qjlw7gp8i5f`
   - `base_url` = `https://{{endpoint_id}}.api.runpod.ai`

3. In request headers:
   - `Authorization` = `Bearer {{runpod_api_key}}`

## Optional: Additional Security Layer

You can optionally set a custom `API_KEY` environment variable in RunPod for extra security:

1. In RunPod endpoint → Environment Variables → Add:
   ```
   API_KEY = your-custom-secret-key
   ```

2. Then also include `X-API-Key` header in requests:
   ```
   X-API-Key: your-custom-secret-key
   ```

This is **optional** - the `Authorization: Bearer` header is **required**.

## Authentication Flow

```
Client Request
    ↓
RunPod Load Balancer
    ↓ (checks Authorization: Bearer header)
    ↓ [401 if missing/invalid]
Your FastAPI Application
    ↓ (optional: checks X-API-Key if API_KEY env var is set)
    ↓ [401 if custom key doesn't match]
Endpoint Handler
```

## Troubleshooting

### 401 Unauthorized

**Cause:** Missing or invalid `Authorization: Bearer` header

**Solution:**
1. Get your RunPod API key from settings
2. Include in header: `Authorization: Bearer YOUR_KEY`
3. Make sure there's a space after "Bearer"

### Still Getting 401?

1. Verify API key is correct in RunPod settings
2. Check header format: `Authorization: Bearer YOUR_KEY` (not `Bearer: YOUR_KEY`)
3. Ensure API key has proper permissions in RunPod
4. Try regenerating API key if issues persist

## Summary

- ✅ **Required:** `Authorization: Bearer YOUR_RUNPOD_API_KEY` header
- ✅ **Optional:** `X-API-Key: YOUR_CUSTOM_KEY` header (if you set API_KEY env var)
- ✅ **Get API Key:** https://www.runpod.io/settings → API Keys

