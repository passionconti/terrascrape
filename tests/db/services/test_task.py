from pytest import fixture, raises

from terrascrape.core.task import Task
from terrascrape.db.models.task import Task as DB_Task
from terrascrape.db.services import DBService
from terrascrape.db.services.task import TaskService
from terrascrape.exceptions import ServiceException


class ServiceTask(Task):
    @property
    def name(self):
        return 'test_service_task'

    @property
    def required_criteria_keys_in_job(self):
        return ['key']

    @property
    def required_tasks_in_job(self):
        return ['test_required_task']

    def run(self):
        return


class LoadTask(Task):
    @property
    def name(self):
        return 'test_load_task'

    def run(self):
        return


class SameNameOneTask(Task):
    @property
    def name(self):
        return 'test_same_name_task'

    def run(self):
        return


class SameNameTwoTask(SameNameOneTask):
    pass


class ResetTask(Task):
    @property
    def name(self):
        return 'test_reset_task'

    def run(self):
        return


@fixture(scope='session')
def test_task_service(test_db_session):
    DBService(test_db_session)
    return TaskService()


def test_get_task_on_name(test_db_session, test_task_service):
    test_db_session.add(
        DB_Task(name='test_get_task', package_name='tests.db.services.test_task', class_name='TestGetTask'))
    task = test_task_service.get('test_get_task')
    assert task.class_name == 'TestGetTask'


def test_add_task(test_task_service):
    test_task_service.insert(ServiceTask())
    task = test_task_service.get('test_service_task')
    assert task.package_name == 'tests.db.services.test_task'
    assert task.class_name == 'ServiceTask'
    assert 'test_required_task' in task.required_tasks


def test_load_task_names_after_add_task(test_task_service):
    test_task_service.insert(LoadTask())
    assert 'test_load_task' in test_task_service._names


def test_raise_exception_when_same_name_of_tasks(test_task_service):
    test_task_service.insert(SameNameOneTask())
    with raises(ServiceException) as e:
        test_task_service.insert(SameNameTwoTask())

    assert 'test_same_name_task is already registered' in str(e.value)


def test_reset_task(test_task_service):
    test_task_service.insert(ResetTask())
    test_task_service.reset()
    assert test_task_service.get('test_reset_task') is None
    assert len(test_task_service._names) == 0
