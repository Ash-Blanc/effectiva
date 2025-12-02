"""Google Tasks integration for Effectiva agents.

This provides full Google Tasks API integration, allowing agents to:
- Create, read, update, and delete tasks
- Manage task lists
- Sync with existing Google Tasks
- Organize tasks by priority and due dates
"""
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Tasks API scopes
SCOPES = ['https://www.googleapis.com/auth/tasks']

# Reuse the same token and credentials paths as calendar
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

def get_tasks_service():
    """Get authenticated Google Tasks service."""
    try:
        creds = get_google_credentials()
        service = build('tasks', 'v1', credentials=creds)
        return service
    except Exception as e:
        return f"Failed to initialize Google Tasks service: {str(e)}"

def list_task_lists() -> str:
    """List all available Google Task Lists."""
    try:
        service = get_tasks_service()
        if isinstance(service, str):  # Error message
            return service

        tasklists = service.tasklists().list().execute()
        lists = tasklists.get('items', [])

        if not lists:
            return "No task lists found."

        result = "**Your Google Task Lists:**\n\n"
        for tasklist in lists:
            result += f"📝 {tasklist['title']}\n"
            result += f"   ID: {tasklist['id']}\n\n"

        return result

    except HttpError as error:
        return f"Google Tasks API error: {error}"
    except Exception as e:
        return f"Error listing task lists: {str(e)}"

def get_tasks(tasklist_id: str = '@default', show_completed: bool = False) -> str:
    """Get tasks from a Google Task List."""
    try:
        service = get_tasks_service()
        if isinstance(service, str):  # Error message
            return service

        # Get all tasks (completed and incomplete)
        if show_completed:
            results = service.tasks().list(tasklist=tasklist_id, showCompleted=True).execute()
        else:
            results = service.tasks().list(tasklist=tasklist_id, showCompleted=False, showHidden=False).execute()

        tasks = results.get('items', [])

        if not tasks:
            status = " (including completed)" if show_completed else ""
            return f"No tasks found in this list{status}."

        result = f"**Google Tasks{ ' (including completed)' if show_completed else ''}:**\n\n"
        for task in tasks:
            status = "✓" if task.get('status') == 'completed' else "○"
            due_date = ""
            if task.get('due'):
                due_dt = datetime.fromisoformat(task['due'].replace('Z', '+00:00'))
                due_date = f" (Due: {due_dt.strftime('%Y-%m-%d')})"

            result += f"{status} {task['title']}{due_date}\n"
            if task.get('notes'):
                notes = task['notes'][:100] + "..." if len(task['notes']) > 100 else task['notes']
                result += f"   📝 {notes}\n"
            result += "\n"

        return result

    except HttpError as error:
        return f"Google Tasks API error: {error}"
    except Exception as e:
        return f"Error getting tasks: {str(e)}"

def create_task(
    title: str,
    tasklist_id: str = '@default',
    notes: str = "",
    due_date: str = None
) -> str:
    """Create a new task in Google Tasks."""
    try:
        service = get_tasks_service()
        if isinstance(service, str):  # Error message
            return service

        task_body = {
            'title': title,
            'notes': notes,
        }

        if due_date:
            # Google Tasks expects RFC 3339 timestamp
            if 'T' not in due_date:
                # If just a date, set to end of day
                due_date += 'T23:59:59.000Z'
            elif not due_date.endswith('Z'):
                due_date += 'Z'
            task_body['due'] = due_date

        created_task = service.tasks().insert(
            tasklist=tasklist_id,
            body=task_body
        ).execute()

        due_info = f" (Due: {due_date[:10]})" if due_date else ""
        return f"✓ Task created in Google Tasks: '{title}'{due_info}"

    except HttpError as error:
        return f"Google Tasks API error: {error}"
    except Exception as e:
        return f"Error creating task: {str(e)}"

def complete_task(task_id: str, tasklist_id: str = '@default') -> str:
    """Mark a task as completed in Google Tasks."""
    try:
        service = get_tasks_service()
        if isinstance(service, str):  # Error message
            return service

        # First get the task to update it
        task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()

        # Update the task status
        task['status'] = 'completed'

        updated_task = service.tasks().update(
            tasklist=tasklist_id,
            task=task_id,
            body=task
        ).execute()

        return f"✓ Task completed: '{updated_task['title']}'"

    except HttpError as error:
        return f"Google Tasks API error: {error}"
    except Exception as e:
        return f"Error completing task: {str(e)}"

def delete_task(task_id: str, tasklist_id: str = '@default') -> str:
    """Delete a task from Google Tasks."""
    try:
        service = get_tasks_service()
        if isinstance(service, str):  # Error message
            return service

        # Get task title before deleting
        task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
        task_title = task['title']

        # Delete the task
        service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()

        return f"✓ Task deleted: '{task_title}'"

    except HttpError as error:
        return f"Google Tasks API error: {error}"
    except Exception as e:
        return f"Error deleting task: {str(e)}"