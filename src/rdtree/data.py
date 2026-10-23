"""Reading the Tech List CSV and building the canonical graph.

The graph answers one question: what technologies exist and how
are they related? It holds no geometry and no styling decisions
beyond the per-node view dictionaries that views.apply_view fills.
"""

from collections import defaultdict
import csv
import difflib

from .util import warn

CSV_DELIMITER = ","

REQUIRED_COLUMNS = [
    "Tech_ID", "Name", "Domain_code", "Domain", "Tier",
    "Module", "Category", "Path",
    "DepGroup1", "DepGroup2", "DepGroup3", "DepGroup4",
]


def create_graph():

    return {
        "tiers": defaultdict(list),
        "domains": {},
        "cluster_representatives": {},
        "modules": defaultdict(list),
        "path_items": defaultdict(list),
        "nodes": {},
        "edges": [],
    }


def create_node(
    tech_id,
    name,
    domain_code,
    domain,
    tier,
    cluster,
    module,
    category,
    label,
    path,
    dependencies
):

    return {
        "name": name,
        "domain_code": domain_code,
        "domain": domain,
        "tier": tier,
        "cluster": cluster,
        "module": module,
        "category": category,
        "label": label,
        "path": path,
        "dependencies": dependencies,
        "view": {}
    }


def create_domain(domain_code):

    return {
        "domain_code": domain_code,
        "clusters": {}
    }


def create_cluster(tier, label):

    return {
        "tier": tier,
        "label": label,
        "nodes": [],
        "representative": None,
        "view": {}
    }


def create_edge(source, target, edge_type, or_group_id=None):

    return {
        "source": source,
        "target": target,
        "type": edge_type,
        "or_group_id": or_group_id,
        "view": {}
    }


def create_endpoint(graph_node, routing, members=None, cluster=None):

    return {
        # What Graphviz needs: one real node (for a cluster, its
        # representative) plus the ltail/lhead routing hint.
        "graph_node": graph_node,
        "routing": routing,

        # What the dependency means: the real technologies this
        # endpoint stands for. One for a node, every member for a
        # cluster. A dependency ON a cluster means "any one of its
        # members" (an OR over all of them); a dependency OF a cluster
        # means "every member".
        "members": members if members is not None else [graph_node],

        # (domain, cluster id) for a cluster endpoint, else None.
        "cluster": cluster,
    }


def load_data(input_file):

    rows = []

    # utf-8-sig silently drops the byte-order mark that spreadsheet
    # exports often add; otherwise it would end up in the name of
    # the first column ("\ufeffTech_ID").
    with open(input_file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=CSV_DELIMITER)

        fieldnames = reader.fieldnames or []
        missing = [c for c in REQUIRED_COLUMNS if c not in fieldnames]

        if missing:
            hint = ""
            if len(fieldnames) == 1 and ";" in fieldnames[0]:
                hint = " The file looks semicolon-separated; this " \
                       "script expects commas."
            elif "ID" in fieldnames and "Tech_ID" in missing:
                hint = " The first column is still called 'ID'; " \
                       "rename it to 'Tech_ID'."
            raise SystemExit(
                f"{input_file}: missing column(s) "
                f"{', '.join(missing)}.{hint}"
            )

        for row in reader:
            # Skip completely empty rows (e.g. trailing blank lines
            # in a spreadsheet export).
            if not any(
                isinstance(v, str) and v.strip() for v in row.values()
            ):
                continue
            rows.append(row)

    return rows


def routing_endpoint(endpoint_type, endpoint_id):

    return {
        "type": endpoint_type,
        "id": endpoint_id
    }


def resolve_endpoint(endpoint_id, graph):

    # Real technology node
    if (
        endpoint_id in graph["nodes"]
        and graph["nodes"][endpoint_id]["category"] != "CLUSTER"
    ):

        return create_endpoint(
            endpoint_id,
            routing_endpoint(
                "node",
                endpoint_id
            )
        )

    # Cluster dependency node
    if endpoint_id in graph["cluster_representatives"]:

        cluster_dependency = graph["nodes"][endpoint_id]

        domain = cluster_dependency["domain"]
        cluster_id = cluster_dependency["cluster"]

        cluster = graph["domains"][domain]["clusters"][cluster_id]

        representative = cluster["representative"]

        members = [
            tech_id
            for tech_id in cluster["nodes"]
            if graph["nodes"][tech_id]["category"] != "CLUSTER"
        ]

        return create_endpoint(
            representative,
            routing_endpoint(
                "cluster",
                cluster_id
            ),
            members=members,
            cluster=(domain, cluster_id)
        )

    raise ValueError(
        f"Unknown endpoint '{endpoint_id}'"
    )


