from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarAPI:
    def __init__(self):

        self.CALENDATID = "9c81c7a6e3570f9e5be8dbe3cf8dab1565d21141f5d2d3dd4dc5787c7a787ac2@group.calendar.google.com"
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        if os.path.exists('services/discord_bot/googleCalendar/token.json'):
            self.creds = Credentials.from_authorized_user_file('services/discord_bot/googleCalendar/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'services/discord_bot/googleCalendar/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('services/discord_bot/googleCalendar/token.json', 'w') as token:
                token.write(self.creds.to_json())

    def getDate(self, date:str, hours:str):


        day, month, year = date.split()[1].split('/')
        hour_start, hour_end = hours.split(' - ')
        
        date_start = f'20{year}-{month}-{day}T{hour_start}:00+02:00'
        date_end = f'20{year}-{month}-{day}T{hour_end}:00+02:00'

        return date_start, date_end



    def newEvent(self, data):

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            for subject in data:

                date_start, date_end = self.getDate(subject["day"], subject["time"])
                print("dates -> ", date_start, date_end)

                event = {
                    'summary': subject["matiere"],
                    'location': subject["classroom"],
                    'description': f'{subject["intervenant"]} - {subject["modality"]}',
                    'start': {
                        'dateTime': date_start,
                        # 'dateTime': '2023-06-30T10:45:00+02:00',
                        'timeZone': 'Europe/Paris',
                    },
                    'end': {
                        'dateTime': date_end,
                        'timeZone': 'Europe/Paris',
                    }
                }
                event = service.events().insert(calendarId=self.CALENDATID, body=event).execute()
                # print('Event created: %s' % (event.get('htmlLink')))
            return True


        except HttpError as error:
            print('An error occurred: %s' % error)
            return False


if __name__ == '__main__':
    cal = CalendarAPI()
    cal.newEvent("testone", "idk", "Paris 12 Erard")