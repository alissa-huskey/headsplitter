"""Heading module."""

from mdsplitter.object import Object


class Heading(Object):
    """Class representing a markdown heading."""

    _token = None
    _title_token = None

    EXCLUDE = ("children")

    level: int = 0
    line: int = 0
    nesting: int = 0
    title: str = None
    children: list = None

    def __init__(self, token=None, **kwargs):
        super().__init__(**kwargs)
        self.token = token
        self.children = []

    @property
    def token(self):
        """Get header token."""
        return self._token

    @token.setter
    def token(self, token):
        """Set header token."""
        if not token:
            return
        self._token = token
        self.level = int(token.tag[1])

    @property
    def title_token(self):
        """Get header token."""
        return self._title_token

    @title_token.setter
    def title_token(self, token):
        """Set header token."""
        if not token:
            return
        self._title_token = token
        self.title = token.content

        # strip link markdown
        if hasattr(token, "children") and token.children:
            self.title = " ".join([c.content for c in token.children if c.type == "text"])
