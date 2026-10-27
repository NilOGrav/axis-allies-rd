import contextlib
import os
import unittest

import helpers
from helpers import Base
from rdtree import check, data, settings


def row(tech_id, tier, deps=(), domain="Air", code=None, module="CORE",
        category="", name="Test", description="Test technology."):
    code = code or tech_id.split(".")[0]
    cells = list(deps) + [""] * (4 - len(deps))
    return {
        "Tech_ID": tech_id, "Domain_code": code, "Tier": str(tier),
        "Domain": domain, "Name": name, "Description": description,
        "Module": module, "Category": category,
        "DepGroup1": cells[0], "DepGroup2": cells[1],
        "DepGroup3": cells[2], "DepGroup4": cells[3],
    }


def cluster(tech_id, tier, deps=(), domain="Air"):
    return row(tech_id, tier, deps, domain=domain, module="",
               category="CLUSTER", name="Cluster", description="")


@contextlib.contextmanager
def levels(**changes):
    saved = dict(settings.check_levels)
    settings.check_levels.update(changes)
    try:
        yield
    finally:
        settings.check_levels.clear()
        settings.check_levels.update(saved)


class CheckBase(Base):

    def found(self, rows, ignore=("domain_config",)):
        return [(f.check, f.tech_id) for f in check.run_checks(rows)
                if f.check not in ignore]

    def messages(self, rows, name):
        return [f.message for f in check.run_checks(rows) if f.check == name]


class IntegrityTest(CheckBase):

    def test_duplicate_id(self):
        rows = [row("A.1.01", 1), row("A.1.01", 1)]
        self.assertEqual(self.found(rows), [("duplicate_id", "A.1.01")])

    def test_missing_and_malformed_fields(self):
        rows = [row("A.1.01", ""), row("A.1.02", "two"), row("", 1)]
        found = self.found(rows)
        self.assertIn(("missing_field", "A.1.01"), found)
        self.assertIn(("missing_field", "A.1.02"), found)
        self.assertTrue(any(c == "missing_field" and "row 3" in t
                            for c, t in found))

    def test_unknown_reference(self):
        rows = [row("A.1.01", 1), row("A.2.01", 2, ["A.1.01", "Z.9.99"])]
        self.assertIn(("unknown_reference", "A.2.01"), self.found(rows))

    def test_cluster_without_members(self):
        rows = [row("A.1.01", 1), cluster("X.A.07", 7)]
        self.assertIn(("unknown_reference", "X.A.07"), self.found(rows))


class ResearchabilityTest(CheckBase):

    def test_a_cycle_can_never_be_researched(self):
        rows = [row("A.2.01", 2, ["A.2.02"]), row("A.2.02", 2, ["A.2.01"])]
        unresearchable = {t for c, t in self.found(rows) if c == "unresearchable"}
        self.assertEqual(unresearchable, {"A.2.01", "A.2.02"})

    def test_an_or_alternative_breaks_a_cycle(self):
        rows = [row("A.1.01", 1),
                row("A.2.01", 2, ["A.2.02|A.1.01"]),
                row("A.2.02", 2, ["A.2.01"])]
        self.assertFalse([f for f in self.found(rows) if f[0] == "unresearchable"])

    def test_self_dependency(self):
        rows = [row("A.2.01", 2, ["A.2.01"])]
        self.assertIn(("unresearchable", "A.2.01"), self.found(rows))


