from terrascrape.core.task import Task
from terrascrape.db.models.task import Task as DB_Task
from terrascrape.db.services.component import ComponentService


class TaskService(ComponentService):
    def __init__(self):
        super().__init__(DB_Task)

    def _map_component_to_db_model(self, task: Task) -> DB_Task:
        return DB_Task(
            name=task.name,
            package_name=task.package_name,
            class_name=task.class_name,
            required_criteria_keys=task.required_criteria_keys_in_job,
            required_tasks=task.required_tasks_in_job,
            description=task.description,
        )
