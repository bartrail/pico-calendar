from dataclasses import dataclass
import datetime

@dataclass(frozen=True)
class Alarm:
    description: str
    date: datetime.datetime