import urequests
import json
import re

from src.AppError import AppError
from src.helper import regex_findall
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
                ev = self.__parse_event(event)
                # print('Event "{0}" at {1} with alarm at {2}'.format(
                #     ev.summary,
                #     ev.date_start.iso8601,
                #     ev.alarms[0].date.iso8601
                # ))
                events.append(ev)

        return events

    def __parse_event(self, event: dict):

        alarms = []
        date_start = Date.from_date_str(event['dtstart'][0])
        date_end = Date.from_date_str(event['dtstart'][0])

        for alarm in event['valarm']:
            alarms.append(self.__parse_alarm(alarm, date_start))

        return Event(
            event['uid'],
            event['summary'],
            event['description'],
            date_start,
            date_end,
            alarms
        )

    """Parses the alarm from the TRIGGER by calculating a new date
https://www.kanzaki.com/docs/ical/trigger.html
Formats:

-PT16H
-P23T
-P12T5H
-PT23M
-P10T12H34M
-P3T4H2M  
    """
    def __parse_alarm(self, alarm: dict, date_offset: 'Date'):

        trigger_offset = list(regex_findall('\d+\D', alarm['trigger']))

        seconds = 0
        for part in trigger_offset:
            num = int(re.search('\d+', part).group(0))
            date_range = part[-1]
            if date_range == 'T':
                seconds += num * 86400
            if date_range == 'H':
                seconds += num * 3600
            if date_range == 'M':
                seconds += num * 60
            if date_range == 'S':
                seconds += num

        alarm_date = Date.from_unix(date_offset.unix - seconds)

        return Alarm(
            alarm_date,
            alarm['description'],
            alarm['trigger']
        )

    # https://www.kanzaki.com/docs/ical/trigger.html
    @staticmethod
    def __parse_date_from_date_str_and_trigger(date_str: str, trigger: str):
        date = Date.from_date_str(date_str)

        if 'RELATED' in trigger:
            raise AppError.not_implemented('The trigger parsing of RELATED is not yet implemented')

        if 'VALUE=' in trigger:
            raise AppError.not_implemented('The trigger parsing of an absolute VALUE is not yet implemented')

        raise AppError.not_implemented('The trigger parsing by regex is not implemented yet as long as regular expressions dont really work for micropython')