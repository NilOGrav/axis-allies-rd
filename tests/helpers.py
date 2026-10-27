"""Shared helpers for the tests."""

import contextlib
import io
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "src")
REAL_CONFIG = os.path.join(SRC, "tech_tree.toml")
CONFIG = os.path.join(HERE, "fixtures", "test.toml")  # frozen, see test.toml
MINI = os.path.join(HERE, "fixtures", "mini.csv")
GOLDEN = os.path.join(HERE, "golden")
REAL = os.path.join(
    ROOT, "data", "research",
    "Axis & Allies Research & Development - tech tree - Tech List.csv",
)

if SRC not in sys.path:
    sys.path.insert(0, SRC)

from rdtree import data, layout, settings, views  # noqa: E402

HAVE_GRAPHVIZ = bool(shutil.which("dot") and shutil.which("neato"))


def load_settings(path=CONFIG):
    with contextlib.redirect_stdout(io.StringIO()):
        settings.load(path)


def build(csv_path=MINI, styled=True):
    """(graph, resolved layout) for a CSV, with the real config."""

    graph = data.build_graph(data.load_data(csv_path))

    if styled:
        graph = views.apply_view(graph)

    return graph, layout.resolve_layout(graph, settings.layout)


def quiet_stderr():
    return contextlib.redirect_stderr(io.StringIO())


import unittest  # noqa: E402


class Base(unittest.TestCase):
    """Every test starts from the frozen test config, since settings
    are global and other tests may have loaded a different one."""

    def setUp(self):
        load_settings()
