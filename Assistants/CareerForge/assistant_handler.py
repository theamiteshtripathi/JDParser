import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv
from src.utils.logger import get_logger

# Load environment variables
load_dotenv()
logger = get_logger(__name__)

class CareerForgeAssistant:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.assistant_name = "CareerForge AI"
        self.assistant_filepath = os.path.join('Assistants', 'CareerForge')
        
        # Verify API key on initialization
        try:
            # Make a simple API call to verify the key
            self.client.models.list()
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise ValueError("Invalid OpenAI API key or authentication failed")

    def _read_instructions(self) -> str:
        try:
            instructions_path = os.path.join(self.assistant_filepath, "instructions.txt")
            with open(instructions_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            logger.error(f"instructions.txt not found at {instructions_path}")
            raise

    def create_assistant(self):
        logger.info("Creating CareerForge AI assistant")
        try:
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    # Check if assistant exists
                    assistant_file = f'{self.assistant_filepath}/{self.assistant_name}.json'
                    if os.path.exists(assistant_file):
                        with open(assistant_file, 'r') as file:
                            assistant_data = json.load(file)
                        try:
                            self.client.beta.assistants.delete(assistant_data['assistant_id'])
                        except Exception as e:
                            logger.warning(f"Error cleaning up old assistant: {str(e)}")

                    # Create new assistant
                    instructions = self._read_instructions()
                    assistant = self.client.beta.assistants.create(
                        name=self.assistant_name,
                        instructions=instructions,
                        model="gpt-3.5-turbo-1106",
                        tools=[
                            {"type": "code_interpreter"},
                            {"type": "file_search"}
                        ]
                    )

                    # Save assistant data
                    assistant_data = {
                        'assistant_id': assistant.id,
                        'created_at': assistant.created_at,
                        'model': assistant.model
                    }
                    
                    with open(assistant_file, 'w') as file:
                        json.dump(assistant_data, file, indent=2)

                    logger.info(f"Assistant created successfully with ID: {assistant.id}")
                    return assistant

                except Exception as e:
                    logger.error(f"Error creating assistant: {str(e)}")
                    retry_count += 1
                    time.sleep(2 ** retry_count)

            raise Exception("Failed to create assistant after multiple retries")

        except Exception as e:
            logger.error(f"Error creating assistant: {str(e)}")
            raise

    def chat(self, user_input: str):
        logger.info(f"Processing chat input: {user_input}")
        try:
            thread = self.client.beta.threads.create()
            
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input
            )
            
            # Get assistant ID from saved file
            with open(f'{self.assistant_filepath}/{self.assistant_name}.json', 'r') as file:
                assistant_data = json.load(file)
            
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_data['assistant_id']
            )
            
            while run.status not in ["completed", "failed"]:
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread.id, 
                    run_id=run.id
                )
            
            if run.status == "failed":
                raise Exception(f"Run failed: {run.last_error}")
            
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            response = messages.data[0].content[0].text.value
            
            logger.info("Chat response generated successfully")
            return response

        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            raise 