from pydantic import validator
from pytest import fixture, raises

import requests

from terrascrape.core.terra import Terra
from terrascrape.exceptions import (
    TERRA_FETCH_ERROR,
    TERRA_PARAMETERS_ERROR,
    TERRA_TRANSFORM_ERROR,
    TERRA_VALIDATION_ERROR,
    TerraException,
)


class MockResponse:
    @staticmethod
    def json():
        return {'k1': 'abc', 'k2': 123}


class ValidateErrorMockResponse:
    @staticmethod
    def json():
        return {'k2': 123}


@fixture
def mock_simple_terra_fetch(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)


@fixture
def mock_validate_error_simple_terra_fetch(monkeypatch):
    def mock_get(*args, **kwargs):
        return ValidateErrorMockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)


class SimpleTerra(Terra):
    @property
    def name(self):
        return 'simple_terra'

    class Parameters(Terra.Parameters):
        id: int = ...
        test_from: str = ...
        test_to: str = ...

        @validator('id')
        def user_id_must_over_1(cls, v):
            if v < 1:
                raise ValueError('id must over 1')
            return v

    def fetch(self, parameters: Parameters):
        results = requests.get('https://test.com').json()
        results['id'] = parameters.id
        results['period'] = {'from': parameters.test_from, 'to': parameters.test_to}
        return results

    def transform(self, fetched_data):
        fetched_data.update({'url': 'https://test.com'})
        return fetched_data

    def validate(self, fetched_data):
        return 'k1' in fetched_data


class RealAPITESTTerra(Terra):
    @property
    def name(self):
        return 'real_api_test_terra'

    class Parameters(Terra.Parameters):
        user_id: int = ...

    def fetch(self, parameters: Parameters):
        return requests.get(f'https://jsonplaceholder.typicode.com/todos/{str(parameters.user_id)}',
                            verify=False).json()

    def validate(self, fetched_data):
        return fetched_data.get('userId') is not None


class FetchErrorTestTerra(Terra):
    @property
    def name(self):
        return 'fetch_error_test_terra'

    class Parameters(Terra.Parameters):
        id: int = ...

    def fetch(self, parameters: Parameters):
        raise Exception('test error')


class TransformErrorTestTerra(Terra):
    @property
    def name(self):
        return 'transform_error_test_terra'

    class Parameters(Terra.Parameters):
        id: int = ...

    def fetch(self, parameters: Parameters):
        return requests.get('https://test.com').json()

    def transform(self, fetched_data):
        fetched_data['k3'] = fetched_data['k3'] + fetched_data['k2']
        return fetched_data


def test_run_in_terra(mock_simple_terra_fetch):
    results = SimpleTerra().run(id=1, test_from='yesterday', test_to='today')
    assert results.fetched_data['k1'] == 'abc'
    assert results.fetched_data['period']['from'] == 'yesterday'
    assert results.fetched_data['id'] == 1
    assert 'url' not in results.fetched_data
    assert results.transformed_data['url'] == 'https://test.com'


def test_check_fetch_parameters_in_terra(mock_simple_terra_fetch):
    with raises(TerraException) as e:
        SimpleTerra().run(test_from='yesterday')

    assert TERRA_PARAMETERS_ERROR in e.value.message


def test_check_fetch_parameters_validator_in_terra(mock_simple_terra_fetch):
    with raises(TerraException) as e:
        SimpleTerra().run(id=0, test_from='yesterday', test_to='today')

    assert TERRA_PARAMETERS_ERROR in e.value.message
    assert 'id must over 1' in e.value.extra['message']


def test_fetch_error_in_terra():
    with raises(TerraException) as e:
        FetchErrorTestTerra().run(id=1)

    assert TERRA_FETCH_ERROR in e.value.message
    assert 'test error' in e.value.extra['message']


def test_transform_error_in_terra(mock_simple_terra_fetch):
    with raises(TerraException) as e:
        TransformErrorTestTerra().run(id=1)

    assert TERRA_TRANSFORM_ERROR in e.value.message
    assert 'k3' in e.value.extra['message']


def test_validate_in_terra(mock_validate_error_simple_terra_fetch):
    with raises(TerraException) as e:
        SimpleTerra().run(id=1, test_from='yesterday', test_to='today')

    assert TERRA_VALIDATION_ERROR in e.value.message
    assert e.value.extra['name'] == 'simple_terra'
    assert e.value.extra['fetched_data'] == {'k2': 123, 'id': 1, 'period': {'from': 'yesterday', 'to': 'today'}}


def test_run_in_real_api_terra():
    results = RealAPITESTTerra().run(user_id=1)
    assert results.fetched_data['userId'] == 1
    assert results.fetched_data.get('completed', False) is False
    assert results.transformed_data == results.fetched_data
