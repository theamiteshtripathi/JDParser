import os
import sys
from pathlib import Path

# Add the project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from src.utils.logger import get_logger
from Assistants.CareerForge.assistant_handler import CareerForgeAssistant
from dotenv import load_dotenv

logger = get_logger(__name__)

def validate_environment():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")
    if not api_key.startswith("sk-"):
        raise ValueError("Invalid OpenAI API key format")

def main():
    try:
        # Validate environment first
        validate_environment()
        
        assistant = CareerForgeAssistant()
        created_assistant = assistant.create_assistant()
        logger.info(f"Assistant initialized with ID: {created_assistant.id}")
        print("✅ CareerForge AI initialized successfully!")
    except ValueError as ve:
        logger.error(f"Environment error: {str(ve)}")
        print(f"❌ Setup Error: {str(ve)}")
    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}")
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 