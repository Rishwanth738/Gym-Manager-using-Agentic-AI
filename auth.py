import os
from composio import Composio
from composio_gemini import GeminiProvider
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

COMPOSIO_USER_ID = os.getenv("COMPOSIO_USER_ID")   # e.g. your Gmail email
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 1. Init composio with Gemini provider
composio = Composio(provider=GeminiProvider())

# 2. Get Gmail tool
tools = composio.tools.get(user_id=COMPOSIO_USER_ID, tools=["GMAIL_SEND_EMAIL"])

# 3. Init Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# 4. Attach tool to Gemini
config = types.GenerateContentConfig(tools=tools)
chat = client.chats.create(model="gemini-2.0-flash", config=config)

# 5. Ask Gemini to send email
response = chat.send_message(
    "Send an email to rishwanth738@gmail.com "
    "with the subject 'Hello from Gemini + Composio 👋🏻' "
    "and the body 'Congrats! You just sent your first email using Gemini Agents and Composio.'"
)

# 6. Print response only (tool executed automatically)
print(response.text)
print("✅ Email sent successfully!")
