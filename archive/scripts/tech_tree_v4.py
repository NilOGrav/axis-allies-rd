import csv
from collections import defaultdict

input_file = "tech_tree_v51.csv"
output_file = "tech_tree_v51.dot"

#tiers = {str(i): [] for i in range(0, 9)}
tiers = defaultdict(list)
domains = {}

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
    "Help": "#eeeeee"
}

with open(input_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')

    for row in reader:
        tech_id = row["ID"].strip()
        name = row["Name"].strip()
        tier = row["Tier"].strip()
        domain = row["Domain"].strip()
        node_type = row["Type"].strip()
        dep1 = row["Dependency1"].strip()
        dep2 = row["Dependency2"].strip()
        dep3 = row["Dependency3"].strip()
        dep4 = row["Dependency4"].strip()

        label = f"{tech_id}\\n{name}"

        tiers[tier].append(tech_id)

        domain_tier_map[(domain, tier)].append((tech_id, label, node_type))

        if domain not in domains:
            domains[domain] = []
        domains[domain].append((tech_id, label))

        if dep1:
            for d in dep1.split(','):
                edges.append((d.strip(), tech_id))

        if dep2:
            for d in dep2.split(','):
                edges.append((d.strip(), tech_id))

        if dep3:
            for d in dep3.split(','):
                edges.append((d.strip(), tech_id))

        if dep4:
            for d in dep4.split(','):
                edges.append((d.strip(), tech_id))

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
width=3.2,
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
        f.write('margin=20;\n')


        for tech_id, label, node_type in nodes:
            if node_type == "Dummy":
                f.write(f'"{tech_id}" [style="rounded,dotted", color="gray", label="{label}"];\n')
            else:
                if node_type == "KEYSTONE":
                    f.write(f'"{tech_id}" [label="{label}", shape=doubleoctagon, penwidth=2];\n')
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
    for src, dst in edges:
        f.write(f'"{src}" -> "{dst}" [weight=1];\n')

    f.write("}\n")
