"""Data lint for the Tech List CSV (tech_tree.py --check).

Works on the raw CSV rows, before any graph is built, so it can also
report the mistakes that would make building the graph fail.

Dependencies are read with the same meaning as everywhere else:
separate DepGroup cells are AND, alternatives inside a cell (|) are OR,
a cluster row (Category CLUSTER) stands for all technologies of its
domain and tier. A technology that depends on a cluster needs any one
of its members; a dependency listed on a cluster row applies to every
member. The severity of each check (error, warning or off) is set in
the [check] section of tech_tree.toml.
"""

import itertools
import re
from collections import defaultdict, namedtuple

from . import settings

Finding = namedtuple("Finding", "check severity tech_id message")

DEP_COLUMNS = ["DepGroup1", "DepGroup2", "DepGroup3", "DepGroup4"]

# One dependency group of one technology, with cluster references
# expanded to their members: alternatives are the real technologies
# any one of which satisfies the group.
Group = namedtuple("Group", "label tokens alternatives inherited")


def _field(row, name):
    return (row.get(name) or "").strip()


def _tokens(cell):
    return [t.strip() for t in cell.split("|") if t.strip()]


def _group_met(group, present, done):
    """Is one dependency group satisfied?

    `present` are the technologies that exist (those of switched-off
    modules do not). A group none of whose alternatives is present is
    obsolete and counts as met: a dependency on a switched-off module
    is dropped. Otherwise one of the alternatives that exist must be
    researchable. A group that never had an alternative (only unknown
    references) can never be met."""

    if not group.alternatives:
        return False

    live = group.alternatives & present

    if not live:
        return True

    return any(alt in done for alt in live)


def _researchable(present, groups):
    """Technologies that can eventually be researched when only the
    `present` ones exist. Starting from nothing and repeating until
    nothing changes handles AND, OR and cycles correctly."""

    present = set(present)
    done = set()
    changed = True

    while changed:
        changed = False
        for tech_id in sorted(present):
            if tech_id in done:
                continue
            if all(_group_met(g, present, done) for g in groups[tech_id]):
                done.add(tech_id)
                changed = True

    return done


def _blocking_group(tech_id, groups, present, done, modules):
    """Describe the first group of a technology that is not met,
    listing the alternatives that exist with their module."""

    for group in groups[tech_id]:
        if not _group_met(group, present, done):
            shown = "|".join(group.tokens)
            live = sorted({
                f"{alt} [{modules.get(alt, '?')}]"
                for alt in group.alternatives & present
            })
            listed = ", ".join(live[:6]) + (" ..." if len(live) > 6 else "")
            return f"{group.label} ({shown}) -> {listed or 'nothing'}"

    return "no blocking group found"


