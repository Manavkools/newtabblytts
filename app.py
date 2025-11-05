"""
Sesame CSM 1B Text-to-Speech API for RunPod Serverless
"""
import os
import io
import logging
from typing import Optional
from contextlib import asynccontextmanager
import torch
from fastapi import FastAPI, HTTPException, Header, Security, Depends
from fastapi.security import APIKeyHeader
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model variables (will be set during startup)
model = None
processor = None
device = None

# Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "saishah/sesame-csm-1b")
PORT = int(os.getenv("PORT", 8000))
# Allow PORT_HEALTH to be same as PORT by default for RunPod LB
PORT_HEALTH = int(os.getenv("PORT_HEALTH", PORT))
DEVICE = os.getenv("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
API_KEY = os.getenv("API_KEY", os.getenv("RUNPOD_API_KEY", ""))  # Optional app-level API key
HF_TOKEN = os.getenv("HF_TOKEN", os.getenv("HUGGINGFACEHUB_API_TOKEN", ""))  # Optional HF token for gated models
TRUST_REMOTE_CODE = os.getenv("TRUST_REMOTE_CODE", "false").lower() in {"1", "true", "yes"}

# API Key Security - accepts X-API-Key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(x_api_key: Optional[str] = Security(api_key_header)):
    """
    Verify custom API key (optional additional security layer).
    RunPod handles primary authentication via Authorization: Bearer header at load balancer level.
    This is an optional extra security layer if you set API_KEY environment variable.
    """
    # If no custom API key is configured, allow all requests
    # RunPod's load balancer already handles authentication
    if not API_KEY:
        return True
    
    # If custom API key is configured (optional extra security), require it
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Missing custom API key. Please provide X-API-Key header."
        )
    
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Invalid custom API key."
        )
    
    return True


class TextInput(BaseModel):
    """Input model for text-to-speech requests"""
    text: str = Field(..., description="Text to convert to speech", min_length=1, max_length=500)
    language: Optional[str] = Field(None, description="Language code (optional)")
    temperature: Optional[float] = Field(0.7, description="Generation temperature", ge=0.0, le=2.0)


def load_model():
    """Load the Sesame CSM 1B model and processor"""
    global model, processor, device
    
    # Verify transformers is installed before trying to import
    try:
        import transformers
        logger.info(f"Transformers version: {transformers.__version__}")
    except ImportError as e:
        logger.error(f"CRITICAL: transformers library is not installed: {e}")
        logger.error("Install with: pip install transformers")
        raise ImportError("transformers library not found. Please install it.")
    
    try:
        from transformers import AutoProcessor, AutoModelForTextToSpeech
        
        logger.info(f"Loading model: {MODEL_NAME}")
        logger.info(f"Device: {DEVICE}")
        
        # Set device
        device = torch.device(DEVICE if torch.cuda.is_available() and DEVICE == "cuda" else "cpu")
        logger.info(f"Using device: {device}")
        
        # Load processor
        logger.info("Loading processor...")
        processor = AutoProcessor.from_pretrained(
            MODEL_NAME,
            token=HF_TOKEN or None,
            trust_remote_code=TRUST_REMOTE_CODE,
        )
        logger.info("Processor loaded successfully")
        
        # Load model
        logger.info("Loading model...")
        if device.type == "cuda":
            model = AutoModelForTextToSpeech.from_pretrained(
                MODEL_NAME,
                torch_dtype=torch.float16,
                device_map="auto",
                token=HF_TOKEN or None,
                trust_remote_code=TRUST_REMOTE_CODE,
            )
        else:
            model = AutoModelForTextToSpeech.from_pretrained(
                MODEL_NAME,
                torch_dtype=torch.float32,
                token=HF_TOKEN or None,
                trust_remote_code=TRUST_REMOTE_CODE,
            )
            model = model.to(device)
        
        model.eval()
        
        logger.info(f"Model loaded successfully on {device}")
        logger.info(f"Model config: {model.config if hasattr(model, 'config') else 'N/A'}")
        
    except ImportError as e:
        logger.error(f"Import error: {str(e)}")
        logger.error("Failed to import from transformers library")
        logger.error("Check that transformers is properly installed")
        raise
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {repr(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise


# Lifespan event handler for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    try:
        logger.info("Starting application...")
        load_model()
        logger.info("API startup complete")
    except Exception as e:
        logger.error(f"Failed to start API: {str(e)}")
        logger.error(f"Error details: {repr(e)}")
        # Don't raise - allow health check to indicate failure
        # Model will be None, which health check will detect
    
    yield
    
    # Shutdown (if needed)
    logger.info("Shutting down application...")


# Initialize FastAPI app with lifespan handler
app = FastAPI(title="Sesame CSM 1B TTS API", version="1.0.0", lifespan=lifespan)


@app.get("/")
async def root(api_key_valid: bool = Depends(verify_api_key)):
    """Root endpoint"""
    return {
        "service": "Sesame CSM 1B TTS API",
        "status": "running",
        "model_loaded": model is not None,
        "auth_enabled": bool(API_KEY)
    }


@app.get("/health")
async def health_check(api_key_valid: bool = Depends(verify_api_key)):
    """Health check endpoint for RunPod"""
    if model is None:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "message": "Model not loaded"}
        )
    return {"status": "healthy", "model": MODEL_NAME}


