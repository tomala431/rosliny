import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_google_event(plant_name, date_str, time_str):
    # Wczytaj dane uwierzytelniające z ENV jako JSON
    creds_dict = json.loads(os.environ['GOOGLE_CREDS_JSON'])
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=["https://www.googleapis.com/auth/calendar"]
    )

    service = build('calendar', 'v3', credentials=creds)

    # Sformatuj datę i czas
    start_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    end_dt = start_dt + datetime.timedelta(minutes=30)

    event = {
        'summary': f'Podlewanie {plant_name}',
        'description': f'Podlej roślinę {plant_name}',
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Europe/Warsaw'},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Europe/Warsaw'},
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')
