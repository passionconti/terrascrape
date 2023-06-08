from pytest import fixture

from terrascrape.www.run import app


@fixture(scope='session')
def test_client():
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
