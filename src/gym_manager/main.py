import os
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv
from .crew import GymManagerCrew

# Load env vars
load_dotenv()

# Initialize crew from CrewBase
crew_instance = GymManagerCrew()
crew = crew_instance.crew()

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")

def assign_output_files():
    """Assign timestamped output files for each task dynamically."""
    today = datetime.now().strftime("%Y-%m-%d")
    file_map = {
        "summarize_responses_task": f"summarizer_output_{today}.md",
        "review_pain_task": f"doctor_recommendations_{today}.md",
        "generate_workout_plan_task": f"trainer_plan_{today}.md",
        "nutrition_plan_task": f"nutrition_plan_{today}.md",
        "chef_meal_plan_task": f"chef_meals_{today}.md",
    }
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for task in crew.tasks:
        if task.id in file_map:
            task.output_file = os.path.join(OUTPUT_DIR, file_map[task.id])

def run_daily_survey():
    """Triggers the Survey Agent's Gmail task at 6 PM daily."""
    print("📨 Sending daily survey form via Gmail...")
    crew.kickoff(inputs={"task": "send_daily_survey_task"})

def run_full_pipeline():
    """Runs the entire workflow in sequence."""
    print("🔄 Running the full gym workflow...")
    assign_output_files()
    result = crew.kickoff()
    print("✅ Workflow complete.\n")
    print(result)

if __name__ == "__main__":
    # Schedule the survey task for 6 PM daily
    schedule.every().day.at("18:00").do(run_daily_survey)
    print("🤖 Gym Manager running. Survey scheduled for 6 PM daily.")
    print("Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        cmd = input("Type 'run' to execute full pipeline manually, or Enter to wait:\n")
        if cmd.strip().lower() == "run":
            run_full_pipeline()
        time.sleep(60)