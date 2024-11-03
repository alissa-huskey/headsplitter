"""Document module."""

from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from mdsplitter.heading import Heading
from mdsplitter.object import Object
from mdsplitter.section import Section
from mdsplitter.tree import Tree

bp = breakpoint


class Document(Object):
    """Class representing the source markdown document."""

    _path: Path = None
    _text: str = None
    _title: str = None
    _tokens: list = None
    _tree: Tree = None

    def __init__(self, path: Path=None, **kwargs):
        super().__init__(**kwargs)
        self.path = path

    @classmethod
    @property
    def parser(self):
        """Return a markdown parser."""
        return (
            MarkdownIt('commonmark', {'breaks': True, 'html': True})
            .use(front_matter_plugin)
            .use(footnote_plugin)
            .enable('table')
        )

    @property
    def path(self):
        """Get path to markdown file."""
        return self._path

    @path.setter
    def path(self, path):
        """Get path to markdown file."""
        if not path:
            return
        if not isinstance(path, Path):
            path = Path(path)
        self._path = path

    @property
    def text(self):
        """Get document text."""
        if self.path and not self._text:
            if not self.path.is_file():
                raise Exception("No such file exists: {self.path}.")
            self._text = self.path.read_text()
        return self._text

    @property
    def title(self):
        """Get document title."""
        if self.path and not self._title:
            self._title = self.path.stem
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def lines(self):
        if not self.text:
            return
        return self.text.splitlines()

    @text.setter
    def text(self, text):
        """Set document text."""
        self._text = text

    @property
    def tokens(self):
        """Get document tokens."""
        if self._path and not self._tokens:
            self.parse()
        return self._tokens

    @tokens.setter
    def tokens(self, tokens):
        """Set document tokens."""
        if not tokens:
            return
        self._tokens = tokens

    def parse(self):
        """Parse markdown."""
        self._tokens = self.parser.parse(self.text)

    @property
    def heading_tokens(self):
        """Return a dictionary of line no -> headings."""
        if not self.tokens:
            return
        return {i:t for i, t in enumerate(self.tokens) if t.type == "heading_open"}

    @property
    def headings(self):
        """Return a list of Heading objects."""
        if not self.heading_tokens:
            return

        headings = []

        for i, token in self.heading_tokens.items():
            heading = Heading(line=token.map[0], token=token, title_token=self.tokens[i+1])
            headings.append(heading)

        return headings

    @property
    def tree(self):
        """Return a hierarchical tree of sections."""
        if not self.headings:
            return

        if not self._tree:
            self._tree = Tree(document=self)
            self._tree.build()
        return self._tree

