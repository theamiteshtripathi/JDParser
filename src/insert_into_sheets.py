from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

class GoogleSheetsManager:
    def __init__(self, credentials_path):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=self.SCOPES)
        self.service = build('sheets', 'v4', credentials=self.creds)
        
    def insert_job_data(self, spreadsheet_id, parsed_data):
        # Specify the Jobs sheet
        range_name = 'Jobs!A:K'  # Adjust based on your columns
        
        # Format current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Format data for sheets - adjust these columns based on your sheet structure
        values = [[
            current_date,  # Date Added
            parsed_data.get('Job Title', ''),
            parsed_data.get('Company Name', ''),
            parsed_data.get('Job Location', ''),
            parsed_data.get('Job Link', ''),
            parsed_data.get('Tailored Resume', ''),
            'New',  # Status
            '',  # Applied Date (empty initially)
            parsed_data.get('Keywords', ''),
            parsed_data.get('Salary Range', ''),
            parsed_data.get('Notes', '')  # Additional notes column
        ]]
        
        body = {
            'values': values,
            'majorDimension': 'ROWS'
        }
        
        try:
            result = self.service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            print(f"Data inserted successfully: {result.get('updates').get('updatedRows')} rows added.")
            return result
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            raise e
            
    def update_job_status(self, spreadsheet_id, row_number, new_status):
        """Update the status of a job application"""
        range_name = f'Jobs!G{row_number}'
        body = {
            'values': [[new_status]]
        }
        
        try:
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            return result
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            raise e
