from machine import RTC
from src.model.Date import Date
from src.model.Event import Event


class EventManager:

    events: [Event]
    today: Date
    now: Date
    rtc: RTC

    def __init__(self, now: 'Date', rtc: RTC, events: [Event]):
        self.now = now
        self.rtc = rtc
        self.today = Date(now.year, now.month, now.day, 0, 0, 0)
        self.events = events

    # run on every tick
    def update_now_from_rtc(self):
        date_tupel = self.rtc.datetime()
        # dont update now when we are in the same second
        if date_tupel[0][6] != self.now.seconds or date_tupel[0][5] != self.now.minute:
            self.now = Date.from_rtc(self.rtc.datetime())

    def get_events_of_today(self) -> [Event]:
        events = []
        for event in self.events:
            if event.date_start.is_same_day(self.today):
                events.append(event)

        return events

    def get_events_of_tomorrow(self) -> [Event]:
        events = []
        tomorrow = self.today.get_next_day()
        for event in self.events:
            if event.date_start.is_same_day(tomorrow):
                events.append(event)

        return events