"""SVG post-processing of the grid renderer.

Neato only places nodes and routes edges. Everything that is
purely visual is added afterwards, directly in the SVG. At the
moment that is the cluster background (one box per domain/tier
cluster). Nothing here moves a node or an edge.
"""

import re
import statistics
import xml.etree.ElementTree as ET

from . import settings
from .util import warn

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def svg_tag(name):
    return f"{{{SVG_NS}}}{name}"


def svg_shape_bbox(group):
    """Bounding box (x0, y0, x1, y1) of the shapes in an SVG group."""

    xs, ys = [], []
    number = r"-?\d+(?:\.\d+)?"

    for child in group:

        tag = child.tag.split("}")[-1]

        if tag in ("path", "polygon", "polyline"):
            text = child.get("d") if tag == "path" else child.get("points")
            values = [float(v) for v in re.findall(number, text or "")]
            xs += values[0::2]
            ys += values[1::2]

        elif tag == "ellipse":
            cx, cy = float(child.get("cx")), float(child.get("cy"))
            rx, ry = float(child.get("rx")), float(child.get("ry"))
            xs += [cx - rx, cx + rx]
            ys += [cy - ry, cy + ry]

    if not xs:
        return None

    return min(xs), min(ys), max(xs), max(ys)


def measure_svg_offset(graph_group, neato_model):
    """Offset between model coordinates and SVG graph coordinates.

    Neato -n re-normalises the drawing so its bounding box starts at
    the origin, so model positions and SVG positions differ by a
    constant. It is measured from the drawn node shapes instead of
    being computed, so it also holds when a view filter has changed
    the bounding box. Returns (dx, dy, spread) or None; spread is the
    largest disagreement between nodes and should be ~0.
    """

    dxs, dys = [], []

    for group in graph_group.findall(svg_tag("g")):

        if group.get("class") != "node":
            continue

        title = group.find(svg_tag("title"))
        node = (
            neato_model["nodes"].get(title.text)
            if title is not None else None
        )
        bbox = svg_shape_bbox(group) if node else None

        if bbox is None:
            continue

        x, y = (float(v) for v in node["pos"].split(","))

        # svg_x = x + dx ;  svg_y = -y + dy  (SVG y points down)
        dxs.append((bbox[0] + bbox[2]) / 2 - x)
        dys.append((bbox[1] + bbox[3]) / 2 + y)

    if not dxs:
        return None

    spread = max(max(dxs) - min(dxs), max(dys) - min(dys))

    return statistics.median(dxs), statistics.median(dys), spread


def add_cluster_boxes_to_svg(svg_file, neato_model, boxes):
    """Insert the cluster boxes behind the nodes and edges of the SVG
    and widen the canvas so the boxes keep the same padding."""

    if not boxes:
        return

    tree = ET.parse(svg_file)
    root = tree.getroot()

    graph_group = next(
        (
            g for g in root.findall(svg_tag("g"))
            if g.get("class") == "graph"
        ),
        None,
    )

    offset = (
        measure_svg_offset(graph_group, neato_model)
        if graph_group is not None else None
    )

    if offset is None:
        warn("could not locate the nodes in the SVG; "
             "cluster boxes were not added")
        return

    dx, dy, spread = offset

    if spread > 1.0:
        warn(
            f"node positions in the SVG differ from the model by up "
            f"to {spread:.1f} pt; cluster boxes may be misaligned"
        )

    style = settings.cluster_view.get("style", "")
    radius = (
        settings.config["postprocess"]["corner_radius"]
        if "rounded" in style else 0
    )

    layer = ET.Element(svg_tag("g"), {"id": "clusters"})

    for box in boxes:

        group = ET.SubElement(
            layer, svg_tag("g"),
            {"id": box["id"], "class": "cluster"},
        )
        ET.SubElement(group, svg_tag("title")).text = box["title"]

        attributes = {
            "x": f"{box['left'] + dx:.1f}",
            "y": f"{box['top'] + dy:.1f}",
            "width": f"{box['width']:.1f}",
            "height": f"{box['height']:.1f}",
            "rx": str(radius),
            "ry": str(radius),
            "fill": box["fill"],
            "stroke": box["stroke"],
            "stroke-width": str(settings.cluster_view.get("penwidth", 1)),
        }

        if "dashed" in style:
            attributes["stroke-dasharray"] = "5,2"

        ET.SubElement(group, svg_tag("rect"), attributes)

    # Insert directly after the white page background so the boxes
    # lie behind every edge and node.
    background = next(
        (
            c for c in graph_group
            if c.tag == svg_tag("polygon") and c.get("fill") == "white"
        ),
        None,
    )
    insert_at = (
        list(graph_group).index(background) + 1
        if background is not None else 1
    )
    graph_group.insert(insert_at, layer)

    # Widen the canvas where the boxes reach past the original
    # padding around the nodes.
    translate = re.search(
        r"translate\(\s*(-?[\d.]+)[ ,]+(-?[\d.]+)\s*\)",
        graph_group.get("transform", ""),
    )
    view_box = root.get("viewBox")

    if translate and view_box:

        tx, ty = float(translate.group(1)), float(translate.group(2))
        _, _, width, height = (float(v) for v in view_box.split())
        pad = settings.dot_view["graph"]["pad"] * 72

        min_x = min(b["left"] for b in boxes) + dx
        max_x = max(b["left"] + b["width"] for b in boxes) + dx
        min_y = min(b["top"] for b in boxes) + dy
        max_y = max(b["top"] + b["height"] for b in boxes) + dy

        # The canvas spans [-tx, width - tx] x [-ty, height - ty]
        # in graph coordinates.
        grow_left = max(0.0, -tx - (min_x - pad))
        grow_right = max(0.0, (max_x + pad) - (width - tx))
        grow_top = max(0.0, -ty - (min_y - pad))
        grow_bottom = max(0.0, (max_y + pad) - (height - ty))

        new_width = width + grow_left + grow_right
        new_height = height + grow_top + grow_bottom
        new_tx, new_ty = tx + grow_left, ty + grow_top

        root.set("viewBox", f"0.00 0.00 {new_width:.2f} {new_height:.2f}")
        root.set("width", f"{new_width:.0f}pt")
        root.set("height", f"{new_height:.0f}pt")
        graph_group.set(
            "transform",
            re.sub(
                r"translate\([^)]*\)",
                f"translate({new_tx:.2f} {new_ty:.2f})",
                graph_group.get("transform"),
            ),
        )

        if background is not None:
            x0, x1 = -new_tx, new_width - new_tx
            y0, y1 = -new_ty, new_height - new_ty
            background.set(
                "points",
                f"{x0:.2f},{y0:.2f} {x1:.2f},{y0:.2f} "
                f"{x1:.2f},{y1:.2f} {x0:.2f},{y1:.2f} {x0:.2f},{y0:.2f}",
            )

    tree.write(svg_file, encoding="utf-8", xml_declaration=True)