def run_checks(rows):
    """Run every enabled check on the CSV rows; returns Findings."""

    findings = []

    def add(check, tech_id, message):
        level = settings.check_levels[check]
        if level != "off":
            findings.append(Finding(check, level, tech_id, message))

    # ── Fields and duplicate ids ─────────────────────────────────
    by_id = {}
    tier_of = {}

    for position, row in enumerate(rows, start=1):

        tech_id = _field(row, "Tech_ID")
        name = _field(row, "Name")
        shown = tech_id or f"(row {position}: {name or 'no name'})"

        if not tech_id:
            add("missing_field", shown, "Tech_ID is empty")
            continue

        if tech_id in by_id:
            add("duplicate_id", tech_id, "Tech_ID appears more than once; "
                "the later row replaces the earlier one")
            continue

        by_id[tech_id] = row

        for column in ("Domain", "Domain_code", "Tier"):
            if not _field(row, column):
                add("missing_field", tech_id, f"{column} is empty")

        tier = _field(row, "Tier")

        if tier:
            if tier.isdigit():
                tier_of[tech_id] = int(tier)
            else:
                add("missing_field", tech_id,
                    f"Tier '{tier}' is not a whole number")

    cluster_ids = [
        t for t, r in by_id.items() if _field(r, "Category") == "CLUSTER"
    ]
    real_ids = [t for t in by_id if t not in set(cluster_ids)]

    modules = {
        t: (_field(by_id[t], "Module") or "CORE") for t in real_ids
    }

    # Members of every domain/tier cluster.
    members_of = defaultdict(list)
    for tech_id in real_ids:
        row = by_id[tech_id]
        members_of[(_field(row, "Domain"), _field(row, "Tier"))].append(tech_id)

    cluster_members = {}
    for cluster_id in cluster_ids:
        row = by_id[cluster_id]
        key = (_field(row, "Domain"), _field(row, "Tier"))
        cluster_members[cluster_id] = list(members_of.get(key, []))
        if not cluster_members[cluster_id]:
            add("unknown_reference", cluster_id,
                f"cluster has no technologies in {key[0]} tier {key[1]}")

    # ── Expand every dependency group ────────────────────────────
    referenced = set()

    def expand(owner, label, cell):
        tokens = _tokens(cell)
        alternatives = set()
        for token in tokens:
            referenced.add(token)
            if token in cluster_members:
                alternatives.update(cluster_members[token])
            elif token in by_id:
                alternatives.add(token)
            else:
                add("unknown_reference", owner,
                    f"{label}: '{token}' is not a technology or cluster")
        if len(set(tokens)) != len(tokens):
            add("redundant_dependency", owner,
                f"{label} lists the same entry more than once "
                f"({'|'.join(tokens)})")
        return Group(label, tokens, frozenset(alternatives), False)

    own_groups = {}
    for tech_id, row in by_id.items():
        own_groups[tech_id] = [
            expand(tech_id, column, _field(row, column))
            for column in DEP_COLUMNS if _field(row, column)
        ]

    # A technology also inherits the groups listed on its cluster's
    # row: "every member of this cluster needs this".
    groups = {}
    for tech_id in real_ids:
        row = by_id[tech_id]
        inherited = []
        for cluster_id in cluster_ids:
            c = by_id[cluster_id]
            if (_field(c, "Domain"), _field(c, "Tier")) == (
                _field(row, "Domain"), _field(row, "Tier")
            ):
                for g in own_groups[cluster_id]:
                    inherited.append(
                        Group(f"{cluster_id} {g.label}", g.tokens,
                              g.alternatives, True)
                    )
        groups[tech_id] = own_groups[tech_id] + inherited

    # ── Redundant groups ─────────────────────────────────────────
    for tech_id in real_ids:
        gs = [g for g in groups[tech_id] if g.alternatives]
        for i, g in enumerate(gs):
            if g.inherited:
                # A cluster-wide gate is a default for all members; a
                # member that names something more specific does not
                # make the gate a mistake.
                continue
            for j, other in enumerate(gs):
                if i == j or not other.alternatives <= g.alternatives:
                    continue
                if other.alternatives == g.alternatives and j > i:
                    continue
                add("redundant_dependency", tech_id,
                    f"{g.label} ({'|'.join(g.tokens)}) is implied by "
                    f"{other.label} ({'|'.join(other.tokens)}) and "
                    f"changes nothing")
                break

    # ── Can everything be researched? ────────────────────────────
    everything = set(real_ids)
    ok_all = _researchable(everything, groups)

    for tech_id in real_ids:
        if tech_id not in ok_all:
            add("unresearchable", tech_id,
                "can never become eligible; blocked by "
                + _blocking_group(tech_id, groups, everything, ok_all,
                                  modules))

    # ── Optional modules switched off ────────────────────────────
    # Switching a module off removes its technologies. A technology
    # of another module that depended on them stays, and a dependency
    # group made only of removed technologies becomes obsolete. Try
    # every combination of modules that are on (CORE always is).
    optional = sorted({m for m in modules.values() if m != "CORE"})
    blocked = {}
    thinned = {}

    for size in range(len(optional)):
        for on in itertools.combinations(optional, size):
            enabled = {"CORE", *on}
            present = {t for t in real_ids if modules[t] in enabled}
            done = _researchable(present, groups)

            for tech_id in sorted(present):
                if tech_id not in ok_all:
                    continue  # reported as unresearchable already
                if tech_id not in done and tech_id not in blocked:
                    blocked[tech_id] = (on, _blocking_group(
                        tech_id, groups, present, done, modules))
                real = [g for g in groups[tech_id] if g.alternatives]
                if (real and tech_id not in thinned
                        and not any(g.alternatives & present for g in real)):
                    thinned[tech_id] = on

    def modules_on(on):
        return " + ".join(["CORE", *on])

    for tech_id, (on, text) in blocked.items():
        add("module_combination_blocked", tech_id,
            f"cannot be researched when only {modules_on(on)} are on; "
            f"blocked by {text}")

    for tech_id, on in thinned.items():
        add("module_loses_prerequisites", tech_id,
            f"has no prerequisite left when only {modules_on(on)} are on "
            f"(every dependency group is obsolete)")

    # ── Tier order ───────────────────────────────────────────────
    for tech_id in real_ids:
        if tech_id not in tier_of:
            continue
        for g in groups[tech_id]:
            tiers = [tier_of[a] for a in g.alternatives if a in tier_of]
            if not tiers:
                continue
            earliest = min(tiers)
            where = f"{g.label} ({'|'.join(g.tokens)})"
            if earliest > tier_of[tech_id]:
                add("tier_higher", tech_id,
                    f"{where} only offers technologies from a later tier "
                    f"(tier {earliest}, this is tier {tier_of[tech_id]})")
            elif earliest == tier_of[tech_id]:
                add("tier_same", tech_id,
                    f"{where} only offers technologies from the same tier")

    for tech_id in real_ids:
        if (tier_of.get(tech_id, 0) >= 2
                and not any(g.alternatives for g in groups[tech_id])):
            add("no_prerequisites", tech_id,
                f"tier {tier_of[tech_id]} technology has no prerequisites")

    # ── Categories, ids, names, descriptions ─────────────────────
    for tech_id, row in by_id.items():
        category = _field(row, "Category")
        if category and category not in settings.node_views:
            add("unknown_category", tech_id,
                f"category '{category}' has no entry in [node_views]; "
                f"drawn with DEFAULT")

    codes = defaultdict(set)
    for tech_id in real_ids:
        row = by_id[tech_id]
        code = _field(row, "Domain_code")
        codes[code].add(_field(row, "Domain"))
        match = re.match(r"^([A-Za-z]+)\.(\d+)\.", tech_id)
        if match:
            if code and match.group(1) != code:
                add("id_mismatch", tech_id,
                    f"Tech_ID starts with '{match.group(1)}' but "
                    f"Domain_code is '{code}'")
            if tech_id in tier_of and int(match.group(2)) != tier_of[tech_id]:
                add("id_mismatch", tech_id,
                    f"Tech_ID says tier {int(match.group(2))} but Tier is "
                    f"{tier_of[tech_id]}")
    for code, names in sorted(codes.items()):
        if len(names) > 1:
            add("id_mismatch", f"code {code}",
                f"Domain_code is used by several domains: "
                f"{', '.join(sorted(names))}")

    for tech_id in real_ids:
        row = by_id[tech_id]
        if not _field(row, "Name"):
            add("missing_name", tech_id, "Name is empty")
        if not _field(row, "Description"):
            add("missing_description", tech_id, "Description is empty")

    for cluster_id in cluster_ids:
        # A cluster row is used if something depends on it, or if it
        # carries dependencies itself (a gate for all its members).
        if cluster_id not in referenced and not own_groups[cluster_id]:
            add("unused_cluster_row", cluster_id,
                "cluster row is neither used in a dependency nor has "
                "dependencies of its own")

    # ── Domains against the config ───────────────────────────────
    in_data = {_field(r, "Domain") for r in rows if _field(r, "Domain")}
    for name in settings.domain_order:
        if name not in in_data:
            add("domain_config", name,
                "configured in [[domains]] but not in the data")
    for name in sorted(in_data - set(settings.domain_order)):
        add("domain_config", name,
            "in the data but not in [[domains]]")

    return findings


def format_report(findings, source, row_count):
    """The findings as text: errors first, then warnings."""

    order = {"error": 0, "warning": 1}
    lines = [f"Checked {row_count} rows from {source}", ""]

    for f in sorted(findings, key=lambda f: (order[f.severity], f.check,
                                             f.tech_id)):
        lines.append(
            f"{f.severity.upper():7s} {f.check:20s} {f.tech_id}: {f.message}"
        )

    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")

    if findings:
        lines.append("")
    lines.append(f"{errors} error(s), {warnings} warning(s)")

    return "\n".join(lines)


def exit_status(findings, strict=False):
    """1 if there is an error (or a warning, in strict mode)."""

    for f in findings:
        if f.severity == "error" or (strict and f.severity == "warning"):
            return 1

    return 0
