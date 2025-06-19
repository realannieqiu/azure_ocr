import os
import asyncio
import aiohttp
import aiofiles
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import tempfile
import json
import time
import base64
import logging
from typing import Dict, Any

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="Project Evaluation MVP", version="1.0.0")

# FIXED: Correct CORS configuration for port 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000", "*"],  # Added port 8000 and wildcard for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class EvaluationResponse(BaseModel):
    innovation_score: int
    feasibility_score: int
    market_potential_score: int
    innovation_justification: str
    feasibility_justification: str
    market_potential_justification: str
    overall_feedback: str

class OCRService:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.key = os.getenv("AZURE_OPENAI_KEY")
        self.deployment_name = os.getenv("DEPLOYMENT_NAME")
        self.api_version = os.getenv("API_VERSION")
        
        # Debug logging
        logger.info(f"OCR Service initialized with endpoint: {self.endpoint}")
        logger.info(f"Deployment name: {self.deployment_name}")
        logger.info(f"API version: {self.api_version}")
        
        if not all([self.endpoint, self.key, self.deployment_name, self.api_version]):
            missing = []
            if not self.endpoint: missing.append("AZURE_OPENAI_ENDPOINT")
            if not self.key: missing.append("AZURE_OPENAI_KEY")
            if not self.deployment_name: missing.append("DEPLOYMENT_NAME")
            if not self.api_version: missing.append("API_VERSION")
            raise ValueError(f"Missing environment variables: {missing}")
    
    async def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from image using Azure OpenAI GPT-4o vision model"""
        
        try:
            logger.info(f"Processing file: {file_path}")
            
            # Read and encode the image file
            async with aiofiles.open(file_path, "rb") as f:
                file_data = await f.read()
            
            logger.info(f"File size: {len(file_data)} bytes")
            
            # Convert to base64
            base64_image = base64.b64encode(file_data).decode('utf-8')
            logger.info(f"Base64 encoded, length: {len(base64_image)}")
            
            # Determine the image format
            image_format = self._get_image_format(file_path)
            logger.info(f"Detected image format: {image_format}")
            
            # FIXED: Corrected URL construction
            url = f"{self.endpoint.rstrip('/')}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
            logger.info(f"Making request to: {url}")
            
            headers = {
                "api-key": self.key,
                "Content-Type": "application/json"
            }
            
            # FIXED: Improved payload structure based on research
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert OCR system. Extract all visible text from the provided image accurately. Return only the extracted text without any additional commentary or formatting."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please extract all text from this image. Return only the text content, preserving the original structure as much as possible."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{image_format};base64,{base64_image}",
                                    "detail": "high"  # For better OCR accuracy
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.1
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
                logger.info("Sending request to Azure OpenAI...")
                async with session.post(url, headers=headers, json=payload) as response:
                    response_text = await response.text()
                    logger.info(f"Response status: {response.status}")
                    logger.info(f"Response: {response_text[:500]}...")  # Log first 500 chars
                    
                    if response.status != 200:
                        logger.error(f"Azure OpenAI API error: {response_text}")
                        raise HTTPException(status_code=400, detail=f"OCR extraction failed: {response_text}")
                    
                    try:
                        result = json.loads(response_text)
                        extracted_text = result["choices"][0]["message"]["content"]
                        logger.info(f"Successfully extracted text: {len(extracted_text)} characters")
                        return extracted_text.strip()
                    except (KeyError, IndexError, json.JSONDecodeError) as e:
                        logger.error(f"Failed to parse response: {e}")
                        raise HTTPException(status_code=500, detail=f"Failed to extract text from OpenAI response: {str(e)}")
                        
        except Exception as e:
            logger.error(f"OCR error: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
    def _get_image_format(self, file_path: str) -> str:
        """Determine image format from file path"""
        file_extension = file_path.lower().split('.')[-1]
        format_mapping = {
            'jpg': 'jpeg',
            'jpeg': 'jpeg', 
            'png': 'png',
            'gif': 'gif',
            'bmp': 'bmp',
            'tiff': 'tiff',
            'tif': 'tiff'
        }
        return format_mapping.get(file_extension, 'jpeg')

class OpenAIService:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.key = os.getenv("AZURE_OPENAI_KEY")
        self.deployment_name = os.getenv("DEPLOYMENT_NAME")
        self.api_version = os.getenv("API_VERSION")
        
        if not all([self.endpoint, self.key, self.deployment_name, self.api_version]):
            raise ValueError("Azure OpenAI credentials not found in environment variables")
    
    async def evaluate_project(self, extracted_text: str) -> EvaluationResponse:
        """Evaluate project using Azure OpenAI Chat Completion API"""
        
        prompt = f"""Read the following project description and rate it from 0 to 10 in the areas of Innovation, Feasibility, and Market Potential. Justify each score briefly.

