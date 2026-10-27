import os
import re
import tempfile
import unittest

import helpers
from helpers import Base, quiet_stderr
from rdtree import settings


def config_text():
    """The REAL config; the variants below are modified copies of it."""
    with open(helpers.REAL_CONFIG, encoding="utf-8") as f:
        return f.read()


def load_variant(text):
    """Load a modified copy of the config; returns the temp file path."""
    handle, path = tempfile.mkstemp(suffix=".toml")
    os.close(handle)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


class SettingsTest(Base):

    def tearDown(self):
        helpers.load_settings()

    def test_real_config_loads_consistently(self):
        settings.load(helpers.REAL_CONFIG)
        self.assertEqual(list(settings.domain_colors), settings.domain_order)
        self.assertEqual(settings.layout["domain_order"], settings.domain_order)
        for color in settings.domain_colors.values():
            self.assertRegex(color, r"^#[0-9a-fA-F]{6}$")
        self.assertEqual(set(settings.check_levels), set(settings.CHECK_IDS))

    def test_every_required_key_is_reported_by_name(self):
        text = config_text()
        for key, pattern in {
            "dot_view.graph.ranksep": r"(?m)^ranksep\s*=.*$",
            "paths.tech_list": r"(?m)^tech_list\s*=.*$",
            "postprocess.corner_radius": r"(?m)^corner_radius\s*=.*$",
            "check.duplicate_id": r"(?m)^duplicate_id\s*=.*$",
        }.items():
            with self.subTest(key=key):
                path = load_variant(re.sub(pattern, "", text, count=1))
                with self.assertRaises(SystemExit) as raised:
                    settings.load(path)
                self.assertIn(key, str(raised.exception))

    def test_missing_config_file(self):
        with self.assertRaises(SystemExit) as raised:
            settings.load("/no/such/tech_tree.toml")
        self.assertIn("not found", str(raised.exception))

    def test_invalid_toml(self):
        path = load_variant("[layout\nrow_offset = 1\n")
        with self.assertRaises(SystemExit) as raised:
            settings.load(path)
        self.assertIn("Invalid config", str(raised.exception))

    def test_bad_check_level(self):
        text = re.sub(r"(?m)^duplicate_id\s*=.*$", 'duplicate_id = "fatal"',
                      config_text(), count=1)
        with self.assertRaises(SystemExit) as raised:
            settings.load(load_variant(text))
        self.assertIn("duplicate_id", str(raised.exception))
        self.assertIn("error, warning, off", str(raised.exception))

    def test_bad_domain_colour(self):
        text = re.sub(r'(?m)^color\s*=\s*"#[0-9a-fA-F]{6}"', 'color = "#12345"',
                      config_text(), count=1)
        with self.assertRaises(SystemExit) as raised:
            settings.load(load_variant(text))
        self.assertIn("#RRGGBB", str(raised.exception))

    def test_duplicate_domain(self):
        text = config_text() + '\n[[domains]]\nname = "Air"\ncolor = "#000000"\n'
        with self.assertRaises(SystemExit) as raised:
            settings.load(load_variant(text))
        self.assertIn("more than once", str(raised.exception))

    def test_band_tiers_must_be_ordered(self):
        text = re.sub(r"(?m)^band_tiers_to\s*=.*$", "band_tiers_to = 0",
                      config_text(), count=1)
        with self.assertRaises(SystemExit) as raised:
            settings.load(load_variant(text))
        self.assertIn("band_tiers", str(raised.exception))

    def test_unknown_section_is_a_warning(self):
        path = load_variant(config_text() + "\n[colour_typo]\nx = 1\n")
        import io, contextlib
        buffer = io.StringIO()
        with contextlib.redirect_stderr(buffer):
            settings.load(path)
        self.assertIn("colour_typo", buffer.getvalue())

    def test_paths_are_relative_to_root_which_is_relative_to_the_config(self):
        folder = tempfile.mkdtemp()
        text = re.sub(r'(?m)^root\s*=.*$', 'root = "."', config_text(), count=1)
        text = re.sub(r'(?m)^tech_list\s*=.*$', 'tech_list = "data/x.csv"',
                      text, count=1)
        path = os.path.join(folder, "tech_tree.toml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        settings.load(path)
        self.assertEqual(settings.paths["root"], os.path.normpath(folder))
        self.assertEqual(settings.paths["tech_list"],
                         os.path.join(os.path.normpath(folder), "data", "x.csv"))

    def test_real_config_points_at_the_repository_root(self):
        settings.load(helpers.REAL_CONFIG)
        self.assertEqual(os.path.normpath(settings.paths["root"]),
                         os.path.normpath(helpers.ROOT))


if __name__ == "__main__":
    unittest.main()
