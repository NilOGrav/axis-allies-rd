import csv
from collections import defaultdict

# v7 - added OR and AND dependencies

input_file = "tech_tree.csv"
output_file = "tech_tree.dot"

#tiers = {str(i): [] for i in range(0, 9)}
tiers = defaultdict(list)

domains = {}

node_to_cluster = {}

edges = []

domain_tier_map = defaultdict(list)

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

or_color_index = 0


def process_dependency(dep, target):
    global or_color_index

    if not dep:
        return

    parts = [d.strip() for d in dep.split('|') if d.strip()]

    # OR group
    if len(parts) > 1:
        color = or_colors[or_color_index % len(or_colors)]
        or_color_index += 1

        for p in parts:
            edges.append((p, target, "dashed", color))

    # single AND
    else:
        edges.append((parts[0], target, "solid", "black"))


#def process_dependency(dep, target):
#    if not dep:
#        return
#
#    parts = [d.strip() for d in dep.split('|') if d.strip()]
#
#    # If multiple parts → OR
#    if len(parts) > 1:
#        for p in parts:
#            edges.append((p, target, "OR"))
#    else:
#        edges.append((parts[0], target, "AND"))

with open(input_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')

    for row in reader:
        tech_id = row["ID"].strip()
        name = row["Name"].strip()
        tier = row["Tier"].strip()
        domain = row["Domain"].strip()
#        node_type = row["Type"].strip()
        node_cat = row["Category"].strip()
        dep1 = row["DepGroup1"].strip()
        dep2 = row["DepGroup2"].strip()
        dep3 = row["DepGroup3"].strip()
        dep4 = row["DepGroup4"].strip()

        label = f"{tech_id}\\n{name}"

        tiers[tier].append(tech_id)

        domain_tier_map[(domain, tier)].append((tech_id, label, node_cat))

        if domain not in domains:
            domains[domain] = []
        domains[domain].append((tech_id, label))

        process_dependency(dep1, tech_id)
        process_dependency(dep2, tech_id)
        process_dependency(dep3, tech_id)
        process_dependency(dep4, tech_id)

with open(output_file, "w", encoding="utf-8") as f:
    f.write("digraph TechTree {\n")
    f.write("rankdir=LR;\n")
#    f.write("splines=ortho;\n")
    f.write("splines=polyline;\n")
    f.write("compound=true;\n")
    f.write("clusterrank=local;\n")
    f.write("newrank=true;\n")

    f.write("""
graph [
pad=0.5, 
nodesep=0.6, 
ranksep=3.5];
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
    for (domain, tier), nodes in domain_tier_map.items():
        cluster_name = f'cluster_{domain.replace(" ", "_")}_{tier}'

        f.write(f'subgraph {cluster_name} {{\n')
        f.write(f'label="{domain} - Tier {tier}";\n')
        color = domain_colors.get(domain, "black")
        f.write(f'fillcolor="{color}"; style="rounded,filled,dashed";\n')
        f.write(f'color="blue";\n')
        f.write(f'penwidth=1.5;\n')
        f.write('margin=30;\n')


        for tech_id, label, node_cat in nodes:
            if node_cat == "DUMMY":
                #ToDo: make the dummy items invisible
                f.write(f'"{tech_id}" [style=invis, width=0, height=0, label=""];\n')
                node_to_cluster[tech_id] = cluster_name
            else:
                if node_cat == "KEYSTONE":
                    f.write(f'"{tech_id}" [label="{label}", shape=doubleoctagon, penwidth=2];\n')
                else:
                    if node_cat == "OIL":
                        f.write(f'"{tech_id}" [style="rounded,filled,dotted,bold", color="#fff4bc", label="{label}", penwidth=2];\n')
                    else:
                        if node_cat == "NUCLEAR":
                            f.write(f'"{tech_id}" [style="rounded,filled,dotted,bold", color="#f2f8ff", label="{label}", penwidth=2];\n')
                        else:
                            if node_cat == "OCCULTISM":
                                f.write(f'"{tech_id}" [style="rounded,filled,dotted,bold", color="#ffeff6", label="{label}", penwidth=2];\n')
                            else:
                                if domain == "Programs":
                                    f.write(f'"{tech_id}" [style="rounded,filled,bold", color="#ffe599", label="{label}"];\n')
                                else:
                                    f.write(f'"{tech_id}" [style="rounded,filled", color="#fffdf2", label="{label}"];\n')

        f.write("}\n")

    # Tier alignment of nodes overall.
    for t, node_ids in tiers.items():
        f.write("{ rank=same; " + " ".join(f'"{n}"' for n in node_ids) + "; }\n")

    # Edges
    # ToDo: Group ORs by color for visual differentiation
    # ToDo: For dummy dependencies let the arrows connect to the cluster in stead of individual items

    for src, dst, style, color in edges:
        attrs = []

        attrs.append(f'style={style}')
        attrs.append(f'color="{color}"')
        attrs.append('weight=2')

        # Attach to clusters if nodes are dummy or cross clusters
        if src in node_to_cluster:
            attrs.append(f'ltail={node_to_cluster[src]}')
        if dst in node_to_cluster:
            attrs.append(f'lhead={node_to_cluster[dst]}')

        attr_str = ", ".join(attrs)
        f.write(f'"{src}" -> "{dst}" [{attr_str}];\n')



#    for src, dst, style in edges:
#        if style == "OR":
#            f.write(f'"{src}" -> "{dst}" [style=dashed, color="gray40", weight=1];\n')
#        else:
#            f.write(f'"{src}" -> "{dst}" [style=solid, weight=2];\n')

    f.write("}\n")