def process_dependency(dep, target, or_group_id, graph):

    if not dep:
        return or_group_id

    parts = [d.strip() for d in dep.split('|') if d.strip()]

    if len(parts) > 1:
        edge_type = "OR"
        current_or_group_id = or_group_id
        or_group_id += 1

    else:
        edge_type = "AND"
        current_or_group_id = None

    target_endpoint = resolve_endpoint(target, graph)

    for p in parts:

        source_endpoint = resolve_endpoint(p, graph)

        graph["edges"].append(
            create_edge(
                source_endpoint,
                target_endpoint,
                edge_type,
                current_or_group_id
            )
        )

    return or_group_id


def process_path(path, tech_id, graph):

    if not path:
        return

    parts = [p.strip() for p in path.split(',') if p.strip()]

    for p in parts:
        graph["path_items"][p].append(tech_id)


def build_graph(rows):

    # Create the canonical graph containers.
    graph = create_graph()

    or_group_id = 0
    or_color_index = 0

    for row in rows:
        tech_id = row["Tech_ID"].strip()
        name = row["Name"].strip()
        domain_code = row["Domain_code"].strip()
        tier = row["Tier"].strip()
        domain = row["Domain"].strip()
        module = row["Module"].strip()
        category = row["Category"].strip()
        path = row["Path"].strip()

        dep1 = row["DepGroup1"].strip()
        dep2 = row["DepGroup2"].strip()
        dep3 = row["DepGroup3"].strip()
        dep4 = row["DepGroup4"].strip()

        cluster = f"{domain_code}_{tier}"

        if domain not in graph["domains"]:
            graph["domains"][domain] = create_domain(domain_code)

        if cluster not in graph["domains"][domain]["clusters"]:
            graph["domains"][domain]["clusters"][cluster] = create_cluster(
                tier,
                f"{domain} - Tier {tier}"
        )

        label = f"{tech_id}\\n{name}"

        graph["nodes"][tech_id] = create_node(
            tech_id,
            name,
            domain_code,
            domain,
            tier,
            cluster,
            module,
            category,
            label,
            path,
            [
                dep1,
                dep2,
                dep3,
                dep4
                ]
            )

        graph["tiers"][tier].append(tech_id)

        graph["modules"][module].append(tech_id)

        graph["domains"][domain]["clusters"][cluster]["nodes"].append(tech_id)

        if category == "CLUSTER":
            graph["cluster_representatives"][tech_id] = None

        process_path(path, tech_id, graph)

    # Resolve a real representative node for every cluster dependency.
    for cluster_id in graph["cluster_representatives"]:

        # The CLUSTER row itself already knows which semantic cluster
        # it belongs to. Do not reconstruct the cluster ID from X.*.
        cluster_node = graph["nodes"][cluster_id]

        domain = cluster_node["domain"]
        cluster = cluster_node["cluster"]

        cluster_data = graph["domains"][domain]["clusters"][cluster]

        # Only real nodes may represent the cluster.
        real_nodes = [
            tech_id
            for tech_id in cluster_data["nodes"]
            if graph["nodes"][tech_id]["category"] != "CLUSTER"
        ]

        if not real_nodes:
            raise ValueError(
                f"Cluster dependency '{cluster_id}' contains no real node"
            )

        # Temporary deterministic selection.
        # This selection rule will be refined later.
        cluster_data["representative"] = real_nodes[0]

    # Now that all nodes and cluster representatives exist,
    # construct the dependency edges.
    for tech_id, node in graph["nodes"].items():

        for dep in node["dependencies"]:

            or_group_id = process_dependency(
                dep,
                tech_id,
                or_group_id,
                graph
            )

    return graph


def check_domain_config(graph, configured_names):
    """Compare the domains found in the CSV with the configured ones.

    The CSV decides which domains exist; the config only decides how
    they look and in which order. Mismatches are reported, not fatal:
    unconfigured domains are appended after the configured ones with
    the default colour, and configured-but-absent domains are skipped.
    """

    data_domains = list(graph["domains"])

    # A typo in the config shows up as a configured name that is
    # absent from the data, next to a data domain that is not
    # configured. Only unconfigured data domains are offered as
    # suggestions, so a legitimately configured domain is never
    # proposed as the "correct" spelling.
    unconfigured = [
        name for name in data_domains if name not in configured_names
    ]

    for name in configured_names:
        if name not in graph["domains"]:
            hint = difflib.get_close_matches(name, unconfigured, n=1)
            suggestion = f" Did you mean '{hint[0]}'?" if hint else ""
            warn(
                f"domain '{name}' is in the config but not in the "
                f"data and is ignored.{suggestion}"
            )

    for name in data_domains:
        if name not in configured_names:
            warn(
                f"domain '{name}' is in the data but not in the "
                f"config; it is placed after the configured domains "
                f"and uses the default colour."
            )
