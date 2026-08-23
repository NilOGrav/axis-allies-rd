import sys
import csv
from collections import defaultdict

input_file = sys.argv[1]
output_file = "tech_tree.dot"

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

or_colors = [
    "#e41a1c", "#377eb8", "#4daf4a",
    "#984ea3", "#ff7f00", "#ffff33",
    "#a65628", "#f781bf"
]

dot_view = {
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


def process_dependency(dep, target, or_color_index, graph):

    if not dep:
        return or_color_index

    parts = [d.strip() for d in dep.split('|') if d.strip()]

    # OR group
    if len(parts) > 1:
        color = or_colors[or_color_index % len(or_colors)]
        or_color_index += 1

    else:
        color = "black"

    for p in parts:

        # Dependency refers to a real technology node.
        if p in graph["nodes"]:
            src = p
            src_type = "node"
            src_id = p

        # Dependency refers to a cluster.
        elif p in graph["cluster_representatives"]:
            src = graph["cluster_representatives"][p]
            src_type = "cluster"
            src_id = p

        else:
            raise ValueError(
                f"Unknown dependency '{p}' for target '{target}'"
            )

        graph["edges"].append({
            "src": src,
            "dst": target,

            "view": {
                "style": "dashed" if len(parts) > 1 else "solid",
                "color": color,
                "weight": 2
            },

            "routing": {
                "source": routing_endpoint(src_type, src_id),
                "target": routing_endpoint("node", target)
            }
        })

    return or_color_index


def process_path(path, tech_id, graph):

    if not path:
        return

    parts = [p.strip() for p in path.split(',') if p.strip()]

    for p in parts:
        graph["path_items"][p].append(tech_id)


def build_graph(rows):

    # create tiers, domains, edges, etc.
    graph = create_graph()

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
            graph["domains"][domain] = {
                "domain_code": domain_code,
                "clusters": {}
            }

        if cluster not in graph["domains"][domain]["clusters"]:
            graph["domains"][domain]["clusters"][cluster] = {
                "tier": tier,
                "label": f"{domain} - Tier {tier}",
                "nodes": [],
                "view": {}
            }

        label = f"{tech_id}\\n{name}"

        graph["nodes"][tech_id] = {
            "name": name,
            "domain_code": domain_code,
            "domain": domain,
            "tier": tier,
            "cluster": cluster,
            "module": module,
            "category": category,
            "label": label,
            "path": path,
            "dependencies": [
                dep1,
                dep2,
                dep3,
                dep4
            ],
            "view": {}
        }

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
        graph["cluster_representatives"][cluster_id] = real_nodes[0]

    # Now that all nodes and cluster representatives exist,
    # construct the dependency edges.
    for tech_id, node in graph["nodes"].items():

        for dep in node["dependencies"]:

            or_color_index = process_dependency(
                dep,
                tech_id,
                or_color_index,
                graph
            )

    return graph


def apply_view(graph):

    for tech_id, node in graph["nodes"].items():

        category = node["category"]

        if category == "KEYSTONE":
            node["view"] = {
                "shape": "doubleoctagon",
                "style": "rounded,filled",
                "color": "#fffdf2",
                "penwidth": 2
            }

        elif category == "RCENTER":
            node["view"] = {
                "shape": "doublecircle",
                "style": "filled",
                "color": "#fffdf2",
                "penwidth": 2
            }

        elif category == "RESOURCE":
            node["view"] = {
                "shape": "box",
                "style": "rounded,filled,dotted,bold",
                "color": "#fffdf2",
                "penwidth": 1
            }

        else:
            node["view"] = {
                "shape": "box",
                "style": "rounded,filled",
                "color": "#fffdf2",
                "penwidth": 2
            }

    for domain, domain_data in graph["domains"].items():

        for cluster, cluster_data in domain_data["clusters"].items():

            # Setting the colors of the clusters
            cluster_data["view"] = {
                "fillcolor": domain_colors.get(domain, "black"),
                "style": "rounded,filled,dashed",
                "color": "blue",
                "penwidth": 1.5,
                "margin": 30
            }

    return graph

def apply_graphviz_routing(edge, attrs):

    routing = edge["routing"]

    source = routing["source"]
    target = routing["target"]

    if source["type"] == "cluster":
        attrs.append(
            f'ltail=cluster_{source["id"]}'
        )

    if target["type"] == "cluster":
        attrs.append(
            f'lhead=cluster_{target["id"]}'
        )

def write_dot(graph, output_file):

    with open(output_file, "w", encoding="utf-8") as f:

        f.write("digraph TechTree {\n")
        # f.write("rankdir=LR;\n")
        # f.write("splines=polyline;\n")
        # f.write("compound=true;\n")
        # f.write("clusterrank=local;\n")
        # f.write("newrank=true;\n")
        #
        # f.write("""
        #     graph [
        #         pad=0.5,
        #         nodesep=0.6,
        #         ranksep=7.0
        #         ];
        #     """)
        #
        # f.write("""
        #     node [
        #         shape=box,
        #         width=3.5,
        #         height=1.0,
        #         fixedsize=true,
        #         fontsize=10
        #         ];
        #     """)


        # Global Graphviz view settings
        graph_attrs = []

        for key, value in dot_view["graph"].items():
            if isinstance(value, str):
                graph_attrs.append(f'{key}="{value}"')
            else:
                graph_attrs.append(f'{key}={str(value).lower() if isinstance(value, bool) else value}')

        f.write(
            "graph [\n    "
            + ",\n    ".join(graph_attrs)
            + "\n];\n"
        )

        node_attrs = []

        for key, value in dot_view["node"].items():
            if isinstance(value, str):
                node_attrs.append(f'{key}="{value}"')
            else:
                node_attrs.append(f'{key}={str(value).lower() if isinstance(value, bool) else value}')

        f.write(
            "node [\n    "
            + ",\n    ".join(node_attrs)
            + "\n];\n"
        )

        # Domain together with tiers combined to clusters and place node within
        for domain, domain_data in graph["domains"].items():

            for cluster, cluster_data in domain_data["clusters"].items():

                cluster_name = f'cluster_{cluster}'

                f.write(f'subgraph {cluster_name} {{\n')
                f.write(f'label="{cluster_data["label"]}";\n')

                f.write(f'fillcolor="{cluster_data["view"]["fillcolor"]}"; style="{cluster_data["view"]["style"]}";\n')
                f.write(f'color="{cluster_data["view"]["color"]}";\n')
                f.write(f'penwidth="{cluster_data["view"]["penwidth"]}";\n')
                f.write(f'margin="{cluster_data["view"]["margin"]}";\n')

                for tech_id in cluster_data["nodes"]:

                    node = graph["nodes"][tech_id]
                    view = node["view"]

                    view_attrs = []

                    for key, value in view.items():

                        if isinstance(value, str):
                            view_attrs.append(f'{key}="{value}"')
                        else:
                            view_attrs.append(f'{key}={value}')

                    attrs = ", ".join(view_attrs)

                    f.write(f'"{tech_id}" [label="{node["label"]}", {attrs}];\n')

                f.write("}\n")

        # Tier alignment of nodes overall.
        for t, node_ids in graph["tiers"].items():
            f.write("{ rank=same; " + " ".join(f'"{n}"' for n in node_ids) + "; }\n")

        # Edges
        for edge in graph["edges"]:

            src = edge["src"]
            dst = edge["dst"]

            # Edge presentation
            edge_view = edge["view"]

            attrs = []

            for key, value in edge_view.items():
                if isinstance(value, str):
                    attrs.append(f'{key}="{value}"')
                else:
                    attrs.append(f'{key}={value}')

            # Translate semantic routing into Graphviz routing.
            apply_graphviz_routing(edge, attrs)

            attr_str = ", ".join(attrs)

            f.write(
                f'"{src}" -> "{dst}" [{attr_str}];\n'
            )

        f.write("}\n")


rows = load_data(input_file)

graph = build_graph(rows)

graph = apply_view(graph)

write_dot(graph, output_file)





