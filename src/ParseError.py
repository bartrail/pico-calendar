
class ParseError(Exception):

    def __init__(self, message):
        self.message = message

        super().__init__(self.message)

    @staticmethod
    def date_format_invalid(date):
        message = 'Parsing date from [{0}] is not supported yet. Must be in format YYYYDDMM for now'.format(date)
        return ParseError(message)

    @staticmethod
    def year_out_of_range(year):
        return ParseError('Year must be between 2000 and 2100. {0} given'.format(year))

    @staticmethod
    def month_out_of_range(month):
        return ParseError('Month must be between 1 and 12. {0} given'.format(month))

    @staticmethod
    def day_out_of_range(day, month, year, maxDays):
        return ParseError('Day must be between 1 and {0} for {1}/{2}. {3} given'.format(
            maxDays,
            month,
            year,
            day
        ))

    @staticmethod
    def hour_out_of_range(hour):
        return ParseError('Hour must be between 0 and 24. {0} given'.format(hour))

    @staticmethod
    def minute_out_of_range(minute):
        return ParseError('Minute must be between 0 and 60. {0} given'.format(minute))
