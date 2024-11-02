"""Section module."""

from anytree import NodeMixin

from mdsplitter.object import Object

bp = breakpoint


class Section(Object, NodeMixin):
    """Class representing a section in a markdown document."""

    line: int = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next = None

    def __hash__(self):
        return hash(self.line)
