import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.gym_manager.crew import GymManagerCrew
from src.gym_manager.tools.sheets_fetch import GoogleSheetsFetchTool
from datetime import datetime

def test_full_workflow():
    # Load environment variables
    load_dotenv()
    
    print("🏋️‍♂️ Testing GymManager Full Workflow")
    print("======================================")

    try:
        # 1. Initialize the crew
        print("\n1. Initializing GymManager Crew...")
        crew = GymManagerCrew()
        
        # Initialize the crew's workflow
        print("\n2. Starting the GymManager workflow...")
        crew_instance = crew.crew()
        
        # First, verify we can fetch form responses
        print("\n3. Testing Google Sheets connection...")
        sheets_tool = GoogleSheetsFetchTool()
        form_response = sheets_tool._run()
        if form_response.get("status") == "success":
            print("Successfully connected to Google Sheets!")
            print("Latest response available:", form_response["response"]["timestamp"])
        else:
            print("Warning: Couldn't fetch from Google Sheets:", form_response.get("error"))
        
        # Execute the full workflow
        print("\n4. Executing the complete workflow...")
        workflow_result = crew_instance.kickoff()
        
        # Print the results
        print("\n5. Workflow Results:")
        print("-" * 50)
        print(workflow_result)
        
        print("\n✅ Workflow Test Completed Successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during workflow test: {str(e)}")
        raise

if __name__ == "__main__":
    test_full_workflow()
