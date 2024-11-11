import os
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

class DataStore:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')
        self.headers = [
            'Date Added',
            'Job Title',
            'Company',
            'Location',
            'Job Link',
            'Resume Link',
            'Status',
            'Applied Date',
            'Keywords',
            'Salary Range',
            'Notes'
        ]
        
        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SPREADSHEET_ID not found in environment variables")
        
        self.creds = self._get_credentials()
        self.service = build('sheets', 'v4', credentials=self.creds)
        self._initialize_sheet()
    
    def _get_credentials(self):
        creds_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
        if not creds_file:
            raise ValueError("GOOGLE_SHEETS_CREDENTIALS not found in environment variables")
        return service_account.Credentials.from_service_account_file(
            creds_file,
            scopes=self.SCOPES
        )
    
    def _initialize_sheet(self):
        try:
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            sheet_exists = False
            for sheet in sheet_metadata.get('sheets', ''):
                if sheet.get('properties', {}).get('title') == 'Applications':
                    sheet_exists = True
                    break
            
            if not sheet_exists:
                body = {
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': 'Applications'
                            }
                        }
                    }]
                }
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body=body
                ).execute()
                
                # Add headers
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range='Applications!A1:K1',
                    valueInputOption='RAW',
                    body={'values': [self.headers]}
                ).execute()
                
                logger.info("Applications sheet initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize sheet: {str(e)}")
            raise
    
    def save_application(self, application_data):
        try:
            sheet = self.service.spreadsheets()
            range_name = 'Applications!A:G'
            
            values = [[
                application_data['date'],
                application_data['company'],
                application_data['title'],
                application_data['url'],
                application_data['status'],
                application_data['location'],
                application_data['notes']
            ]]
            
            body = {
                'values': values,
                'majorDimension': 'ROWS'
            }
            
            result = sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Successfully saved application to Google Sheets")
            return result
            
        except Exception as e:
            logger.error(f"Failed to save to Google Sheets: {str(e)}")
            raise

    def load_applications(self):
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range='Applications!A:G'
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return pd.DataFrame(columns=['Date', 'Company', 'Position', 'URL', 'Status', 'Location', 'Notes'])
                
            return pd.DataFrame(values[1:], columns=values[0])
            
        except Exception as e:
            logger.error(f"Failed to load from Google Sheets: {str(e)}")
            raise
