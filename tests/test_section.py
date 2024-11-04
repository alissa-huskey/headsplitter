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


def test_section_next():
    """
    GIVEN: A number of nodes ordered like so:

            Main
            |-- A
            |   |-- I
            |   +-- II
            |       |-- 1
            |       +-- 2
            |-- B
            +-- C

    WHEN: .next is accessed on each node
    THEN: it should return the next node: either its next sibling, its parents
          next sibling, or the next ancestor to have a sibling if there is one.
    """
    main = Section(name="Main")
    a, b, c = Section(name="A"), Section(name="B"), Section(name="C")
    i, ii = Section(name="I"), Section(name="II")
    one, two = Section(name="1"), Section(name="2")

    main.children += a, b, c
    a.children = i, ii
    ii.children = one, two

    assert not main.next
    assert a.next == b
    assert i.next == ii
    assert ii.next == b
    assert one.next == two
    assert two.next == b
    assert b.next == c
    assert not c.next

def test_section_order():
    """
    GIVEN: A number of section nodes attached to a parent
    WHEN: .order is accessed
    THEN: each node should return the order among its siblings
    """
    a, b, c = Section(name="A"), Section(name="B"), Section(name="C")
    main = Section(name="Main", children=[a, b, c])

    assert a.order == 0
    assert b.order == 1
    assert c.order == 2


def test_section_last():
    """
    GIVEN: A number of nodes connected in a tree
    AND: each node has a .tree attribute with a .line_count attribute
    WHEN: .last is accessed
    THEN: the last line number (the first line of the next line) should be returned
    OR: the .line_count value should be returned if there is no next node
    """

    tree = Stub(line_count=40)
    main, a, b, c = (
        Section(name="main", first=0, tree=tree),
        Section(name="a", first=10),
        Section(name="b", first=20),
        Section(name="c", first=30, tree=tree),
    )

    main.children = a, b, c

    assert main.last == 40
    assert a.last == 20
    assert b.last == 30
    assert c.last == 40
