from pytest import fixture, raises

from terrascrape.core.task import Task
from terrascrape.engine.message_handler import MessageHandler
from terrascrape.engine.runner.message_runner import JobRunner
from terrascrape.exceptions import TASK_ERROR_HAS_TO_RUN_REQUIRED_TASK, TaskException


class SetConfigTask(Task):
    @property
    def name(self):
        return 'set_config'

    def run(self):
        self.set_config('key', 'value')


class GetConfigTask(Task):
    @property
    def name(self):
        return 'get_config'

    @property
    def required_tasks_in_job(self):
        return ['set_config']

    def run(self):
        value_from_config = self.get_from_config('key')
        return f'{value_from_config} comes from config'


class LoadResultTask(Task):
    @property
    def name(self):
        return 'load_result'

    @property
    def required_tasks_in_job(self):
        return ['get_config']

    def run(self):
        return self.load_from_job_results('get_config') + ' loaded'


@fixture(scope='function')
def test_message_for_task_handler(test_message_for_task_uuid_from_db):
    return MessageHandler(message_uuid=test_message_for_task_uuid_from_db)


def test_set_config_task(test_message_for_task_handler):
    test_message_for_task_handler.current_job = test_message_for_task_handler.message.jobs[0]
    JobRunner(test_message_for_task_handler).run()
    job_results = test_message_for_task_handler.current_job.results
    assert test_message_for_task_handler.config.get('key') == 'value'
    assert job_results.load('set_config') is None


def test_get_config_task(test_message_for_task_handler):
    test_message_for_task_handler.current_job = test_message_for_task_handler.message.jobs[0]
    JobRunner(test_message_for_task_handler).run()
    job_results = test_message_for_task_handler.current_job.results
    assert job_results.load('get_config') == 'value comes from config'


def test_load_result_task(test_message_for_task_handler):
    test_message_for_task_handler.current_job = test_message_for_task_handler.message.jobs[0]
    JobRunner(test_message_for_task_handler).run()
    job_results = test_message_for_task_handler.current_job.results
    assert job_results.load('load_result') == 'value comes from config loaded'


def test_check_required_task(test_message_to_check_required_task_uuid_from_db):
    test_to_check_required_task_handler = MessageHandler(test_message_to_check_required_task_uuid_from_db)
    test_to_check_required_task_handler.current_job = test_to_check_required_task_handler.message.jobs[0]
    with raises(TaskException) as e:
        JobRunner(test_to_check_required_task_handler).run()

    assert TASK_ERROR_HAS_TO_RUN_REQUIRED_TASK.format('set_config') in str(e.value)
