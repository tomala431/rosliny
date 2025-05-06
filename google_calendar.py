import os
import json
from io import StringIO
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_event(plant_name, date_str, time_str, user_email="user@example.com"):
    creds_json = os.getenv("GOOGLE_CREDS_JSON")
    if not creds_json:
        raise ValueError("Brak zmiennej GOOGLE_CREDS_JSON")

    # 🔧 Naprawa błędu: zamieniamy string na obiekt podobny do pliku
    creds_stream = StringIO(creds_json)
    creds_dict = json.load(creds_stream)

    credentials = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=["https://www.googleapis.com/auth/calendar"]
    )

    service = build("calendar", "v3", credentials=credentials)

    start = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    end = start + timedelta(minutes=30)

    event = {
        "summary": f"Podlewanie {plant_name}",
        "location": "Dom",
        "description": f"Podlej roślinę {plant_name}",
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": "Europe/Warsaw",
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "Europe/Warsaw",
        },
        "attendees": [{"email": user_email}],
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')
