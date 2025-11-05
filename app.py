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
    speaker_id: Optional[str] = Field("0", description="Speaker id string for conversation role")
    reference_audio_url: Optional[str] = Field(None, description="URL to reference audio to condition voice")


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
        from transformers import AutoProcessor, AutoModel
        
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
            model = AutoModel.from_pretrained(
                MODEL_NAME,
                torch_dtype=torch.float16,
                device_map="auto",
                token=HF_TOKEN or None,
                trust_remote_code=TRUST_REMOTE_CODE,
            )
        else:
            model = AutoModel.from_pretrained(
                MODEL_NAME,
                torch_dtype=torch.float32,
                token=HF_TOKEN or None,
                trust_remote_code=TRUST_REMOTE_CODE,
            )
            model = model.to(device)
        
        model.eval()
        
        logger.info(f"Model loaded successfully on {device}")
        logger.info(f"Model config: {model.config if hasattr(model, 'config') else 'N/A'}")
        if not hasattr(model, "generate"):
            logger.warning("Model does not expose a 'generate' method; the repository may define a different inference API when using trust_remote_code.")
        
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
        
        # For CSM, using chat template with speaker id and optional reference audio yields better consistency
        conversation = []
        
        # If a reference audio URL is provided, fetch and include as context
        if input_data.reference_audio_url:
            try:
                import requests
                import soundfile as sf
                import numpy as np
                from io import BytesIO
                from scipy.signal import resample_poly
                import tempfile
                
                resp = requests.get(input_data.reference_audio_url, timeout=20)
                resp.raise_for_status()
                audio_data, sr = sf.read(BytesIO(resp.content), always_2d=False)
                if audio_data.ndim > 1:
                    audio_data = audio_data.mean(axis=1)
                target_sr = (
                    getattr(getattr(processor, 'feature_extractor', None) or object(), 'sampling_rate', None) or
                    24000
                )
                if sr != target_sr and sr > 0:
                    # Resample with polyphase filtering
                    # Compute up/down factors approximately
                    # Use simple resample_poly with gcd approximation
                    up = target_sr
                    down = sr
                    audio_data = resample_poly(audio_data, up, down)
                audio_data = np.asarray(audio_data, dtype=np.float32)
                # Save to a temporary WAV file and pass its path
                tmp_wav = tempfile.NamedTemporaryFile(prefix="ref_audio_", suffix=".wav", delete=False)
                sf.write(tmp_wav.name, audio_data, int(target_sr), format='WAV')
                # Context turn with reference audio file path
                conversation.append({
                    "role": str(input_data.speaker_id or "0"),
                    "content": [
                        {"type": "audio", "path": tmp_wav.name},
                    ],
                })
            except Exception as e:
                logger.warning(f"Failed to fetch/process reference audio: {e}")
        
        # Add the actual text prompt turn
        conversation.append({
            "role": str(input_data.speaker_id or "0"),
            "content": [{"type": "text", "text": input_data.text}],
        })
        
        # Prepare inputs; fall back to simple tokenization if template unsupported
        try:
            inputs = processor.apply_chat_template(
                conversation,
                tokenize=True,
                return_dict=True,
            )
        except Exception:
            inputs = processor(text=input_data.text, return_tensors="pt")
        
        # Move inputs to device
        inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}
        
        # Generate audio - for CSM, output_audio=True yields decoded waveform codes
        with torch.no_grad():
            gen_kwargs = {}
            # Some repos don't accept temperature; pass only if supported
            try:
                gen_kwargs["temperature"] = input_data.temperature
            except Exception:
                pass
            if device.type == "cuda":
                with torch.amp.autocast("cuda"):
                    try:
                        audio_output = model.generate(**inputs, output_audio=True, **gen_kwargs)
                    except TypeError:
                        audio_output = model.generate(**inputs, output_audio=True)
            else:
                try:
                    audio_output = model.generate(**inputs, output_audio=True, **gen_kwargs)
                except TypeError:
                    audio_output = model.generate(**inputs, output_audio=True)
        
        # Serialize audio using processor if available, else manual write
        audio_bytes = io.BytesIO()
        try:
            # processor.save_audio can save a single or list of audios
            # Save to a temporary file-like by using soundfile directly after extracting array
            raise NotImplementedError
        except Exception:
            import numpy as np
            import soundfile as sf
            
            # audio_output may be a list/tuple or tensor; handle common cases
            if isinstance(audio_output, (list, tuple)):
                audio_arr = audio_output[0]
            else:
                audio_arr = audio_output
            
            if hasattr(audio_arr, "cpu"):
                audio_arr = audio_arr.cpu().numpy()
            audio_arr = np.asarray(audio_arr)
            if audio_arr.ndim > 1:
                # flatten to mono if multi-channel
                audio_arr = audio_arr.squeeze()
            
            # Use 24000 Hz as CSM default per model card if processor doesn't expose
            sampling_rate = (
                getattr(model.config, 'sample_rate', None) or
                getattr(model.config, 'sampling_rate', None) or
                getattr(getattr(processor, 'feature_extractor', None) or object(), 'sampling_rate', None) or
                24000
            )
            
            # Ensure float32 within [-1, 1]
            audio_arr = np.clip(audio_arr, -1.0, 1.0).astype(np.float32)
            sf.write(audio_bytes, audio_arr, int(sampling_rate), format='WAV')
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

