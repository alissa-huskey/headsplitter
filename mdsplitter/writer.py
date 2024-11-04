"""For writing files."""

from pathlib import Path

from mdsplitter.object import Object


class Writer(Object):
    """Class to write files."""

    source: list = []
    """List of lines from source file."""

    bounds: tuple = ()
    """Tuple containing start and end lines."""

    dir: Path = Path()
    """Destination directory path."""

    _name: str = None
    """Name of output file."""

    _lines: list = []
    """Lines to write to file."""

    @property
    def dest(self):
        """Return the destination file Path object."""
        if not self.name:
            raise Exception("Missing required name attribute.")

        return self.dir / self.name

    @property
    def name(self):
        "Return the name."
        return f"{self._name}.md"

    @name.setter
    def name(self, name):
        self._name = name.lower().replace(" ", "-")

    @property
    def lines(self):
        """Return the lines to write to the file."""
        if not self._lines:

            if not self.source:
                raise Exception("Writer.source attribute missing or empty.")

            if not self.bounds:
                raise Exception("Writer.bounds attribute missing or empty.")

            first, last = self.bounds
            self._lines = self.source[first:last]
        return self._lines

    @lines.setter
    def lines(self, lines):
        """Set lines."""
        self._lines = lines

    def write(self):
        """Write the lines to a file."""
        text = "\n".join(self.lines).strip() + "\n"
        self.dest.write_text(text)
