"""The virtual grid: where each visible technology sits, as a
column (tier) and a row. Knows nothing about Graphviz.
"""


def clusters_for_tier(graph, domain, tier):
    """Return the clusters for a domain that belong to a tier."""

    domain_data = graph["domains"].get(domain)

    if domain_data is None:
        return []

    return [
        cluster_data
        for cluster_data in domain_data["clusters"].values()
        if cluster_data["tier"] == tier
    ]


def create_tier_to_column(graph):

    tiers = sorted(
        (t for t in graph["tiers"] if t.strip()),
        key=lambda tier: int(tier)
    )

    return {
        tier: column
        for column, tier in enumerate(tiers, start=1)
    }


def resolve_domain_order(graph, configured_order=None):

    actual_domains = list(graph["domains"])

    if configured_order is None:
        return actual_domains

    configured = [
        domain
        for domain in configured_order
        if domain in graph["domains"]
    ]

    remaining = [
        domain
        for domain in actual_domains
        if domain not in configured
    ]

    return configured + remaining


def validate_layout(layout):

    # TODO - Make this variable
    valid_policies = {
        "compact",
        "uniform",
        "aligned",
        "fixed"
    }

    if layout["policy"] not in valid_policies:
        raise ValueError(
            f"Unknown layout policy '{layout['policy']}'"
        )

    if layout["row_offset"] < 0:
        raise ValueError(
            "row_offset must be >= 0"
        )


def validate_resolved_layout(graph, resolved_layout):

    occupied = {}

    for tech_id, position in resolved_layout["nodes"].items():

        coordinate = (
            position["column"],
            position["row"]
        )

        if coordinate in occupied:

            raise ValueError(
                f"Layout collision: "
                f"'{tech_id}' and "
                f"'{occupied[coordinate]}' "
                f"share position {coordinate}"
            )

        occupied[coordinate] = tech_id

    for tech_id, node in graph["nodes"].items():

        if not node["view"].get("visible", True):
            continue

        if tech_id not in resolved_layout["nodes"]:

            raise ValueError(
                f"Visible node '{tech_id}' "
                f"has no layout position"
            )


def resolve_layout(graph, layout):

    validate_layout(layout)

    resolved = layout.copy()

    resolved["tier_to_column"] = create_tier_to_column(graph)

    resolved["domain_order"] = resolve_domain_order(
        graph,
        layout.get("domain_order")
    )

    resolved["nodes"] = calculate_node_positions(
        graph,
        resolved
    )

    validate_resolved_layout(
        graph,
        resolved
    )

    return resolved


def compute_max_cluster_sizes_per_domain(graph, tier_filter=None):
    """Return the largest visible cluster row-height per domain.

    RCENTRE nodes occupy 2 virtual rows each; all other nodes
    occupy 1. This count is used to pad smaller clusters so every
    cluster in a domain occupies the same number of virtual rows,
    creating consistent horizontal domain bands in the grid.

    tier_filter: optional set of tier strings. When provided only
    clusters belonging to those tiers are considered.
    """

    max_sizes = {}

    for domain, domain_data in graph["domains"].items():

        max_rows = 0

        for cluster_data in domain_data["clusters"].values():

            if (
                tier_filter is not None
                and cluster_data["tier"] not in tier_filter
            ):
                continue

            cluster_rows = sum(
                2 if graph["nodes"][tid]["category"] == "RCENTRE"
                else 1
                for tid in cluster_data["nodes"]
                if graph["nodes"][tid]["view"].get("visible", True)
            )

            max_rows = max(max_rows, cluster_rows)

        max_sizes[domain] = max_rows

    return max_sizes


def find_cluster_start(natural_start, cluster_rows, occupied, prev_end_row):
    """Find the first consecutive run of free rows for a cluster.

    Starts at max(natural_start, prev_end_row + 2) so a one-free-row
    gap between domain clusters is always respected. Advances past
    any occupied block (from a centred cluster) by jumping to
    max_conflict + 2, maintaining the same gap rule. The entire
    cluster shifts as a unit — no splits.
    """

    start = max(int(natural_start), prev_end_row + 2)

    while True:
        conflicts = [
            r for r in range(start, start + cluster_rows)
            if r in occupied
        ]
        if not conflicts:
            return start
        # Jump past the conflicting block with one free row gap.
        start = max(conflicts) + 2


