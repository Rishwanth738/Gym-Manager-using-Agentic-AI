import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.gym_manager.tools.sheets_fetch import GoogleSheetsFetchTool

def test_sheets_fetch():
    # Load environment variables
    load_dotenv()
    
    print("Testing Google Sheets fetch...")
    try:
        # Initialize the tool
        sheets_tool = GoogleSheetsFetchTool()
        
        # Fetch the latest response
        result = sheets_tool._run()
        
        # Print the result
        if result.get("status") == "success":
            print("\nSuccessfully fetched latest response:")
            print(result["response"])
        else:
            print("\nError fetching response:")
            print(result.get("error", "Unknown error"))
            
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    test_sheets_fetch()
