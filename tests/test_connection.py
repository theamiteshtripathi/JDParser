import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

def test_google_connection():
    try:
        # Create credentials
        credentials = service_account.Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build service
        service = build('sheets', 'v4', credentials=credentials)
        
        # Test read
        spreadsheet_id = '1nDsC9xbbR9LSWUUmwIXKgn3qFNImjOpfbrCPKcMSE8I'
        range_name = 'Jobs!A1:A2'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        print("Connection successful!")
        print("Data:", result.get('values', []))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_google_connection() 