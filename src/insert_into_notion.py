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
        # Differentiate field type based on the key
        if key == "Job Title":
            field_type = "title"
        elif key == "Job Link":
            field_type = "url"
        else:
            field_type = "rich_text"

        if field_type == "url":
            # For URL type
            payload["properties"][key] = {
                "type": field_type,
                field_type: value
            }
        else:
            # For title and rich_text types
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
