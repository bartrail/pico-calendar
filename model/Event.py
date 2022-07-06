from dataclasses import dataclass
import datetime
import Alarm

@dataclass(frozen=True)
class Event:
    uid: str
    summary: str
    description: str
    dateStart: datetime.datetime
    dateEnd: datetime.datetime
    alarms: [Alarm]