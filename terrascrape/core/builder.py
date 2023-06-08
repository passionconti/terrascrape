from abc import abstractmethod
from traceback import format_exc
from typing import List, Type

from pydantic import BaseModel, ValidationError

from terrascrape.builder.models.job import Job
from terrascrape.builder.models.message import Message
from terrascrape.core.component import Component
from terrascrape.exceptions import BUILDER_CONTENTS_ERROR, BUILDER_MESSAGE_ERROR, BuilderException
from terrascrape.utils import generate_message_uuid


class Builder(Component):
    class Contents(BaseModel):
        pass

    @property
    @abstractmethod
    def topic(self) -> str:
        raise NotImplementedError(f'implement {self.class_name} topic')

    @property
    def name(self) -> str:
        return self.topic

    @property
    def contents_model(self) -> Type[Contents]:
        return self.Contents

    @abstractmethod
    def create_jobs(self, contents: Contents) -> List[Job]:
        raise NotImplementedError('implement create jobs')

    @classmethod
    def create_message(cls, contents: dict) -> Message:
        _inst = cls()
        try:
            contents = cls.Contents(**contents)
        except ValidationError as e:
            raise BuilderException(BUILDER_CONTENTS_ERROR,
                                   extra=dict(topic=_inst.topic, exception=e.__class__, message=str(e),
                                              tb=format_exc()))
        try:
            return Message(
                uuid=generate_message_uuid(),
                topic=_inst.name,
                contents=contents.dict(),
                jobs=cls.create_jobs(_inst, contents)
            )
        except ValidationError as e:
            raise BuilderException(BUILDER_MESSAGE_ERROR,
                                   extra=dict(topic=_inst.topic, exception=e.__class__, message=str(e),
                                              tb=format_exc()))
