import pytest

from yadd import make_versions_file


@pytest.fixture(scope="session", autouse=True)
def session_fixture():
    make_versions_file()  # not really a test, but automatically keep version file up to date
