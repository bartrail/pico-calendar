import urequests
import json

from src.model.Alarm import Alarm
from src.model.Date import Date
from src.model.Event import Event


class ApiClient:
    url: str
    content: str

    def __init__(self, url, mock=False):
        self.url = url
        if mock:
            self.content = str(mock)
        else:
            self.load()

    def load(self):
        print('request to: {0}'.format(self.url))
        request = urequests.get(self.url)
        print('request status: {0}'.format(request.status_code))
        self.content = request.content
        request.close()

        if request.status_code != 200:
            raise RuntimeError('Error loading URL {0}: Status code {1}'.format(self.url, self.request.status_code))

    def parse_response(self):
        jsonData = json.loads(self.content)

        events = []
        vcalendar = jsonData['vcalendar']

        for calendar in vcalendar:
            for event in calendar['vevent']:
                events.append(self.__parse_event(event))

        return events

    def __parse_event(self, event: dict):

        alarms = []
        for alarm in event['valarm']:
            alarms.append(
                self.__parse_alarm(alarm, event['dtstart'][0])
            )

        return Event(
            event['uid'],
            event['summary'],
            event['description'],
            event['dtstart'][0],
            event['dtend'][0],
            alarms
        )

    def __parse_alarm(self, alarm: dict, date_str):
        date = Date.from_date_str_and_date_diff(date_str, alarm['trigger'])

        return Alarm(
            date,
            alarm['description'],
            alarm['trigger']
        )
