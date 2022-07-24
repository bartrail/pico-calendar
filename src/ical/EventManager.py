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
        self.__set_today(now)
        self.events = events

    # run on every tick
    def update_from_rtc(self):
        date_tupel = self.rtc.datetime()
        # dont update now when we are in the same second
        if date_tupel[6] == self.now.seconds and date_tupel[5] == self.now.minute:
            return

        self.now = Date.from_rtc(self.rtc)

        if self.now.is_same_day(self.today):
            return

        self.__set_today(self.now)

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

    def __set_today(self, date):
        self.today = Date(date.year, date.month, date.day, 0, 0, 0)

    def first_event(self) -> 'Event':
        return self.events[0]

    def last_event(self) -> 'Event':
        return self.events[len(self.events) - 1]