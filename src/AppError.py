
class AppError(Exception):

    def __init__(self, message):
        self.message = message

        super().__init__(self.message)

    @staticmethod
    def not_implemented(message):
        return AppError(message)

