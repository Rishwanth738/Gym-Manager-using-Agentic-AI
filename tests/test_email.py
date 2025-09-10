from crewai_tools import GmailSendEmailTool
import os
from dotenv import load_dotenv

load_dotenv()

def test_gmail_send():
    # Initialize the Gmail tool
    gmail_tool = GmailSendEmailTool()
    
    # Test email parameters
    test_email = {
        "to": "rishwanth738@gmail.com",  # Replace with your email
        "subject": "Test Email from GymManager",
        "body": "This is a test email to verify Gmail functionality is working."
    }
    
    # Try sending the email
    try:
        result = gmail_tool.run(test_email)
        print("Email sending result:", result)
    except Exception as e:
        print("Error sending email:", str(e))

if __name__ == "__main__":
    test_gmail_send()
