
from dataclasses import dataclass


@dataclass
class UserSession:
    activity_type: str
    duration: int
    exertion_level: str

