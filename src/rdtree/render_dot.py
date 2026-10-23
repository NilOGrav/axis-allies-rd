"""Simple renderer: Graphviz dot lays the tree out itself, with
clusters as subgraphs. Always shows the full tree.
"""

from collections import defaultdict
import subprocess

from . import settings


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

    graph_attrs = format_dot_attrs(settings.dot_view["graph"])

    f.write(
        f"graph [{graph_attrs}];\n"
    )

    node_attrs = format_dot_attrs(settings.dot_view["node"])

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
            f'digraph {settings.dot_view["name"]} {{\n'
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


def run_graphviz(dot_file, svg_file):

    subprocess.run(
        ["dot", "-Tsvg", dot_file, "-o", svg_file],
        check=True
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

    if svg_file is None:
        return

    run_graphviz(
        dot_file,
        svg_file
    )
