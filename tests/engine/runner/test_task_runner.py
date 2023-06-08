from terrascrape.db.services.task import TaskService
from terrascrape.engine.runner.task_runner import TaskRunner


def test_run_task_runner(test_message_handler):
    test_message_handler.current_job = test_message_handler.message.jobs[0]
    task_name = test_message_handler.current_job.tasks[0]
    task = TaskService().get(task_name)
    assert TaskRunner(task=task, message_handler=test_message_handler).run() is None
