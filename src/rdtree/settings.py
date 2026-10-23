"""Configuration, read from tech_tree.toml.

The TOML file is the single source of truth for everything about how
the tree is presented and where files live: domain order and colours,
layout parameters, node and edge styling, dimming for the view
filters, SVG post-processing and the input/output paths.

There are deliberately no built-in defaults. A missing setting is an
error that names the setting, so the file and the program cannot
drift apart unnoticed.

Call load(path) once. The values are then available as module
attributes, e.g. settings.dot_view or settings.domain_colors.
"""

import os
import re

from .util import warn

try:
    import tomllib  # Python 3.11+
except ImportError:  # pragma: no cover
    tomllib = None


HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")

# Top-level sections that exist. Anything else is reported as a typo.
SECTIONS = {
    "layout", "domains", "colors", "dim", "dot_view", "edge_views",
    "node_views", "cluster_view", "postprocess", "paths",
}

# Settings the program cannot work without. Other keys inside the
# style tables (dot_view.graph, node_views.*, ...) are passed through
# to Graphviz as they are, so any Graphviz attribute may be added.
REQUIRED_KEYS = [
    "layout.policy", "layout.row_offset", "layout.late_tiers_from",
    "domains",
    "colors.default_domain", "colors.cluster_darken", "colors.or_groups",
    "dim.grey.fillcolor", "dim.grey.color", "dim.grey.fontcolor",
    "dim.grey.edge_color",
    "dim.fade.blend", "dim.fade.unknown_fill", "dim.fade.color",
    "dim.fade.fontcolor", "dim.fade.edge_color",
    "dot_view.name", "dot_view.graph.pad", "dot_view.graph.nodesep",
    "dot_view.graph.ranksep", "dot_view.node.width", "dot_view.node.height",
    "edge_views.AND", "edge_views.OR", "edge_views.ANY.style",
    "node_views.DEFAULT", "node_views.CLUSTER",
    "cluster_view.color", "cluster_view.margin",
    "postprocess.band_tiers_from", "postprocess.band_tiers_to",
    "postprocess.corner_radius",
    "paths.root", "paths.tech_list", "paths.txt_dir", "paths.svg_dir",
    "paths.dot_dir",
]

# Loaded values (set by load()).
config_file = None
config = None
layout = None
domain_order = None
domain_colors = None
DEFAULT_DOMAIN_COLOR = None
CLUSTER_DARKEN_FACTOR = None
or_colors = None
dim_config = None
dot_view = None
edge_views = None
node_views = None
cluster_view = None
paths = None


def _has(table, dotted_key):
    node = table
    for part in dotted_key.split("."):
        if not isinstance(node, dict) or part not in node:
            return False
        node = node[part]
    return True


def _validate(cfg, source):
    """Fail early, with a pointed message, on mistakes that would
    otherwise surface later as obscure errors."""

    missing = [key for key in REQUIRED_KEYS if not _has(cfg, key)]

    if missing:
        raise SystemExit(
            f"{source}: missing required setting(s): "
            f"{', '.join(missing)}"
        )

    post = cfg["postprocess"]

    if not (
        isinstance(post["band_tiers_from"], int)
        and isinstance(post["band_tiers_to"], int)
        and post["band_tiers_from"] <= post["band_tiers_to"]
    ):
        raise SystemExit(
            f"{source}: [postprocess] band_tiers_from and "
            f"band_tiers_to must be integers with from <= to."
        )

    seen = set()

    for index, entry in enumerate(cfg["domains"], start=1):

        if (
            not isinstance(entry, dict)
            or "name" not in entry
            or "color" not in entry
        ):
            raise SystemExit(
                f"{source}: [[domains]] entry {index} needs both "
                f"'name' and 'color'."
            )

        name = entry["name"]

        if name in seen:
            raise SystemExit(
                f"{source}: domain '{name}' is listed more than once."
            )
        seen.add(name)

        if not HEX_COLOR.match(str(entry["color"])):
            raise SystemExit(
                f"{source}: colour '{entry['color']}' for domain "
                f"'{name}' must be of the form #RRGGBB."
            )


def _resolve_paths(cfg, config_path):
    """Absolute paths. 'root' is relative to the config file, every
    other path is relative to root. Absolute paths are kept as they
    are."""

    base = os.path.dirname(os.path.abspath(config_path))
    root = os.path.normpath(os.path.join(base, cfg["paths"]["root"]))

    resolved = {"root": root}

    for key in ("tech_list", "txt_dir", "svg_dir", "dot_dir"):
        resolved[key] = os.path.normpath(
            os.path.join(root, cfg["paths"][key])
        )

    return resolved


def load(config_path):
    """Read and validate the config file and publish its values."""

    global config_file, config, layout, domain_order, domain_colors
    global DEFAULT_DOMAIN_COLOR, CLUSTER_DARKEN_FACTOR, or_colors
    global dim_config, dot_view, edge_views, node_views, cluster_view
    global paths

    if tomllib is None:
        raise SystemExit(
            "Reading the config file needs Python 3.11 or newer "
            "(tomllib)."
        )

    if not os.path.isfile(config_path):
        raise SystemExit(f"Config file not found: {config_path}")

    with open(config_path, "rb") as f:
        try:
            cfg = tomllib.load(f)
        except tomllib.TOMLDecodeError as error:
            raise SystemExit(f"Invalid config file {config_path}: {error}")

    for section in cfg:
        if section not in SECTIONS:
            warn(
                f"unknown config section '{section}' in {config_path} "
                f"is ignored"
            )

    _validate(cfg, config_path)

    config_file = config_path
    config = cfg

    domain_order = [entry["name"] for entry in cfg["domains"]]
    domain_colors = {
        entry["name"]: entry["color"] for entry in cfg["domains"]
    }

    DEFAULT_DOMAIN_COLOR = cfg["colors"]["default_domain"]
    CLUSTER_DARKEN_FACTOR = cfg["colors"]["cluster_darken"]
    or_colors = cfg["colors"]["or_groups"]
    dim_config = cfg["dim"]

    # The layout settings plus the domain order, which resolve_layout
    # reads from the same dictionary.
    layout = dict(cfg["layout"])
    layout["domain_order"] = domain_order

    dot_view = cfg["dot_view"]
    edge_views = cfg["edge_views"]
    node_views = cfg["node_views"]
    cluster_view = cfg["cluster_view"]

    paths = _resolve_paths(cfg, config_path)

    return config_path
