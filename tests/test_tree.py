import pytest
from anytree import Node, NodeMixin

from headsplitter.document import Document
from headsplitter.section import Section
from headsplitter.tree import Tree

# NOTE: don't use tests.Stub here, it breaks node.children
from headsplitter.object import Object as Stub

from . import assert_tree_equal, render_tree

bp = breakpoint


def test_tree():
    tree = Tree()
    assert tree


def test_tree_document():
    """
    WHEN: A new Tree object is constructed with a document kwarg passed
    THEN: The .document attribute should be set
    AND: The .headings attribute should be set
    """
    doc = Stub(lines="\n"*40, title="My Document", headings=["A", "B", "C"])
    tree = Tree(document=doc)

    assert tree.document == doc
    assert tree.title == "My Document"
    assert tree.headings == ["A", "B", "C"]
    assert tree.line_count == 40

def test_tree_build():
    """
    GIVEN: A Tree with with headings
    WHEN: .build() is called
    THEN: a list of section nodes should be returned
    AND: the nodes should be build in a tree by heading
    """
    tree = Tree(headings=(
        Stub(title="Main", line=1, level=1),
        Stub(title="A", line=10, level=2),
        Stub(title="B", line=20, level=2),
        Stub(title="C", line=30, level=2),
    ))
    tree.build()

    text = """
Document
+-- Main
    |-- A
    |-- B
    +-- C
    """

    assert tree.sections

    assert_tree_equal(tree, text)

def test_tree_():
    """
    GIVEN: ...
    WHEN: ...
    THEN: ...
    """
