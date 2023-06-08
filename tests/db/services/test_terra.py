from pytest import fixture

from terrascrape.core.terra import Terra
from terrascrape.db.services import DBService
from terrascrape.db.services.terra import TerraService


class DBServiceTestTerra(Terra):
    @property
    def name(self):
        return 'db_service_test_terra'

    class Parameters(Terra.Parameters):
        date: str = ...

    def fetch(self, date):
        return {'date': date, 'url': 'https://db_test.com'}


@fixture(scope='session')
def test_terra_service(test_db_session):
    DBService(test_db_session)
    return TerraService()


def test_insert_and_get_terra(test_db_session, test_terra_service):
    test_terra_service.insert(DBServiceTestTerra())
    terra = test_terra_service.get('db_service_test_terra')
    assert terra.class_name == 'DBServiceTestTerra'
    assert terra.package_name == 'tests.db.services.test_terra'
    assert terra.parameters_schema.get('required') == ['date']
    assert terra.is_valid
