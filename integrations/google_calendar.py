"""Google Calendar integration for Effectiva agents.

This provides full Google Calendar API integration, allowing agents to:
- Create, read, update, and delete calendar events
- Sync with existing Google Calendar
- Find free/busy times
- Manage multiple calendars
"""
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events']

# Token storage
TOKEN_PATH = Path(__file__).parent.parent / 'google_token.json'
CREDENTIALS_PATH = Path(__file__).parent.parent / 'google_credentials.json'

def get_google_credentials():
    """Get or refresh Google API credentials."""
    creds = None

    # Load existing token if available
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                raise FileNotFoundError(
                    f"Google credentials file not found at {CREDENTIALS_PATH}. "
                    "Please download your OAuth 2.0 credentials from Google Cloud Console "
                    "and save as 'google_credentials.json'"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return creds

def get_calendar_service():
    """Get authenticated Google Calendar service."""
    try:
        creds = get_google_credentials()
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        return f"Failed to initialize Google Calendar service: {str(e)}"

def list_calendars() -> str:
    """List all available Google Calendars."""
    try:
        service = get_calendar_service()
        if isinstance(service, str):  # Error message
            return service

        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])

        if not calendars:
            return "No calendars found."

        result = "**Your Google Calendars:**\n\n"
        for calendar in calendars:
            primary = " (Primary)" if calendar.get('primary', False) else ""
            result += f"📅 {calendar['summary']}{primary}\n"
            result += f"   ID: {calendar['id']}\n\n"

        return result

    except HttpError as error:
        return f"Google Calendar API error: {error}"
    except Exception as e:
        return f"Error listing calendars: {str(e)}"

def get_events(calendar_id: str = 'primary', days: int = 7) -> str:
    """Get upcoming events from Google Calendar."""
    try:
        service = get_calendar_service()
        if isinstance(service, str):  # Error message
            return service

        now = datetime.utcnow()
        time_max = now + timedelta(days=days)

        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=now.isoformat() + 'Z',
            timeMax=time_max.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            return f"No upcoming events found in the next {days} days."

        result = f"**Upcoming Google Calendar Events (next {days} days):**\n\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))

            result += f"📅 {start_dt.strftime('%Y-%m-%d %H:%M')}: **{event['summary']}**\n"
            if event.get('location'):
                result += f"   📍 {event['location']}\n"
            if event.get('description'):
                desc = event['description'][:100] + "..." if len(event['description']) > 100 else event['description']
                result += f"   {desc}\n"
            result += "\n"

        return result

    except HttpError as error:
        return f"Google Calendar API error: {error}"
    except Exception as e:
        return f"Error getting events: {str(e)}"

def create_event(
    title: str,
    start_time: str,
    end_time: str,
    calendar_id: str = 'primary',
    description: str = "",
    location: str = ""
) -> str:
    """Create a new event in Google Calendar."""
    try:
        service = get_calendar_service()
        if isinstance(service, str):  # Error message
            return service

        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            }
        }

        if location:
            event['location'] = location

        created_event = service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()

        return f"✓ Event created in Google Calendar: '{title}' at {start_time}"

    except HttpError as error:
        return f"Google Calendar API error: {error}"
    except Exception as e:
        return f"Error creating event: {str(e)}"

def find_free_slots(calendar_id: str = 'primary', date: str = None, duration_minutes: int = 60) -> str:
    """Find free time slots in Google Calendar."""
    try:
        service = get_calendar_service()
        if isinstance(service, str):  # Error message
            return service

        if date is None:
            date = datetime.now().date().isoformat()

        # Define the time range for the day
        day_start = datetime.fromisoformat(f"{date}T08:00:00")
        day_end = datetime.fromisoformat(f"{date}T22:00:00")

        # Get busy times
        body = {
            "timeMin": day_start.isoformat() + 'Z',
            "timeMax": day_end.isoformat() + 'Z',
            "items": [{"id": calendar_id}]
        }

        freebusy_result = service.freebusy().query(body=body).execute()
        busy_periods = freebusy_result['calendars'][calendar_id].get('busy', [])

        if not busy_periods:
            return f"The entire day {date} is free in Google Calendar!"

        # Convert busy periods to datetime objects
        busy_slots = []
        for period in busy_periods:
            start = datetime.fromisoformat(period['start'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(period['end'].replace('Z', '+00:00'))
            busy_slots.append((start, end))

        # Find free slots
        free_slots = []
        current_time = day_start

        for busy_start, busy_end in busy_slots:
            if (busy_start - current_time).total_seconds() / 60 >= duration_minutes:
                free_slots.append(
                    f"{current_time.strftime('%H:%M')} - {busy_start.strftime('%H:%M')}"
                )
            current_time = max(current_time, busy_end)

        # Check remaining time after last busy period
        if (day_end - current_time).total_seconds() / 60 >= duration_minutes:
            free_slots.append(
                f"{current_time.strftime('%H:%M')} - {day_end.strftime('%H:%M')}"
            )

        if not free_slots:
            return f"No free slots of {duration_minutes} minutes found on {date} in Google Calendar."

        result = f"**Free time slots on {date} in Google Calendar (min {duration_minutes} min):**\n\n"
        for slot in free_slots:
            result += f"🕐 {slot}\n"

        return result

    except HttpError as error:
        return f"Google Calendar API error: {error}"
    except Exception as e:
        return f"Error finding free slots: {str(e)}"