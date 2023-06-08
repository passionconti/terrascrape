from terrascrape.db.models.task import Task
from terrascrape.engine.message_handler import MessageHandler


class TaskRunner:
    def __init__(self, task: Task, message_handler: MessageHandler):
        self._task = task
        self._message_handler = message_handler

    def run(self):
        return self._run_task()

    def _run_task(self):
        task = getattr(__import__(self._task.package_name, fromlist=[self._task.package_name]), self._task.class_name)()
        task.initialize(self._message_handler)
        return task.run()
