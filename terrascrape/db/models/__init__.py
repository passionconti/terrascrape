import enum


class ScrapStatus(enum.Enum):
    READY = enum.auto()
    SCRAPING = enum.auto()
    UP_FOR_RETRY = enum.auto()
    SUCCEED = enum.auto()
    FAILED = enum.auto()
