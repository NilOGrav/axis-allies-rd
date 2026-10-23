"""Where the output files go, and which of them are written."""

import os
import tempfile

from . import settings


def output_suffix(args):
    """Build a filename suffix that reflects the active view filter."""

    if args.view == "full":
        return ""

    value = (args.filter_value or "unknown").lower()
    # Sanitise for use in file names.
    for char in [".", " ", "&", "/", "\\"]:
        value = value.replace(char, "_")
    value = value.strip("_")

    return f"_{args.view}_{value}"


def output_files(args):
    """The five output files of one run, inside the configured
    directories. Only the grid files carry the view suffix: the simple
    view always shows the full tree, whatever --view says."""

    suffix = output_suffix(args)
    paths = settings.paths

    return {
        "text": os.path.join(paths["txt_dir"], "tech_tree.txt"),
        "simple_dot": os.path.join(
            paths["dot_dir"], "tech_tree_simple.dot"),
        "simple_svg": os.path.join(
            paths["svg_dir"], "tech_tree_simple.svg"),
        "grid_dot": os.path.join(
            paths["dot_dir"], f"tech_tree_grid{suffix}.dot"),
        "grid_svg": os.path.join(
            paths["svg_dir"], f"tech_tree_grid{suffix}.svg"),
    }


def resolve_targets(dot_name, svg_name, args):
    """Resolve where one renderer writes, honouring --nodot/--nosvg.

    Returns (dot_path, svg_path, temp_files), or None when both
    outputs are suppressed and there is nothing to produce.
    svg_path None means: stop after writing the DOT file.
    Graphviz needs the DOT file as input, so with --nodot it is
    written to a temporary file that is removed afterwards.
    Output directories are created when they do not exist.
    """

    if args.nodot and args.nosvg:
        return None

    temp_files = []

    if args.nodot:
        handle, dot_path = tempfile.mkstemp(suffix=".dot")
        os.close(handle)
        temp_files.append(dot_path)
    else:
        dot_path = dot_name
        os.makedirs(os.path.dirname(dot_path), exist_ok=True)

    svg_path = None if args.nosvg else svg_name

    if svg_path:
        os.makedirs(os.path.dirname(svg_path), exist_ok=True)

    return dot_path, svg_path, temp_files
