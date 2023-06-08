from abc import abstractmethod
from typing import Any, Optional

from terrascrape.core.component import Component
from terrascrape.engine.message_handler import MessageHandler
from terrascrape.exceptions import TASK_ERROR_HAS_TO_RUN_REQUIRED_TASK, TaskException


class Task(Component):
    def __init__(self):
        self._message_handler = None

    def initialize(self, message_handler: MessageHandler):
        self._set_message_handler(message_handler)
        self._check_required_task()

    def _check_required_task(self):
        for required_task in self.required_tasks_in_job:
            if required_task not in self._message_handler.current_job.results.finished_tasks:
                raise TaskException(TASK_ERROR_HAS_TO_RUN_REQUIRED_TASK.format(required_task))

    def _set_message_handler(self, message_handler: MessageHandler):
        self._message_handler = message_handler

    def get_from_config(self, key: str, default=None) -> Optional[Any]:
        return self._message_handler.config.get(key, default=default)

    def set_config(self, key: str, value: Any):
        self._message_handler.set_config(key, value)

    def load_from_job_results(self, task: str) -> Optional[Any]:
        return self._message_handler.current_job.results.load(task)

    @property
    def required_criteria_keys_in_job(self) -> Optional[list]:
        return []

    @property
    def required_tasks_in_job(self) -> Optional[list]:
        return []

    @abstractmethod
    def run(self):
        raise NotImplementedError('implement task run')