class ModuleTest(CheckBase):
    """Switching a module off removes its technologies. Technologies
    that stay are not blocked by that: a dependency group made only of
    removed technologies becomes obsolete."""

    def test_core_may_depend_on_an_optional_module(self):
        # Without NUCLEAR, "A.2.01 needs A.1.01" is simply dropped and
        # A.2.01 still needs its other prerequisite.
        rows = [row("A.1.01", 1, module="NUCLEAR"), row("A.1.02", 1),
                row("A.2.01", 2, ["A.1.01", "A.1.02"])]
        self.assertEqual(self.found(rows), [])

    def test_an_optional_module_may_depend_on_another_one(self):
        rows = [row("A.1.01", 1, module="OIL"), row("A.1.02", 1),
                row("A.2.01", 2, ["A.1.01", "A.1.02"], module="NUCLEAR")]
        self.assertEqual(self.found(rows), [])

    def test_a_remaining_alternative_is_still_required(self):
        # (A.1.02 | A.1.01): with NUCLEAR off only A.1.02 is left, so
        # it is needed; here it can only be researched after A.2.01,
        # which needs the group: a cycle that only the removed
        # alternative broke.
        rows = [row("A.1.01", 1, module="NUCLEAR"),
                row("A.2.01", 2, ["A.2.02|A.1.01"]),
                row("A.2.02", 2, ["A.2.01"])]
        found = self.found(rows)
        self.assertIn(("module_combination_blocked", "A.2.01"), found)
        self.assertIn(("module_combination_blocked", "A.2.02"), found)
        self.assertFalse([f for f in found if f[0] == "unresearchable"])
        message = self.messages(rows, "module_combination_blocked")[0]
        self.assertIn("only CORE are on", message)

    def test_the_first_failing_combination_is_the_one_with_fewest_modules(self):
        rows = [row("A.1.01", 1, module="OIL"),
                row("A.2.01", 2, ["A.2.02|A.1.01"]),
                row("A.2.02", 2, ["A.2.01"]),
                row("A.3.01", 3, ["A.2.01"], module="NUCLEAR")]
        by_tech = {f.tech_id: f.message for f in check.run_checks(rows)
                   if f.check == "module_combination_blocked"}
        # A.2.01 fails already with nothing but CORE; A.3.01 only exists
        # when NUCLEAR is on, so that is its smallest failing combination.
        self.assertIn("only CORE are on", by_tech["A.2.01"])
        self.assertIn("only CORE + NUCLEAR are on", by_tech["A.3.01"])

    def test_losing_every_prerequisite_is_reported(self):
        rows = [row("A.1.01", 1, module="NUCLEAR"),
                row("A.3.01", 3, ["A.1.01"])]
        found = self.found(rows)
        self.assertIn(("module_loses_prerequisites", "A.3.01"), found)
        self.assertFalse([f for f in found if f[0] == "module_combination_blocked"])

    def test_losing_only_some_prerequisites_is_fine(self):
        rows = [row("A.1.01", 1, module="NUCLEAR"), row("A.1.02", 1),
                row("A.3.01", 3, ["A.1.01|A.1.02"])]
        self.assertEqual(self.found(rows), [])

    def test_a_module_depending_only_on_another_module_is_reported(self):
        rows = [row("A.1.01", 1, module="OIL"),
                row("A.2.01", 2, ["A.1.01"], module="NUCLEAR")]
        found = self.found(rows)
        self.assertIn(("module_loses_prerequisites", "A.2.01"), found)

    def test_a_module_may_need_core(self):
        rows = [row("A.1.01", 1), row("A.2.01", 2, ["A.1.01"], module="NUCLEAR")]
        self.assertEqual(self.found(rows), [])

    def test_every_combination_of_modules_is_tried(self):
        # Blocked only when OIL is off but NUCLEAR is on.
        rows = [row("A.1.01", 1, module="OIL"),
                row("A.2.01", 2, ["A.2.02|A.1.01"], module="NUCLEAR"),
                row("A.2.02", 2, ["A.2.01"], module="NUCLEAR")]
        messages = self.messages(rows, "module_combination_blocked")
        self.assertTrue(messages)
        self.assertTrue(all("CORE + NUCLEAR are on" in m for m in messages))


class RedundancyTest(CheckBase):

    def test_or_group_that_contains_a_required_technology(self):
        # The M.6.02 case: (A|B|C) AND A  -- the OR changes nothing.
        rows = [row("A.1.01", 1), row("A.1.02", 1), row("A.1.03", 1),
                row("A.2.01", 2, ["A.1.01|A.1.02|A.1.03", "A.1.01"])]
        redundant = [f for f in check.run_checks(rows)
                     if f.check == "redundant_dependency"]
        self.assertEqual(len(redundant), 1)
        self.assertIn("DepGroup1", redundant[0].message)

    def test_same_entry_twice_in_one_group(self):
        rows = [row("A.1.01", 1), row("A.2.01", 2, ["A.1.01|A.1.01"])]
        self.assertIn(("redundant_dependency", "A.2.01"), self.found(rows))

    def test_identical_groups_are_reported_once(self):
        rows = [row("A.1.01", 1), row("A.2.01", 2, ["A.1.01", "A.1.01"])]
        self.assertEqual(
            [f for f in self.found(rows) if f[0] == "redundant_dependency"],
            [("redundant_dependency", "A.2.01")])

    def test_a_specific_prerequisite_does_not_make_the_cluster_gate_a_mistake(self):
        rows = [row("A.1.01", 1), row("A.1.02", 1),
                cluster("X.A.01", 1),
                row("A.2.01", 2, ["A.1.01"]),
                cluster("X.A.02", 2, ["X.A.01"])]
        self.assertFalse([f for f in self.found(rows)
                          if f[0] == "redundant_dependency"])

    def test_independent_groups_are_fine(self):
        rows = [row("A.1.01", 1), row("A.1.02", 1),
                row("A.2.01", 2, ["A.1.01", "A.1.02"])]
        self.assertEqual(self.found(rows), [])


