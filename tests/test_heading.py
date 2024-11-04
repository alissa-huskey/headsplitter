from headsplitter.heading import Heading
from headsplitter.object import Object as Stub


def test_heading():
    heading = Heading()
    assert heading


def test_heading_with_attrs():
    """
    GIVEN: A new heading object
    WHEN: keyword args are passed
    THEN: object attrs should be set.
    """
    heading = Heading(title="My Heading", level=1, line=0)

    assert heading.title == "My Heading"
    assert heading.level == 1
    assert heading.line == 0


def test_heading_with_token():
    """
    GIVEN: A new header object
    WHEN: a heading_open token is passed for token kwarg
    THEN: the heading level should be set.
    """
    token = Stub(tag="h3")
    heading = Heading(token=token)

    assert heading.level == 3


def test_heading_title_token():
    """
    GIVEN: A new header object
    WHEN: an inline token is passed for title_token kwarg
    THEN: the title should be set.
    """
    token = Stub(content="My Header")
    heading = Heading(title_token=token)

    assert heading.title == "My Header"


def test_heading_():
    """
    GIVEN: ...
    WHEN: ...
    THEN: ...
    """
    heading = Heading()
    assert heading
