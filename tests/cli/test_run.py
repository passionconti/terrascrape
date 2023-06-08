from click.testing import CliRunner

from terrascrape.cli import run


def test_run_help():
    result = CliRunner().invoke(run, ["--help"])
    assert result.exit_code == 0
    assert "Run some component of Terrascrape" in result.output


def test_run_terra():
    result = CliRunner().invoke(run, ["terra", "sample"])
    assert result.exit_code == 0
    assert 'Run sample terra successfully.' in result.output
