from enum import IntEnum


class ClueStatus(IntEnum):
    PENDING = 0
    RUNNING = 100
    SUCCESS = 200
    FAILED = 500
