from terrascrape.builder.models import TriggerType
from terrascrape.builder.models.job import Job
from terrascrape.db.models import ScrapStatus
from terrascrape.engine.message_handler import MessageHandler
from terrascrape.engine.runner.job_runner import JobRunner


class MessageRunner:
    def __init__(self, message_handler: MessageHandler):
        self._message_handler = message_handler

    def _is_job_finished(self, job: Job) -> bool:
        if job.trigger == TriggerType.ANY:
            return False
        else:
            return job.name in self._message_handler.message_status.finished_jobs

    def _is_job_triggered(self, job: Job) -> bool:
        if job.trigger == TriggerType.SUCCEED:
            return self._message_handler.current_status == ScrapStatus.SUCCEED
        elif job.trigger == TriggerType.FAILED:
            return self._message_handler.current_status == ScrapStatus.FAILED
        else:
            return True

    def check_to_run_job(self, job: Job) -> bool:
        return self._is_job_triggered(job) and not self._is_job_finished(job)

    def run(self):
        self._run_message()

    def _run_message(self):
        for job in self._message_handler.message.jobs:
            if self.check_to_run_job(job):
                self._message_handler.current_job = job
                JobRunner(self._message_handler).run()
                self._message_handler.message_status.finished_jobs.append(job.name)

                # todo update finished job
