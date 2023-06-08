from pydantic import ValidationError

from pytest import raises

from terrascrape.builder.models import OnErrorType, TriggerType
from terrascrape.builder.models.job import Job
from terrascrape.builder.models.message import Message


def test_message(test_raw_message):
    message = Message(**test_raw_message)

    assert message.uuid == 'test_message'
    assert message.topic == 'test_topic'
    assert message.contents.get('business_id') == 1

    assert message.jobs[0].name == 'prepare_job_01'
    assert message.jobs[0].trigger == TriggerType.ANY

    assert len(message.jobs[1].tasks) == 2
    assert message.jobs[1].criteria.get('aaa') == 1
    assert message.jobs[1].on_error == OnErrorType.STOP
    assert message.jobs[1].trigger == TriggerType.SUCCEED

    assert message.jobs[2].on_error == OnErrorType.IGNORE

    assert message.jobs[3].trigger == TriggerType.FAILED

    assert isinstance(message.jobs[0], Job)


def test_message_with_job_size_error():
    raw_data = {
        'uuid': 'test_message',
        'topic': 'test_topic',
        'contents': {
            'business_id': 1,
            'address': 'xxxxx',
        },
        'jobs': []
    }

    with raises(ValidationError) as e:
        _ = Message(**raw_data)

    assert 'size must over 1' in str(e.value)


def test_group_message():
    raw_data = {
        'uuid': 'test_message',
        'topic': 'test_topic',
        'contents': {
            'business_id': 1,
            'address': 'xxxxx',
        },
        'jobs': [
            {
                'name': 'job_01',
                'tasks': ['task_01', 'task_02'],
                'trigger': 'ANY',
            }
        ],
        'group_id': 'message_group',
        'next_message': 'test_next_message',
    }

    message = Message(**raw_data)

    assert message.group_id == 'message_group'
    assert message.next_message == 'test_next_message'


def test_message_with_next_message_group_id_error():
    raw_data = {
        'uuid': 'test_message',
        'topic': 'test_topic',
        'contents': {
            'business_id': 1,
            'address': 'xxxxx',
        },
        'jobs': [
            {
                'name': 'job_01',
                'tasks': ['task_01', 'task_02'],
                'trigger': 'ANY',
            }
        ],
        'next_message': 'test_next_message',
    }

    with raises(ValidationError) as e:
        _ = Message(**raw_data)

    assert 'next message should be with group id' in str(e.value)
