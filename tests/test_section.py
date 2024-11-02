from mdsplitter.section import Section

from . import Stub

bp = breakpoint


def test_section():
    section = Section()
    assert section


def test_section_heading():
    heading = Stub(title="Part Two", level=2, line=200)
    section = Section(heading=heading)

    assert section.heading == heading
    assert section.name == "Part Two"
    assert section.level == 2
    assert section.first == 200
