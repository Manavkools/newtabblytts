# Postman cURL Examples

Copy these cURL commands directly into Postman's "Import" feature or use them to create requests.

## Quick Import to Postman

1. Open Postman
2. Click **Import** (top left)
3. Select **Raw text** tab
4. Paste any cURL command below
5. Click **Import**

## Base URL

Replace these placeholders:
- `YOUR_ENDPOINT_ID` → Your RunPod endpoint ID
- `YOUR_API_KEY` → Your API key (set in RunPod environment variables)

## 1. Health Check (Ping)

**GET Request - No auth required**

```bash
curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/ping'
```

## 2. Health Check (Detailed)

**GET Request - Requires API Key**

```bash
curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/health' \
--header 'X-API-Key: YOUR_API_KEY'
```

## 3. Root Endpoint

**GET Request - Requires API Key**

```bash
curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/' \
--header 'X-API-Key: YOUR_API_KEY'
```

## 4. Generate Audio (Basic)

**POST Request - Requires API Key**

```bash
curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/generate' \
--header 'Content-Type: application/json' \
--header 'X-API-Key: YOUR_API_KEY' \
--data '{
    "text": "Hello, this is a test message."
}'
```

**To save audio file:**
```bash
curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/generate' \
--header 'Content-Type: application/json' \
--header 'X-API-Key: YOUR_API_KEY' \
--data '{
    "text": "Hello, this is a test message."
}' \
--output audio.wav
```

## 5. Generate Audio (With Language)

**POST Request - Requires API Key**

```bash
curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/generate' \
--header 'Content-Type: application/json' \
--header 'X-API-Key: YOUR_API_KEY' \
--data '{
    "text": "Hello world!",
    "language": "en"
}'
```

## 6. Generate Audio (With Temperature)

**POST Request - Requires API Key**

```bash
curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/generate' \
--header 'Content-Type: application/json' \
--header 'X-API-Key: YOUR_API_KEY' \
--data '{
    "text": "Hello world!",
    "temperature": 0.7
}'
```

## 7. Generate Audio (Complete Example)

**POST Request - Requires API Key**

```bash
curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/generate' \
--header 'Content-Type: application/json' \
--header 'X-API-Key: YOUR_API_KEY' \
--data '{
    "text": "This is a complete example with all options.",
    "language": "en",
    "temperature": 0.7
}'
```

## 8. RunPod Handler Format

**POST Request - Requires API Key**

```bash
curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/run' \
--header 'Content-Type: application/json' \
--header 'X-API-Key: YOUR_API_KEY' \
--data '{
    "input": {
        "text": "Hello from RunPod handler!",
        "language": "en",
        "temperature": 0.7
    }
}'
```

## Postman Collection Setup

### Method 1: Import Individual Requests

1. Copy any cURL command above
2. In Postman, click **Import**
3. Paste the cURL command
4. Postman will automatically parse:
   - URL
   - Method (GET/POST)
   - Headers
   - Body (for POST requests)

### Method 2: Create Manually

#### Health Check (GET)
- **Method:** GET
- **URL:** `https://YOUR_ENDPOINT_ID.api.runpod.ai/ping`
- **Headers:** None (no auth required)

#### Generate Audio (POST)
- **Method:** POST
- **URL:** `https://YOUR_ENDPOINT_ID.api.runpod.ai/generate`
- **Headers:**
  - `Content-Type: application/json`
  - `X-API-Key: YOUR_API_KEY`
- **Body (raw JSON):**
```json
{
    "text": "Hello world!",
    "language": "en",
    "temperature": 0.7
}
```

## Setting Up Postman Environment Variables

1. Click **Environments** (left sidebar)
2. Click **+** to create new environment
3. Add variables:
   - `endpoint_id` = `YOUR_ENDPOINT_ID`
   - `api_key` = `YOUR_API_KEY`
   - `base_url` = `https://{{endpoint_id}}.api.runpod.ai`

4. Use in requests:
   - URL: `{{base_url}}/generate`
   - Header: `X-API-Key: {{api_key}}`

## Postman Pre-request Script (Optional)

Add this to set API key automatically:

```javascript
pm.environment.set("api_key", "YOUR_API_KEY");
pm.environment.set("endpoint_id", "YOUR_ENDPOINT_ID");
```

## Testing Audio Response in Postman

1. Send the POST request to `/generate`
2. Response will be binary audio data
3. Click **Send and Download** or save response
4. Save as `.wav` file

**Note:** Postman shows binary responses as encoded text. To save properly:
1. Click **Save Response** → **Save to a file**
2. Name it `audio.wav`
3. Play the file in a media player

## Quick Reference Table

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/ping` | GET | No | Simple health check |
| `/health` | GET | Yes | Detailed health status |
| `/` | GET | Yes | Service information |
| `/generate` | POST | Yes | Generate audio from text |
| `/run` | POST | Yes | RunPod handler format |

## Example Workflow

1. **Test Health:**
   ```bash
   curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/ping'
   ```

2. **Generate Audio:**
   ```bash
   curl --location 'https://YOUR_ENDPOINT_ID.api.runpod.ai/generate' \
   --header 'Content-Type: application/json' \
   --header 'X-API-Key: YOUR_API_KEY' \
   --data '{"text": "Hello from Postman!"}' \
   --output audio.wav
   ```

3. **Play Audio** (macOS):
   ```bash
   afplay audio.wav
   ```

## Troubleshooting in Postman

**401 Unauthorized:**
- Check `X-API-Key` header is included
- Verify API key matches RunPod environment variable
- Ensure API key is set in RunPod endpoint settings

**503 Service Unavailable:**
- Model may still be loading
- Wait 2-5 minutes after deployment
- Check `/ping` endpoint first

**Empty/Binary Response:**
- Normal for audio generation
- Save response as `.wav` file
- Response is binary audio data

