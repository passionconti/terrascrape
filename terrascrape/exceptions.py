class TerrascrapeException(Exception):
    """
    Base class for all Terrascrape's errors.
    Each custom exception should be derived from this class.
    """

    def __init__(self, message: str, extra: dict = None):
        self.message = message
        self.extra = extra

    def __str__(self):
        return f'{self.__class__.__name__}:{self.message}'


class WebserverException(TerrascrapeException):
    """
    Any errors occurred while running webserver
    """
    pass


WEBSERVER_ERROR_TIMEOUT = 'timeout'


class ServiceException(TerrascrapeException):
    """
    Any errors occurred at service logic
    """
    pass


SERVICE_ERROR_ALREADY_REGISTERED = '{} is already registered'


class ConfigException(TerrascrapeException):
    """
    Any errors related on config
    """
    pass


CONFIG_ERROR_SET_WITHOUT_ANY_TYPE = 'only ANY trigger_type can set config'
CONFIG_ERROR_SET_EXIST_KEY = 'key already exists in config'


class MessageException(TerrascrapeException):
    """
    Any errors related on message
    """
    pass


MESSAGE_ERROR_ILLEGAL_FORMAT = 'illegal message format'


class TaskException(TerrascrapeException):
    """
    Any errors related on tasks
    """
    pass


TASK_ERROR_HAS_TO_RUN_REQUIRED_TASK = '{} has to be run'


class TerraException(TerrascrapeException):
    """
    Any errors related on terras
    """
    pass


TERRA_PARAMETERS_ERROR = 'terra parameters error'
TERRA_FETCH_ERROR = 'terra fetch error'
TERRA_TRANSFORM_ERROR = 'terra transform error'
TERRA_VALIDATION_ERROR = 'terra fetched data is not passed in validation'


class BuilderException(TerrascrapeException):
    """
    Any errors related on builders
    """
    pass


BUILDER_CONTENTS_ERROR = 'builder contents validation error'
BUILDER_MESSAGE_ERROR = 'builder message validation error'
