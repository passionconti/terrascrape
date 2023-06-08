from pytest import raises

from terrascrape.builder.models.job import Job
from terrascrape.db.models import ScrapStatus
from terrascrape.engine.message_handler import MessageConfig
from terrascrape.exceptions import CONFIG_ERROR_SET_EXIST_KEY, CONFIG_ERROR_SET_WITHOUT_ANY_TYPE, ConfigException


def test_message_config_with_any_triggered_job():
    message_config = MessageConfig()
    raw_data = {
        'name': 'job_any_trigger_test',
        'tasks': ['test_task_1'],
        'criteria': {'from': 1, 'to': 2},
        'trigger': 'ANY'
    }
    any_triggered_job = Job(**raw_data)
    message_config.set(any_triggered_job, 'key1', 123).set(any_triggered_job, 'key2', [1, 2, 3])
    assert message_config.get('key1') == 123
    with raises(ConfigException) as e:
        message_config.set(any_triggered_job, 'key2', [2, 3, 4])

    assert CONFIG_ERROR_SET_EXIST_KEY in str(e.value)


def test_set_config_with_succeed_triggered_job_in_message_config():
    message_config = MessageConfig()
    raw_data = {
        'name': 'job_succeed_trigger_test',
        'tasks': ['test_task_2'],
        'criteria': {'from': 1, 'to': 2},
        'trigger': 'SUCCEED'
    }
    succeed_job = Job(**raw_data)

    with raises(ConfigException) as e:
        message_config.set(succeed_job, 'key1', 123)

    assert CONFIG_ERROR_SET_WITHOUT_ANY_TYPE in str(e.value)


def test_get_message_in_message_handler(test_message_handler):
    assert test_message_handler.message.topic == 'test_message_topic'
    assert len(test_message_handler.message.jobs) == 3


def test_validate_components_in_message_handler(test_message_handler):
    assert test_message_handler.current_job is None
    assert test_message_handler.current_status == ScrapStatus.SUCCEED
    assert isinstance(test_message_handler.config, MessageConfig)


def test_set_config_in_message_handler(test_message_handler):
    test_message_handler.current_job = test_message_handler.message.jobs[0]
    test_message_handler.set_config('key1', 123)
    assert test_message_handler.config.get('key1') == 123
