from typing import Any, Optional

from terrascrape.builder.models.job import Job
from terrascrape.builder.models.message import Message
from terrascrape.db.models import ScrapStatus
from terrascrape.db.models.message_status import MessageStatus
from terrascrape.db.services.message_status import MessageStatusService
from terrascrape.exceptions import CONFIG_ERROR_SET_EXIST_KEY, CONFIG_ERROR_SET_WITHOUT_ANY_TYPE, ConfigException, \
    MESSAGE_ERROR_ILLEGAL_FORMAT, MessageException


class MessageConfig:
    def __init__(self):
        self._config = dict()

    def set(self, job: Job, key: str, value: Any):
        if not job.is_always_triggered:
            raise ConfigException(CONFIG_ERROR_SET_WITHOUT_ANY_TYPE)
        if key in self._config:
            raise ConfigException(CONFIG_ERROR_SET_EXIST_KEY)
        self._config[key] = value
        return self

    def get(self, key: str, default=None) -> Any:
        return self._config.get(key, default)


class MessageHandler:
    def __init__(self, message_uuid: str):
        self.message_status = self._get_message_status(message_uuid)
        self.message = self._get_message()
        self.current_job: Optional[Job] = None
        self.current_status = ScrapStatus.SUCCEED
        self.config = MessageConfig()

    @staticmethod
    def _get_message_status(message_uuid: str) -> MessageStatus:
        return MessageStatusService().get(message_uuid)

    def _get_message(self) -> Message:
        try:
            return Message(**self.message_status.message)
        except Exception:
            raise MessageException(MESSAGE_ERROR_ILLEGAL_FORMAT)

    def set_config(self, key: str, value: Any):
        self.config.set(self.current_job, key, value)
