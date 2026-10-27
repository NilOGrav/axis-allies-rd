"""Geometry checks on a finished grid SVG, using only the SVG itself."""

import re
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
NUMBER = r"-?\d+(?:\.\d+)?"


def load(svg_path):
    root = ET.parse(svg_path).getroot()
    graph = next(g for g in root.findall(NS + "g") if g.get("class") == "graph")
    return root, graph


def shape_bbox(group):
    xs, ys = [], []
    for child in group:
        tag = child.tag.split("}")[-1]
        if tag in ("path", "polygon"):
            text = child.get("d") if tag == "path" else child.get("points")
            values = [float(v) for v in re.findall(NUMBER, text or "")]
            xs += values[0::2]
            ys += values[1::2]
        elif tag == "ellipse":
            cx, cy = float(child.get("cx")), float(child.get("cy"))
            rx, ry = float(child.get("rx")), float(child.get("ry"))
            xs += [cx - rx, cx + rx]
            ys += [cy - ry, cy + ry]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def nodes(graph):
    """{tech id: bbox} of every drawn node."""
    found = {}
    for group in graph.findall(NS + "g"):
        if group.get("class") == "node":
            bbox = shape_bbox(group)
            if bbox:
                found[group.find(NS + "title").text] = bbox
    return found


def clusters(graph):
    """{box id: (title, (x0, y0, x1, y1), fill)} of every cluster box."""
    found = {}
    for group in graph.iter(NS + "g"):
        if group.get("class") == "cluster":
            rect = group.find(NS + "rect")
            x, y = float(rect.get("x")), float(rect.get("y"))
            w, h = float(rect.get("width")), float(rect.get("height"))
            found[group.get("id")] = (
                group.find(NS + "title").text, (x, y, x + w, y + h),
                rect.get("fill"),
            )
    return found


def inside(inner, outer, tolerance=0.5):
    return (inner[0] >= outer[0] - tolerance and inner[1] >= outer[1] - tolerance
            and inner[2] <= outer[2] + tolerance
            and inner[3] <= outer[3] + tolerance)


def membership(graph):
    """{tech id: [titles of the boxes that contain it]}"""
    boxes = clusters(graph)
    return {
        tech_id: [t for t, b, _ in boxes.values() if inside(bbox, b)]
        for tech_id, bbox in nodes(graph).items()
    }


def overlapping_boxes(graph):
    boxes = list(clusters(graph).values())
    pairs = []
    for i, (title_a, a, _) in enumerate(boxes):
        for title_b, b, _ in boxes[i + 1:]:
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                pairs.append((title_a, title_b))
    return pairs


def edges(graph):
    """{title: (path element, arrowhead polygon or None)}"""
    found = {}
    for group in graph.findall(NS + "g"):
        if group.get("class") == "edge":
            found[group.find(NS + "title").text] = (
                group.find(NS + "path"), group.find(NS + "polygon"))
    return found


def anchor_end_deviations(graph):
    """For every edge end attached to a cluster box: (edge title, which
    end, horizontal deviation, vertical deviation) from the middle of
    the box edge it should touch."""
    boxes = {k: v[1] for k, v in clusters(graph).items()}
    result = []

    for title, (path, polygon) in edges(graph).items():
        source, target = title.split("->")
        numbers = [float(v) for v in re.findall(NUMBER, path.get("d"))]

        for name, end in (("source", source), ("target", target)):
            match = re.match(r"__anchor_(.+)_([LR])$", end)
            if not match:
                continue
            box = boxes[match.group(1)]
            middle = (box[1] + box[3]) / 2

            if name == "source":
                dx = abs(numbers[0] - box[2])
                dy = abs(numbers[1] - middle)
            else:
                points = [float(v) for v in re.findall(NUMBER, polygon.get("points"))]
                xs, ys = points[0::2], points[1::2]
                base = (numbers[-2], numbers[-1])
                tip = max(range(len(xs)),
                          key=lambda i: (xs[i] - base[0]) ** 2 + (ys[i] - base[1]) ** 2)
                dx, dy = abs(xs[tip] - box[0]), abs(ys[tip] - middle)

            result.append((title, name, dx, dy))

    return result


def canvas_padding(root, graph, pad):
    """Smallest distance (points) from any cluster box to the canvas edge."""
    translate = re.search(r"translate\(\s*(-?[\d.]+)[ ,]+(-?[\d.]+)\s*\)",
                          graph.get("transform"))
    tx, ty = float(translate.group(1)), float(translate.group(2))
    _, _, width, height = (float(v) for v in root.get("viewBox").split())
    boxes = [b for _, b, _ in clusters(graph).values()]
    return min(
        min(b[0] for b in boxes) + tx, min(b[1] for b in boxes) + ty,
        width - (max(b[2] for b in boxes) + tx),
        height - (max(b[3] for b in boxes) + ty),
    )
