import os
import tempfile

import pytest

from terrascrape import configuration

default_template = b"""
    debug = false
    [general]
    x = 1
    y = "hi"
        [general.nested]
        x = 2
        y = "bye"
    [logging]
    format = "log-format"
    [secrets]
    password = "1234"
    """

user_template = b"""
    [general]
        [general.nested]
        x = 3
    [logging]
    format = "custom-format"
    [secrets]
    password = "password"
    """


@pytest.fixture
def test_default_config_file_path():
    with tempfile.TemporaryDirectory() as test_config_dir:
        test_config_loc = os.path.join(test_config_dir, "test_config.toml")
        with open(test_config_loc, "wb") as test_default_config:
            test_default_config.write(default_template)
        yield test_config_loc


@pytest.fixture
def test_user_config_file_path():
    with tempfile.TemporaryDirectory() as test_config_dir:
        test_config_loc = os.path.join(test_config_dir, "test_config.toml")
        with open(test_config_loc, "wb") as test_user_config:
            test_user_config.write(user_template)
        yield test_config_loc


@pytest.fixture
def config(test_default_config_file_path, test_user_config_file_path, monkeypatch):
    monkeypatch.setenv("TERRASCRAPE__SECRETS__PASSWORD", "password123")
    monkeypatch.setenv("TERRASCRAPE__DEBUG", "true")
    monkeypatch.setenv("TERRASCRAPE__SUBSCRIBE_COUNT", "10")
    yield configuration.load_configuration(test_default_config_file_path, test_user_config_file_path)


def test_config(config):
    assert config.debug is True
    assert config.subscribe_count == 10
    assert config.general.x == 1
    assert config.general.nested.x == 3
    assert config.general.nested.y == 'bye'
    assert config.logging.format == 'custom-format'
    assert config.secrets.password == 'password123'
