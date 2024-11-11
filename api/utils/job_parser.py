from Assistants.CareerForge.assistant_handler import CareerForgeAssistant
from typing import Dict, Any
import json

class JobParser:
    def __init__(self):
        self.assistant = CareerForgeAssistant()

    def analyze_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        Analyze this job posting and extract key information in JSON format:
        
        Title: {job_data.get('title')}
        Description: {job_data.get('description')}
        URL: {job_data.get('url')}
        
        Please extract and format as JSON:
        1. Company name
        2. Required skills (as array)
        3. Experience level
        4. Key responsibilities (as array)
        5. Required qualifications
        6. Location (if mentioned)
        7. Employment type
        """
        
        response = self.assistant.chat(prompt)
        return json.loads(response)
