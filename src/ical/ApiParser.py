import json
import re
import urequests

from src.helper import regex_findall, print_debug
from src.model.Alarm import Alarm
from src.model.Date import Date
from src.model.Event import Event


class ApiParser:

    def __init__(self, content):
        self.content = content

    def parse_response(self):

        events = []
        vcalendar = self.content['vcalendar']

        for calendar in vcalendar:
            for event in calendar['vevent']:
                ev = self.__parse_event(event)
                print_debug('Event "{0}" at {1} with alarms at {2}'.format(
                    ev.summary,
                    ev.date_start.iso8601,
                    ev.print_alarm_dates()
                ))
                events.append(ev)

        return events

    def __parse_event(self, event: dict) -> 'Event':

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
    def __parse_alarm(self, alarm: dict, date_offset: 'Date') -> 'Alarm':

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
