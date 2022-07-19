
class AppError(Exception):

    def __init__(self, message):
        self.message = message

        super().__init__(self.message)

    @staticmethod
    def not_implemented(message):
        return AppError(message)

    @staticmethod
    def unexpected_content(message):
        return AppError(message)

    @staticmethod
    def request_failed(url: str, status_code: int):
        message = 'Error loading URL {0} with status code {1}'.format(url, status_code)
        return AppError(message)