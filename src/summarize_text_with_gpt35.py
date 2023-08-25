import openai
import requests
import json

# Function to summarize text using GPT-3.5
def summarize_text_with_gpt35(jdtext, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"""Please extract the following details from the job description below:Job Description:
                    {jdtext}

                    Job Title:
                    Years of Work Experience Required:
                    Keywords:
                    Tools Needed:
                    Technologies Needed:
                    Company Name:
                    Job Location:
                    Industry:
                    Salary Range:
                    Education Level:
                    Job Type:
                    Application Deadline:

                    Make sure to clearly identify each field so that it can be easily parsed into a JSON payload for a database.""",
        temperature=0.5,
        max_tokens=500
    )
    summarized_text = response.choices[0].text.strip()
    return summarized_text
