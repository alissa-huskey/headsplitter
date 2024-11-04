from pathlib import Path

import pytest

from headsplitter.writer import Writer

bp = breakpoint


def test_writer():
    writer = Writer()
    assert writer


def test_writer_name():
    """
    GIVEN: A Writer object with a name set.
    WHEN: .name is accessed
    THEN: the name should be lower-cased
    AND: the name should be dashed
    AND: the name should include the count for that writer
    AND: the name should include the count
    """
    writer = Writer(name="My Thingie")
    assert writer.name == "01-my-thingie.md"

def test_writer_dest():
    """
    GIVEN: A Writer object with an output dir and name
    WHEN: .destination is accessed
    THEN: the path to the output file should be returned
    """
    cwd = Path()
    writer = Writer(dir=cwd, name="file")

    assert writer.dest == cwd / "01-file.md"


def test_writer_lines():
    """
    GIVEN: A Writer object with source lines
    AND: a .bounds tuple containing start and end line numbers
    WHEN: .lines is accessed
    THEN: the lines specified by .bounds should be returned from .source.
    """
    writer = Writer(
        source=list("abcdefghijk"),
        bounds=(3,6),
    )
    assert writer.lines == ["d", "e", "f"]


def test_writer_write(fixtures, tmp_path):
    """
    GIVEN: A Writer object with a list of ._lines to write to a file
    AND: a destination dir and name
    WHEN: .write() is called
    THEN: the file should be created
    AND: those lines should be written to it.
    """
    outfile = tmp_path / "01-def.md"
    writer = Writer(
        lines=list("def"),
        bounds=(3,6),
        dir=tmp_path,
        name="def",
    )

    writer.write()

    assert outfile.is_file()
    assert outfile.read_text() == "d\ne\nf\n"


def test_writer_():
    """
    GIVEN: ...
    WHEN: ...
    THEN: ...
    """
