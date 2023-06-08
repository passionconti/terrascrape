from terrascrape.builder.models import TriggerType
from terrascrape.db.models import ScrapStatus
from terrascrape.engine.runner.message_runner import MessageRunner


def test_check_any_trigger_job_run(test_message_handler):
    test_message_handler.current_status = ScrapStatus.SUCCEED
    test_message_handler.message_status.finished_jobs = []
    message_runner = MessageRunner(message_handler=test_message_handler)
    any_trigger_job = test_message_handler.message.jobs[0]
    assert message_runner.check_to_run_job(any_trigger_job)

    test_message_handler.current_status = ScrapStatus.FAILED
    assert message_runner.check_to_run_job(any_trigger_job)

    test_message_handler.message_status.finished_jobs.append(any_trigger_job.name)
    assert message_runner.check_to_run_job(any_trigger_job)


def test_check_succeed_trigger_job_run(test_message_handler):
    test_message_handler.current_status = ScrapStatus.SUCCEED
    test_message_handler.message_status.finished_jobs = []

    message_runner = MessageRunner(message_handler=test_message_handler)
    succeed_trigger_job = test_message_handler.message.jobs[1]
    assert message_runner.check_to_run_job(succeed_trigger_job)

    test_message_handler.current_status = ScrapStatus.FAILED
    assert not message_runner.check_to_run_job(succeed_trigger_job)

    test_message_handler.message_status.finished_jobs.append(succeed_trigger_job.name)
    assert not message_runner.check_to_run_job(succeed_trigger_job)


def test_check_failed_trigger_job_run(test_message_handler):
    test_message_handler.current_status = ScrapStatus.SUCCEED
    test_message_handler.message_status.finished_jobs = []

    message_runner = MessageRunner(message_handler=test_message_handler)
    failed_trigger_job = test_message_handler.message.jobs[2]
    assert not message_runner.check_to_run_job(failed_trigger_job)

    test_message_handler.current_status = ScrapStatus.FAILED
    assert message_runner.check_to_run_job(failed_trigger_job)

    test_message_handler.message_status.finished_jobs.append(failed_trigger_job.name)
    assert not message_runner.check_to_run_job(failed_trigger_job)


def test_update_message_status_finished_jobs_after_run_message_runner(test_message_handler):
    test_message_handler.current_status = ScrapStatus.SUCCEED
    test_message_handler.message_status.finished_jobs = []

    MessageRunner(message_handler=test_message_handler).run()
    assert len(test_message_handler.message_status.finished_jobs) == len(
        [job for job in test_message_handler.message.jobs if job.trigger != TriggerType.FAILED])
