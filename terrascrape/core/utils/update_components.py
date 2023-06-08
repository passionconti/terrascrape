import os

from terrascrape import config
from terrascrape.core.builder import Builder
from terrascrape.core.task import Task
from terrascrape.core.terra import Terra
from terrascrape.core.utils.load_components import load_components, reset_modules_to_get_classes_in_file
from terrascrape.db.services.builder import BuilderService
from terrascrape.db.services.task import TaskService
from terrascrape.db.services.terra import TerraService


def update_terras(terras_path: str = None):
    terras_path = terras_path or config.directory.terra or os.getenv('TERRASCRAPE_PATH')
    TerraService().reset()
    for task_class in load_components(terras_path, Terra):
        TerraService().insert(task_class)
    reset_modules_to_get_classes_in_file()


def update_tasks(tasks_path: str = None):
    tasks_path = tasks_path or config.directory.tasks or os.getenv('TERRASCRAPE_PATH')
    TaskService().reset()
    for task_class in load_components(tasks_path, Task):
        TaskService().insert(task_class)
    reset_modules_to_get_classes_in_file()


def update_builders(builders_path: str = None):
    builders_path = builders_path or config.directory.builders or os.getenv('TERRASCRAPE_PATH')
    BuilderService().reset()
    for builder_class in load_components(builders_path, Builder):
        BuilderService().insert(builder_class)
    reset_modules_to_get_classes_in_file()


def update_whole_components(path: str = None):
    update_terras(path)
    update_tasks(path)
    update_builders(path)
