import os
import base64
from dotenv import load_dotenv
from langchain_core.tools import tool
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

def get_gmail_service():
    creds = Credentials.from_authorized_user_file("token.json")
    return build("gmail", "v1", credentials=creds)

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email via Gmail. Use when user wants to 
    email a professor, classmate, or anyone."""
    try:
        service = get_gmail_service()
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(
            userId="me", body={"raw": encoded}
        ).execute()
        return f"Email sent successfully to {to}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"