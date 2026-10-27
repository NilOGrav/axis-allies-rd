"""Rewrite the golden DOT files from the current code.

The DOT files are written by this program, not by Graphviz, so they do
not depend on the installed Graphviz version. Run this only after a
deliberate change to what the renderers write, and review the diff:

    python tests/regen_golden.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import helpers  # noqa: E402
from rdtree import render_dot, render_grid  # noqa: E402


def render_dots(folder):
    """Write the simple and grid DOT of the mini fixture into folder."""

    helpers.load_settings()
    graph, layout = helpers.build()
    simple = os.path.join(folder, "mini_simple.dot")
    grid = os.path.join(folder, "mini_grid.dot")
    render_dot.render_simple_svg(graph, layout, simple, None)
    render_grid.render_grid_svg(graph, layout, grid, None,
                                {"highlighted": None, "dim": "grey"})
    return simple, grid


if __name__ == "__main__":
    for path in render_dots(helpers.GOLDEN):
        print("written", os.path.relpath(path, helpers.ROOT))
