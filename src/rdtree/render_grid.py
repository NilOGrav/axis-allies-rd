"""Grid renderer: every node is pinned to its virtual-grid
position and neato -n only routes the edges. A dependency on a
whole cluster attaches to the edge of the cluster's background
box. The boxes themselves are added by svg_postprocess.
"""

import re
import subprocess

from . import settings
from .render_dot import format_dot_attrs
from .svg_postprocess import add_cluster_boxes_to_svg
from .util import blend_to_white, darken_color


def grid_geometry():
    """Grid spacing and node size in points (72 pt = 1 inch)."""

    return {
        "col_spacing": (
            settings.dot_view["node"]["width"] + settings.dot_view["graph"]["ranksep"]
        ) * 72,
        "row_spacing": (
            settings.dot_view["node"]["height"] + settings.dot_view["graph"]["nodesep"]
        ) * 72,
        "node_w": settings.dot_view["node"]["width"] * 72,
        "node_h": settings.dot_view["node"]["height"] * 72,
    }


def build_neato_model(graph, resolved_layout, boxes):
    """Build a neato-compatible model from the canonical graph.

    Unlike the dot model:
    - No subgraph clusters (neato ignores them anyway)
    - Every visible node gets a pos="x,y!" from the virtual grid
    - X. cluster proxy nodes are excluded (not visible)
    - ltail/lhead cluster routing is dropped
    - A dependency on a whole cluster is routed to an invisible
      anchor point on the edge of that cluster's background box
      (left edge when entering the cluster, right edge when leaving
      it, at the vertical middle), not to one of its nodes. Edges
      between real nodes go directly between them.

    Coordinates are in points (72pt = 1 inch), derived from the
    same dot_view width/height/ranksep/nodesep values used by the
    simple renderer, so horizontal spacing matches.
    """

    geometry = grid_geometry()

    col_spacing = geometry["col_spacing"]
    row_spacing = geometry["row_spacing"]

    # --- Nodes ---

    # RCENTRE nodes are rendered at 2× height, centred between
    # their virtual row and the reserved row below it.
    # calculate_node_positions() already advances 2 rows for each
    # RCENTRE, so subsequent nodes in the same cluster naturally
    # start below the full height of the research centre box.
    rcentre_height = (
        2 * settings.dot_view["node"]["height"]
        + settings.dot_view["graph"]["nodesep"]
    )

    neato_nodes = {}

    for tech_id, node in graph["nodes"].items():

        if not node["view"].get("visible", True):
            continue

        position = resolved_layout["nodes"].get(tech_id)

        if position is None:
            continue

        x = position["column"] * col_spacing

        node_view = {
            k: v
            for k, v in node["view"].items()
            if k != "visible"
        }

        if node["category"] == "RCENTRE":
            # Centre shifted half a row down to sit in the middle
            # of the 2 virtual rows reserved for this node.
            y = -(position["row"] + 0.5) * row_spacing
            node_view["height"] = rcentre_height
            node_view["width"] = settings.dot_view["node"]["width"]
            node_view["fixedsize"] = True
        else:
            y = -position["row"] * row_spacing

        neato_nodes[tech_id] = {
            "id": tech_id,
            "label": node["label"],
            "pos": f"{x:.1f},{y:.1f}",
            "view": node_view,
        }

    # --- Cluster anchors and edges ---

    boxes_by_cluster = {box["cluster"]: box for box in boxes}
    anchors = {}

    def endpoint_id(endpoint, entering):
        """Neato node id an edge should attach to, or None if that
        end is not drawn (hidden node, or cluster without a box)."""

        cluster = endpoint.get("cluster")

        if cluster is None:
            node_id = endpoint["graph_node"]
            return node_id if node_id in neato_nodes else None

        box = boxes_by_cluster.get(cluster)

        if box is None:
            return None

        side = "L" if entering else "R"
        anchor_id = f"__anchor_{box['id']}_{side}"

        if anchor_id not in anchors:
            x = box["left"] if entering else box["left"] + box["width"]
            y = -(box["top"] + box["height"] / 2)
            anchors[anchor_id] = {"pos": f"{x:.1f},{y:.1f}"}

        return anchor_id

    neato_edges = []
    seen = set()

    for edge in graph["edges"]:

        source = endpoint_id(edge["source"], entering=False)
        target = endpoint_id(edge["target"], entering=True)

        if source is None or target is None:
            continue

        key = (source, target)
        if key in seen:
            continue
        seen.add(key)

        view = edge["view"].copy()

        # An edge leaving a whole cluster means "any one of its
        # nodes": draw it like an OR edge. Edges entering a cluster
        # ("every node requires this") keep their normal style.
        # Hidden (invisible) edges stay hidden.
        if (
            edge["source"].get("cluster") is not None
            and edge["type"] == "AND"
            and view.get("style") != "invis"
        ):
            view["style"] = settings.edge_views["ANY"]["style"]

        neato_edges.append(
            {
                "source": source,
                "target": target,
                "view": view,
            }
        )

    return {
        "nodes": neato_nodes,
        "anchors": anchors,
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
            "pad": settings.dot_view["graph"]["pad"],
        }
    )

    neato_node_attrs = format_dot_attrs(settings.dot_view["node"])

    with open(dot_file, "w", encoding="utf-8") as f:

        f.write(f'digraph {settings.dot_view["name"]} {{\n')

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

        for anchor_id, anchor in neato_model["anchors"].items():

            f.write(
                f'"{anchor_id}" '
                f'[label="", shape=point, width=0.02, height=0.02, '
                f'fixedsize=true, style=invis, '
                f'pos="{anchor["pos"]}!"];\n'
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


def cluster_row_span(graph, resolved_layout, node_ids):
    """First and last virtual row occupied by a set of laid-out nodes.

    An RCENTRE occupies two rows. Uses the positions fixed at layout
    time, so the result does not change when a view filter hides
    nodes afterwards. Returns None if none of the nodes was placed.
    """

    rows = []

    for tech_id in node_ids:

        position = resolved_layout["nodes"].get(tech_id)

        if position is None:
            continue

        rows.append(position["row"])

        if graph["nodes"][tech_id]["category"] == "RCENTRE":
            rows.append(position["row"] + 1)

    if not rows:
        return None

    return min(rows), max(rows)


def domain_band_rows(graph, resolved_layout):
    """Height in rows of the largest cluster per domain, measured
    over the configured band tiers only."""

    first_tier = settings.config["postprocess"]["band_tiers_from"]
    last_tier = settings.config["postprocess"]["band_tiers_to"]

    band_rows = {}

    for domain, domain_data in graph["domains"].items():

        biggest = 0

        for cluster in domain_data["clusters"].values():

            span = cluster_row_span(
                graph, resolved_layout, cluster["nodes"]
            )

            if span is None:
                continue

            if not first_tier <= int(cluster["tier"]) <= last_tier:
                continue

            biggest = max(biggest, span[1] - span[0] + 1)

        band_rows[domain] = biggest

    return band_rows


def cluster_box_colors(domain, cluster, dimmed, dim_mode):
    """(fill, stroke) of a cluster box.

    Normal boxes use exactly the colours of the simple renderer.
    In a filtered view, clusters without any highlighted node are
    dimmed the same way as their nodes, with the fill kept slightly
    darker than the node fill, as everywhere else.
    """

    if not dimmed:
        return cluster["view"]["fillcolor"], settings.cluster_view["color"]

    if dim_mode == "grey":
        grey = settings.dim_config["grey"]
        node_fill, stroke = grey["fillcolor"], grey["color"]
    else:
        fade = settings.dim_config["fade"]
        base = settings.domain_colors.get(domain)
        node_fill = (
            blend_to_white(base, factor=fade["blend"])
            if base
            else fade["unknown_fill"]
        )
        stroke = fade["color"]

    return darken_color(node_fill, settings.CLUSTER_DARKEN_FACTOR), stroke


def build_cluster_boxes(graph, resolved_layout, view_state=None):
    """Compute one background box per cluster.

    Coordinates are in the model's grid space (x grows right, y grows
    down, one row = row_spacing); the offset neato applied to the
    drawing is measured from the SVG later.

    - Clusters in the band tiers are as tall as the largest cluster
      of their domain in those tiers.
    - All other clusters are as tall as their own nodes.
    - Clusters whose nodes were all removed by a view filter get no
      box. Partly removed clusters keep their full footprint, so the
      grid looks the same in every view.
    """

    geometry = grid_geometry()
    margin = settings.cluster_view["margin"]

    band_from = settings.config["postprocess"]["band_tiers_from"]
    band_to = settings.config["postprocess"]["band_tiers_to"]
    band_rows = domain_band_rows(graph, resolved_layout)

    state = view_state or {}
    highlighted = state.get("highlighted")
    dim_mode = state.get("dim")

    boxes = []

    for domain, domain_data in graph["domains"].items():

        for cluster_key, cluster in domain_data["clusters"].items():

            members = [
                tid for tid in cluster["nodes"]
                if tid in resolved_layout["nodes"]
            ]

            if not members:
                continue

            if not any(
                graph["nodes"][tid]["view"].get("visible", True)
                for tid in members
            ):
                continue

            first_row, last_row = cluster_row_span(
                graph, resolved_layout, members
            )

            tier = int(cluster["tier"])

            if band_from <= tier <= band_to:
                last_row = max(
                    last_row, first_row + band_rows[domain] - 1
                )

            column = resolved_layout["nodes"][members[0]]["column"]

            dimmed = (
                highlighted is not None
                and not highlighted.intersection(members)
            )

            fill, stroke = cluster_box_colors(
                domain, cluster, dimmed, dim_mode
            )

            boxes.append({
                "id": re.sub(r"\W+", "_", f"cluster_{domain}_{tier}"),
                "title": f"{domain} - Tier {tier}",
                "cluster": (domain, cluster_key),
                "left": (
                    column * geometry["col_spacing"]
                    - geometry["node_w"] / 2 - margin
                ),
                "top": (
                    first_row * geometry["row_spacing"]
                    - geometry["node_h"] / 2 - margin
                ),
                "width": geometry["node_w"] + 2 * margin,
                "height": (
                    (last_row - first_row) * geometry["row_spacing"]
                    + geometry["node_h"] + 2 * margin
                ),
                "fill": fill,
                "stroke": stroke,
            })

    return boxes


def render_grid_svg(
    graph,
    resolved_layout,
    dot_file,
    svg_file,
    view_state=None,
):
    """Render the grid view: neato places and routes, then the
    cluster backgrounds are added to the SVG.

    svg_file=None stops after writing the DOT file.
    view_state carries {"highlighted": set | None, "dim": mode} so
    the cluster backgrounds can be dimmed like their nodes.
    """

    # The boxes come first: edges that enter or leave a whole
    # cluster are anchored on the edges of its box.
    boxes = build_cluster_boxes(graph, resolved_layout, view_state)

    neato_model = build_neato_model(
        graph,
        resolved_layout,
        boxes,
    )

    write_neato_dot(
        neato_model,
        dot_file,
    )

    if svg_file is None:
        return

    run_neato(
        dot_file,
        svg_file,
    )

    add_cluster_boxes_to_svg(svg_file, neato_model, boxes)
