import urequests
import json

from config import FIXTURES_MAP
from src.AppError import AppError


class Request:

    is_loading: bool

    @staticmethod
    def get(url: str) -> str:
        return Request.__get(url)

    @staticmethod
    def get_json(url):
        content = Request.__get(url)
        return json.loads(content)

    @staticmethod
    def __get(url: str) -> str:
        Request.is_loading = True
        if url in FIXTURES_MAP:
            print('loading file: {0}'.format(FIXTURES_MAP[url]))
            file = open(FIXTURES_MAP[url], "r")
            Request.is_loading = False

            return file.read()

        # todo handle timeouts

        print('request to: {0}'.format(url))
        request = urequests.get(url)
        print('request status: {0}'.format(request.status_code))
        content = request.content
        request.close()

        if request.status_code != 200:
            raise AppError.request_failed(url, request.status_code)

        Request.is_loading = False

        return content
