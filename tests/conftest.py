import pytest

from pathlib import Path


@pytest.fixture
def fixtures():
    """Return the fixture Path."""
    return Path(__file__).parent / "fixtures"
