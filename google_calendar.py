# from __future__ import print_function

from datetime import datetime, timedelta
import os.path
import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']


def my_calendar():
    """
   Create the events
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        timezone = 'Asia/Kolkata'

        result = service.calendarList().list().execute()
        calendar_id = result['items'][0]['id']
        start_time = datetime.now(pytz.timezone(timezone))

        end_time = start_time + timedelta(hours=4)

        event = {
            'summary': 'Meeting with blinctrip',
            'location': 'Hyderabad',
            'description': 'discussion',
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },

        }
        create_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print("Event created with current time:", start_time.strftime("%Y-%m-%dT%H:%M:%S"))
        print("Event details:", event)
        print(create_event['htmlLink'])
    #         events = events_result.get('items', [])

    #         if not events:
    #             print('No upcoming events found.')
    #             return

    #         # Prints the start and name of the next 10 events
    #         for event in events:
    #             start = event['start'].get('dateTime', event['start'].get('date'))
    #             print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


my_calendar()