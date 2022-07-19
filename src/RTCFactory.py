from machine import RTC

from src.AppError import AppError
from src.Request import Request
from src.model.Date import Date

"""Initializes RTC by using an online time-service 
"""
class RTCFactory:

    rtc: RTC

    @staticmethod
    def init_rtc() -> 'Date':
        url = 'http://date.jsontest.com'
        json = Request.get_json(url)

        key = 'milliseconds_since_epoch'
        if key not in json:
            raise AppError.unexpected_content(
                'Expected to find key "{0}" in json payload from [{1}]'.format(key, url)
            )

        unixms = json[key]

        if type(unixms) is not int:
            raise AppError.unexpected_content(
                'Expected key "{0}" in json payload from [{1}] to be integer but got [{2}]'.format(
                    key,
                    url,
                    type(unixms)
                )
            )

        unix = int(str(unixms)[0:-3])
        ms   = unixms % 1000

        date = Date.from_unix(unix)
        tupel = (
            date.year,
            date.month,
            date.day,
            date.weekday - 1,
            date.hour,
            date.minute,
            date.seconds,
            ms
        )
        RTCFactory.rtc = RTC()
        RTCFactory.rtc.datetime(tupel)

        return date