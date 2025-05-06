# google_calendar.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'google_credentials.json'  # nazwij jak plik który pobierzesz

def create_event(name, date_str, time_str):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('calendar', 'v3', credentials=credentials)

    # Połączenie daty i czasu
    start_datetime = f"{date_str}T{time_str}:00"
    end_datetime = f"{date_str}T{time_str}:59"

    event = {
        'summary': f'Podlewanie {name}',
        'description': f'Podlej roślinę {name}',
        'start': {
            'dateTime': start_datetime,
            'timeZone': 'Europe/Warsaw',
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': 'Europe/Warsaw',
        }
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')
