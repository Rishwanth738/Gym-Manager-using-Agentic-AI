import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from crewai.tools import tool
from crewai_tools import PDFSearchTool
from crewai import LLM
from crewai.memory import LongTermMemory, ShortTermMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from google import genai
from pydantic import BaseModel
from datetime import datetime as DateTime

load_dotenv()

# --- Set up memory storage ---
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)
llma = LLM(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini/gemini-1.5-flash",
)
gapi = os.getenv("GEMINI_API_KEY")

WEEK_MEMORY = LongTermMemory(
    storage=LTMSQLiteStorage(
        db_path=f"{STORAGE_DIR}/week_memory.db"
    )
)

emconfig = {
            "provider": "google",
            "config": {
                "api_key": gapi,
                "model": "models/gemini-embedding-001" 
            }
        }
rag_tool = PDFSearchTool(config = dict(llm = dict(
    provider = "google",
    config = dict(model = "gemini/gemini-2.5-flash"),
), embedder = dict(
    provider = "google",
    config = dict(
        model = "models/gemini-embedding-001"
    ),
),),pdf="./knowledge/gym_timetable.pdf")

SHORT_TERM_MEMORY=ShortTermMemory(
                storage=RAGStorage(
                    embedder_config= emconfig,
                    type="short_term",
                    path="./memory/"
                )
            )
from .tools.youtube_search_tool import youtube_search_tool
from .tools.pg_tool import insert_summary_tool, fetch_latest_summary_tool
from .tools.survey_email_template import get_survey_email
from .tools.form_response import FormResponseFetchTool

# --- Composio Gmail integration ---
from composio import Composio
from composio_gemini import GeminiProvider

COMPOSIO_USER_ID = os.getenv("COMPOSIO_USER_ID")
composio = Composio(provider=GeminiProvider())
bdy = get_survey_email()

gmail_tools = composio.tools.get(user_id=COMPOSIO_USER_ID, tools=["GMAIL_SEND_EMAIL"])
gmail_send_tool = gmail_tools[0] if gmail_tools else None

##Pydantic output objects:
class summary(BaseModel):
    date: DateTime
    went_to_gym: bool
    muscle_trained: str
    summary: str
    pain_experienced: bool
    pain_details: str

class review_pain(BaseModel):
    date: DateTime
    muscle_trained: str
    pain_details: str
    treatment_recommendations: str
    youtube_links: list[str]

class tomorrow_workout_plan(BaseModel):
    date: DateTime
    comments_on_progress: str
    muscle_to_train: str
    workout_plan: str
    youtube_links_for_proper_form: list[str]

class nutrition(BaseModel):
    date: DateTime
    dietary_restrictions: str
    nutrition_plan: str

class meal_plan(BaseModel):
    date: DateTime
    dietary_restrictions: str
    meal_plan: str
    youtube_links_for_recipes: list[str]

class gym_knowledge(BaseModel):
    user_goals: str
    weekly_timetable: list[list[str]]

@tool("gmail_send_email")
def gmail_send_email(recipient_email: str, subject: str = "Daily Gym Feedback", body: str = None) -> str:
    """Send an email using Gmail via Composio."""
    if not gmail_send_tool:
        return "Error: Gmail tool not initialized."
    try:
        email_body = get_survey_email()
        # Send the email with HTML enabled
        result = gmail_send_tool(
            recipient_email=recipient_email,
            subject=subject,
            body=email_body,
            is_html=True
        )
        
        if result.get('successful'):
            return "Email sent successfully!"
        else:
            return f"Error sending email: {result.get('error', 'Unknown error')}"
    except Exception as e:
        return f"Error sending email: {e}"




