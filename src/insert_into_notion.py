import openai
import requests
import json

def insert_into_notion(data, notion_api_key, database_id):
    url = f"https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json"
    }
    payload = {
        "parent": {"database_id": database_id},
        "properties": {}
    }

    for key, value in data.items():
        # Use "title" type for "Job Post" and "rich_text" for all other fields
        field_type = "title" if key == "Job Title" else "rich_text"
        payload["properties"][key] = {
            "type": field_type,
            field_type: [{"text": {"content": value}}]
        }

    print("Sending the following payload:")
    print(json.dumps(payload, indent=4))

    response = requests.post(url, headers=headers, json=payload)

    print("Received the following response:")
    print(response.text)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Failed to insert data into Notion: {response.text}")
