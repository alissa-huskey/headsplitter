from pathlib import Path

from typer.testing import CliRunner

from headsplitter.cli import cli

bp = breakpoint

runner = CliRunner()


def test_cli_split(fixtures, tmp_path):
    """
    GIVEN: a markdown file with h2 headings
    WHEN: the app is called
    THEN: a file
    """
    source_file = fixtures / "simple_headings.md"
    lines = source_file.read_text().splitlines()
    output_files = {
        (2, 14): tmp_path / "01-subheading-a.md",
        (14, 25): tmp_path / "02-subheading-b.md",
        (25, 40): tmp_path / "03-subheading-c.md",
    }

    result = runner.invoke(cli, [
        "--outdir", str(tmp_path),
        str(source_file),
    ])

    assert result.exit_code == 0

    for (first, last), file in output_files.items():
        text = "\n".join(lines[first:last]).strip() + "\n"

        assert file.is_file()
        assert file.read_text() == text
