import os.path
import sys
from pathlib import Path
from pytest import fixture

from terrascrape.core.task import Task
from terrascrape.core.utils.load_components import (
    MODULE_PREFIX,
    get_all_bases_in_class,
    get_classes_in_file,
    get_code_string_in_file,
    get_files_imported_class_in_directory,
    get_inheritance_classes_in_directory,
    is_class_imported,
    is_inherited_class,
    load_components,
    reset_modules_to_get_classes_in_file,
)
from terrascrape.db.services import DBService
from terrascrape.db.services.task import TaskService


class CustomTask(Task):
    @property
    def name(self):
        return 'custom_task'

    def run(self):
        return 'test run'


class OneDepthTask(CustomTask):
    @property
    def name(self):
        return 'one_depth_task'

    def run(self):
        return 'test one depth run'


class TwoDepthTask(OneDepthTask):
    @property
    def name(self):
        return 'two_depth_task'

    def run(self):
        return 'test two depth run'


@fixture(scope='session')
def file():
    return Path(__file__)


@fixture(scope='session')
def directory():
    return os.path.dirname(__file__)


@fixture(scope='session')
def test_task_service(test_db_session):
    DBService(test_db_session)
    return TaskService()


def test_get_all_bases_in_class():
    one_depth_bases = get_all_bases_in_class(OneDepthTask)
    assert CustomTask in one_depth_bases
    assert Task in one_depth_bases

    two_depth_bases = get_all_bases_in_class(TwoDepthTask)
    assert OneDepthTask in two_depth_bases
    assert CustomTask in two_depth_bases
    assert Task in two_depth_bases


def test_get_code_string_in_file(file):
    code = get_code_string_in_file(file)
    assert 'test_get_code_string_in_file' in code


def test_get_files_imported_class_in_directory(directory):
    files = get_files_imported_class_in_directory(directory, 'Path')
    assert len(files) > 0


def test_get_classes_in_file(file):
    assert 'Task' in get_classes_in_file(file)


def test_get_inheritance_classes_in_directory(directory):
    test_dirname = os.path.dirname(os.path.dirname(directory))
    inheritance_classes = get_inheritance_classes_in_directory(test_dirname, Task)
    assert len(inheritance_classes) > 0


def test_is_class_imported(file):
    assert is_class_imported(file, 'Path')
    assert not is_class_imported(file, 'List')


def test_is_inherited_class():
    assert is_inherited_class(CustomTask, Task)
    assert not is_inherited_class(TaskService, Task)


def test_load_task_components(directory):
    components = load_components(directory, Task)
    assert CustomTask().name in [component.name for component in components]
    assert all([isinstance(component, Task) for component in components])


def test_reset_modules_to_get_classes(file):
    get_classes_in_file(file)
    reset_modules_to_get_classes_in_file()
    assert len([module for module in sys.modules.keys() if MODULE_PREFIX in module]) == 0