Project Description:
{extracted_text}

You MUST respond with ONLY a valid JSON object in exactly this format:
{{
    "innovation_score": 7,
    "feasibility_score": 8,
    "market_potential_score": 6,
    "innovation_justification": "Brief explanation for innovation score",
    "feasibility_justification": "Brief explanation for feasibility score", 
    "market_potential_justification": "Brief explanation for market potential score",
    "overall_feedback": "General feedback about the project"
}}

Do not include any text before or after the JSON. Respond with valid JSON only."""

        url = f"{self.endpoint.rstrip('/')}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        
        headers = {
            "api-key": self.key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert project evaluator. You MUST respond with valid JSON only. Do not include any explanatory text outside the JSON response."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.3
        }
        
        async with aiohttp.ClientSession() as session:
            logger.info("Sending evaluation request to Azure OpenAI...")
            async with session.post(url, headers=headers, json=payload) as response:
                response_text = await response.text()
                logger.info(f"Evaluation response status: {response.status}")
                logger.info(f"Evaluation response: {response_text[:1000]}...")  # Log more chars
                
                if response.status != 200:
                    logger.error(f"Azure OpenAI API error: {response_text}")
                    raise HTTPException(status_code=400, detail=f"OpenAI API failed: {response_text}")
                
                try:
                    result = json.loads(response_text)
                    content = result["choices"][0]["message"]["content"]
                    logger.info(f"AI response content: {content}")
                    
                    # Clean the content (remove any extra whitespace, markdown formatting, etc.)
                    content = content.strip()
                    if content.startswith("```json"):
                        content = content.replace("```json", "").replace("```", "").strip()
                    
                    # Parse JSON response
                    evaluation_data = json.loads(content)
                    logger.info(f"Successfully parsed evaluation data: {evaluation_data}")
                    return EvaluationResponse(**evaluation_data)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    logger.error(f"Content that failed to parse: '{content}'")
                    raise HTTPException(status_code=500, detail=f"AI response is not valid JSON: {content[:200]}...")
                except KeyError as e:
                    logger.error(f"Missing key in response: {e}")
                    raise HTTPException(status_code=500, detail=f"Invalid response structure: {str(e)}")
                except Exception as e:
                    logger.error(f"Unexpected error parsing response: {e}")
                    raise HTTPException(status_code=500, detail=f"Failed to parse OpenAI response: {str(e)}")

# Initialize services with error handling
try:
    ocr_service = OCRService()
    openai_service = OpenAIService()
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Service initialization error: {e}")
    ocr_service = None
    openai_service = None

@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML file"""
    return FileResponse("frontend/index.html")

@app.post("/upload-and-evaluate")
async def upload_and_evaluate(file: UploadFile = File(...)):
    """Main endpoint with improved error handling and debugging"""
    
    logger.info(f"Received file: {file.filename}, type: {file.content_type}")
    
    # Check if services are initialized
    if not ocr_service or not openai_service:
        logger.error("Services not properly initialized")
        raise HTTPException(
            status_code=500, 
            detail="Service not configured. Please check your Azure OpenAI credentials in .env file."
        )
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/tiff"]
    if file.content_type not in allowed_types:
        logger.warning(f"Invalid file type: {file.content_type}")
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported: {file.content_type}. Please upload image files (JPEG, PNG, GIF, BMP, TIFF)."
        )
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp_file:
        temp_path = temp_file.name
        logger.info(f"Created temp file: {temp_path}")
        
        try:
            # Save uploaded file
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            logger.info(f"File saved, size: {len(content)} bytes")
            
            # Step 1: Extract text using Azure OpenAI OCR
            extracted_text = await ocr_service.extract_text_from_file(temp_path)
            
            if not extracted_text.strip():
                raise HTTPException(status_code=400, detail="No text could be extracted from the file")
            
            # Step 2: Evaluate with OpenAI
            evaluation = await openai_service.evaluate_project(extracted_text)
            
            return {
                "success": True,
                "extracted_text": extracted_text,
                "evaluation": evaluation.dict()
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
                logger.info(f"Cleaned up temp file: {temp_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up temp file: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 