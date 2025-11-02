#!/usr/bin/env python3
"""
Test script for Sesame CSM 1B API
Usage: python test_api.py [endpoint_url]
"""
import sys
import requests
import json

def test_api(endpoint_url="http://localhost:8000"):
    """Test the API endpoints"""
    
    print(f"Testing API at: {endpoint_url}\n")
    
    # Test 1: Health Check
    print("1. Testing /ping endpoint...")
    try:
        response = requests.get(f"{endpoint_url}/ping", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 2: Health Check
    print("2. Testing /health endpoint...")
    try:
        response = requests.get(f"{endpoint_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 3: Root endpoint
    print("3. Testing / endpoint...")
    try:
        response = requests.get(f"{endpoint_url}/", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 4: Generate Audio
    print("4. Testing /generate endpoint...")
    test_text = "Hello, this is a test of the Sesame CSM 1B text-to-speech API."
    try:
        payload = {
            "text": test_text,
            "temperature": 0.7
        }
        print(f"   Sending request with text: '{test_text}'")
        response = requests.post(
            f"{endpoint_url}/generate",
            json=payload,
            timeout=120  # Longer timeout for inference
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            # Save audio file
            with open("test_output.wav", "wb") as f:
                f.write(response.content)
            print(f"   ✅ Audio saved to test_output.wav")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            print(f"   Size: {len(response.content)} bytes\n")
        else:
            print(f"   ❌ Error: {response.text}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 5: RunPod Handler
    print("5. Testing /run endpoint (RunPod format)...")
    try:
        payload = {
            "input": {
                "text": "This is a test using the RunPod handler format.",
                "temperature": 0.7
            }
        }
        print(f"   Sending RunPod format request...")
        response = requests.post(
            f"{endpoint_url}/run",
            json=payload,
            timeout=120
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        
        if "error" in result:
            print(f"   ❌ Error: {result['error']}\n")
        else:
            output = result.get("output", {})
            audio_b64 = output.get("audio_base64", "")
            if audio_b64:
                import base64
                audio_bytes = base64.b64decode(audio_b64)
                with open("test_output_runpod.wav", "wb") as f:
                    f.write(audio_bytes)
                print(f"   ✅ Audio saved to test_output_runpod.wav")
                print(f"   Audio format: {output.get('audio_format')}\n")
            else:
                print(f"   Response: {json.dumps(result, indent=2)}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    print("Testing complete!")

if __name__ == "__main__":
    endpoint = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    test_api(endpoint)

