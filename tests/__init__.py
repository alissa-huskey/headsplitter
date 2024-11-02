from anytree import AsciiStyle, RenderTree

bp = breakpoint


def render_tree(tree):
    """Return a string rendering of a tree."""

    return RenderTree(tree.root, style=AsciiStyle()).by_attr().strip()

def assert_tree_equal(tree, text):
    """Assert the rendering of root node is equal to text."""

    assert render_tree(tree) == text.strip()
