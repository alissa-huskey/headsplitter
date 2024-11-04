import pytest

from pathlib import Path

from headsplitter.writer import Writer


@pytest.fixture
def fixtures():
    """Return the fixture Path."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def clear_writer_count():
    """Clear the file count on the Writer class."""
    Writer.count = 0
