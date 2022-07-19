from src.model.Date import Date


class Alarm:
    date: Date
    description: str
    trigger: str

    def __init__(self, date: 'Date', description: str, trigger: str):
        self.date = date
        self.description = description
        self.trigger = trigger