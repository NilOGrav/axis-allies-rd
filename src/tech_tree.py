import sys
import csv
import subprocess
from collections import defaultdict

input_file = sys.argv[1]

terminal_file = "tech_tree.txt"
simple_dot_file = "tech_tree_simple.dot"
simple_svg_file = "tech_tree_simple.svg"
grid_dot_file = "tech_tree_grid.dot"
grid_svg_file = "tech_tree_grid.svg"

WRITE_TERMINAL_FILE = True

#                        CSV DATA
#                            │
#                            ▼
#                      build_graph()
#                            │
#                            ▼
# ┌────────────────────────────────────────────────────────┐
# │                    CANONICAL GRAPH                     │
# │                                                        │
# │  What technologies exist and how are they related?     │
# └──────────────────────────┬─────────────────────────────┘
#                            │
#                  ┌─────────┴─────────┐
#                  ▼                   ▼
#             apply_view()       resolve_layout()
#                                      │
#                                      ▼
#           ┌────────────────────────────────────────────────────────┐
#           │                    VIRTUAL GRID                        │
#           │                                                        │
#           │        Where should each visible technology be?        │
#           │                                                        │
#           │                    column / row                        │
#           │                                                        │
#           │          *** KNOWS NOTHING ABOUT GRAPHVIZ ***          │
#           └──────────────────────────┬─────────────────────────────┘
#                                      │
#                         ═════════════╪═════════════
#                                 RENDERER API
#                         ═════════════╪═════════════
#                                      │
#                 ┌────────────────────┼────────────────────┐
#                 ▼                    ▼                    ▼
#            Graphviz DOT          SVG/HTML          render_terminal()
#                 │
#                 ▼
#       resolve_graphviz_layout()
#                 │
#                 ▼
#           GRAPHVIZ MODEL
#                 │
#                 ▼
#             write_dot()
#                 │
#                 ▼
#             Graphviz


domain_colors = {
    "Air": "#cfe8ff",
    "Land": "#d9f2d9",
    "Naval": "#fff2cc",
    "Logistics And Industry": "#c4a6ff",
    "Intelligence": "#e0f7fa",
    "Energy And Physics": "#f8d7da",
    "Programs": "#ffd9b3",
    "Resource": "#eeeeee",
}

DEFAULT_DOMAIN_COLOR = "black"

or_colors = [
    "#e41a1c", "#377eb8", "#4daf4a",
    "#984ea3", "#ff7f00", "#ffff33",
    "#a65628", "#f781bf"
]


layout = {
    "policy": "compact",
    "row_offset": 1,

    "domain_order": [
        "Air",
        "Land",
        "Naval",
        "Logistics And Industry",
        "Intelligence",
        "Energy And Physics",
        "Programs",
        "Resource",
    ],
}


dot_view = {
    "name": "TechTree",

    "graph": {
        "rankdir": "LR",
        "splines": "polyline",
        "compound": True,
        "clusterrank": "local",
        "newrank": True,
        "pad": 0.5,
        "nodesep": 0.6,
        "ranksep": 7.0,
    },

    "node": {
        "shape": "box",
        "width": 3.5,
        "height": 1.0,
        "fixedsize": True,
        "fontsize": 10,
    }
}


edge_views = {
    "AND": {
        "style": "solid",
        "color": "black",
        "weight": 5,
    },

    "OR": {
        "style": "dashed",
        "weight": 5,
    }
}

node_views = {
    "KEYSTONE": {
        "shape": "doubleoctagon",
        "style": "rounded,filled",
        "color": "#fffdf2",
        "penwidth": 2
    },

    "RCENTER": {
        "shape": "doublecircle",
        "style": "filled",
        "color": "#fffdf2",
        "penwidth": 2
    },

    "RESOURCE": {
        "shape": "box",
        "style": "rounded,filled,dotted,bold",
        "color": "#fffdf2",
        "penwidth": 1
    },

    "CLUSTER": {
        "visible": False
    },

    "DEFAULT": {
        "shape": "box",
        "style": "rounded,filled",
        "color": "#fffdf2",
        "penwidth": 2
    }
}