@CrewBase
class GymManagerCrew:
    """Multi-agent Gym Manager Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    
    # --- Agents ---
    
    @agent
    def summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config["Summarizer"],
            verbose=True,
            tools=[FormResponseFetchTool(), insert_summary_tool],
        )

    @agent
    def trainer(self) -> Agent:
        return Agent(
            config=self.agents_config["Gym Trainer"],
            verbose=True,
            tools=[fetch_latest_summary_tool, youtube_search_tool,rag_tool],
            memory=WEEK_MEMORY,  # Week-long memory to track exercise variety
            context="You have access to past workout plans. Avoid repeating exercises from the last week unless specifically needed for progression."
        )
    
    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config["Personal Assistant"],
            verbose=True,
            tools=[rag_tool],
            memory=WEEK_MEMORY,  # Week-long memory to track exercise variety
            context="You have access to past workout plans. Avoid repeating exercises from the last week unless specifically needed for progression."
        )

    @agent
    def doctor(self) -> Agent:
        return Agent(
            config=self.agents_config["Doctor"],
            verbose=True,
            tools=[fetch_latest_summary_tool, youtube_search_tool, rag_tool],
            memory=SHORT_TERM_MEMORY,  # Short-term memory to track injury progress
            context="You have access to recent pain and injury reports. Use this to track improvement or deterioration over time."
        )

    @agent
    def nutritionist(self) -> Agent:
        return Agent(
            config=self.agents_config["Nutritionist"],
            verbose=True,
            tools = [rag_tool],
            memory=SHORT_TERM_MEMORY,  # Short-term memory to track dietary adjustments
            context="You have access to recent nutrition recommendations. Use this to track effectiveness and make adjustments."
        )

    @agent
    def chef(self) -> Agent:
        return Agent(
            config=self.agents_config["Chef"],
            verbose=True,
            tools=[youtube_search_tool,rag_tool],
            memory=WEEK_MEMORY,  # Week-long memory to avoid repetitive dishes
            context="You have access to past meal suggestions. Avoid repeating dishes from the last week."
        )

    @agent
    def survey_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["Survey Agent"],
            verbose=True,
            tools=[gmail_send_email],
            memory=None  # Survey agent doesn't need memory
        )
    
    

    # --- Tasks ---
    @task
    def user_goal_task(self) -> Task:
        return Task(config=self.tasks_config["check_gym_plans_task"],
                    output_pydantic=gym_knowledge)
    
    @task
    def summarize_responses_task(self) -> Task:
        return Task(config=self.tasks_config["summarize_responses_task"])

    @task
    def generate_workout_plan_task(self) -> Task:
        goal = os.getenv("goal")
        if not goal:
            raise ValueError("Goal environment variable not set.")
        task_config = self.tasks_config["generate_workout_plan_task"].copy()
        task_config['description'] = task_config['description'].format(goal=goal)
        return Task(config=task_config,
                    output_pydantic=tomorrow_workout_plan)

    @task
    def review_pain_task(self) -> Task:
        return Task(config=self.tasks_config["review_pain_task"],
                    output_pydantic=review_pain)

    @task
    def nutrition_plan_task(self) -> Task:
        goal = os.getenv("goal")
        if not goal:
            raise ValueError("Goal environment variable not set.")
        task_config = self.tasks_config["nutrition_plan_task"].copy()
        task_config['description'] = task_config['description'].format(goal=goal)
        return Task(config=task_config,
                    output_pydantic=nutrition)

    @task
    def chef_meal_plan_task(self) -> Task:
        return Task(config=self.tasks_config["chef_meal_plan_task"],
                    output_pydantic=meal_plan)

    # Tasks
    @task
    def send_daily_survey_task(self) -> Task:
        # Get the task configuration
        task_config = self.tasks_config["send_daily_survey_task"].copy()
        
        # Get recipient email from environment variables
        recipient_email = os.getenv("RECIPIENT_EMAIL")
        if not recipient_email:
            raise ValueError("RECIPIENT_EMAIL environment variable not set.")

        # Format the description with the recipient's email
        task_config['description'] = task_config['description'].format(
            recipient_email=recipient_email
        )
        
        return Task(
            config=task_config,
            tools=[gmail_send_email],
        )

    # --- Crew Assembly ---
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.survey_agent(),    # First: Send survey
                self.summarizer(),      # Second: Summarize responses
                self.trainer(),         # Then process the summary
                self.doctor(),
                self.nutritionist(),
                self.chef(),
            ],
            tasks=[
                self.send_daily_survey_task(),
                self.summarize_responses_task(),
                self.review_pain_task(), 
                self.generate_workout_plan_task(),   
                self.nutrition_plan_task(),
                self.chef_meal_plan_task(),
            ],
            process=Process.sequential,
            memory=True,
            long_term_memory=LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path=f"{STORAGE_DIR}/crew_memory.db"
                )
            ),
            embedder={
            "provider": "google",
            "config": {
                "api_key": gapi,
                "model": "models/gemini-embedding-001"
            }
        },
            llm=llma
        )


