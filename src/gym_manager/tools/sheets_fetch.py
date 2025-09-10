from crewai.tools import BaseTool
from typing import Dict, Any
import os
from google.oauth2.credentials import Credentials
from typing import Any
from googleapiclient.discovery import build
from google.oauth2 import service_account

class GoogleSheetsFetchTool(BaseTool):
    name: str = "google_sheets_fetch_tool"
    description: str = """Fetches responses from the Google Form's response sheet.
    The range will always be 'Form Responses 1!A:Z' since this is a Google Form's response sheet.
    No range_name parameter is needed as it's handled automatically."""
    sheet_id: str = ""
    credentials: Any = None

    def __init__(self):
        super().__init__()
        # Get sheet ID from environment
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")
        if not self.sheet_id:
            raise ValueError("GOOGLE_SHEET_ID must be set in environment variables")

        # Load service account credentials
        try:
            # Get the project root directory
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            creds_path = os.path.join(project_root, 'credentials.json')
            
            self.credentials = service_account.Credentials.from_service_account_file(
                creds_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
        except Exception as e:
            raise ValueError(f"Failed to load service account credentials from {creds_path}: {str(e)}")

    def _run(self, range_name: str = "Form Responses 1!A:Z") -> Dict[str, Any]:
        """
        Fetch the latest response from the Google Sheet
        Returns a dictionary with the structured response
        """
        try:
            # Always use the default range name for Google Forms
            range_name = "Form Responses 1!A:Z"
            
            # Build the Sheets API service
            service = build('sheets', 'v4', credentials=self.credentials)
            sheet = service.spreadsheets()

            # Get the values
            result = sheet.values().get(
                spreadsheetId=self.sheet_id,
                range=range_name
            ).execute()
            
            # Get the latest response (last row)
            values = result.get('values', [])
            if not values or len(values) < 2:  # Need at least headers and one response
                return {
                    "error": "No responses found in the sheet",
                    "status": "error"
                }
            
            # Get headers and latest response
            headers = values[0]
            latest_response = values[-1]
            
            # Print headers for debugging
            print("Sheet Headers:", headers)
            print("Latest Response:", latest_response)
            
            # Get the column mappings from headers
            header_to_index = {header.strip().lower(): idx for idx, header in enumerate(headers)}
            
            # Create a structured response using actual form column names
            response_dict = {
                "timestamp": latest_response[0],  # Timestamp is always first column
                "user_info": {
                    "name": latest_response[1] if len(latest_response) > 1 else "",
                    "email": latest_response[2] if len(latest_response) > 2 else "",
                },
                "workout_data": {
                    "did_workout": latest_response[3] if len(latest_response) > 3 else "No",
                    "muscles_trained": latest_response[4] if len(latest_response) > 4 else "",
                    "did_cardio": latest_response[5] if len(latest_response) > 5 else "No",
                    "exercises": latest_response[6] if len(latest_response) > 6 else "",
                    "experienced_pain": latest_response[7] if len(latest_response) > 7 else "No",
                    "pain_details": latest_response[8] if len(latest_response) > 8 else ""
                }
            }
            
            return {
                "response": response_dict,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "error": f"Failed to fetch sheet data: {str(e)}",
                "status": "error"
            }
