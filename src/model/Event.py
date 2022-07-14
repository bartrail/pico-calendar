#import datetime
from src.model.Alarm import Alarm
from src.model.Date import Date


class Event:
    uid: str
    summary: str
    description: str
    date_start: Date
    date_end: Date
    alarms: [Alarm]

    def __init__(self, uid: str, summary: str, description: str, date_start: str, date_end: str, alarms):
        self.uid = uid
        self.summary = summary
        self.description = description
        self.date_start = Date.from_date_str(date_start)
        self.date_end = Date.from_date_str(date_end)
        self.alarms = alarms
