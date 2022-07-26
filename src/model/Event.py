from src.model.Alarm import Alarm
from src.model.Date import Date


class Event:
    uid: str
    summary: str
    description: str
    date_start: Date
    date_end: Date
    alarms: [Alarm]

    def __init__(self, uid: str, summary: str, description: str, date_start: 'Date', date_end: 'Date', alarms):
        self.uid = uid
        self.summary = summary
        self.description = description
        self.date_start = date_start
        self.date_end = date_end
        self.alarms = alarms

    def print_alarm_dates(self) -> str:
        iso_strings = []
        for alarm in self.alarms:
            iso_strings.append(alarm.date.iso8601)

        return '/'.join(iso_strings)

    def has_alarm_for(self, date: 'Date') -> bool:
        for alarm in self.alarms:
            if alarm.date.is_greater(date):
                return True

        return False