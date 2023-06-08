from terrascrape.db.models import ScrapStatus
from terrascrape.db.services.task import TaskService
from terrascrape.engine.message_handler import MessageHandler
from terrascrape.engine.runner.task_runner import TaskRunner


class JobRunner:
    def __init__(self, message_handler: MessageHandler):
        self._message_handler = message_handler
        self._current_job = self._message_handler.current_job
        self._task_service = TaskService()

    def run(self):
        self._run_job()

    def _run_job(self):
        for task_name in self._current_job.tasks:
            task = self._task_service.get(task_name)
            task_data = TaskRunner(task, self._message_handler).run()
            self._message_handler.current_job.results.save(task_name, task_data)

        self._message_handler.current_status = ScrapStatus.SUCCEED
        # todo update finished tasks
