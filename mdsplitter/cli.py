"""Command Line Interface."""

from pathlib import Path
from typing import Annotated

from rich.console import Console
from rich.traceback import install as rich_tracebacks
from typer import Argument, Exit, Option, Typer, FileTextWrite

from mdsplitter import MdsplitterError
from mdsplitter.writer import Writer
from mdsplitter.document import Document

bp = breakpoint

console = Console()
errors = Console(stderr=True)
rich_tracebacks(show_locals=True)
cli = Typer()


def error(ex: Exception):
    """Print an error message."""
    if isinstance(ex, MdsplitterError):
        ex = ex.message

    errors.print(f"[red]Error[/red] {ex}")


def exit(status: int):
    """Exit with status code."""
    raise Exit(code=status)


def abort(message):
    """Print error message and exit."""
    error(message)
    exit(1)


@cli.command()
def split(
    file: Annotated[Path, Argument(
        help="Markdown file to split.",
        dir_okay=False,
        file_okay=True,
    )],
    outdir: Annotated[Path, Option(
        help="Output directory.",
        exists=True,
        file_okay=False,
        dir_okay=True,
    )] = ".",
    level: Annotated[int, Option(
        help="Header level to split at. (Others are ignored.)",
    )] = 2,
):
    """Split a markdown file by its headers."""
    doc = Document(path=file)

    if not file.is_file():
        abort(f"No such file: {file}")

    for section in doc.tree.sections:
        if section.heading.level == level:
            writer = Writer(
                source=doc.lines,
                bounds=(section.first-1, section.last),
                dir=outdir,
                name=section.heading.title,
            )
            writer.write()

def run():
    """Start the command line interface."""
    try:
        cli()
    except MdsplitterError as e:
        error(e.message)
        exit(e.status)
    except SystemExit:
        ...
    #  except BaseException as e:
    #      breakpoint()
        ...


if __name__ == "__main__":
    run()
