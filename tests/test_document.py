from pathlib import Path

import pytest
from anytree import RenderTree, AsciiStyle

from mdsplitter.document import Document

from . import assert_tree_equal, Stub

bp = breakpoint


def test_document():
    doc = Document()
    assert doc


def test_document_path(fixtures):
    """
    GIVEN: A new Document object
    WHEN: a Path object is passed as the path kwarg
    THEN: .path should be set to that path
    """
    file = fixtures / "markdown.md"
    doc = Document(path=file)
    assert doc.path == file


def test_document_path_str():
    """
    GIVEN: A new Document object
    WHEN: a str object is passed as the path kwarg
    THEN: .path should be set to a Path object for that string
    """
    doc = Document(path="somefile.py")
    assert doc.path == Path("somefile.py")


def test_document_title():
    """
    GIVEN: A document with a path.
    WHEN: .title is accessed
    THEN: the path stem is returned
    """
    doc = Document(path=Path("my-book.md"))
    assert doc.title == "my-book"


def test_document_tokens(fixtures):
    """
    GIVEN: A new document object with a path and no tokens
    WHEN: .tokens is accessed
    THEN: it should return a list of parsed tokens
    """
    path = fixtures / "simple.md"
    doc = Document(path=path)
    assert len(doc.tokens) == 6
    assert doc.tokens[1].content == "Simple Markdown File"
    assert doc.tokens[4].content == "This is a very simple markdown file."


def test_document_heading_tokens():
    """
    GIVEN: A document with header tokens.
    WHEN: .header_tokens is accessed
    THEN: a dictionary of line no -> header tokens should be returned
    """
    doc = Document(tokens=[
        (a := Stub(type="heading_open", name="a")),
        Stub(type="inline"),
        Stub(type="heading_close"),
        (b := Stub(type="heading_open", name="b")),
        Stub(type="inline"),
        Stub(type="heading_close"),
        (c := Stub(type="heading_open", name="c")),
        Stub(type="inline"),
        Stub(type="heading_close"),
    ])

    assert doc.heading_tokens == {0: a, 3: b, 6: c}


def test_document_headings(fixtures):
    """
    GIVEN: A document with headers
    WHEN: .headings is accessed
    THEN: a list of Heading objects should be returned
    """
    doc = Document(path=fixtures / "simple_headings.md")
    assert len(doc.headings) == 4
    assert doc.headings[0].title == "A Simple Markdown Document With Headings"
    assert doc.headings[0].level == 1

    assert doc.headings[1].title == "Subheading A"
    assert doc.headings[1].level == 2

    assert doc.headings[2].title == "Subheading B"
    assert doc.headings[2].level == 2

    assert doc.headings[3].title == "Subheading C"
    assert doc.headings[3].level == 2


def test_document_tree(fixtures):
    """
    GIVEN: A document with headings
    WHEN: .tree is accessed
    THEN: a list of root node section should be returned
    """
    doc = Document(path=fixtures / "complex_headings.md")

    tree = """
complex_headings
+-- Main
    |-- A
    |   |-- I
    |   +-- II
    |       |-- 1
    |       +-- 2
    |-- B
    +-- C
    """

    assert_tree_equal(doc.tree, tree)


def test_document_():
    """
    GIVEN: ...
    WHEN: ...
    THEN: ...
    """
