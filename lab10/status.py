from enum import Enum

class Status(Enum):
    FOLLOWER = 1
    LEADER = 2
    CANDIDATE = 3