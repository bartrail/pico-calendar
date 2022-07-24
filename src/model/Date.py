import math

from machine import RTC
from src.ParseError import ParseError


class Date:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    seconds: int
    unix: int
    weekday: int
    iso8601: str

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, seconds: int):

        self.iso8601 = '{0}-{1}-{2}T{3}:{4}:{5}+00'.format(
            year,
            '{:0>2}'.format(str(month)),
            '{:0>2}'.format(str(day)),
            '{:0>2}'.format(str(hour)),
            '{:0>2}'.format(str(minute)),
            '{:0>2}'.format(str(seconds)),
        )
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.seconds = seconds

        self.__assert_values()

        self.unix = self.__calculate_unix()
        # https://stackoverflow.com/questions/36389130/how-to-calculate-the-day-of-the-week-based-on-unix-time
        self.weekday = (math.floor(self.unix / 86400) + 4) % 7

    @staticmethod
    def from_date_str(date_str: str) -> 'Date':
        # todo better format detection and more format supported once this is resolved https://github.com/micropython/micropython/issues/7920
        if not date_str.isdigit() and len(date_str) != 8:
            raise ParseError.date_format_invalid(date_str)

        year = int(date_str[0:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])

        return Date(year, month, day, 0, 0, 0)

    @staticmethod
    def from_unix(unix: int) -> 'Date':
        days_from_1970 = int(unix / 86400)
        seconds_left = unix % 86400
        hours = int(seconds_left / 3600)
        minutes = int((seconds_left - hours * 3600) / 60)
        seconds = seconds_left % 60

        # we add +1 because we add the days AFTER january, the 1st 1970!
        days_left = days_from_1970 + 1
        year = 1970
        month = 1
        while days_left > 0:
            days_per_year = 366 if Date.__is_leap_year(year) else 365

            # when there are more days per year left, increase the year first sca
            if days_left > days_per_year:
                year += 1
                days_left -= days_per_year
                continue

            # count the months
            if days_left <= days_per_year:
                days_per_month = Date.__days_in_month(year, month)
                # when we have days for the current month left, increase month
                if days_left - days_per_month > 0:
                    days_left -= days_per_month
                    month += 1

                # when we have no days left, exit the loop
                if days_left - days_per_month <= 0:
                    break

        return Date(year, month, days_left, hours, minutes, seconds)

    @staticmethod
    def from_rtc(rtc: 'RTC') -> 'Date':
        # tupel of (year, month, day, weekday, hours, minutes, seconds, subseconds)
        tupel = rtc.datetime()
        return Date(
            tupel[0],
            tupel[1],
            tupel[2],
            tupel[4],
            tupel[5],
            tupel[6],
        )

    def __calculate_unix(self) -> int:
        days = 0
        year = self.year
        while year >= 1970:
            for month in range(1, 13):
                # skip months later from current year
                if year == self.year and month > self.month:
                    continue

                # from current month, just take the day we have
                if year == self.year and month == self.month:
                    days += self.day - 1 # subtract one day because math :P
                    continue

                days += Date.__days_in_month(year, month)

            year -= 1

        return days * 86400 + self.hour * 3600 + self.minute * 60 + self.seconds

    @staticmethod
    def __is_leap_year(year: int) -> bool:
        leap = False

        if year % 400 == 0:
            leap = True
        elif year % 100 == 0:
            leap = False
        elif year % 4 == 0:
            leap = True

        return leap

    @staticmethod
    def __days_in_month(y: int, m: int) -> int:
        leap = 1 if Date.__is_leap_year(y) else 0
        if m == 2:
            return 28 + leap
        list = [1, 3, 5, 7, 8, 10, 12]
        if m in list:
            return 31
        return 30

    def is_same_day(self, date: 'Date') -> bool:
        return self.year == date.year and self.month == date.month and self.day == date.day

    def get_next_day(self) -> 'Date':
        return Date.from_unix(self.unix + 86400)

    def is_greater(self, date: 'Date') -> bool:
        return self.unix > date.unix

    def is_lower(self, date: 'Date') -> bool:
        return not self.is_greater(date)

    def is_equal(self, date: 'Date') -> bool:
        return self.iso8601 == date.iso8601

    def __assert_values(self):
        if self.year < 1900 or self.year > 2100:
            raise ParseError.year_out_of_range(self.year)

        if self.month < 1 or self.month > 12:
            raise ParseError.month_out_of_range(self.month)

        possible_days = Date.__days_in_month(self.year, self.month)
        if self.day < 0 or self.day > possible_days:
            raise ParseError.day_out_of_range(self.day, self.month, self.year, possible_days)

        if self.hour < 0 or self.hour > 24:
            raise ParseError.hour_out_of_range(self.hour)

        if self.minute < 0 or self.minute > 60:
            raise ParseError.minute_out_of_range(self.minute)
