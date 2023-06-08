import json

from click.testing import CliRunner

import terrascrape
from terrascrape.cli import WELCOME_TITLE, cli


def test_init():
    result = CliRunner().invoke(cli)
    assert result.exit_code == 0
    assert ("The Terrascrape CLI for build your own scrape pipeline." in result.output)


def test_welcome():
    result = CliRunner().invoke(cli, ["welcome"])
    assert result.exit_code == 0
    assert result.output.rstrip() == WELCOME_TITLE.rstrip()


def test_config():
    result = CliRunner().invoke(cli, ["config"])
    assert result.exit_code == 0
    assert json.loads(result.output)['debug'] == terrascrape.config.debug