def calculate_node_positions(graph, resolved_layout):

    node_positions  = {}
    tier_to_column  = resolved_layout["tier_to_column"]
    late_tiers_from = resolved_layout.get("late_tiers_from", 7)
    row_offset      = resolved_layout["row_offset"]

    early_tiers = {
        t for t in tier_to_column if int(t) < late_tiers_from
    }
    late_tiers = {
        t for t in tier_to_column if int(t) >= late_tiers_from
    }

    early_max_sizes = compute_max_cluster_sizes_per_domain(
        graph, tier_filter=early_tiers
    )
    late_max_sizes = compute_max_cluster_sizes_per_domain(
        graph, tier_filter=late_tiers
    )

    # Domains whose late-tier cluster exceeds the early-tier band
    # are centred on their own domain band rather than top-aligned.
    centred_domains = {
        domain
        for domain in resolved_layout["domain_order"]
        if late_max_sizes.get(domain, 0) > early_max_sizes.get(domain, 0)
    }

    # Domain band starts and centres derived from the early-tier layout.
    # Used for centering and for the natural top-row of late-tier clusters.
    domain_band_starts  = {}
    domain_band_centres = {}
    accum = 0

    for domain in resolved_layout["domain_order"]:
        early_max = early_max_sizes.get(domain, 0)
        if early_max > 0:
            band_start = accum + 1
            domain_band_starts[domain]  = band_start
            domain_band_centres[domain] = band_start + (early_max - 1) / 2
        accum += early_max + row_offset

    fallback_centre = accum / 2

    # ── Shared placement helpers ──────────────────────────────────

    def visible_in_cluster(cluster):
        return [
            tid for tid in cluster["nodes"]
            if graph["nodes"][tid]["view"].get("visible", True)
        ]

    def count_rows(nodes):
        return sum(
            2 if graph["nodes"][tid]["category"] == "RCENTRE" else 1
            for tid in nodes
        )

    def place_nodes(nodes, column, start_r):
        """Write positions consecutively from start_r; return next free row."""
        r = start_r
        for tid in nodes:
            node_positions[tid] = {"column": column, "row": r}
            r += 2 if graph["nodes"][tid]["category"] == "RCENTRE" else 1
        return r

    def mark_occupied(nodes, start_r, occupied):
        """Add node rows (and RCENTRE reserved rows) to the occupied set."""
        r = start_r
        for tid in nodes:
            occupied.add(r)
            if graph["nodes"][tid]["category"] == "RCENTRE":
                occupied.add(r + 1)
                r += 2
            else:
                r += 1

    # ─────────────────────────────────────────────────────────────

    for tier, column in tier_to_column.items():

        is_late = int(tier) >= late_tiers_from

        if not is_late:

            # ── Early tiers: normal band placement ───────────────────
            row = 0

            for domain in resolved_layout["domain_order"]:
                early_max = early_max_sizes.get(domain, 0)
                clusters  = clusters_for_tier(graph, domain, tier)

                if not clusters:
                    row += early_max + row_offset
                    continue

                for cluster in clusters:
                    nodes = visible_in_cluster(cluster)
                    if not nodes:
                        continue

                    rows_used = 0
                    for tid in nodes:
                        row       += 1
                        rows_used += 1
                        node_positions[tid] = {"column": column, "row": row}
                        if graph["nodes"][tid]["category"] == "RCENTRE":
                            row       += 1
                            rows_used += 1

                    row += max(0, early_max - rows_used) + row_offset

        else:

            # ── Late tiers: two-pass collision-aware placement ────────
            occupied = set()

            # Pass 1 — centred domains.
            #
            # Alignment node index (0-based): (cluster_rows - 1) // 2
            # → Even n:   node n//2     (1-based) sits at band centre.
            # → Odd  n:   node (n+1)//2 (1-based) sits at band centre.
            for domain in resolved_layout["domain_order"]:
                if domain not in centred_domains:
                    continue

                for cluster in clusters_for_tier(graph, domain, tier):
                    nodes = visible_in_cluster(cluster)
                    if not nodes:
                        continue

                    cluster_rows = count_rows(nodes)
                    centre = domain_band_centres.get(domain, fallback_centre)
                    start  = round(centre) - (cluster_rows - 1) // 2

                    place_nodes(nodes, column, start)
                    mark_occupied(nodes, start, occupied)

            # Pass 2 — non-centred domains.
            #
            # Each cluster tries to start at its natural band-start row.
            # If that consecutive range is blocked by a centred cluster,
            # find_cluster_start() shifts the whole cluster past the
            # conflict with a one-free-row gap. No splits within a cluster.
            prev_end_row = -1  # allows first domain to start at row 1

            for domain in resolved_layout["domain_order"]:

                if domain in centred_domains:
                    # Already placed in pass 1; sync prev_end_row.
                    placed = [
                        pos["row"]
                        for tid, pos in node_positions.items()
                        if graph["nodes"][tid]["domain"] == domain
                        and pos["column"] == column
                    ]
                    if placed:
                        prev_end_row = max(prev_end_row, max(placed))
                    continue

                for cluster in clusters_for_tier(graph, domain, tier):
                    nodes = visible_in_cluster(cluster)
                    if not nodes:
                        continue

                    cluster_rows  = count_rows(nodes)
                    natural_start = domain_band_starts.get(domain, 1)

                    start = find_cluster_start(
                        natural_start, cluster_rows, occupied, prev_end_row
                    )

                    end_r = place_nodes(nodes, column, start)
                    mark_occupied(nodes, start, occupied)
                    prev_end_row = end_r - 1  # last occupied row

    return node_positions
