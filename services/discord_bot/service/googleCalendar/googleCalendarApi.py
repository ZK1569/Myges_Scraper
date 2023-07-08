from pprint import pprint
from typing import List

import os.path
import datetime

from typing import List 
from Models.oneWeekModel import oneWeekModel

import settings

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Models.oneDayModel import oneDay

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
logger = settings.logging.getLogger("bot")

class CalendarAPI:
    def __init__(self):

        self.CALENDATID = settings.CALENDAR
        self.creds = None
        
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        if os.path.exists(f'{settings.GOOGLECREDENTIALS}/token.json'):
            self.creds = Credentials.from_authorized_user_file(f'{settings.GOOGLECREDENTIALS}/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f'{settings.GOOGLECREDENTIALS}/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(f'{settings.GOOGLECREDENTIALS}/token.json', 'w') as token:
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
    
    def intervalDateWeek(self, schedule:List[oneWeekModel]):

        date_start = self.getDate(schedule[0].day, schedule[0].time)
        date_end = self.getDate(schedule[-1].day, schedule[-1].time)

        return date_start[0], date_end[1]


    def newEvent(self, data:List[oneWeekModel]):
        """
            Create new events in the calendar
        """

        logger.info("Save Calendar")

        try:

            for subject in data:

                date_start, date_end = self.getDate(subject.day, subject.time)

                event = {
                    'summary': subject.couse,
                    'location': subject.classroom,
                    'description': f'{subject.teacher} - {subject.modality}',
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
            return True


        except HttpError as error:
            logger.error(error)
            return False

    def getWeekEvents(self, date_start:str, date_end:str):
        """
            Retrieve the number of requested week's events
        """

        try:
            events_result = self.service.events().list(calendarId=self.CALENDATID, timeMin=date_start, timeMax=date_end, singleEvents=True,orderBy='startTime').execute()

            events = events_result.get('items', [])

            return len(events)

        except Exception as e:
            return 0
        
    def getTodayEvents(self)->List[oneDay]:
        now = datetime.datetime.utcnow()
        start_of_day = datetime.datetime(now.year, now.month, now.day)
        end_of_day = start_of_day + datetime.timedelta(days=1)

        events_result = self.service.events().list(
            calendarId=self.CALENDATID,
            timeMin=start_of_day.strftime('%Y-%m-%dT%H:%M:%S+02:00'),
            timeMax=end_of_day.strftime('%Y-%m-%dT%H:%M:%S+02:00'),
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        lessons = []
        if not events:
            return lessons

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            # Convertir les dates en objets datetime
            start_dt = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
            end_dt = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
            
            # Formater les dates et heures au format souhaité
            start_formatted = start_dt.strftime('%Y-%m-%d %H:%M:%S')
            end_formatted = end_dt.strftime('%Y-%m-%d %H:%M:%S')
            
            description = event.get('description', 'Aucune description disponible')
            summary = event.get('summary', 'Aucun résumé disponible')
            location = event.get('location', 'Aucune classe')

            lesson = oneDay(
                start_formatted,
                end_formatted,
                summary,
                description,
                location
            )

            lessons.append(lesson)

        return lessons




if __name__ == '__main__':
    print("---Start---")
    cal = CalendarAPI()
    print(cal.getWeekEvents("2023-06-26T01:00:00+02:00", "2023-06-30T19:23:00+02:00"))
