import csv
from collections import defaultdict

input_file = "tech_tree_v51.csv"
output_file = "tech_tree_v51.dot"

#tiers = {str(i): [] for i in range(0, 9)}
tiers = defaultdict(list)
domains = {}

edges = []

domain_tier_map = defaultdict(list)

with open(input_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')

    for row in reader:
        tech_id = row["ID"].strip()
        name = row["Name"].strip()
        tier = row["Tier"].strip()
        domain = row["Domain"].strip()
        dep1 = row["Dependency1"].strip()
        dep2 = row["Dependency2"].strip()
        dep3 = row["Dependency3"].strip()
        dep4 = row["Dependency4"].strip()

        label = f"{tech_id}\\n{name}"

        tiers[tier].append(tech_id)

        domain_tier_map[(domain, tier)].append((tech_id, label))

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
    f.write("splines=ortho;\n")

    f.write("""
node [
shape=box,
width=3.2,
height=0.8,
fixedsize=true,
fontsize=10
];
""")

    # Tier clusters
#    for t in range(0, 9):
#        if t == 0:
#            f.write(f'subgraph cluster_t{t} {{ label="Tier {t}"; style=dashed; }}\n')
#        else:
#            f.write(f'subgraph cluster_t{t} {{ label="Tier {t}"; style=dotted; }}\n')

    # Domain clusters : together with tiers combine to clusters
#    for d, nodes in domains.items():
#        for t, nodes in tiers.items():
#            f.write(f'subgraph cluster_{d.replace(" ", "_")}_{t} {{\n')
#            f.write(f'label="{d} - Tier {t}";\n')
#            for tech_id in nodes:
#        for tech_id, label in nodes:
#                if d == domains.items():
#                    f.write(f'"{tech_id}" [label="{label}"];\n')
#            f.write("}\n")

    for (domain, tier), nodes in domain_tier_map.items():
        cluster_name = f'cluster_{domain.replace(" ", "_")}_{tier}'

        f.write(f'subgraph {cluster_name} {{\n')
        f.write(f'label="{domain} - Tier {tier}";\n')

        for tech_id, label in nodes:
            f.write(f'"{tech_id}" [label="{label}"];\n')

        f.write("}\n")

    # Tier alignment : of clusters in the same tiers, not nodes.
    for t, node_ids in tiers.items():
        f.write("{ rank=same; " + " ".join(f'"{n}"' for n in node_ids) + "; }\n")

    # Edges
    for src, dst in edges:
        f.write(f'"{src}" -> "{dst}";\n')

    f.write("}\n")
