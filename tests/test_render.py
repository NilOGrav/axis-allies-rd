import os
import tempfile
import unittest

import helpers
import regen_golden
import svgcheck
from helpers import Base
from rdtree import render_dot, render_grid, settings, util, views


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


class GoldenDotTest(Base):
    """The DOT files are written by this program, so they can be
    compared exactly, without Graphviz."""

    def test_dot_output_matches_the_golden_files(self):
        folder = tempfile.mkdtemp()
        for path in regen_golden.render_dots(folder):
            name = os.path.basename(path)
            with self.subTest(file=name):
                self.assertEqual(
                    read(path), read(os.path.join(helpers.GOLDEN, name)),
                    "DOT output changed; if that was intended, run "
                    "python tests/regen_golden.py and review the diff")


@unittest.skipUnless(helpers.HAVE_GRAPHVIZ, "Graphviz (dot, neato) not installed")
class GridSvgTest(Base):

    def render(self, highlighted=None, dim="grey", filter_dim=None):
        graph, layout = helpers.build()
        if filter_dim:
            views.apply_view_filter(graph, highlighted, filter_dim)
        folder = tempfile.mkdtemp()
        svg = os.path.join(folder, "grid.svg")
        render_grid.render_grid_svg(
            graph, layout, os.path.join(folder, "grid.dot"), svg,
            {"highlighted": highlighted, "dim": dim})
        self.geometry = render_grid.grid_geometry()
        return svgcheck.load(svg)

    def test_every_node_is_in_exactly_one_box_and_boxes_do_not_overlap(self):
        root, graph = self.render()
        membership = svgcheck.membership(graph)
        self.assertEqual(len(membership), 24)
        self.assertTrue(all(len(m) == 1 for m in membership.values()), membership)
        self.assertEqual(svgcheck.overlapping_boxes(graph), [])
        # one box per domain/tier cluster that has technologies
        self.assertEqual(len(svgcheck.clusters(graph)), 13)

    def height(self, rows, margin=None):
        g = self.geometry
        margin = margin if margin is not None else settings.cluster_view["margin"]
        return (rows - 1) * g["row_spacing"] + g["node_h"] + 2 * margin

    def test_band_tiers_share_the_height_of_the_largest_cluster(self):
        root, graph = self.render()
        height = {t: b[3] - b[1] for t, b, _ in svgcheck.clusters(graph).values()}
        # Air: largest cluster in tiers 1-6 has 3 rows
        # (tier 1: 3 nodes; tier 3: research centre = 2 rows + 1 node)
        for tier in range(1, 6):
            self.assertAlmostEqual(height[f"Air - Tier {tier}"], self.height(3), 1)
        for tier in range(1, 5):
            self.assertAlmostEqual(height[f"Land - Tier {tier}"], self.height(2), 1)

    def test_other_tiers_wrap_their_own_nodes(self):
        root, graph = self.render()
        height = {t: b[3] - b[1] for t, b, _ in svgcheck.clusters(graph).values()}
        self.assertAlmostEqual(height["Programs - Tier 7"], self.height(4), 1)
        self.assertAlmostEqual(height["Programs - Tier 8"], self.height(2), 1)
        # tier 0 holds a single research centre = two rows
        self.assertAlmostEqual(height["Research - Tier 0"], self.height(2), 1)

    def test_cluster_edges_end_on_the_box_edge(self):
        root, graph = self.render()
        ends = svgcheck.anchor_end_deviations(graph)
        # R.0.01 -> 2 gated clusters (1 end each), tier gates between
        # boxes (2 ends each), two research-centre gates (1 end each)
        self.assertEqual(len(ends), 9)
        for title, which, dx, dy in ends:
            self.assertLess(dx, 4, (title, which))
            self.assertLess(dy, 4, (title, which))

    def test_edges_leaving_a_cluster_are_dashed_and_entering_ones_solid(self):
        root, graph = self.render()
        edges = svgcheck.edges(graph)
        leaving, _ = edges["__anchor_cluster_Air_2_R->A.3.01"]
        entering, _ = edges["R.0.01->__anchor_cluster_Air_1_L"]
        self.assertIsNotNone(leaving.get("stroke-dasharray"))
        self.assertIsNone(entering.get("stroke-dasharray"))

    def test_canvas_keeps_the_padding_around_the_boxes(self):
        root, graph = self.render()
        pad = settings.dot_view["graph"]["pad"] * 72
        self.assertGreaterEqual(svgcheck.canvas_padding(root, graph, pad), pad - 1)

    def test_cluster_boxes_use_the_simple_views_colours(self):
        root, graph = self.render()
        boxes = {t: f for t, _, f in svgcheck.clusters(graph).values()}
        expected = util.darken_color(settings.domain_colors["Air"],
                                     settings.CLUSTER_DARKEN_FACTOR)
        self.assertEqual(boxes["Air - Tier 1"], expected)

    def test_removed_nodes_leave_no_box_and_no_dangling_arrow(self):
        graph, _ = helpers.build()
        highlighted = views.find_chain_ancestors(graph, "A.3.01")
        root, g = self.render(highlighted, "none", filter_dim="none")
        titles = {t for t, _, _ in svgcheck.clusters(g).values()}
        self.assertFalse([t for t in titles if t.startswith(("Land", "Programs"))])
        membership = svgcheck.membership(g)
        self.assertEqual(set(membership), highlighted)
        self.assertTrue(all(len(m) == 1 for m in membership.values()))
        for title, which, dx, dy in svgcheck.anchor_end_deviations(g):
            self.assertLess(dx, 4)
            self.assertLess(dy, 4)

    def test_boxes_without_highlight_are_dimmed_like_their_nodes(self):
        graph, _ = helpers.build()
        highlighted = {t for t, n in graph["nodes"].items()
                       if n["domain"] == "Air" and n["category"] != "CLUSTER"}
        root, g = self.render(highlighted, "fade", filter_dim="fade")
        boxes = {t: f for t, _, f in svgcheck.clusters(g).values()}
        normal = util.darken_color(settings.domain_colors["Air"],
                                   settings.CLUSTER_DARKEN_FACTOR)
        self.assertEqual(boxes["Air - Tier 1"], normal)
        self.assertNotEqual(boxes["Land - Tier 1"], util.darken_color(
            settings.domain_colors["Land"], settings.CLUSTER_DARKEN_FACTOR))


if __name__ == "__main__":
    unittest.main()
