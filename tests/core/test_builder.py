from typing import List

from pytest import raises

from terrascrape.builder.models.job import Job
from terrascrape.core.builder import Builder
from terrascrape.exceptions import BUILDER_CONTENTS_ERROR, BUILDER_MESSAGE_ERROR, BuilderException


class SampleBuilder(Builder):
    class Contents(Builder.Contents):
        source_id: int = ...
        source_type: str = ...

    def create_jobs(self, contents: Contents) -> List[Job]:
        return [
            Job(
                name='test_job01',
                tasks=['task_01', 'task_02']
            ),
            Job(
                name='test_job02',
                tasks=['task_03', 'task_04']
            )
        ]

    @property
    def topic(self):
        return 'sample_builder'


class EmptyJobBuilder(Builder):
    class Contents(Builder.Contents):
        source_id: int = ...
        source_type: str = ...

    def create_jobs(self, contents: Contents) -> List[Job]:
        return []

    @property
    def topic(self):
        return 'empty_job_builder'


def test_get_message():
    contents = {
        'source_id': 123,
        'source_type': 'place'
    }
    message = SampleBuilder.create_message(contents)
    assert len(message.jobs) == 2
    assert message.contents == contents
    assert message.topic == 'sample_builder'

    first_job = message.jobs[0]
    assert first_job.name == 'test_job01'
    assert len(first_job.tasks) == 2


def test_contents_with_format_error():
    with raises(BuilderException) as e:
        contents = {
            'source_id': 'abc',
            'source_type': 'place'
        }
        SampleBuilder.create_message(contents)
    assert BUILDER_CONTENTS_ERROR in str(e.value)


def test_builder_with_error():
    with raises(BuilderException) as e:
        contents = {
            'source_id': 123,
            'source_type': 'place'
        }
        EmptyJobBuilder.create_message(contents)
    assert BUILDER_MESSAGE_ERROR in str(e.value)
