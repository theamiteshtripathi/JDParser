import openai
import requests
import json
def parse_summarized_text(summarized_text, curated_bullets, job_link):
    lines = summarized_text.split('\n')
    parsed_data = {}
    current_field = ""
    for line in lines:
        # Try to find ':' in the line
        if ':' in line:
            field, value = line.split(':', 1)  # Split only at the first ':'
            field = field.strip()
            value = value.strip()
            parsed_data[field] = value
            current_field = field  # Store the current field name
        else:
            # If ':' is not found, this line is a continuation of the previous field's value
            if current_field:
                parsed_data[current_field] += " " + line.strip()  # Append to the last known field
        
        # Add the job link to the parsed data
        parsed_data['Job Link'] = job_link
        parsed_data["Resume Bullets"] = curated_bullets

    return parsed_data