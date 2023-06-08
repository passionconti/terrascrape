from terrascrape.db.models import ScrapStatus
from terrascrape.engine.runner.job_runner import JobRunner


def test_save_results_after_run_job_runner(test_message_handler):
    test_message_handler.current_job = test_message_handler.message.jobs[0]
    tasks = test_message_handler.current_job.tasks
    JobRunner(message_handler=test_message_handler).run()
    assert test_message_handler.current_job.results.load(tasks[0]) is None
    assert test_message_handler.current_job.results.finished_tasks == tasks
    assert test_message_handler.current_status == ScrapStatus.SUCCEED
