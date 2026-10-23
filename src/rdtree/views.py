"""View logic on top of the canonical graph: styling, hiding
domains, highlighting (module / domain / path / chain) and
dimming. Nothing here changes what the graph says.
"""

from collections import defaultdict

from . import settings
from .util import blend_to_white, darken_color


def or_group_color(or_group_id):

    return settings.or_colors[
        or_group_id % len(settings.or_colors)
    ]


def apply_view(graph):

    for tech_id, node in graph["nodes"].items():

        category = node["category"]

        node["view"] = settings.node_views.get(
            category,
            settings.node_views["DEFAULT"]
        ).copy()

        # Domain colour coding: nodes use the same colours
        # as cluster backgrounds so domain membership is
        # visible without cluster boxes (neato renderer).
        node["view"]["fillcolor"] = settings.domain_colors.get(
            node["domain"],
            settings.DEFAULT_DOMAIN_COLOR
        )

        # Make the border visible against the coloured fill.
        # Category shape already distinguishes node types;
        # penwidth distinguishes KEYSTONE / RCENTRE.
        node["view"]["color"] = "#555555"

    for domain, domain_data in graph["domains"].items():

        for cluster, cluster_data in domain_data["clusters"].items():

            cluster_data["view"] = settings.cluster_view.copy()
            domain_color = settings.domain_colors.get(domain)
            cluster_data["view"]["fillcolor"] = (
                darken_color(domain_color, settings.CLUSTER_DARKEN_FACTOR)
                if domain_color
                else settings.DEFAULT_DOMAIN_COLOR
            )

    for edge in graph["edges"]:

        if edge["type"] == "AND":

            edge["view"] = settings.edge_views["AND"].copy()

        elif edge["type"] == "OR":

            edge["view"] = settings.edge_views["OR"].copy()
            edge["view"]["color"] = or_group_color(
                edge["or_group_id"]
            )

        else:

            raise ValueError(
                f"Unknown edge type '{edge['type']}'"
            )

    return graph


def apply_hide_domain(graph, domain):
    """Hide all nodes in domain from all renderers.

    Sets visible=False before layout so hidden nodes are excluded
    from position calculation and do not appear in any output.
    """

    for node in graph["nodes"].values():
        if node["domain"] == domain:
            node["view"]["visible"] = False


def find_chain_ancestors(graph, target_id):
    """Return target_id and every prerequisite node recursively.

    Traverses dependency edges backwards from target_id, following
    both AND and OR edges. The result is the full set of nodes a
    player could need to research before reaching target_id.
    """

    if target_id not in graph["nodes"]:
        raise ValueError(
            f"Chain target '{target_id}' not found in graph"
        )

    # Build reverse edge map: target -> {sources}.
    # A cluster endpoint stands for all of its members: every member
    # of a target cluster has the sources as prerequisites, and any
    # member of a source cluster can be the prerequisite.
    reverse_edges = defaultdict(set)

    for edge in graph["edges"]:
        for dst in edge["target"]["members"]:
            reverse_edges[dst].update(edge["source"]["members"])

    visited = {target_id}
    queue = [target_id]

    while queue:
        node_id = queue.pop()
        for src in reverse_edges[node_id]:
            if src not in visited:
                visited.add(src)
                queue.append(src)

    return visited


def get_highlighted_nodes(graph, args):
    """Return the set of node IDs to highlight for the active view.

    Full view: all nodes.
    Module:    nodes whose module field matches filter_value.
    Domain:    nodes whose domain field matches filter_value.
    Chain:     target node and all its recursive prerequisites.
    """

    view = args.view
    value = args.filter_value

    if view == "full" or value is None:
        return {
            tid for tid, node in graph["nodes"].items()
            if node["view"].get("visible", True)
        }

    if view == "module":
        return {
            tid
            for tid, node in graph["nodes"].items()
            if node["module"] == value
            and node["view"].get("visible", True)
        }

    if view == "domain":
        return {
            tid
            for tid, node in graph["nodes"].items()
            if node["domain"] == value
            and node["view"].get("visible", True)
        }

    if view == "path":
        # path_items is a dict of {path_name: [node_ids]}, built
        # during graph construction from the Path column. A node
        # can belong to multiple paths (comma-separated in the ODS).
        return {
            tid
            for tid in graph["path_items"].get(value, [])
            if graph["nodes"][tid]["view"].get("visible", True)
        }

    if view == "chain":
        return find_chain_ancestors(graph, value)

    raise ValueError(f"Unknown view type '{view}'")


def apply_view_filter(graph, highlighted, dim_mode):
    """Apply highlighting and dimming to node and edge views.

    highlighted: set of node IDs to keep at full brightness.
    dim_mode:
      "grey" — flat grey fill and border, grey label text.
      "fade" — domain colour washed out toward white.
      "none" — node marked invisible; excluded from all output.

    Edges where both endpoints are highlighted are kept unchanged.
    All other edges are greyed out (or hidden for dim_mode 'none').
    """

    for tech_id, node in graph["nodes"].items():

        if not node["view"].get("visible", True):
            continue

        if tech_id in highlighted:
            continue

        if dim_mode == "none":
            node["view"]["visible"] = False

        elif dim_mode == "grey":
            grey = settings.dim_config["grey"]
            node["view"]["fillcolor"] = grey["fillcolor"]
            node["view"]["color"]     = grey["color"]
            node["view"]["fontcolor"] = grey["fontcolor"]

        elif dim_mode == "fade":
            fade = settings.dim_config["fade"]
            domain_color = settings.domain_colors.get(node["domain"])
            node["view"]["fillcolor"] = (
                blend_to_white(domain_color, factor=fade["blend"])
                if domain_color
                else fade["unknown_fill"]
            )
            node["view"]["color"]     = fade["color"]
            node["view"]["fontcolor"] = fade["fontcolor"]

    def lit(endpoint):
        """A cluster endpoint counts as highlighted if any member is."""
        return any(m in highlighted for m in endpoint["members"])

    for edge in graph["edges"]:

        if lit(edge["source"]) and lit(edge["target"]):
            continue

        if dim_mode == "none":
            # Edges to removed nodes are automatically excluded
            # in build_neato_model() / build_graphviz_model()
            # since their endpoints won't be in the node dict.
            # Mark them invisible as a belt-and-braces measure
            # for the simple renderer's write_dot_edges().
            edge["view"]["style"] = "invis"

        else:
            # Retain original style (solid/dashed) but grey the colour.
            edge["view"]["color"]  = settings.dim_config[dim_mode]["edge_color"]
            edge["view"]["weight"] = 1
