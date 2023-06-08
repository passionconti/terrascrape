from typing import Any, List

from pydantic import BaseModel, validator

from terrascrape.builder.models import OnErrorType, TriggerType
from terrascrape.db.models import ScrapStatus


class Results:
    def __init__(self):
        self._results = dict()

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        pass

    @property
    def finished_tasks(self):
        return list(self._results.keys())

    def save(self, task: str, task_data: Any):
        self._results[task] = task_data

    def load(self, task: str):
        return self._results.get(task)


class Job(BaseModel):
    name: str = ...
    tasks: List[str] = ...
    criteria: dict = None
    on_error: OnErrorType = OnErrorType.STOP
    trigger: TriggerType = TriggerType.SUCCEED

    status: ScrapStatus = ScrapStatus.READY
    results: Results = Results()

    @validator('tasks')
    def tasks_size_must_over_1(cls, v):
        if len(v) < 1:
            raise ValueError('task size must over 1')
        return v

    @property
    def is_always_triggered(self):
        return self.trigger == TriggerType.ANY