@app.get("/ping")
async def ping():
    """
    Ping endpoint for RunPod health checks.
    Note: RunPod load balancer requires Authorization header, but this endpoint
    has no custom authentication for health monitoring purposes.
    """
    return {"status": "ok"}


@app.post("/generate")
async def generate_audio(input_data: TextInput, api_key_valid: bool = Depends(verify_api_key)):
    """
    Generate audio from text using Sesame CSM 1B model
    
    Args:
        input_data: TextInput containing text and optional parameters
    
    Returns:
        Audio file as streaming response
    """
    if model is None or processor is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please check server logs."
        )
    
    try:
        logger.info(f"Generating audio for text: {input_data.text[:50]}...")
        
        # Process input text
        # Handle processor call - some models use different parameter names
        try:
            if input_data.language:
                inputs = processor(text=input_data.text, return_tensors="pt", language=input_data.language)
            else:
                inputs = processor(text=input_data.text, return_tensors="pt")
        except TypeError:
            # If language parameter not supported, use without it
            inputs = processor(text=input_data.text, return_tensors="pt")
        
        # Move inputs to device
        inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v 
                 for k, v in inputs.items()}
        
        # Generate audio
        with torch.no_grad():
            if device.type == "cuda":
                with torch.cuda.amp.autocast():
                    # Try to generate with temperature parameter
                    try:
                        audio_output = model.generate(**inputs, temperature=input_data.temperature)
                    except TypeError:
                        # If temperature not supported, generate without it
                        audio_output = model.generate(**inputs)
            else:
                try:
                    audio_output = model.generate(**inputs, temperature=input_data.temperature)
                except TypeError:
                    audio_output = model.generate(**inputs)
        
        # Convert to numpy and then to bytes
        if isinstance(audio_output, torch.Tensor):
            audio_np = audio_output.cpu().numpy()
        else:
            audio_np = audio_output
        
        # Get sampling rate (usually 16000 or 22050 for TTS models)
        # Check multiple possible locations for sample_rate
        sampling_rate = (
            getattr(model.config, 'sample_rate', None) or
            getattr(model.config, 'sampling_rate', None) or
            getattr(processor, 'sampling_rate', None) or
            22050  # Default fallback
        )
        
        # Convert numpy array to WAV bytes
        import numpy as np
        import soundfile as sf
        
        # Ensure audio is in the right format (1D array)
        if len(audio_np.shape) > 1:
            audio_np = audio_np.flatten()
        
        # Normalize audio - handle different output formats
        # Some models output normalized [-1, 1], others [0, 1], or raw values
        audio_max = np.abs(audio_np).max()
        if audio_max > 1.0:
            # Scale down if values are outside [-1, 1]
            audio_normalized = np.clip(audio_np / audio_max, -1.0, 1.0)
        else:
            audio_normalized = np.clip(audio_np, -1.0, 1.0)
        
        if audio_normalized.dtype != np.float32:
            audio_normalized = audio_normalized.astype(np.float32)
        
        # Create WAV file in memory
        audio_bytes = io.BytesIO()
        sf.write(audio_bytes, audio_normalized, sampling_rate, format='WAV')
        audio_bytes.seek(0)
        
        logger.info("Audio generation successful")
        
        return StreamingResponse(
            audio_bytes,
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=generated_audio.wav"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generating audio: {str(e)}"
        )


@app.post("/run")
async def runpod_handler(job: dict, api_key_valid: bool = Depends(verify_api_key)):
    """
    RunPod serverless handler endpoint
    Accepts RunPod job format and returns result
    """
    try:
        # Extract input from RunPod job format
        input_data = job.get("input", {})
        text = input_data.get("text", "")
        
        if not text:
            return {
                "error": "No text provided in input"
            }
        
        # Create TextInput object
        text_input = TextInput(
            text=text,
            language=input_data.get("language"),
            temperature=input_data.get("temperature", 0.7)
        )
        
        # Generate audio
        result = await generate_audio(text_input)
        
        # For RunPod, we need to return base64 encoded audio or URL
        # Since we're streaming, let's convert to base64
        import base64
        
        audio_bytes = b""
        async for chunk in result.body_iterator:
            audio_bytes += chunk
        
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        return {
            "output": {
                "audio_base64": audio_base64,
                "audio_format": "wav",
                "text": text
            }
        }
        
    except Exception as e:
        logger.error(f"Error in RunPod handler: {str(e)}", exc_info=True)
        return {
            "error": str(e)
        }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )

