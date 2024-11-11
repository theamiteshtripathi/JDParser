from fastapi import APIRouter, Request
from pydantic import BaseModel
from src.utils.logger import get_logger
from Assistants.CareerForge import CareerForgeAssistant
import json

router = APIRouter()
logger = get_logger(__name__)
assistant = CareerForgeAssistant()

# Match exactly what content.js sends
class RawJobContent(BaseModel):
    raw_content: str
    html_content: str
    url: str

@router.post("/parse-job")
async def parse_job(request: Request, content: RawJobContent):
    # Log the raw request body
    raw_body = await request.body()
    logger.info(f"Received raw request body: {raw_body.decode()}")
    
    try:
        # Send to OpenAI for extraction
        prompt = f"""
        Extract job details from this webpage content and return ONLY a JSON object.
        URL: {content.url}
        Content: {content.raw_content[:4000]}
        """
        
        # Get structured response from OpenAI
        parsed_json = assistant.chat(prompt)
        
        # Log for debugging
        logger.info(f"OpenAI response: {parsed_json}")
        
        # Ensure we have valid JSON
        if isinstance(parsed_json, str):
            try:
                parsed_json = json.loads(parsed_json)
            except json.JSONDecodeError:
                logger.error("Failed to parse OpenAI response as JSON")
                raise
        
        return parsed_json
        
    except Exception as e:
        logger.error(f"Error processing job: {str(e)}")
        return {
            "job_title": "Not found",
            "company": "Not found",
            "location": "Not found",
            "job_link": content.url,
            "keywords": "Not found",
            "salary_range": "Not mentioned",
            "notes": str(e)
        }
