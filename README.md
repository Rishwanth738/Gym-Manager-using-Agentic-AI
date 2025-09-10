# Gym Manager using Agentic AI 🏋️‍♂️

An intelligent AI-powered gym management system that creates a personalized fitness ecosystem. Built with CrewAI and powered by Gemini 2.5 Flash, this system helps track workouts, manage nutrition, and ensure safe progression in your fitness journey.

## Core Features 🌟

### Daily Workout Management 📋
- Automated Google Form surveys at 6 PM
- Comprehensive workout tracking:
  - Gym attendance
  - Muscle groups trained
  - Exercise sets and reps
  - Cardio activity
  - Pain/discomfort monitoring

### Smart Exercise Planning 💪
- Personalized workout plans based on:
  - Previous workout history
  - Recovery status
  - Pain points and limitations
  - Weekly gym timetable
- YouTube links for proper form demonstrations

### Health Monitoring 🏥
- Pain and injury tracking
- Recovery-focused recommendations
- Corrective exercise suggestions
- Real-time workout adjustments

### Nutrition and Meal Planning 🍳
- Customized nutrition guidelines
- Macronutrient calculations
- Indian cuisine meal plans
- Recipe videos and cooking tutorials

## AI Agents 🤖

### Survey Agent
- Sends daily workout feedback forms via Gmail
- Ensures timely data collection at 6 PM
- Tracks responses for analysis

### Summarizer
- Processes Google Form responses
- Structures workout data
- Maintains PostgreSQL database records

### Gym Trainer
- Analyzes workout patterns
- Creates progressive exercise plans
- Provides form demonstration videos
- Adapts plans based on weekly history

### Doctor
- Reviews pain and injury reports
- Suggests corrective exercises
- Coordinates with Trainer for safe progression
- Provides rehabilitation advice

### Nutritionist
- Creates personalized nutrition plans
- Calculates macro requirements
- Considers workout intensity
- Adapts to fitness goals (bulk/cut/maintain)

### Chef
- Converts nutrition plans to Indian meals
- Provides recipe videos
- Ensures meal variety
- Considers gym timing for meal scheduling

## Technical Infrastructure 🔧

### Data Storage
- PostgreSQL: Workout history and tracking
- Chroma Vector DB: Knowledge storage
- SQLite: Agent memory management
- JSON: Daily recommendations

### Integrations
- Google Forms & Sheets: Data collection
- Composio with GeminiProvider: Email automation
- Serper API: YouTube video search
- PostgreSQL: Data persistence
- Chroma DB: Vector storage

### Memory Systems
- Week-long training history
- Meal variety tracking
- Pain point monitoring
- Global crew coordination

## File Structure 📁
```
├── db/                  # Vector database storage
├── knowledge/          # Gym timetable and resources
├── memory/            # Agent memory storage
├── outputs/           # JSON output files
├── src/
│   └── gym_manager/
│       ├── config/    # Agent and task configurations
│       ├── tools/     # Integration tools
│       ├── crew.py    # Core agent logic
│       └── main.py    # Application entry point
```

## Tools and Integrations 🛠️

### Data Collection Tools
1. **Form Response Tool**
   - Fetches latest responses from Google Forms
   - Handles data validation and structuring
   - Maps form fields to database schema

2. **Google Sheets Integration**
   - Direct access to form response sheets
   - Service account authentication
   - Real-time data fetching

### Database Tools
1. **PostgreSQL Tool**
   - `insert_summary_tool`: Stores structured workout data
   - `fetch_latest_summary_tool`: Retrieves recent workout history
   - Handles data conflicts with upsert operations

### Content Search Tools
1. **YouTube Search Tool**
   - Powered by Serper API
   - Finds exercise demonstration videos
   - Retrieves cooking tutorials for meal plans
   - Returns top 2-3 relevant video links
   - Ensures no placeholder links in responses

### Communication Tools
1. **Survey Email Tool**
   - Composio integration with GeminiProvider for email handling
   - Custom HTML email templates via `survey_email_template.py`
   - Automated survey delivery at 6 PM
   - Error handling and delivery status tracking
   - Uses Composio's GMAIL_SEND_EMAIL tool for reliable delivery

### Special Purpose Tools
1. **Planner Tool**
   - Reads gym timetable from PDF
   - Extracts user's fitness goals
   - Coordinates with trainer and doctor
   - Updates weekly schedule

### Tool Features
- Error handling and retries
- Logging and monitoring
- Service authentication
- Rate limiting compliance
- Data validation

## Setup 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/Rishwanth738/Gym-Manager-using-Agentic-AI.git
   cd gymman
   ```

2. Install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. Configure environment variables in `.env`:
   ```env
   # API Keys
   GOOGLE_API_KEY=your-gemini-api-key
   SERPER_API_KEY=your-serper-api-key
   
   # Database
   DATABASE_URL=your-postgres-url
   GOOGLE_SHEET_ID=your-form-response-sheet-id
   
<<<<<<< HEAD
   # Composio Configuration
   COMPOSIO_USER_ID=your-composio-user-id
=======
   # Email
   COMPOSIO_API_KEY = your-api-key
   COMPOSIO USER ID = your-user-id
>>>>>>> 435bc27553a93c9bfb5f74038ef072d97b2eabc4
   RECIPIENT_EMAIL=your-email@example.com
   ```

4. Place your Google service account credentials in `credentials.json`

## Usage 🎯

1. Start the application:
   ```bash
   python -m src.gym_manager.main
   ```

2. The system will:
   - Send workout survey at 6 PM daily
   - Wait for your form submission
   - Type 'run' to process your data
   - Generate personalized outputs:
     - Next day's workout plan
     - Health recommendations
     - Nutrition guidelines
     - Meal suggestions

## Output Files 📊

Daily outputs in JSON format:
- `workout_plan.json`: Exercise routines
- `review_pain.json`: Health recommendations
- `nutrition_plan.json`: Dietary guidelines
- `food.json`: Meal plans

## Dependencies 📦

- crewai[tools]>=0.156.0
- google-generativeai>=0.3.0
- google-api-python-client
- psycopg2-binary
- schedule
- python-dotenv
- composio
- composio_gemini

## Contributing 🤝

Feel free to contribute by opening issues or submitting pull requests.

## License 📄

This project is licensed under the MIT License.
