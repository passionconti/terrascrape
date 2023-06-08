import enum


class OnErrorType(enum.Enum):
    STOP = 'STOP'
    IGNORE = 'IGNORE'


class TriggerType(enum.Enum):
    ANY = 'ANY'
    FAILED = 'FAILED'
    SUCCEED = 'SUCCEED'
