from mdsplitter.section import Section
from mdsplitter.object import Object as Stub

bp = breakpoint


def test_section():
    section = Section()
    assert section
