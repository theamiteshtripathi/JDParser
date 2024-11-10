import openai
import requests
import json
from src.insert_into_sheets import GoogleSheetsManager
from src.config import GOOGLE_SHEETS_CONFIG
from src.parse_summarized_text import parse_summarized_text
from src.summarize_text_with_gpt35 import summarize_text_with_gpt35
from src.generate_full_resume_with_gpt35 import read_or_upload_resume
from src.generate_full_resume_with_gpt35 import read_resume_from_docx
from src.generate_full_resume_with_gpt35 import generate_full_resume_with_gpt35
from src.generate_full_resume_with_gpt35 import upload_to_github

# Main function
def main():
    # API keys
    openai_api_key = "your_openai_key"
    github_token = "your_github_token"
    repo_name = "JDParser"

    # Initialize Google Sheets manager
    sheets_manager = GoogleSheetsManager(GOOGLE_SHEETS_CONFIG['CREDENTIALS_PATH'])

    resume_data = read_or_upload_resume()
    print("Resume data successfully read!!!")
    
    # Ask the user for the job link
    job_link = input("Please enter the job link: ")
    print("Job Link stored successfully!!!")

    # Ask the user for the job description
    print("Please enter the job description. Type 'END' on a new line when you're finished.")

    lines = []
    while True:
        line = input()
        if line == 'END':
            break
        lines.append(line)

    job_description = '\n'.join(lines)
    print("Job description Entered Successfully!")


    # Summarize the job description using GPT-3.5
    summarized_text = summarize_text_with_gpt35(job_description, openai_api_key)
    print(summarized_text)

    # Curating Resume Bullets
    tailored_resume_path = generate_full_resume_with_gpt35(job_description, resume_data, openai_api_key)
    print(tailored_resume_path)

    #Uploading File to Github repository
    github_url = upload_to_github(tailored_resume_path, repo_name, github_token)
    print(f"File uploaded to: {github_url}")
    
    #Parsing the summerized data into proper format
    parsed_data = parse_summarized_text(summarized_text, github_url, job_link)
    print("Parsed Data:", parsed_data)
    
    # Instead of inserting into Notion, insert into Google Sheets
    try:
        response = sheets_manager.insert_job_data(
            GOOGLE_SHEETS_CONFIG['SPREADSHEET_ID'],
            parsed_data
        )
        print("Data successfully inserted into Google Sheets:", response)
    except Exception as e:
        print(f"Failed to insert data into Google Sheets: {str(e)}")

if __name__ == "__main__":
    main()
