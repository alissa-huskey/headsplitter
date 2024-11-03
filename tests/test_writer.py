from pathlib import Path

import pytest

from mdsplitter.writer import Writer

bp = breakpoint


def test_writer():
    writer = Writer()
    assert writer

def test_writer_dest():
    """
    GIVEN: A Writer object with an output dir and name
    WHEN: .destination is accessed
    THEN: the path to the output file should be returned
    """
    cwd = Path()
    writer = Writer(dir=cwd, name="file")

    assert writer.dest == cwd / "file.md"


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
    outfile = tmp_path / "def.md"
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
