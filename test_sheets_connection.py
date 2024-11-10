from src.insert_into_sheets import GoogleSheetsManager
from src.config import GOOGLE_SHEETS_CONFIG

def test_connection():
    try:
        # Initialize Google Sheets manager
        sheets_manager = GoogleSheetsManager(GOOGLE_SHEETS_CONFIG['CREDENTIALS_PATH'])
        
        # Test data
        test_data = {
            'Job Title': 'Test Position',
            'Company Name': 'Test Company',
            'Job Location': 'Test Location',
            'Job Link': 'https://test.com',
            'Tailored Resume': 'https://github.com/test',
            'Keywords': 'test, python',
            'Salary Range': '100k-120k',
            'Notes': 'Test entry'
        }
        
        # Try to insert test data
        response = sheets_manager.insert_job_data(
            GOOGLE_SHEETS_CONFIG['SPREADSHEET_ID'],
            test_data
        )
        print("Connection successful! Test data inserted.")
        print("Response:", response)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_connection() 