cluster_view = {
    "style": "rounded,filled,dashed",
    "color": "blue",
    "penwidth": 1.5,
    "margin": 30
}


grid_experiment = {
    "cluster_fillers": True,
    "visible_fillers": True,
    "horizontal_edges": False,
    "vertical_edges": False,
}


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


def create_endpoint(graph_node, routing):

    return {
        "graph_node": graph_node,
        "routing": routing
    }


def load_data(input_file):

    rows = []

    with open(input_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
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

        return create_endpoint(
            representative,
            routing_endpoint(
                "cluster",
                cluster_id
            )
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
        tech_id = row["ID"].strip()
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


def or_group_color(or_group_id):

    return or_colors[
        or_group_id % len(or_colors)
    ]


def apply_view(graph):

    for tech_id, node in graph["nodes"].items():

        category = node["category"]

        node["view"] = node_views.get(
            category,
            node_views["DEFAULT"]
        ).copy()

    for domain, domain_data in graph["domains"].items():

        for cluster, cluster_data in domain_data["clusters"].items():

            cluster_data["view"] = cluster_view.copy()
            cluster_data["view"]["fillcolor"] = domain_colors.get(
                domain,
                DEFAULT_DOMAIN_COLOR
            )

    for edge in graph["edges"]:

        if edge["type"] == "AND":

            edge["view"] = edge_views["AND"].copy()

        elif edge["type"] == "OR":

            edge["view"] = edge_views["OR"].copy()
            edge["view"]["color"] = or_group_color(
                edge["or_group_id"]
            )

        else:

            raise ValueError(
                f"Unknown edge type '{edge['type']}'"
            )

    return graph


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
        graph["tiers"],
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


def calculate_node_positions(graph, resolved_layout):

    node_positions = {}

    tier_to_column = resolved_layout["tier_to_column"]

    for tier, column in tier_to_column.items():

        row = 0

        for domain in resolved_layout["domain_order"]:

            clusters = clusters_for_tier(
                graph,
                domain,
                tier
            )

            for cluster in clusters:

                visible_nodes = [
                    tech_id
                    for tech_id in cluster["nodes"]
                    if graph["nodes"][tech_id]["view"].get(
                        "visible",
                        True
                    )
                ]

                if not visible_nodes:
                    continue

                for tech_id in visible_nodes:

                    row += 1

                    node_positions[tech_id] = {
                        "column": column,
                        "row": row
                    }

                row += resolved_layout["row_offset"]

    return node_positions


def build_graphviz_model(graph, resolved_layout):

    graphviz_model = {
        "nodes": {},
        "clusters": [],
        "edges": [],
        "layout_edges": []
    }

    # ---------------------------------------------------------
    # Pass 1: Graphviz nodes
    # ---------------------------------------------------------

    for tech_id, node in graph["nodes"].items():

        if not node["view"].get("visible", True):
            continue

        position = resolved_layout["nodes"].get(
            tech_id
        )

        if position is None:
            raise ValueError(
                f"Visible node '{tech_id}' "
                f"has no resolved layout position"
            )

        graphviz_model["nodes"][tech_id] = {
            "id": tech_id,
            "label": node["label"],
            "column": position["column"],
            "row": position["row"],
            "type": "real",
            "view": node["view"].copy()
        }

    # ---------------------------------------------------------
    # Pass 2: Graphviz clusters
    # ---------------------------------------------------------

    for domain, domain_data in graph["domains"].items():

        for cluster_id, cluster_data in (
            domain_data["clusters"].items()
        ):

            cluster_nodes = [
                tech_id
                for tech_id in cluster_data["nodes"]
                if tech_id in graphviz_model["nodes"]
            ]

            if not cluster_nodes:
                continue

            graphviz_model["clusters"].append(
                {
                    "id": cluster_id,
                    "domain": domain,
                    "tier": cluster_data["tier"],
                    "label": cluster_data["label"],
                    "nodes": cluster_nodes,
                    "view": cluster_data["view"].copy()
                }
            )

    # ---------------------------------------------------------
    # Pass 3: Real dependency edges
    # ---------------------------------------------------------

    for edge in graph["edges"]:

        source = edge["source"]["graph_node"]
        target = edge["target"]["graph_node"]

        if source not in graphviz_model["nodes"]:
            continue

        if target not in graphviz_model["nodes"]:
            continue

        graphviz_model["edges"].append(
            {
                "source": source,
                "target": target,
                "view": edge["view"].copy(),
                "routing": {
                    "source": edge["source"]["routing"].copy(),
                    "target": edge["target"]["routing"].copy()
                }
            }
        )

    return graphviz_model


# def largest_cluster_size_by_tier(graphviz_model):
#     """Return the largest cluster node count per tier.
#
#     Used to determine the target size when equalizing
#     cluster heights within each tier.
#     """
#
#     largest = {}
#
#     for cluster in graphviz_model["clusters"]:
#
#         tier = cluster["tier"]
#         size = len(cluster["nodes"])
#
#         if tier not in largest:
#             largest[tier] = size
#         else:
#             largest[tier] = max(largest[tier], size)
#
#     return largest
def largest_cluster_size_by_domain(graphviz_model):
    """Return the largest cluster node count per domain.

    Used to give every cluster in a domain a consistent
    height, creating stable horizontal domain bands
    across the full width of the tree.
    """

    largest = {}

    for cluster in graphviz_model["clusters"]:

        domain = cluster["domain"]
        size = len(cluster["nodes"])

        if domain not in largest:
            largest[domain] = size
        else:
            largest[domain] = max(largest[domain], size)

    return largest


def add_cluster_fillers(graphviz_model, grid_experiment):
    """Pad clusters within each tier to match the largest
    cluster in that tier.

    Fillers are added to both graphviz_model["nodes"] and
    cluster["nodes"] so Graphviz treats them as genuine
    cluster members, giving each cluster a consistent height.

    Type "cluster_filler" distinguishes these from any future
    gap-filler nodes, preventing double-writing in
    write_dot_filler_nodes().
    """

    largest_sizes = largest_cluster_size_by_domain(graphviz_model)

    filler_index = 0

    for cluster in graphviz_model["clusters"]:

        domain = cluster["domain"]
        target_size = largest_sizes[domain]
        current_size = len(cluster["nodes"])
        filler_count = target_size - current_size

        if filler_count == 0:
            continue

        # All real nodes in a cluster share the same column
        # (same tier). Read it from the first real node so
        # fillers can be placed in the correct rank group.
        cluster_column = next(
            graphviz_model["nodes"][nid]["column"]
            for nid in cluster["nodes"]
            if graphviz_model["nodes"][nid]["type"] == "real"
        )

        for filler_row in range(filler_count):

            filler_id = (
                f"__filler_"
                f"{cluster['id']}_"
                f"{filler_row}_"
                f"{filler_index}"
            )

            filler_index += 1

            if grid_experiment.get("visible_fillers", False):

                filler_view = {
                    "shape": "box",
                    "style": "rounded,dashed",
                    "color": "gray",
                    "penwidth": 1,
                    "width": dot_view["node"]["width"],
                    "height": dot_view["node"]["height"],
                    "fixedsize": True,
                }

                filler_label = "FILLER"

            else:

                filler_view = {
                    "shape": "box",
                    "style": "invis",
                    "width": dot_view["node"]["width"],
                    "height": dot_view["node"]["height"],
                    "fixedsize": True,
                }

                filler_label = ""

            # Add to the global node registry.
            # column is set to the cluster's tier column so
            # write_dot_grid_ranks() can include this filler
            # in the correct rank=same group.
            # row remains None — fillers have no specific
            # virtual grid row within the cluster.
            graphviz_model["nodes"][filler_id] = {
                "id": filler_id,
                "label": filler_label,
                "column": cluster_column,
                "row": None,
                "type": "cluster_filler",
                "view": filler_view,
            }

            # Add to the cluster so Graphviz places it
            # inside the subgraph — this is the essential step.
            cluster["nodes"].append(filler_id)


def add_row_ordering_edges(graphviz_model):
    """Add invisible edges that preserve virtual row order
    within each Graphviz column.
    """

    columns = defaultdict(list)

    for node_id, node in graphviz_model["nodes"].items():

        columns[node["column"]].append(
            (
                node["row"],
                node_id
            )
        )

    for column in sorted(columns):

        nodes = sorted(
            columns[column],
            key=lambda item: item[0]
        )

        node_ids = [
            node_id
            for row, node_id in nodes
        ]

        for source, target in zip(
            node_ids,
            node_ids[1:]
        ):

            graphviz_model["layout_edges"].append(
                {
                    "source": source,
                    "target": target,
                    "view": {
                        "style": "invis",
                        "constraint": False,
                        "weight": 100
                    }
                }
            )


# def apply_grid_experiment(
#     graphviz_model,
#     grid_experiment
# ):
#
#     if grid_experiment.get(
#         "row_ordering",
#         False
#     ):
#
#         add_row_ordering_edges(
#             graphviz_model
#         )
#
#     return graphviz_model
def apply_grid_experiment(
    graphviz_model,
    grid_experiment
):

    if grid_experiment.get(
        "cluster_fillers",
        False
    ):

        add_cluster_fillers(
            graphviz_model,
            grid_experiment
        )

    # horizontal_edges and vertical_edges branches
    # will be added here when those functions are implemented.

    return graphviz_model

# def build_grid_graphviz_model(
#     graph,
#     resolved_layout,
#     grid_experiment
# ):
#
#     graphviz_model = build_graphviz_model(
#         graph,
#         resolved_layout
#     )
#
#     if grid_experiment["cluster_fillers"]:
#
#         add_cluster_fillers(
#             graphviz_model
#         )
#
#     if grid_experiment["horizontal_edges"]:
#
#         add_horizontal_grid_edges(
#             graphviz_model
#         )
#
#     if grid_experiment["vertical_edges"]:
#
#         add_vertical_grid_edges(
#             graphviz_model
#         )
#
#     return graphviz_model


def apply_graphviz_routing(edge, attrs):

    source = edge["source"]["routing"]
    target = edge["target"]["routing"]

    if source["type"] == "cluster":
        attrs.append(
            f'ltail=cluster_{source["id"]}'
        )

    if target["type"] == "cluster":
        attrs.append(
            f'lhead=cluster_{target["id"]}'
        )


def format_dot_attrs(attrs):

    formatted = []

    for key, value in attrs.items():

        if isinstance(value, str):
            formatted.append(f'{key}="{value}"')

        elif isinstance(value, bool):
            formatted.append(f'{key}={str(value).lower()}')

        else:
            formatted.append(f'{key}={value}')

    return ", ".join(formatted)


def write_dot_graph(f):

    graph_attrs = format_dot_attrs(dot_view["graph"])

    f.write(
        f"graph [{graph_attrs}];\n"
    )

    node_attrs = format_dot_attrs(dot_view["node"])

    f.write(
        f"node [{node_attrs}];\n"
    )


def write_dot_clusters(f, graphviz_model):

    for cluster in graphviz_model["clusters"]:

        cluster_name = f'cluster_{cluster["id"]}'

        f.write(
            f'subgraph {cluster_name} {{\n'
        )

        f.write(
            f'label="{cluster["label"]}";\n'
        )

        cluster_attrs = format_dot_attrs(
            cluster["view"]
        )

        f.write(
            f'graph [{cluster_attrs}];\n'
        )

        for node_id in cluster["nodes"]:

            node = graphviz_model["nodes"][node_id]

            attrs = format_dot_attrs(
                {
                    key: value
                    for key, value in node["view"].items()
                    if key != "visible"
                }
            )

            f.write(
                f'"{node_id}" '
                f'[label="{node["label"]}", '
                f'{attrs}];\n'
            )

        f.write("}\n")


def write_dot_filler_nodes(f, graphviz_model):

    for node_id, node in (
        graphviz_model["nodes"].items()
    ):

        if node["type"] != "filler":
            continue

        attrs = format_dot_attrs(
            node["view"]
        )

        f.write(
            f'"{node_id}" '
            f'[label="{node["label"]}", '
            f'{attrs}];\n'
        )


# def write_dot_ranks(f, graphviz_model):
#
#     columns = defaultdict(list)
#
#     for node_id, node in (
#         graphviz_model["nodes"].items()
#     ):
#
#         columns[node["column"]].append(
#             node_id
#         )
#
#     for column in sorted(columns):
#
#         node_ids = columns[column]
#
#         f.write(
#             "{ rank=same; "
#             + " ".join(
#                 f'"{node_id}"'
#                 for node_id in node_ids
#             )
#             + "; }\n"
#         )
# def write_dot_ranks(f, graphviz_model):
#
#     columns = defaultdict(list)
#
#     for node_id, node in (
#         graphviz_model["nodes"].items()
#     ):
#
#         columns[node["column"]].append(
#             (
#                 node["row"],
#                 node_id
#             )
#         )
#
#     for column in sorted(columns):
#
#         nodes = sorted(
#             columns[column],
#             key=lambda item: item[0]
#         )
#
#         node_ids = [
#             node_id
#             for row, node_id in nodes
#         ]
#
#         f.write(
#             "{ rank=same; "
#             + " ".join(
#                 f'"{node_id}"'
#                 for node_id in node_ids
#             )
#             + "; }\n"
#         )
def write_dot_ranks(f, graphviz_model):

    columns = defaultdict(list)

    for node_id, node in (
        graphviz_model["nodes"].items()
    ):

        columns[node["column"]].append(
            node_id
        )

    for column in sorted(columns):

        node_ids = columns[column]

        f.write(
            "{ rank=same; "
            + " ".join(
                f'"{node_id}"'
                for node_id in node_ids
            )
            + "; }\n"
        )


# def write_dot_grid_ranks(f, graphviz_model):
#
#     columns = defaultdict(list)
#
#     for node_id, node in (
#         graphviz_model["nodes"].items()
#     ):
#
#         # Cluster fillers have column=None and row=None.
#         # They belong to their cluster structurally but
#         # have no virtual grid position, so exclude them
#         # from rank declarations.
#         if node["type"] != "real":
#             continue
#
#         columns[node["column"]].append(
#             (
#                 node["row"],
#                 node_id
#             )
#         )
#
#     for column in sorted(columns):
#
#         nodes = sorted(
#             columns[column],
#             key=lambda item: item[0]
#         )
#
#         node_ids = [
#             node_id
#             for row, node_id in nodes
#         ]
#
#         f.write(
#             "{ rank=same; "
#             + " ".join(
#                 f'"{node_id}"'
#                 for node_id in node_ids
#             )
#             + "; }\n"
#         )
def write_dot_grid_ranks(f, graphviz_model):

    columns = defaultdict(list)

    for node_id, node in (
        graphviz_model["nodes"].items()
    ):

        # Skip nodes with no column assignment.
        # Any node with a column participates in rank
        # declarations, including cluster fillers.
        if node["column"] is None:
            continue

        columns[node["column"]].append(
            (
                node["row"],
                node_id
            )
        )

    for column in sorted(columns):

        # Sort real nodes by row; fillers have row=None
        # and sort after all real nodes.
        nodes = sorted(
            columns[column],
            key=lambda item: (
                item[0] is None,
                item[0] if item[0] is not None else 0
            )
        )

        node_ids = [
            node_id
            for row, node_id in nodes
        ]

        f.write(
            "{ rank=same; "
            + " ".join(
                f'"{node_id}"'
                for node_id in node_ids
            )
            + "; }\n"
        )


def write_dot_edges(f, graphviz_model):

    for edge in graphviz_model["edges"]:

        attrs = []

        edge_view_attrs = format_dot_attrs(
            edge["view"]
        )

        if edge_view_attrs:

            attrs.append(
                edge_view_attrs
            )

        routing_edge = {
            "source": {
                "routing": edge["routing"]["source"]
            },
            "target": {
                "routing": edge["routing"]["target"]
            }
        }

        apply_graphviz_routing(
            routing_edge,
            attrs
        )

        attr_str = ", ".join(attrs)

        f.write(
            f'"{edge["source"]}" '
            f'-> "{edge["target"]}" '
            f'[{attr_str}];\n'
        )


def write_dot_layout_edges(f, graphviz_model):

    for edge in graphviz_model["layout_edges"]:

        attrs = format_dot_attrs(
            edge["view"]
        )

        f.write(
            f'"{edge["source"]}" '
            f'-> "{edge["target"]}" '
            f'[{attrs}];\n'
        )


def write_dot(graphviz_model, dot_file):

    with open(
        dot_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f'digraph {dot_view["name"]} {{\n'
        )

        write_dot_graph(f)

        write_dot_clusters(
            f,
            graphviz_model
        )

        write_dot_ranks(
            f,
            graphviz_model
        )

        write_dot_layout_edges(
            f,
            graphviz_model
        )

        write_dot_edges(
            f,
            graphviz_model
        )

        f.write("}\n")


def write_grid_dot(graphviz_model, dot_file):

    with open(
        dot_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f'digraph {dot_view["name"]} {{\n'
        )

        write_dot_graph(f)

        write_dot_clusters(
            f,
            graphviz_model
        )

        write_dot_filler_nodes(
            f,
            graphviz_model
        )

        write_dot_grid_ranks(
            f,
            graphviz_model
        )

        write_dot_layout_edges(
            f,
            graphviz_model
        )

        write_dot_edges(
            f,
            graphviz_model
        )

        f.write("}\n")


def run_graphviz(dot_file, svg_file):

    subprocess.run(
        ["dot", "-Tsvg", dot_file, "-o", svg_file],
        check=True
    )


# DEBUG Function
def print_layout(resolved_layout):

    for tech_id, position in resolved_layout["nodes"].items():

        print(
            tech_id,
            "column=", position["column"],
            "row=", position["row"]
        )


# DEBUG Function
# def print_graphviz_model(graphviz_model):
#
#     print("\nGRAPHVIZ MODEL CLUSTERS")
#
#     for cluster in graphviz_model["clusters"]:
#
#         print(
#             f'{cluster["id"]}: '
#             f'{cluster["nodes"]}'
#         )
def print_graphviz_model(graphviz_model):

    print("\nGRAPHVIZ MODEL NODES")

    nodes = sorted(
        graphviz_model["nodes"].items(),
        key=lambda item: (
            item[1]["column"],
            item[1]["row"]
        )
    )

    for node_id, node in nodes:

        print(
            f'{node_id}: '
            f'column={node["column"]}, '
            f'row={node["row"]}'
        )

    print("\nGRAPHVIZ MODEL CLUSTERS")

    for cluster in graphviz_model["clusters"]:

        print(
            f'{cluster["id"]}: '
            f'{cluster["nodes"]}'
        )


def render_terminal(graph, resolved_layout):

    lines = []

    nodes_by_position = sorted(
        resolved_layout["nodes"].items(),
        key=lambda item: (
            item[1]["column"],
            item[1]["row"]
        )
    )

    current_column = None

    for tech_id, position in nodes_by_position:

        column = position["column"]

        if current_column is not None and column != current_column:
            lines.append("")

        current_column = column

        node = graph["nodes"][tech_id]

        lines.append(
            f"row {position['row']:>3}: "
            f"{tech_id} - {node['name']}"
        )

    return "\n".join(lines)


def write_text_file(text, output_file):

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)
        f.write("\n")


def render_text(graph, resolved_layout, terminal_file):

    terminal_output = render_terminal(
        graph,
        resolved_layout
    )

    print(terminal_output)

    if WRITE_TERMINAL_FILE:

        write_text_file(
            terminal_output,
            terminal_file
        )


def render_simple_svg(
    graph,
    resolved_layout,
    dot_file,
    svg_file
):

    graphviz_model = build_graphviz_model(
        graph,
        resolved_layout
    )

    write_dot(
        graphviz_model,
        dot_file
    )

    run_graphviz(
        dot_file,
        svg_file
    )


# def render_grid_svg(
#     graph,
#     resolved_layout,
#     dot_file,
#     svg_file,
#     grid_experiment
# ):
#
#     graphviz_model = build_grid_graphviz_model(
#         graph,
#         resolved_layout,
#         grid_experiment
#     )
#
#     write_dot(
#         graphviz_model,
#         dot_file
#     )
#
#     run_graphviz(
#         dot_file,
#         svg_file
#     )
# def render_grid_svg(
#     graph,
#     resolved_layout,
#     dot_file,
#     svg_file,
#     grid_experiment
# ):
#
#     graphviz_model = build_graphviz_model(
#         graph,
#         resolved_layout
#     )
#
#     graphviz_model = apply_grid_experiment(
#         graphviz_model,
#         grid_experiment
#     )
#
#     write_grid_dot(
#         graphviz_model,
#         dot_file
#     )
#
#     run_graphviz(
#         dot_file,
#         svg_file
#     )
#
#     # TODO - post-processing SVG
#
#
# rows = load_data(input_file)
#
# graph = build_graph(rows)
#
# graph = apply_view(graph)
#
# resolved_layout = resolve_layout(
#     graph,
#     layout
# )
#
# render_text(
#     graph,
#     resolved_layout,
#     terminal_file
# )
#
# render_simple_svg(
#     graph,
#     resolved_layout,
#     simple_dot_file,
#     simple_svg_file
# )
#
# render_grid_svg(
#     graph,
#     resolved_layout,
#     grid_dot_file,
#     grid_svg_file,
#     grid_experiment
# )

def build_neato_model(graph, resolved_layout):
    """Build a neato-compatible model from the canonical graph.

    Unlike the dot model:
    - No subgraph clusters (neato ignores them anyway)
    - Every visible node gets a pos="x,y!" from the virtual grid
    - X. cluster proxy nodes are excluded (not visible)
    - ltail/lhead cluster routing is dropped — edges go directly
      between real nodes

    Coordinates are in points (72pt = 1 inch), derived from the
    same dot_view width/height/ranksep/nodesep values used by the
    simple renderer, so horizontal spacing matches.
    """

    col_spacing = (
        dot_view["node"]["width"]
        + dot_view["graph"]["ranksep"]
    ) * 72

    row_spacing = (
        dot_view["node"]["height"]
        + dot_view["graph"]["nodesep"]
    ) * 72

    # --- Nodes ---

    neato_nodes = {}

    for tech_id, node in graph["nodes"].items():

        if not node["view"].get("visible", True):
            continue

        position = resolved_layout["nodes"].get(tech_id)

        if position is None:
            continue

        x = position["column"] * col_spacing
        y = -position["row"] * row_spacing

        neato_nodes[tech_id] = {
            "id": tech_id,
            "label": node["label"],
            "pos": f"{x:.1f},{y:.1f}",
            "view": {
                k: v
                for k, v in node["view"].items()
                if k != "visible"
            },
        }

    # --- Edges ---
    # Read directly from graph["edges"] so we get the original
    # source/target pairs before any cluster-routing substitution.
    # Edges whose source or target is invisible (e.g. X. proxies)
    # are skipped — both endpoints must be rendered nodes.

    neato_edges = []
    seen = set()

    for edge in graph["edges"]:

        source = edge["source"]["graph_node"]
        target = edge["target"]["graph_node"]

        if source not in neato_nodes:
            continue

        if target not in neato_nodes:
            continue

        key = (source, target)
        if key in seen:
            continue
        seen.add(key)

        neato_edges.append(
            {
                "source": source,
                "target": target,
                "view": edge["view"].copy(),
            }
        )

    return {
        "nodes": neato_nodes,
        "edges": neato_edges,
    }


def write_neato_dot(neato_model, dot_file):
    """Write a DOT file for neato -n rendering.

    Omits dot-specific attributes (rankdir, compound, clusterrank,
    newrank) and rank=same groups. Adds pos="x,y!" to every node
    so neato uses virtual grid positions directly and only computes
    edge routing.
    """

    neato_graph_attrs = format_dot_attrs(
        {
            "splines": "spline",
            "outputorder": "edgesfirst",
            "pad": dot_view["graph"]["pad"],
        }
    )

    neato_node_attrs = format_dot_attrs(dot_view["node"])

    with open(dot_file, "w", encoding="utf-8") as f:

        f.write(f'digraph {dot_view["name"]} {{\n')

        f.write(f"graph [{neato_graph_attrs}];\n")

        f.write(f"node [{neato_node_attrs}];\n\n")

        for node_id, node in neato_model["nodes"].items():

            node_attrs = format_dot_attrs(node["view"])

            f.write(
                f'"{node_id}" '
                f'[label="{node["label"]}", '
                f'pos="{node["pos"]}!", '
                f'{node_attrs}];\n'
            )

        f.write("\n")

        for edge in neato_model["edges"]:

            edge_attrs = format_dot_attrs(edge["view"])

            if edge_attrs:
                f.write(
                    f'"{edge["source"]}" -> "{edge["target"]}" '
                    f'[{edge_attrs}];\n'
                )
            else:
                f.write(
                    f'"{edge["source"]}" -> "{edge["target"]}";\n'
                )

        f.write("}\n")


def run_neato(dot_file, svg_file):
    """Run neato with -n to fix node positions and only route edges.

    -n tells neato: use the pos attributes as given, do not run
    the spring-model layout, only compute edge paths.
    """

    subprocess.run(
        [
            "neato",
            "-n",
            "-Tsvg",
            dot_file,
            "-o",
            svg_file,
        ],
        check=True,
    )


def render_grid_svg(
    graph,
    resolved_layout,
    dot_file,
    svg_file,
    grid_experiment,
):
    """Render the grid view via neato with explicit node positions.

    The grid_experiment parameter is retained for signature
    compatibility but is not used in the neato path.
    Visual enhancements (domain bands, cluster outlines, tier
    labels) will be added here as SVG post-processing.
    """

    neato_model = build_neato_model(
        graph,
        resolved_layout,
    )

    write_neato_dot(
        neato_model,
        dot_file,
    )

    run_neato(
        dot_file,
        svg_file,
    )

    # TODO: SVG post-processing — domain background bands,
    # cluster outlines, tier column headers, legend.


rows = load_data(input_file)

graph = build_graph(rows)

graph = apply_view(graph)

resolved_layout = resolve_layout(
    graph,
    layout
)

render_text(
    graph,
    resolved_layout,
    terminal_file
)

render_simple_svg(
    graph,
    resolved_layout,
    simple_dot_file,
    simple_svg_file
)

render_grid_svg(
    graph,
    resolved_layout,
    grid_dot_file,
    grid_svg_file,
    grid_experiment
)

