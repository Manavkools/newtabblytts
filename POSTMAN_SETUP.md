# Postman Setup Guide - Fix 401 Unauthorized

## Quick Fix

The 401 error is from RunPod's load balancer authentication. You need:

1. **Get your RunPod API key** from https://www.runpod.io/settings → API Keys
2. **Include it in the `Authorization: Bearer` header** in all Postman requests

## Step-by-Step Solution

### Step 1: Get Your RunPod API Key

1. Go to [RunPod Settings](https://www.runpod.io/settings)
2. Click on **API Keys** section
3. Copy your existing API key OR create a new one
4. Save it securely

### Step 2: Configure Postman Request

#### Option A: Using cURL Import (Recommended)

**Copy this cURL command** (replace YOUR_RUNPOD_API_KEY with your actual RunPod API key):

```bash
curl --location 'https://oc4qjlw7gp8i5f.api.runpod.ai/generate' \
--header 'Authorization: Bearer YOUR_RUNPOD_API_KEY' \
--header 'Content-Type: application/json' \
--data '{
    "text": "Hello world!"
}'
```

**In Postman:**
1. Click **Import** button (top left)
2. Select **Raw text** tab
3. Paste the cURL command above
4. Replace `your-secret-key-123` with your actual API key
5. Click **Import**

#### Option B: Manual Setup in Postman

**Create a new POST request:**

1. **Method:** `POST`
2. **URL:** `https://oc4qjlw7gp8i5f.api.runpod.ai/generate`
3. **Headers tab:**
   - `Authorization` = `Bearer YOUR_RUNPOD_API_KEY` ← Your RunPod API key from settings
   - `Content-Type` = `application/json`
4. **Body tab:**
   - Select **raw**
   - Select **JSON** (from dropdown)
   - Paste:
   ```json
   {
       "text": "Hello world!"
   }
   ```
5. Click **Send**

### Step 3: Test Health Check (No Auth Required)

First, test the ping endpoint (doesn't require API key):

**GET Request:**
- **URL:** `https://oc4qjlw7gp8i5f.api.runpod.ai/ping`
- **Headers:**
  - `Authorization` = `Bearer YOUR_RUNPOD_API_KEY`
- **Body:** None

This should return: `{"status":"ok"}`

### Step 4: Test Generate Audio (Requires API Key)

**POST Request:**
- **URL:** `https://oc4qjlw7gp8i5f.api.runpod.ai/generate`
- **Headers:**
  - `Authorization` = `Bearer YOUR_RUNPOD_API_KEY` ← **Your RunPod API key from settings**
  - `Content-Type` = `application/json`
- **Body (raw JSON):**
```json
{
    "text": "Hello from Postman!"
}
```

## Complete Postman Request Examples

### Request 1: Health Check (Ping)
```
GET https://oc4qjlw7gp8i5f.api.runpod.ai/ping

Headers:
Authorization: Bearer YOUR_RUNPOD_API_KEY
```

### Request 2: Generate Audio
```
POST https://oc4qjlw7gp8i5f.api.runpod.ai/generate

Headers:
Authorization: Bearer YOUR_RUNPOD_API_KEY
Content-Type: application/json

Body (raw JSON):
{
    "text": "Hello world!"
}
```

## Postman Environment Variables (Recommended)

Set up variables to avoid typing the API key each time:

1. Click **Environments** (left sidebar)
2. Click **+** to create new environment
3. Name it "RunPod API"
4. Add these variables:
   - `base_url` = `https://oc4qjlw7gp8i5f.api.runpod.ai`
   - `api_key` = `your-secret-key-123` ← Same as RunPod API_KEY
5. Click **Save**
6. Select this environment from dropdown (top right)

**Now use in requests:**
- URL: `{{base_url}}/generate`
- Header: `X-API-Key: {{api_key}}`

## Troubleshooting 401 Unauthorized

### Issue 1: API Key Not Set in RunPod
**Solution:**
- Go to RunPod endpoint → Environment Variables
- Add: `API_KEY` = `your-secret-key`
- Redeploy endpoint

### Issue 2: API Key Mismatch
**Solution:**
- The `X-API-Key` header in Postman must **exactly match** the `API_KEY` in RunPod
- Check for extra spaces or typos
- Case-sensitive: `mykey` ≠ `MyKey`

### Issue 3: Header Name Wrong
**Solution:**
- Must be exactly: `X-API-Key` (capital X, capital API, capital Key)
- Not: `x-api-key` or `X-Api-Key`

### Issue 4: Endpoint Not Redeployed
**Solution:**
- After setting API_KEY in RunPod, you must redeploy
- Go to endpoint → Click "Redeploy" or wait for auto-redeploy

## Quick Test Commands

### Test 1: Ping (should work without API key)
```bash
curl https://oc4qjlw7gp8i5f.api.runpod.ai/ping
```

**Expected:** `{"status":"ok"}`

### Test 2: Generate (requires API key)
```bash
curl -X POST "https://oc4qjlw7gp8i5f.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-secret-key-123" \
     -d '{"text": "Test"}'
```

**Expected:** Binary audio data (WAV file)

## Disable Authentication (For Testing)

If you want to test without authentication temporarily:

1. In RunPod, **remove** or **empty** the `API_KEY` environment variable
2. Redeploy endpoint
3. Now requests work without `X-API-Key` header

**⚠️ Warning:** Only for testing! Always enable API key in production.

## Postman Collection JSON

Save this as a Postman Collection file:

```json
{
    "info": {
        "name": "Sesame CSM 1B API",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Health Check",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "https://oc4qjlw7gp8i5f.api.runpod.ai/ping",
                    "protocol": "https",
                    "host": ["oc4qjlw7gp8i5f", "api", "runpod", "ai"],
                    "path": ["ping"]
                }
            }
        },
        {
            "name": "Generate Audio",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    },
                    {
                        "key": "X-API-Key",
                        "value": "{{api_key}}"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"text\": \"Hello world!\"\n}"
                },
                "url": {
                    "raw": "{{base_url}}/generate",
                    "host": ["{{base_url}}"],
                    "path": ["generate"]
                }
            }
        }
    ],
    "variable": [
        {
            "key": "base_url",
            "value": "https://oc4qjlw7gp8i5f.api.runpod.ai"
        },
        {
            "key": "api_key",
            "value": "your-secret-key-123"
        }
    ]
}
```

Import this JSON file into Postman to get a ready-made collection!

## Summary

**The 401 error is normal and expected until you:**
1. ✅ Set `API_KEY` environment variable in RunPod
2. ✅ Use that same key in Postman's `X-API-Key` header
3. ✅ Make sure they match exactly

Once both are set and matching, the 401 will go away! 🎉

