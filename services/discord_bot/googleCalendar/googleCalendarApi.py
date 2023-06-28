from pprint import pprint

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
        
        self.service = build('calendar', 'v3', credentials=self.creds)

    def getDate(self, date:str, hours:str):
        """
            Convert date and hour from "Jeudi 29/06/23", "10:30 - 12:45" 
                TO 
            "2023-06-30T10:30:00+02:00"
            "2023-06-30T12:45:00+02:00"

            Return :
                [0] => date_start
                [1] => date_end
        """

        day, month, year = date.split()[1].split('/')
        hour_start, hour_end = hours.split(' - ')
        
        date_start = f'20{year}-{month}-{day}T{hour_start}:00+02:00'
        date_end = f'20{year}-{month}-{day}T{hour_end}:00+02:00'

        return date_start, date_end
    
    def intervalDateWeek(self, schedule):

        date_start = self.getDate(schedule[0]["day"], schedule[0]["time"])
        date_end = self.getDate(schedule[-1]["day"], schedule[-1]["time"])

        return date_start[0], date_end[1]


    def newEvent(self, data):
        """
            Create new events in the calendar
        """

        print("--- Save Calendar ---")

        try:

            for subject in data:

                date_start, date_end = self.getDate(subject["day"], subject["time"])

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
                event = self.service.events().insert(calendarId=self.CALENDATID, body=event).execute()
                # print('Event created: %s' % (event.get('htmlLink')))
            return True


        except HttpError as error:
            print('An error occurred: %s' % error)
            return False

    def getWeekEvents(self, date_start:str, date_end:str):
        """
            Retrieve the requested week's events
        """

        try:
            events_result = self.service.events().list(calendarId=self.CALENDATID, timeMin=date_start, timeMax=date_end, singleEvents=True,orderBy='startTime').execute()

            events = events_result.get('items', [])

            print(len(events))

            return len(events)

        except Exception as e:
            return 0


if __name__ == '__main__':
    print("---Start---")
    cal = CalendarAPI()
    print(cal.getWeekEvents("2023-06-26T01:00:00+02:00", "2023-06-30T19:23:00+02:00"))
