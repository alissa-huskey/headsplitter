import pytest
from anytree import Node, NodeMixin

from mdsplitter.document import Document
from mdsplitter.object import Object as Stub
from mdsplitter.tree import Tree

from . import assert_tree_equal, render_tree

bp = breakpoint


class StubNode(Stub, NodeMixin):
    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.next = None


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

def test_tree_construct():
    """
    GIVEN: A Tree with with headings
    WHEN: .construct() is called
    THEN: a list of section nodes should be returned
    AND: the nodes should be organized in a tree by heading
    """
    tree = Tree(headings=(
        Stub(title="Main", line=1, level=1),
        Stub(title="A", line=10, level=2),
        Stub(title="B", line=20, level=2),
        Stub(title="C", line=30, level=2),
    ))
    tree.construct()

    text = """
Main
|-- A
|-- B
+-- C
    """

    assert tree._sections

    assert_tree_equal(tree, text)

def test_tree_order_siblings():
    """
    GIVEN: A tree with sections
    WHEN: .order_siblings() is called
    THEN: each section node should assign .order to be its order among its siblings
    """
    a, b, c = Node("A"), Node("B"), Node("C")
    main = Node(name="Main", children=[a, b, c])
    tree = Tree(_sections=(main, a, b, c))
    tree.order_siblings()

    assert a.order == 0
    assert b.order == 1
    assert c.order == 2


def test_tree_find_next_nodes():
    """
    GIVEN: A tree with a list of ordered section nodes
    WHEN: .find_next_node() is called
    THEN: each section should have .next assigned to the next section
    """

    main = StubNode("Main")
    a, b, c = StubNode("A", order=0), StubNode("B", order=1), StubNode("C", order=2)
    i, ii = StubNode("I", order=0), StubNode("II", order=1)
    one, two = StubNode("1", order=0), StubNode("2", order=1)

    main.children = a, b, c
    a.children = i, ii
    ii.children = one, two

    text = """
Main
|-- A
|   |-- I
|   +-- II
|       |-- 1
|       +-- 2
|-- B
+-- C
    """

    assert_tree_equal(main, text)
    tree = Tree(_sections=(main, a, i, ii, one, two, b, c))
    tree.find_next_nodes()

    assert not main.next
    assert a.next == b
    assert i.next == ii
    assert ii.next == b
    assert one.next == two
    assert two.next == b
    assert b.next == c
    assert not c.next


def test_tree_identify_last_lines():
    """
    GIVEN: A tree with a list of section nodes that each have .next assigned
    AND: a .line_count integer
    WHEN: .identify_last_lines() is called
    THEN: each section .last should be assigned to the last line number of the section
    """

    main, a, b, c = StubNode("main", first=0), StubNode("a", first=10), StubNode("b", first=20), StubNode("c", first=30)
    a.next = b
    b.next = c

    tree = Tree(line_count = 40, _sections = (main, a, b, c))
    tree.identify_last_lines()

    assert main.last == 40
    assert a.last == 19
    assert b.last == 29
    assert c.last == 40

def test_tree_():
    """
    GIVEN: ...
    WHEN: ...
    THEN: ...
    """
