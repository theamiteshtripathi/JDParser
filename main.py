import openai
import requests
import json
from src.insert_into_notion import insert_into_notion
from src.parse_summarized_text import parse_summarized_text
from src.summarize_text_with_gpt35 import summarize_text_with_gpt35

# Main function
def main():
    # API keys and database ID
    openai_api_key = "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"
    notion_api_key = "secret_uKSFFPco2C0ZT9yzZXSCN2GbDdShpEOkfjYNd6bEzIe"
    database_id = "6ad8aedf97634b94b79ecc0943398158"

    # Ask the user for the job description
    #job_description = input("Please enter the job description: ")
    print("Please enter the job description. Type 'END' on a new line when you're finished.")

    lines = []
    while True:
        line = input()
        if line == 'END':
            break
        lines.append(line)

    job_description = '\n'.join(lines)
    print("You entered the following job description:")
    print(job_description)


    # Summarize the job description using GPT-3.5
    summarized_text = summarize_text_with_gpt35(job_description, openai_api_key)
    print(summarized_text)
    parsed_data = parse_summarized_text(summarized_text)
    print("Parsed Data:", parsed_data)
    # Insert the parsed details into the Notion database
    response = insert_into_notion(parsed_data, notion_api_key, database_id)
    print("Data successfully inserted into Notion:", response)

if __name__ == "__main__":
    main()
