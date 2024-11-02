"""Tree module."""

from anytree import AsciiStyle, RenderTree

from mdsplitter.heading import Heading
from mdsplitter.object import Object
from mdsplitter.section import Section

bp = breakpoint


class Tree(Object):
    """A hierarchical tree of sections including first and last line number,
    nested by markdown header.."""

    _document = None
    title: str = None
    headings: list = None
    line_count: int = 0

    @property
    def document(self):
        """."""
        return self._document

    @document.setter
    def document(self, doc):
        self._document = doc
        self.headings = doc.headings
        self.line_count = len(doc.lines)
        self.title = doc.title

    @property
    def sections(self):
        """."""
        self.construct()
        self.order_siblings()
        self.find_next_nodes()
        self.identify_last_lines()
        return self._sections

    @property
    def root(self):
        """Return the root node."""
        if not self.sections:
            return
        return self.sections[0]

    def construct(self):
        """Construct a hierarchical tree of sections nested by markdown heading."""
        sections = []
        previous = None

        for i, h in enumerate(self.headings):
            section = Section(heading=h, name=h.title, level=h.level, first=h.line)

            if previous:
                difference = section.level - previous.level

                # at the same level
                if difference == 0:
                    section.parent = previous.parent

                # down a level
                elif difference >= 1:
                    section.parent = previous

                # up one or more levels
                elif difference <= -1:
                    section.parent = previous.ancestors[difference -1]

            sections.append(section)
            previous = section


        # put everything is under a single document root
        root = Section(heading=Heading(title=(self.title or "Document")))
        root.children += tuple(set([node.root for node in sections]))
        sections.insert(0, root)

        self._sections = sections

        return sections

    def order_siblings(self):
        """Mark the position of each section among its siblings."""
        if not self._sections:
            return

        for node in self._sections:
            if node.siblings:
                siblings = node.parent.children
                node.order = siblings.index(node)

    def find_next_nodes(self):
        """Identify the next node for each section.

        Find the next sibling or walk up the tree until you do or until you
        reach the root."""
        if not self._sections:
            return

        for section in self._sections:
            marker = section

            while not section.next:
                # use the previously determined value
                if marker.next:
                    section.next = marker.next
                    continue

                # root node -- no next node to find
                if not marker.parent:
                    section.next = None
                    break

                # this node has no siblings -- get the parent's next sibling
                elif not marker.siblings:
                    marker = marker.parent
                    continue

                # this node is last among siblings - get the parent's next sibling
                elif (marker.order + 1) >= len(marker.parent.children):
                    marker = marker.parent
                    continue

                # this node has more siblings - get the next one
                else:
                    section.next = marker.parent.children[marker.order + 1]

    def identify_last_lines(self):
        """Identify the last line number for each section."""
        if not self._sections:
            return

        for section in self._sections:
            if section.next:
                section.last = section.next.first - 1
            else:
                section.last = self.line_count

    def __str__(self):
        """Return a text representation of tree."""
        if not self._sections:
            return super().__str__()
        root = self._sections[0]
        return RenderTree(root, style=AsciiStyle()).by_attr()
