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


def load_data(input_file):

    rows = []

    with open(input_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            rows.append(row)

    return rows


def process_dependency(dep, target, or_color_index, graph):

    if not dep:
        return or_color_index

    parts = [d.strip() for d in dep.split('|') if d.strip()]

    # OR group
    if len(parts) > 1:
        color = or_colors[or_color_index % len(or_colors)]
        or_color_index += 1

        for p in parts:
            graph["edges"].append((p, target, "dashed", color))

    # single AND
    else:
        graph["edges"].append((parts[0], target, "solid", "black"))

    return or_color_index


def process_path(path, tech_id, graph):

    if not path:
        return

    parts = [p.strip() for p in path.split(',') if p.strip()]

    for p in parts:
        graph["path_items"][p].append(tech_id)


def build_graph(rows):
    # create tiers, domains, domain_tier_map, edges, etc.
    graph = {
        "tiers": defaultdict(list),
        "domains": {},
        "clusters": {},
        "domain_tier_map": defaultdict(list),
        "node_to_cluster": {},
        "modules": defaultdict(list),
        "path_items": defaultdict(list),
        "nodes": {},
        "edges": []
    }

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

        if cluster not in graph["clusters"]:
            graph["clusters"][cluster] = {
                "domain_code": domain_code,
                "domain": domain,
                "tier": tier,
                "label": f"{domain} - Tier {tier}",
            }

        if category == "DUMMY":
            label = ""
            graph["node_to_cluster"][tech_id] = f"cluster_{cluster}"
        else:
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
            "view": {}
        }

        graph["tiers"][tier].append(tech_id)

        graph["modules"][module].append(tech_id)

        graph["domain_tier_map"][(domain, tier)].append((tech_id, label, category))

        if domain not in graph["domains"]:
            graph["domains"][domain] = []

        graph["domains"][domain].append((tech_id, label))

        process_path(path, tech_id, graph)

        or_color_index = process_dependency(dep1, tech_id, or_color_index, graph)
        or_color_index = process_dependency(dep2, tech_id, or_color_index, graph)
        or_color_index = process_dependency(dep3, tech_id, or_color_index, graph)
        or_color_index = process_dependency(dep4, tech_id, or_color_index, graph)

    return graph


def apply_view(graph):

    for tech_id, node in graph["nodes"].items():

        category = node["category"]

        if category == "DUMMY":
            node["view"] = {
                "style": "invis",
                "width": 0,
                "height": 0,
            }

        elif category == "KEYSTONE":
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

    return graph


def write_dot(graph, output_file):

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("digraph TechTree {\n")
        f.write("rankdir=LR;\n")
#        f.write("splines=ortho;\n")
        f.write("splines=polyline;\n")
        f.write("compound=true;\n")
        f.write("clusterrank=local;\n")
        f.write("newrank=true;\n")

        f.write("""
            graph [
                pad=0.5,
                nodesep=0.6,
                ranksep=3.5
                ];
            """)

        f.write("""
            node [
                shape=box,
                width=3.5,
                height=1.0,
                fixedsize=true,
                fontsize=10
                ];
            """)

        # Domain together with tiers combined to clusters and place node within
        for cluster, cluster_data in graph["clusters"].items():

            cluster_name = f'cluster_{cluster}'

            f.write(f'subgraph {cluster_name} {{\n')
            f.write(f'label="{cluster_data["label"]}";\n')

            # Setting the colors of the nodes
            domain = cluster_data["domain"]
            color = domain_colors.get(domain, "black")
            f.write(f'fillcolor="{color}"; style="rounded,filled,dashed";\n')
            f.write(f'color="blue";\n')
            f.write(f'penwidth=1.5;\n')
            f.write('margin=30;\n')

            nodes = graph["domain_tier_map"][
                (cluster_data["domain"], cluster_data["tier"])
            ]

            for tech_id, label, category in nodes:

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

               # f.write(f'"{tech_id}" [label="{graph["nodes"][tech_id]["label"]}", {graph["nodes"][tech_id]["view"]}];\n')
               # if category == "DUMMY":
               #     f.write(f'"{tech_id}" [style=invis, width=0, height=0, label=""];\n')
               #     graph["node_to_cluster"][tech_id] = cluster_name
               # else:
               #     if category == "KEYSTONE":
               #         f.write(f'"{tech_id}" [label="{label}", shape=doubleoctagon, penwidth=2];\n')
               #     else:
               #         if category == "RCENTER":
               #             f.write(f'"{tech_id}" [label="{label}", shape=doublecircle, penwidth=2];\n')
               #         else:
               #             if category == "OIL":
               #                 f.write(f'"{tech_id}" [style="rounded,filled,dotted,bold", color="#fff4bc", label="{label}", penwidth=2];\n')
               #             else:
               #                 if category == "NUCLEAR":
               #                      f.write(f'"{tech_id}" [style="rounded,filled,dotted,bold", color="#f2f8ff", label="{label}", penwidth=2];\n')
               #                  else:
               #                      if category == "OCCULTISM":
               #                          f.write(f'"{tech_id}" [style="rounded,filled,dotted,bold", color="#ffeff6", label="{label}", penwidth=2];\n')
               #                      else:
               #                          if domain == "Programs":
               #                              f.write(f'"{tech_id}" [style="rounded,filled,bold", color="#ffe599", label="{label}"];\n')
               #                          else:
               #                              f.write(f'"{tech_id}" [style="rounded,filled", color="#fffdf2", label="{label}"];\n')

            f.write("}\n")

        # Tier alignment of nodes overall.
        for t, node_ids in graph["tiers"].items():
            f.write("{ rank=same; " + " ".join(f'"{n}"' for n in node_ids) + "; }\n")

        # Edges
        for src, dst, style, color in graph["edges"]:
            attrs = []

            attrs.append(f'style={style}')
            attrs.append(f'color="{color}"')
            attrs.append('weight=2')

            # Attach to clusters if nodes are dummy or cross clusters
            if src in graph["node_to_cluster"]:
                attrs.append(f'ltail={graph["node_to_cluster"][src]}')
            if dst in graph["node_to_cluster"]:
                attrs.append(f'lhead={graph["node_to_cluster"][dst]}')

            attr_str = ", ".join(attrs)
            f.write(f'"{src}" -> "{dst}" [{attr_str}];\n')

        f.write("}\n")



rows = load_data(input_file)

graph = build_graph(rows)

graph = apply_view(graph)

write_dot(graph, output_file)





