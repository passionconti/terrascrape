from pydantic import ValidationError

from pytest import raises

from terrascrape.builder.models import OnErrorType, TriggerType
from terrascrape.builder.models.job import Job


def test_defualt_job():
    raw_data = {
        'name': 'job_test',
        'tasks': ['test_task_1', 'test_task_2'],
        'criteria': {'from': 1, 'to': 2},
    }
    job = Job(**raw_data)

    assert job.name == 'job_test'
    assert len(job.tasks) == 2
    assert job.tasks[0] == 'test_task_1'
    assert job.criteria.get('from') == 1
    assert job.on_error == OnErrorType.STOP
    assert job.trigger == TriggerType.SUCCEED
    assert job.is_always_triggered is False


def test_ignore_error_failed_trigger_job():
    raw_data = {
        'name': 'job_ignore_error_failed_trigger_test',
        'tasks': ['test_task_3'],
        'criteria': {'from': 1, 'to': 2},
        'on_error': 'IGNORE',
        'trigger': 'FAILED'
    }
    job = Job(**raw_data)

    assert job.name == 'job_ignore_error_failed_trigger_test'
    assert job.on_error == OnErrorType.IGNORE
    assert job.trigger == TriggerType.FAILED


def test_is_always_triggered_any_trigger_job():
    raw_data = {
        'name': 'job_any_trigger_test',
        'tasks': ['test_task_1'],
        'criteria': {'from': 1, 'to': 2},
        'trigger': 'ANY'
    }
    job = Job(**raw_data)
    assert job.trigger == TriggerType.ANY
    assert job.is_always_triggered


def test_job_with_task_size_error():
    raw_data = {
        'name': 'job_test',
        'tasks': [],
    }

    with raises(ValidationError) as e:
        _ = Job(**raw_data)

    assert 'size must over 1' in str(e.value)


def test_job_with_required_field_error():
    raw_data = {
        'name': 'task_test',
    }

    with raises(ValidationError) as e:
        _ = Job(**raw_data)

    assert 'value_error.missing' in str(e.value)


def test_save_and_load_job_results():
    raw_data = {
        'name': 'job_test',
        'tasks': ['test_task_1', 'test_task_2'],
        'criteria': {'from': 1, 'to': 2},
    }
    job = Job(**raw_data)
    job.results.save('test_task_1', [1, 2, 3])
    assert job.results.load('test_task_1') == [1, 2, 3]
    assert job.results.load('test_task_2') is None
