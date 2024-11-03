"""Section module."""

from anytree import NodeMixin

from mdsplitter.object import Object
from mdsplitter.heading import Heading

bp = breakpoint


class Section(Object, NodeMixin):
    """Class representing a section in a markdown document."""

    line: int = 0
    name: str = None
    level: int = 0
    first: int = None
    last: int = None
    _heading: Heading = None

    EXCLUDE = ("next")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next = None

    def __hash__(self):
        return hash(self.line)

    @property
    def heading(self):
        """Get heading."""
        return self._heading

    @heading.setter
    def heading(self, heading):
        """Set heading and adopt attrs."""
        if not heading:
            return
        self._heading = heading
        self.level = heading.level
        self.name = heading.title
        self.first = heading.line
