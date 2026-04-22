import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

def get_calendar_service():
    creds = Credentials.from_authorized_user_file("token.json")
    return build("calendar", "v3", credentials=creds)

@tool
def create_calendar_event(title: str, date: str, time: str, duration_hours: int = 1) -> str:
    """Create a study session or event in Google Calendar.
    date format: YYYY-MM-DD, time format: HH:MM in 24hr"""
    try:
        service = get_calendar_service()
        start = f"{date}T{time}:00"
        end_hour = int(time.split(":")[0]) + duration_hours
        end = f"{date}T{end_hour:02d}:{time.split(':')[1]}:00"
        event = {
            "summary": title,
            "start": {"dateTime": start, "timeZone": "Asia/Kolkata"},
            "end":   {"dateTime": end,   "timeZone": "Asia/Kolkata"},
        }
        result = service.events().insert(
            calendarId="primary", body=event
        ).execute()
        return f"Event '{title}' created! Link: {result.get('htmlLink')}"
    except Exception as e:
        return f"Failed to create event: {str(e)}"
