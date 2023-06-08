from typing import List

from pydantic import BaseModel, validator

from terrascrape.builder.models.job import Job
from terrascrape.db.models import ScrapStatus


class Message(BaseModel):
    uuid: str = ...
    topic: str = ...
    contents: dict = dict()
    jobs: List[Job] = ...
    group_id: str = None
    next_message: str = None

    status: ScrapStatus = ScrapStatus.READY

    class Config:
        arbitrary_types_allowed = True

    @validator('jobs')
    def jobs_size_must_over_1(cls, v):
        if len(v) < 1:
            raise ValueError('job size must over 1')
        return v

    @validator('next_message')
    def next_message_should_be_with_group_id(cls, v, values):
        if v is not None and values.get('group_id') is None:
            raise ValueError('next message should be with group id')
        return v
