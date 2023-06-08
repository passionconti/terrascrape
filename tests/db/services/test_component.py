from pytest import fixture

from terrascrape.core.component import Component
from terrascrape.db import Base
from terrascrape.db.models.component import ComponentMixin
from terrascrape.db.services import DBService
from terrascrape.db.services.component import ComponentService


class CustomServiceComponent(ComponentMixin, Base):
    __tablename__ = 'custom_service_components'


class CustomComponentService(ComponentService):
    def __init__(self):
        super().__init__(CustomServiceComponent)

    def _map_component_to_db_model(self, component: Component):
        return CustomServiceComponent(
            name=component.name,
            package_name=component.package_name,
            class_name=component.class_name,
        )


class CustomComponent(Component):
    @property
    def name(self):
        return 'test_custom_component'


@fixture(scope='session')
def test_custom_component_service(test_db_session):
    DBService(test_db_session)
    return CustomComponentService()


def test_insert_component(test_custom_component_service):
    test_custom_component_service.insert(CustomComponent())
    component = test_custom_component_service.get('test_custom_component')
    assert component.package_name == 'tests.db.services.test_component'
    assert component.class_name == 'CustomComponent'
    assert 'test_custom_component' in test_custom_component_service._names
