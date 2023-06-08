from typing import List

from pytest import fixture, raises

from terrascrape.builder.models.job import Job
from terrascrape.core.builder import Builder
from terrascrape.db.models.builder import Builder as DB_Builder
from terrascrape.db.services import DBService
from terrascrape.db.services.builder import BuilderService
from terrascrape.exceptions import ServiceException


class ServiceBuilder(Builder):
    class Contents(Builder.Contents):
        source_id: int = ...
        source_type: str = ...

    def create_jobs(self, contents: Contents) -> List[Job]:
        return [
            Job(
                name='test_job01',
                tasks=['task_01', 'task_02']
            ),
            Job(
                name='test_job02',
                tasks=['task_03', 'task_04']
            )
        ]

    @property
    def topic(self):
        return 'service_builder'


class AnotherServiceBuilder(ServiceBuilder):
    @property
    def topic(self):
        return 'another_service_builder'


class SameNameBuilder(ServiceBuilder):
    pass


@fixture(scope='function')
def test_builder_service(test_db_session):
    DBService(test_db_session)
    return BuilderService()


def test_get_builder_on_name(test_db_session, test_builder_service):
    test_db_session.add(
        DB_Builder(name='test_get_builder', package_name='tests.db.services.test_builder', class_name='ServiceBuilder'))
    builder = test_builder_service.get('test_get_builder')
    assert builder.class_name == 'ServiceBuilder'


def test_add_builder(test_builder_service):
    test_builder_service.insert(ServiceBuilder())
    builder = test_builder_service.get('service_builder')
    assert builder.package_name == 'tests.db.services.test_builder'
    assert builder.class_name == 'ServiceBuilder'
    assert 'source_id' in builder.contents_schema.get('required')
    # todo scope 변경으로 필요없도록 수정 필요
    test_builder_service.reset()


def test_load_builder_names_after_add_builder(test_builder_service):
    test_builder_service.insert(ServiceBuilder())
    assert 'service_builder' in test_builder_service._names
    test_builder_service.reset()


def test_raise_exception_when_same_name_of_builder(test_builder_service):
    test_builder_service.insert(ServiceBuilder())
    with raises(ServiceException) as e:
        test_builder_service.insert(SameNameBuilder())

    assert 'service_builder is already registered' in str(e.value)
    test_builder_service.reset()


def test_reset_builder(test_builder_service):
    test_builder_service.insert(ServiceBuilder())
    test_builder_service.reset()
    assert test_builder_service.get('service_builder') is None
    assert len(test_builder_service._names) == 0
