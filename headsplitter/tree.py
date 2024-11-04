"""Tree module."""

from anytree import AsciiStyle, RenderTree

from headsplitter.heading import Heading
from headsplitter.object import Object
from headsplitter.section import Section

bp = breakpoint


class Tree(Object):
    """A hierarchical tree of sections including first and last line number,
    nested by markdown header.."""

    _document = None
    title: str = None
    headings: list = None
    line_count: int = 0

    def __init__(self, **kwargs):
        self.sections = []
        super().__init__(**kwargs)

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
    def root(self):
        """Return the root node."""
        if not self.sections:
            return
        return self.sections[0]

    def build(self):
        """Organize sections into a nestedhierarchical tree by markdown
        heading."""
        sections = []
        previous = None

        for i, h in enumerate(self.headings):
            section = Section(
                heading=h,
                name=h.title,
                level=h.level,
                first=h.line,
                tree=self,
            )

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
        root = Section(
            heading=Heading(title=(self.title or "Document")),
            tree=self,
        )
        root.children += tuple(set([node.root for node in sections]))
        sections.insert(0, root)

        self.sections = sections

        return sections

    def __str__(self):
        """Return a text representation of tree."""
        if not self.sections:
            return super().__str__()
        root = self.sections[0]
        return RenderTree(root, style=AsciiStyle()).by_attr()
