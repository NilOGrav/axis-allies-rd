import contextlib
import io
import os
import re
import shutil
import tempfile
import unittest

import helpers
from helpers import Base

import tech_tree


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


class CliTest(Base):
    """End to end: main() with a temporary config whose paths point
    into a scratch directory."""

    def setUp(self):
        super().setUp()
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def config(self, csv=helpers.MINI):
        with open(helpers.CONFIG, encoding="utf-8") as f:
            text = f.read()
        text = re.sub(r'(?m)^root\s*=.*$',
                      f'root = "{self.tmp.replace(os.sep, "/")}"', text, count=1)
        text = re.sub(r'(?m)^tech_list\s*=.*$',
                      f'tech_list = "{csv.replace(os.sep, "/")}"', text, count=1)
        path = os.path.join(self.tmp, "tech_tree.toml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def run_cli(self, *args, csv=helpers.MINI):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = tech_tree.main(["--config", self.config(csv), *args])
            except SystemExit as stop:
                code = stop.code
        return code, out.getvalue(), err.getvalue()

    def out(self, *parts):
        return os.path.join(self.tmp, "output", *parts)

    def csv_variant(self, change):
        with open(helpers.MINI, encoding="utf-8") as f:
            text = change(f.read())
        path = os.path.join(self.tmp, "variant.csv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    # ── files and switches ───────────────────────────────────────

    @unittest.skipUnless(helpers.HAVE_GRAPHVIZ, "Graphviz not installed")
    def test_default_run_writes_every_output_into_the_configured_folders(self):
        code, _, _ = self.run_cli()
        self.assertEqual(code, 0)
        for path in (("txt", "tech_tree.txt"),
                     ("dot", "tech_tree_simple.dot"), ("svg", "tech_tree_simple.svg"),
                     ("dot", "tech_tree_grid.dot"), ("svg", "tech_tree_grid.svg")):
            self.assertTrue(os.path.exists(self.out(*path)), path)

    @unittest.skipUnless(helpers.HAVE_GRAPHVIZ, "Graphviz not installed")
    def test_only_grid_files_get_the_view_suffix_and_simple_view_is_unchanged(self):
        self.run_cli()
        simple_dot = read_bytes(self.out("dot", "tech_tree_simple.dot"))
        simple_svg = read_bytes(self.out("svg", "tech_tree_simple.svg"))

        code, _, _ = self.run_cli("--view", "chain", "--filter", "A.3.01",
                                  "--dim", "none")
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists(self.out("svg", "tech_tree_grid_chain_a_3_01.svg")))
        self.assertEqual(read_bytes(self.out("dot", "tech_tree_simple.dot")), simple_dot)
        self.assertEqual(read_bytes(self.out("svg", "tech_tree_simple.svg")), simple_svg)
        for folder, name in (("svg", "tech_tree_simple.svg"),
                             ("dot", "tech_tree_simple.dot")):
            self.assertEqual(sorted(f for f in os.listdir(self.out(folder))
                                    if "simple" in f), [name])

    @unittest.skipUnless(helpers.HAVE_GRAPHVIZ, "Graphviz not installed")
    def test_nodot_keeps_no_dot_files_but_still_draws(self):
        self.run_cli("--nodot", "--notxt")
        self.assertTrue(os.path.exists(self.out("svg", "tech_tree_grid.svg")))
        self.assertFalse(os.path.isdir(self.out("dot")))

    def test_nosvg_stops_after_the_dot_files(self):
        self.run_cli("--nosvg", "--notxt")
        self.assertTrue(os.path.exists(self.out("dot", "tech_tree_grid.dot")))
        self.assertFalse(os.path.isdir(self.out("svg")))

    def test_nodot_and_nosvg_together_write_nothing(self):
        self.run_cli("--nodot", "--nosvg", "--notxt")
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "output")))

    def test_notxt_skips_the_text_file(self):
        self.run_cli("--notxt", "--nosimple", "--nogrd")
        self.assertFalse(os.path.exists(self.out("txt", "tech_tree.txt")))

    def test_text_file_lists_the_layout(self):
        self.run_cli("--nosimple", "--nogrd")
        with open(self.out("txt", "tech_tree.txt"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("A.3.01 - Test A.3.01", text)

    # ── input ────────────────────────────────────────────────────

    def test_file_option_replaces_the_configured_tech_list(self):
        variant = self.csv_variant(
            lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("P.")))
        code, printed, _ = self.run_cli("--file", variant, "--nosimple", "--nogrd")
        self.assertEqual(code, 0)
        self.assertIn(variant, printed)
        with open(self.out("txt", "tech_tree.txt"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("A.1.01", text)
        self.assertNotIn("P.7.AA", text)

    def test_missing_tech_list(self):
        code, _, _ = self.run_cli("--file", "/no/such.csv")
        self.assertIn("Tech List not found", str(code))

    def test_hide_domain(self):
        self.run_cli("--hide-domain", "Land", "--nosimple", "--nogrd")
        with open(self.out("txt", "tech_tree.txt"), encoding="utf-8") as f:
            text = f.read()
        self.assertNotIn("L.1.01", text)
        self.assertIn("A.1.01", text)

    def test_hide_unknown_domain_lists_the_available_ones(self):
        code, _, _ = self.run_cli("--hide-domain", "Ghost", "--nosimple", "--nogrd")
        message = str(code)
        self.assertIn("Ghost", message)
        available = message.split("Available:")[1]
        for domain in ("Air", "Land", "Programs", "Research"):
            self.assertIn(domain, available)

    # ── --check ──────────────────────────────────────────────────

    def test_check_on_clean_data_exits_zero_and_writes_nothing(self):
        code, printed, _ = self.run_cli("--check")
        self.assertEqual(code, 0)
        self.assertIn("0 error(s)", printed)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "output")))

    def test_check_exits_one_on_errors(self):
        broken = self.csv_variant(lambda t: t + t.splitlines()[1] + "\n")
        code, printed, _ = self.run_cli("--check", "--file", broken)
        self.assertEqual(code, 1)
        self.assertIn("duplicate_id", printed)

    def test_check_fails_on_warnings_only_with_strict(self):
        warned = self.csv_variant(lambda t: t.replace("RCENTRE", "RCENTER", 1))
        self.assertEqual(self.run_cli("--check", "--file", warned)[0], 0)
        code, printed, _ = self.run_cli("--check", "--strict", "--file", warned)
        self.assertEqual(code, 1)
        self.assertIn("unknown_category", printed)


if __name__ == "__main__":
    unittest.main()
