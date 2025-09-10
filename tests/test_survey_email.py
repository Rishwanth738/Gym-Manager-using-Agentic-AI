import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.gym_manager.crew import GymManagerCrew

# Load environment variables
load_dotenv()

def test_survey_email():
    # Initialize the crew
    crew_instance = GymManagerCrew()
    
    print("Testing survey email task...")
    try:
        # Execute the crew with only the survey task
        result = crew_instance.crew().kickoff()
        print("Task execution result:", result)
    except Exception as e:
        print("Error executing survey task:", str(e))

if __name__ == "__main__":
    test_survey_email()
