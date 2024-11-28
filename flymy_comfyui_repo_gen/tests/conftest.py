import pathlib

import pytest


@pytest.fixture(scope="session")
def base_path():
    return pathlib.Path(__file__).parent