class TierAndStructureTest(CheckBase):

    def test_prerequisite_from_a_later_tier(self):
        rows = [row("A.3.01", 3), row("A.2.01", 2, ["A.3.01"])]
        self.assertIn(("tier_higher", "A.2.01"), self.found(rows))

    def test_prerequisite_from_the_same_tier(self):
        rows = [row("A.2.01", 2, ["A.1.01"]), row("A.2.02", 2, ["A.2.01"]),
                row("A.1.01", 1)]
        self.assertIn(("tier_same", "A.2.02"), self.found(rows))

    def test_one_earlier_alternative_is_enough(self):
        rows = [row("A.1.01", 1), row("A.3.01", 3),
                row("A.2.01", 2, ["A.1.01|A.3.01"])]
        self.assertFalse([f for f in self.found(rows) if f[0].startswith("tier_")])

    def test_high_tier_without_prerequisites(self):
        rows = [row("A.3.01", 3), row("A.1.01", 1)]
        found = self.found(rows)
        self.assertIn(("no_prerequisites", "A.3.01"), found)
        self.assertNotIn(("no_prerequisites", "A.1.01"), found)

    def test_a_cluster_gate_counts_as_a_prerequisite(self):
        rows = [row("A.1.01", 1), row("A.2.01", 2), cluster("X.A.02", 2, ["A.1.01"])]
        self.assertNotIn(("no_prerequisites", "A.2.01"), self.found(rows))

    def test_unknown_category(self):
        rows = [row("A.1.01", 1, category="RCENTER"), row("A.1.02", 1, category="RCENTRE")]
        self.assertEqual(self.found(rows), [("unknown_category", "A.1.01")])

    def test_id_that_disagrees_with_the_tier(self):
        rows = [row("A.2.05", 5)]
        self.assertIn(("id_mismatch", "A.2.05"), self.found(rows))

    def test_id_that_disagrees_with_the_domain_code(self):
        rows = [row("A.1.01", 1, code="L")]
        self.assertIn(("id_mismatch", "A.1.01"), self.found(rows))

    def test_one_code_for_two_domains(self):
        rows = [row("A.1.01", 1), row("A.1.02", 1, domain="Land")]
        self.assertIn(("id_mismatch", "code A"), self.found(rows))

    def test_empty_name_and_description(self):
        rows = [row("A.1.01", 1, name="", description="")]
        found = self.found(rows)
        self.assertIn(("missing_name", "A.1.01"), found)
        self.assertIn(("missing_description", "A.1.01"), found)

    def test_unused_cluster_row_but_a_gate_is_used(self):
        rows = [row("A.1.01", 1), cluster("X.A.01", 1),
                row("A.4.01", 4, ["A.1.01"]), cluster("X.A.04", 4, ["A.1.01"])]
        with levels(unused_cluster_row="warning"):
            self.assertEqual(
                [f for f in self.found(rows) if f[0] == "unused_cluster_row"],
                [("unused_cluster_row", "X.A.01")])
        self.assertFalse([f for f in self.found(rows)
                          if f[0] == "unused_cluster_row"], "off by default")

    def test_domains_are_compared_with_the_config(self):
        rows = [row("A.1.01", 1), row("Z.1.01", 1, domain="Zeppelins")]
        findings = {f.tech_id: f.message for f in check.run_checks(rows)
                    if f.check == "domain_config"}
        self.assertIn("not in [[domains]]", findings["Zeppelins"])
        self.assertIn("not in the data", findings["Land"])


class ReportTest(CheckBase):

    def test_a_check_set_to_off_is_silent(self):
        rows = [row("A.1.01", 1), row("A.1.01", 1)]
        with levels(duplicate_id="off"):
            self.assertEqual(self.found(rows), [])

    def test_levels_decide_severity_and_exit_status(self):
        rows = [row("A.1.01", 1, category="RCENTER")]
        findings = check.run_checks(rows)
        warnings_only = [f for f in findings if f.check == "unknown_category"]
        self.assertEqual(warnings_only[0].severity, "warning")
        self.assertEqual(check.exit_status(warnings_only), 0)
        self.assertEqual(check.exit_status(warnings_only, strict=True), 1)
        with levels(unknown_category="error"):
            as_error = [f for f in check.run_checks(rows) if f.check == "unknown_category"]
            self.assertEqual(check.exit_status(as_error), 1)

    def test_report_lists_errors_first_and_counts(self):
        rows = [row("A.1.01", 1, category="RCENTER"), row("A.1.01", 1)]
        report = check.format_report(
            [f for f in check.run_checks(rows) if f.check != "domain_config"],
            "x.csv", len(rows))
        lines = report.splitlines()
        self.assertTrue(lines[2].startswith("ERROR"))
        self.assertTrue(lines[3].startswith("WARNING"))
        self.assertEqual(lines[-1], "1 error(s), 1 warning(s)")


class FixtureAndRealDataTest(CheckBase):

    def test_the_mini_fixture_is_clean(self):
        rows = data.load_data(helpers.MINI)
        self.assertEqual(self.found(rows), [])

    @unittest.skipUnless(os.path.exists(helpers.REAL), "real Tech List not present")
    def test_committed_data_has_no_integrity_errors(self):
        # Design questions (module independence, tiers) are for the
        # designer to judge; these basics must always hold.
        rows = data.load_data(helpers.REAL)
        basics = {"duplicate_id", "missing_field", "unknown_reference",
                  "unresearchable"}
        self.assertEqual([f for f in check.run_checks(rows) if f.check in basics], [])


if __name__ == "__main__":
    unittest.main()
