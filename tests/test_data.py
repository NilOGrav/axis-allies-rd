import os
import tempfile
import unittest

import helpers
from helpers import Base, quiet_stderr
from rdtree import data, views


def write(text, bom=False):
    handle, path = tempfile.mkstemp(suffix=".csv")
    os.close(handle)
    with open(path, "wb") as f:
        f.write((b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8"))
    return path


def mini_text():
    with open(helpers.MINI, encoding="utf-8") as f:
        return f.read()


class LoaderTest(Base):

    def test_reads_the_fixture(self):
        self.assertEqual(len(data.load_data(helpers.MINI)), 29)

    def test_byte_order_mark_is_ignored(self):
        rows = data.load_data(write(mini_text(), bom=True))
        self.assertEqual(rows[0]["Tech_ID"], "R.0.01")

    def test_blank_rows_are_skipped(self):
        text = mini_text() + ",,,,,,,,,,,,,,,,\n\n,,,,,,,,,,,,,,,,\n"
        self.assertEqual(len(data.load_data(write(text))), 29)

    def test_semicolon_file_gets_a_hint(self):
        text = mini_text().replace(",", ";")
        with self.assertRaises(SystemExit) as raised:
            data.load_data(write(text))
        self.assertIn("semicolon", str(raised.exception))

    def test_old_id_column_gets_a_hint(self):
        text = mini_text().replace("Tech_ID", "ID", 1)
        with self.assertRaises(SystemExit) as raised:
            data.load_data(write(text))
        self.assertIn("Tech_ID", str(raised.exception))


class GraphTest(Base):

    def setUp(self):
        super().setUp()
        self.graph, _ = helpers.build()

    def edge(self, source_id, target_id):
        for edge in self.graph["edges"]:
            if (edge["source"]["routing"]["id"] == source_id
                    and edge["target"]["routing"]["id"] == target_id):
                return edge
        self.fail(f"no edge {source_id} -> {target_id}")

    def test_cluster_endpoint_knows_its_members(self):
        edge = self.edge("A_2", "A.3.01")
        self.assertEqual(edge["source"]["members"], ["A.2.01", "A.2.02"])
        self.assertEqual(edge["source"]["cluster"], ("Air", "A_2"))
        self.assertIsNone(edge["target"]["cluster"])

    def test_gate_on_a_cluster_covers_every_member(self):
        edge = self.edge("R.0.01", "A_1")
        self.assertEqual(edge["target"]["members"], ["A.1.01", "A.1.02", "A.1.03"])

    def test_node_endpoint_is_just_itself(self):
        edge = self.edge("A.1.01", "A.2.01")
        self.assertEqual(edge["source"]["members"], ["A.1.01"])
        self.assertEqual(edge["target"]["members"], ["A.2.01"])

    def test_or_group_edges_share_a_group(self):
        a = self.edge("A.1.02", "A.2.02")
        b = self.edge("A.1.03", "A.2.02")
        self.assertEqual(a["type"], "OR")
        self.assertEqual(a["or_group_id"], b["or_group_id"])

    def test_cluster_rows_are_not_drawn(self):
        for tech_id in ("X.A.01", "X.A.02", "X.L.02"):
            self.assertFalse(self.graph["nodes"][tech_id]["view"]["visible"])

    def test_domain_mismatch_with_config_is_reported(self):
        import io, contextlib
        buffer = io.StringIO()
        with contextlib.redirect_stderr(buffer):
            data.check_domain_config(self.graph, ["Air", "Ghost"])
        text = buffer.getvalue()
        self.assertIn("'Ghost' is in the config but not in the data", text)
        self.assertIn("'Land' is in the data but not in the config", text)


class ChainViewTest(Base):
    """A dependency on a cluster means any one of its members; a gate
    listed on a cluster applies to every member."""

    def setUp(self):
        super().setUp()
        self.graph, _ = helpers.build()

    def chain(self, tech_id):
        return views.find_chain_ancestors(self.graph, tech_id)

    def test_depending_on_a_cluster_follows_all_members(self):
        self.assertEqual(
            self.chain("A.3.01"),
            {"A.3.01", "A.2.01", "A.2.02", "A.1.01", "A.1.02", "A.1.03", "R.0.01"},
        )

    def test_a_gate_reaches_members_that_are_not_the_first(self):
        # A.4.02 is the second member of the gated cluster X.A.04.
        self.assertEqual(
            self.chain("A.4.02"),
            {"A.4.02", "A.3.01", "A.2.01", "A.2.02",
             "A.1.01", "A.1.02", "A.1.03", "R.0.01"},
        )

    def test_or_group_includes_every_alternative(self):
        chain = self.chain("P.7.AC")
        self.assertTrue({"A.5.01", "L.4.01", "L.1.01", "A.1.01"} <= chain)

    def test_unknown_target_is_an_error(self):
        with self.assertRaises(ValueError):
            self.chain("Z.9.99")


if __name__ == "__main__":
    unittest.main()
