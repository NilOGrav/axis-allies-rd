"""Axis & Allies R&D tech tree generator (command line).

Reads the Tech List CSV and writes the text, simple and grid views.
Everything about presentation and file locations is in the config
file (tech_tree.toml). See README.md and the architecture picture in
rdtree/__init__.py.
"""

import argparse
import os
import sys

from rdtree import settings
from rdtree.data import build_graph, check_domain_config, load_data
from rdtree.layout import resolve_layout
from rdtree.output import output_files, resolve_targets
from rdtree.render_dot import render_simple_svg
from rdtree.render_grid import render_grid_svg
from rdtree.render_text import render_text
from rdtree.views import (
    apply_hide_domain,
    apply_view,
    apply_view_filter,
    get_highlighted_nodes,
)

CONFIG_FILE_NAME = "tech_tree.toml"


def parse_args(argv=None):
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Axis & Allies R&D Tech Tree Generator"
    )

    parser.add_argument(
        "--file",
        default=None,
        metavar="CSV",
        help=(
            "Tech List CSV to read. Default: paths.tech_list from "
            "the config file."
        ),
    )

    parser.add_argument(
        "--config",
        default=None,
        metavar="FILE",
        help=(
            "TOML config file: domain order and colours, layout, "
            "styling and input/output paths. "
            "Default: tech_tree.toml next to this script."
        ),
    )

    # --- View ---
    parser.add_argument(
        "--view",
        choices=["full", "module", "domain", "path", "chain"],
        default="full",
        help=(
            "View type: full (default), module, domain, path, or chain. "
            "Use --filter to specify the value."
        ),
    )
    parser.add_argument(
        "--filter",
        dest="filter_value",
        default=None,
        metavar="VALUE",
        help=(
            "Value for --view: module name (NUCLEAR), domain name "
            "(Air), or node ID for chain view (P.9.NU)."
        ),
    )
    parser.add_argument(
        "--dim",
        choices=["grey", "fade", "none"],
        default="grey",
        help=(
            "How to display non-highlighted nodes: grey (flat grey), "
            "fade (washed-out domain colour), none (remove entirely). "
            "Default: grey."
        ),
    )

    # --- Domain toggles ---
    parser.add_argument(
        "--hide-domain",
        action="append",
        default=None,
        metavar="NAME",
        help=(
            "Exclude all nodes of this domain from every output. "
            "May be given more than once."
        ),
    )

    # --- Output suppression ---
    parser.add_argument(
        "--notxt",
        action="store_true",
        help="Skip text file output.",
    )
    parser.add_argument(
        "--nodot",
        action="store_true",
        help="Skip writing DOT files (both renderers).",
    )
    parser.add_argument(
        "--nosvg",
        action="store_true",
        help="Skip SVG generation (both renderers).",
    )
    parser.add_argument(
        "--nosimple",
        action="store_true",
        help="Skip the simple Graphviz dot renderer entirely.",
    )
    parser.add_argument(
        "--nogrd",
        action="store_true",
        help="Skip the grid neato renderer entirely.",
    )

    return parser.parse_args(argv)


def main(argv=None):

    args = parse_args(argv)

    config_path = args.config or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        CONFIG_FILE_NAME,
    )

    settings.load(config_path)
    print(f"Config: {config_path}")

    csv_path = args.file or settings.paths["tech_list"]

    if not os.path.isfile(csv_path):
        raise SystemExit(f"Tech List not found: {csv_path}")

    print(f"Input:  {csv_path}")

    files = output_files(args)

    rows = load_data(csv_path)

    graph = build_graph(rows)

    check_domain_config(graph, settings.domain_order)

    graph = apply_view(graph)

    # Pre-layout domain toggles (must run before resolve_layout so
    # hidden nodes are excluded from position calculation).
    for domain_name in args.hide_domain or []:
        if domain_name not in graph["domains"]:
            raise SystemExit(
                f"--hide-domain: no domain '{domain_name}' in the data. "
                f"Available: {', '.join(graph['domains'])}"
            )
        apply_hide_domain(graph, domain_name)

    resolved_layout = resolve_layout(graph, settings.layout)

    # ── Text output ──────────────────────────────────────────────
    if not args.notxt:
        render_text(
            graph,
            resolved_layout,
            files["text"],
        )

    # ── Simple renderer (always full view, unaffected by --view) ─
    if not args.nosimple:
        targets = resolve_targets(
            files["simple_dot"], files["simple_svg"], args
        )
        if targets:
            dot_path, svg_path, temp_files = targets
            try:
                render_simple_svg(
                    graph,
                    resolved_layout,
                    dot_path,
                    svg_path,
                )
            finally:
                for temp_file in temp_files:
                    os.remove(temp_file)

    # ── Apply view filter — grid renderer only ───────────────────
    # Runs after the simple renderer so the simple SVG is never
    # affected by --view / --dim / --filter flags.
    highlighted = None

    if args.view != "full":
        highlighted = get_highlighted_nodes(graph, args)
        apply_view_filter(graph, highlighted, args.dim)

    # ── Grid renderer (filtered if --view is set) ────────────────
    if not args.nogrd:
        targets = resolve_targets(
            files["grid_dot"], files["grid_svg"], args
        )
        if targets:
            dot_path, svg_path, temp_files = targets
            try:
                render_grid_svg(
                    graph,
                    resolved_layout,
                    dot_path,
                    svg_path,
                    {"highlighted": highlighted, "dim": args.dim},
                )
            finally:
                for temp_file in temp_files:
                    os.remove(temp_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
