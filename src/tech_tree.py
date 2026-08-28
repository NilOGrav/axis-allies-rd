import sys
import csv
import subprocess
from collections import defaultdict

input_file = sys.argv[1]
dot_file = "tech_tree.dot"
svg_file = "tech_tree.svg"


#                CANONICAL
#                  GRAPH
#                    │
#                load_data()
#                    │
#               build_graph()
#                    │
#    ┌───────────────┼────────────────┐
#    │               │                │
#  nodes           edges            domains
#    │               │                │
#    │          type / OR-ID          │
#    │               │                │
#    └───────────────┼────────────────┘
#                    ↓
#               apply_view()
#                    │
#     ┌──────────────┼──────────────┐
#     ↓              ↓              ↓
# node.view       edge.view     cluster.view
#     │              │              │
#     └──────────────┼──────────────┘
#                    ↓
#                write_dot()
#                    │
#            Graphviz translation
#                    │
#          routing → ltail/lhead
#                    ↓
#                   DOT
#                    ↓
#                   SVG


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

default_domain_color = "black"

or_colors = [
    "#e41a1c", "#377eb8", "#4daf4a",
    "#984ea3", "#ff7f00", "#ffff33",
    "#a65628", "#f781bf"
]

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
        "weight": 2,
    },

    "OR": {
        "style": "dashed",
        "weight": 2,
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


def create_graph():

    return {
        "tiers": defaultdict(list),
        "domains": {},
        "cluster_representatives": {},
        "modules": defaultdict(list),
        "path_items": defaultdict(list),
        "nodes": {},
        "edges": []
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
                default_domain_color
            )

    # for edge in graph["edges"]:
    #
    #     edge_type = edge["type"]
    #
    #     edge["view"] = edge_views[edge_type].copy()
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


def write_dot(graph, dot_file):

    with open(dot_file, "w", encoding="utf-8") as f:

        # Set name of graph
        f.write(f'digraph {dot_view["name"]} {{\n')

        # Global Graphviz view settings
        graph_attrs = format_dot_attrs(dot_view["graph"])

        f.write(
            f"graph [{graph_attrs}];\n"
        )

        node_attrs = format_dot_attrs(dot_view["node"])

        f.write(
            f"node [{node_attrs}];\n"
        )

        # Domain together with tiers combined to clusters and place node within
        for domain, domain_data in graph["domains"].items():

            for cluster, cluster_data in domain_data["clusters"].items():

                cluster_name = f'cluster_{cluster}'

                f.write(f'subgraph {cluster_name} {{\n')
                f.write(f'label="{cluster_data["label"]}";\n')

                cluster_attrs = format_dot_attrs(cluster_data["view"])

                f.write(
                    f'graph [{cluster_attrs}];\n'
                )

                for tech_id in cluster_data["nodes"]:

                    node = graph["nodes"][tech_id]
                    view = node["view"]

                    if not view.get("visible", True):
                        continue

                    attrs = format_dot_attrs(
                        {
                            key: value
                            for key, value in view.items()
                            if key != "visible"
                        }
                    )

                    f.write(
                        f'"{tech_id}" [label="{node["label"]}", {attrs}];\n'
                    )

                f.write("}\n")

        # Tier alignment of nodes overall.
        for t, node_ids in graph["tiers"].items():

            visible_nodes = [
                n
                for n in node_ids
                if graph["nodes"][n]["view"].get("visible", True)
            ]

            if visible_nodes:
                f.write(
                    "{ rank=same; "
                    + " ".join(f'"{n}"' for n in visible_nodes)
                    + "; }\n"
                )

        # Edges
        for edge in graph["edges"]:

            src = edge["source"]["graph_node"]
            dst = edge["target"]["graph_node"]

            # Edge presentation
            edge_view = edge["view"]

            attrs = []

            edge_view_attrs = format_dot_attrs(edge_view)

            if edge_view_attrs:
                attrs.append(edge_view_attrs)

            # Translate semantic routing into Graphviz routing.
            apply_graphviz_routing(edge, attrs)

            attr_str = ", ".join(attrs)

            f.write(
                f'"{src}" -> "{dst}" [{attr_str}];\n'
            )

        f.write("}\n")


def run_graphviz(dot_file, svg_file):

    subprocess.run(
        ["dot", "-Tsvg", dot_file, "-o", svg_file],
        check=True
    )


rows = load_data(input_file)

graph = build_graph(rows)

graph = apply_view(graph)

write_dot(graph, dot_file)

run_graphviz(dot_file, svg_file)

# TODO - post-processing SVG
