from typing import Dict, Any
from crewai.tools import BaseTool
from .sheets_fetch import GoogleSheetsFetchTool
from pydantic import Field

class FormResponseFetchTool(BaseTool):
    name: str = "fetch_form_response"
    description: str = """Fetch and structure the latest response from the Google Form's response sheet.
    Returns a dictionary containing:
    - timestamp: When the form was submitted
    - user_info: name and email of the respondent
    - workout_data: details about the workout including:
        - did_workout: whether they worked out (Yes/No)
        - muscles_trained: what muscles were worked
        - did_cardio: whether they did cardio (Yes/No)
        - exercises: list of exercises and sets
        - experienced_pain: whether they had pain (Yes/No)
        - pain_details: description of any pain experienced
    """
    sheets_tool: GoogleSheetsFetchTool = Field(default_factory=GoogleSheetsFetchTool)
    
    def _run(self, *args, **kwargs) -> Dict[str, Any]:
        """Fetch the latest form response in a structured format"""
        try:
            result = self.sheets_tool._run()
            if result.get("status") == "success":
                return {
                    "status": "success",
                    "data": result["response"]
                }
            else:
                return {
                    "status": "error",
                    "error": result.get("error", "Unknown error fetching form response")
                }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error while fetching form response: {str(e)}"
            }
