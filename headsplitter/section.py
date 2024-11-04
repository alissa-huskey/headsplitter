"""Section module."""

from anytree import NodeMixin

from headsplitter.object import Object
from headsplitter.heading import Heading

bp = breakpoint


class Section(Object, NodeMixin):
    """Class representing a section in a markdown document."""

    line: int = 0
    name: str = None
    level: int = 0
    first: int = None
    last: int = None
    _heading: Heading = None
    _next = None
    _last: int = None
    tree = None

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

    @property
    def order(self):
        if not self.parent:
            return
        return self.parent.children.index(self)

    @property
    def next(self):
        """Return the next sibling of this node or of its parent."""
        if not self._next:

            # root node -- no next node
            if self.is_root:
                self._next = None

            # this node has no siblings -- get the parent's next sibling
            elif not self.siblings:
                self._next = self.parent.next

            # this node is last among siblings - get the parent's next sibling
            elif (self.order + 1) >= len(self.parent.children):
                self._next = self.parent.next

            # this node has more siblings - get the next one
            else:
                self._next = self.parent.children[self.order + 1]

        return self._next

    @property
    def last(self):
        """Return the last line of this section.

        Either the first line of the next section, or if there is none, the end
        of the document."""
        if not self._last:
            if self.next:
                self._last = self.next.first

            elif self.tree:
                self._last = self.tree.line_count

            elif self.root and self.root.tree:
                self._last = self.root.tree.line_count

        return self._last

    @last.setter
    def last(self, line_no):
        """Set the last line."""
        self._last = line_no
