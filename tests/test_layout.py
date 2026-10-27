import os
import unittest

import helpers
from helpers import Base
from rdtree import layout, views


class MiniLayoutTest(Base):

    def setUp(self):
        super().setUp()
        self.graph, self.layout = helpers.build()
        self.pos = self.layout["nodes"]

    def row(self, tech_id):
        return self.pos[tech_id]["row"]

    def test_every_technology_is_placed_exactly_once(self):
        real = [t for t, n in self.graph["nodes"].items()
                if n["category"] != "CLUSTER"]
        self.assertEqual(sorted(self.pos), sorted(real))
        cells = [(p["column"], p["row"]) for p in self.pos.values()]
        self.assertEqual(len(cells), len(set(cells)))

    def test_columns_follow_the_tiers(self):
        self.assertEqual(self.layout["tier_to_column"],
                         {"0": 1, "1": 2, "2": 3, "3": 4, "4": 5, "5": 6,
                          "7": 7, "8": 8})

    def test_a_research_centre_takes_two_rows(self):
        self.assertEqual(self.row("A.3.02"), self.row("A.3.01") + 2)

    def test_early_clusters_of_a_domain_start_on_the_same_row(self):
        first_rows = {self.row(t) for t in
                      ("A.1.01", "A.2.01", "A.3.01", "A.4.01", "A.5.01")}
        self.assertEqual(len(first_rows), 1)

    def test_domain_bands_follow_the_configured_order(self):
        self.assertLess(self.row("A.1.01"), self.row("L.1.01"))
        self.assertLess(self.row("L.1.01"), self.row("P.3.AA"))
        self.assertLess(self.row("P.3.AA"), self.row("R.0.01"))

    def test_late_clusters_are_centred_on_their_own_domain(self):
        # Programs has one early node; the 4-node tier-7 cluster puts
        # its 2nd node on that row, the 2-node tier-8 cluster its 1st.
        self.assertEqual(self.row("P.7.AB"), self.row("P.3.AA"))
        self.assertEqual(self.row("P.8.AA"), self.row("P.3.AA"))
        rows = [self.row(t) for t in ("P.7.AA", "P.7.AB", "P.7.AC", "P.7.AD")]
        self.assertEqual(rows, sorted(rows))
        self.assertEqual(rows[1] - rows[0], 1)

    def test_hiding_a_domain_removes_it_and_keeps_the_rest_collision_free(self):
        graph = helpers.data.build_graph(helpers.data.load_data(helpers.MINI))
        graph = views.apply_view(graph)
        views.apply_hide_domain(graph, "Land")
        placed = layout.resolve_layout(graph, helpers.settings.layout)["nodes"]
        self.assertFalse([t for t in placed if t.startswith("L.")])
        cells = [(p["column"], p["row"]) for p in placed.values()]
        self.assertEqual(len(cells), len(set(cells)))

    def test_unknown_layout_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            layout.validate_layout({"policy": "spiral", "row_offset": 1})


@unittest.skipUnless(os.path.exists(helpers.REAL), "real Tech List not present")
class RealDataLayoutTest(Base):

    def test_invariants_on_the_real_tree(self):
        graph, lay = helpers.build(helpers.REAL)
        pos = lay["nodes"]

        cells = [(p["column"], p["row"]) for p in pos.values()]
        self.assertEqual(len(cells), len(set(cells)), "two nodes share a cell")

        band_from = helpers.settings.config["postprocess"]["band_tiers_from"]
        band_to = helpers.settings.config["postprocess"]["band_tiers_to"]

        for domain, domain_data in graph["domains"].items():
            starts = set()
            for cluster in domain_data["clusters"].values():
                members = [t for t in cluster["nodes"] if t in pos]
                if members and band_from <= int(cluster["tier"]) <= band_to:
                    starts.add(min(pos[t]["row"] for t in members))
            self.assertLessEqual(len(starts), 1,
                                 f"{domain}: band clusters start on different rows")


if __name__ == "__main__":
    unittest.main()
