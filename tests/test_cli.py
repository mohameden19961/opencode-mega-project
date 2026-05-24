import pytest
from click.testing import CliRunner
from codeguard.cli import cli


class TestCLI:
    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_analyze_no_path(self, runner):
        result = runner.invoke(cli, ["analyze"])
        assert result.exit_code != 0

    def test_analyze_nonexistent(self, runner):
        result = runner.invoke(cli, ["analyze", "nonexistent.py"])
        assert result.exit_code == 0

    def test_init(self, runner, tmp_path):
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["init", "--output", ".codeguard.yml"])
            assert result.exit_code == 0
            assert (tmp_path / ".codeguard.yml").exists()
