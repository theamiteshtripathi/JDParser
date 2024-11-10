import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_SHEETS_CONFIG = {
    'SPREADSHEET_ID': os.getenv('GOOGLE_SPREADSHEET_ID'),
    'CREDENTIALS_PATH': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json'),
    'SHEET_NAME': 'Jobs'
}

# Column structure for the Jobs sheet
JOBS_COLUMNS = {
    'DATE_ADDED': 'A',
    'JOB_TITLE': 'B',
    'COMPANY': 'C',
    'LOCATION': 'D',
    'JOB_LINK': 'E',
    'RESUME_LINK': 'F',
    'STATUS': 'G',
    'APPLIED_DATE': 'H',
    'KEYWORDS': 'I',
    'SALARY': 'J',
    'NOTES': 'K'
} 