from src.ParseError import ParseError


class Date:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    unix: int
    date: str

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int):

        self.date = '{0}-{1}-{2} {3}:{4}'.format(
            year,
            '{:0>2}'.format(str(month)),
            '{:0>2}'.format(str(day)),
            '{:0>2}'.format(str(hour)),
            '{:0>2}'.format(str(minute)),
        )
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.unix = self.__calculate_unix()

        self.__assert_values()

        print(self.unix, self.date, self.year, self.month, self.day)

    @staticmethod
    def from_date_str(date_str: str) -> 'Date':
        # todo better format detection and more format supported once this is resolved https://github.com/micropython/micropython/issues/7920
        if not date_str.isdigit() and len(date_str) != 8:
            raise ParseError.date_format_invalid(date_str)

        year = int(date_str[0:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])

        return Date(year, month, day, 0, 0)

    @staticmethod
    def from_date_str_and_date_diff(date_str: str, date_diff: str):
        date = Date.from_date_str(date_str)

    def __calculate_unix(self) -> int:
        days = 0
        year = self.year
        while year >= 1970:
            for month in range(1, 13):
                # skip months later from current year
                if year == self.year and month > self.month:
                    continue

                # from current month, just take the date we have
                if year == self.year and month == self.month:
                    days += self.day
                    continue

                days += self.__number_of_days(year, month)

            year -= 1

        return days * 86400 + self.hour * 3600 + self.minute * 60

    def __number_of_days(self, y: int, m: int) -> int:
        leap = 0
        if y % 400 == 0:
            leap = 1
        elif y % 100 == 0:
            leap = 0
        elif y % 4 == 0:
            leap = 1
        if m == 2:
            return 28 + leap
        list = [1, 3, 5, 7, 8, 10, 12]
        if m in list:
            return 31
        return 30

    def is_greater(self, date: 'Date') -> bool:
        if (self.year > date.year):
            return True

        if (self.month > date.month):
            return True

        if (self.day > date.day):
            return True

        if (self.hour > date.hour):
            return True

        if (self.minute > date.minute):
            return True

        return False

    def is_lower(self, date: 'Date') -> bool:
        return not self.is_greater(date)

    def is_equal(self, date: 'Date') -> bool:
        return self.date == date.date

    def __assert_values(self):
        if self.year < 1900 or self.year > 2100:
            raise ParseError.year_out_of_range(self.year)

        if self.month < 1 or self.month > 12:
            raise ParseError.month_out_of_range(self.month)

        possible_days = self.__number_of_days(self.year, self.month)
        if (self.day < 0 or self.day > possible_days):
            raise ParseError.day_out_of_range(self.day, self.month, self.year, possible_days)

        if (self.hour < 0 or self.hour > 24):
            raise ParseError.hour_out_of_range(self.hour)

        if (self.minute < 0 or self.minute > 60):
            raise ParseError.minute_out_of_range(self.minute)
