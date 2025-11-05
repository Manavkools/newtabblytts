#!/bin/bash

# Quick curl examples for Sesame CSM 1B API
# Replace YOUR_ENDPOINT_ID with your actual RunPod endpoint ID

ENDPOINT_ID="YOUR_ENDPOINT_ID"
BASE_URL="https://${ENDPOINT_ID}.api.runpod.ai"

echo "=========================================="
echo "CURL Examples for Sesame CSM 1B API"
echo "=========================================="
echo ""
echo "Endpoint: $BASE_URL"
echo ""
echo "Copy and paste these commands (replace YOUR_ENDPOINT_ID first):"
echo ""

cat << 'EOF'

# ==========================================
# 1. HEALTH CHECK - Simple ping
# ==========================================
curl https://YOUR_ENDPOINT_ID.api.runpod.ai/ping

# ==========================================
# 2. HEALTH CHECK - Detailed status
# ==========================================
curl https://YOUR_ENDPOINT_ID.api.runpod.ai/health

# ==========================================
# 3. ROOT ENDPOINT - Service info
# ==========================================
curl https://YOUR_ENDPOINT_ID.api.runpod.ai/

# ==========================================
# 4. GENERATE AUDIO - Basic (saves to audio.wav)
# ==========================================
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, this is a test message."}' \
     --output audio.wav

# ==========================================
# 5. GENERATE AUDIO - With temperature
# ==========================================
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello world!", "temperature": 0.7}' \
     --output audio.wav

# ==========================================
# 6. GENERATE AUDIO - Complete example
# ==========================================
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "This is a complete example with all options.",
       "language": "en",
       "temperature": 0.7
     }' \
     --output complete_example.wav

# ==========================================
# 7. RUNPOD HANDLER FORMAT - Returns base64
# ==========================================
curl -X POST "https://YOUR_ENDPOINT_ID.api.runpod.ai/run" \
     -H "Content-Type: application/json" \
     -d '{
       "input": {
         "text": "Hello from RunPod handler!",
         "language": "en",
         "temperature": 0.7
       }
     }'

EOF

echo ""
echo "=========================================="
echo "Quick Test Commands"
echo "=========================================="
echo ""
echo "# Test health check:"
echo "curl ${BASE_URL}/ping"
echo ""
echo "# Generate audio:"
echo "curl -X POST \"${BASE_URL}/generate\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"text\": \"Hello world!\"}' \\"
echo "     --output test_audio.wav"
echo ""

