import ape
import pytest
from ape._cli import cli as ape_cli
from click.testing import CliRunner


@pytest.fixture
def networks():
    return ape.networks


@pytest.fixture
def accounts():
    return ape.accounts


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli():
    return ape_cli
