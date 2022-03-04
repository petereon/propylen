from click.testing import CliRunner
from propylen import *
import os
import shutil
import pytest

def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output
    
def test_init_defaults():
    runner = CliRunner()
    result = runner.invoke(cli, ["init", "test-project", "--path", "./test/artifacts"])
    
    os.makedirs("./test/artifacts", exist_ok=True)
    assert result.exit_code == 0
    assert "✨ Initializing new awesome project..." in result.output
    assert os.listdir("./test/artifacts") == ["test-project"]
    assert set(os.listdir("./test/artifacts/test-project")) == set(["src", "test", "Pipfile", "pyproject.toml", "README.md"])
    assert set(os.listdir("./test/artifacts/test-project/src/test-project")) == set(["__init__.py", "__main__.py"])
    shutil.rmtree("./test/artifacts")

def test_init_testless():
    runner = CliRunner()
    result = runner.invoke(cli, ["init", "test-project", "--path", "./test/artifacts", "--no-include-tests"])
    
    os.makedirs("./test/artifacts", exist_ok=True)
    assert result.exit_code == 0
    assert "✨ Initializing new awesome project..." in result.output
    assert os.listdir("./test/artifacts") == ["test-project"]
    assert set(os.listdir("./test/artifacts/test-project")) == set(["src", "Pipfile", "pyproject.toml", "README.md"])
    shutil.rmtree("./test/artifacts")
    
