# Topic: Graphviz and SVG Rendering

Last updated: 2026-11-09
Status: Active

## Purpose

Document how the technology tree is drawn with Graphviz and SVG: the two renderers, what was learned from the experiments that led to the current design, the geometry of the grid view, the cluster boxes and cluster arrows, and the conventions of the SVG files.

The rendering must support:

- an automatically generated overview that is always available;
- a fixed grid in which every technology has a predictable position, so that domains and tiers line up;
- dependency arrows that stay readable, including dependencies on whole clusters;
- filtered and dimmed views that stay visually comparable;
- SVG files whose structure can later support an interactive layer.

The surrounding architecture (canonical graph, virtual grid, configuration, data checks, tests) is documented in **20-visualisation-code**.

### Status legend

| Status | Meaning |
|---|---|
| Established | Deliberately decided by the project owner. |
| Established architecture | Part of the settled architecture, including Design Principles. |
| Current design | Implemented and in use, but not formally decided as a rule. |
| Parameter | A value that may change through balancing or taste; held in configuration unless stated. |
| Finding | Something learned from an experiment. It explains a decision; it is not a rule. |
| Superseded | Tried, and replaced by a later approach. |
| Open | Unresolved. Nothing should be invented until it is designed. |
| Exploration | An idea that is not yet a project requirement. |

---

## Principles

| ID | Rule | Status |
|---|---|---|
| GVZ-001 | DOT and SVG are means, not goals. The architecture must not depend on Graphviz being the final renderer. | Established architecture |
| GVZ-002 | Graphviz is used where it is strong (automatic layout, edge routing). It is not forced to act as a programmable coordinate system. | Established architecture |
| GVZ-003 | Two renderers coexist: a simple one (Graphviz `dot`, automatic layout) and a grid one (Graphviz `neato` with fixed positions). Neither replaces the other. | Established |
| GVZ-004 | The grid renderer has a strict division of work. Neato builds the diagram (positions are given, only edges are routed). SVG post-processing adds only visual enhancements and never moves a node or an edge. | Established |
| GVZ-005 | Domain membership is visible from node colour alone. Cluster boxes are an optional background added afterwards. | Established |
| GVZ-006 | Experiments are done one technique at a time and compared against the unchanged simple view. | Established |

---

## The Two Renderers

| | Simple view | Grid view |
|---|---|---|
| Engine | `dot` | `neato -n` |
| Placement | Graphviz decides | Every node pinned to its virtual-grid position |
| Clusters | Graphviz subgraphs (boxes drawn by Graphviz) | Boxes added to the SVG afterwards |
| Dependency on a cluster | One arrow to the cluster box, attached to a representative node (`ltail`/`lhead`) | One arrow to the edge of the cluster box, attached to an anchor point |
| Affected by `--view`, `--dim` | No, always the full tree | Yes |
| Role | Stable reference overview | The ordered, comparable working view |

Both draw each node as a box labelled with its Tech_ID and name, coloured by domain.

---

## What Was Learned with `dot`

The grid view was first attempted with `dot`. These findings explain why it moved to `neato`.

| ID | Finding | Status |
|---|---|---|
| GVZ-010 | The order of nodes inside a `rank=same` group has very little effect on placement. Rank membership decides the column; it is not coordinate control. | Finding |
| GVZ-011 | Invisible layout edges (`style=invis`, `constraint=false`) are a separate mechanism from real dependency edges and must stay out of the canonical graph. Many of them make the layout fragile and unpredictable. | Finding |
| GVZ-012 | Padding clusters with filler nodes only works if the fillers are members of the cluster subgraph and have a column. Fillers outside the cluster, or without a column, produce large unexplained white space or land in the first column. | Finding |
| GVZ-013 | Even with equal-sized clusters, `dot` placed the clusters of one domain at very different heights across tiers (differences of thousands of points), because it optimises edge lengths and crossings globally. Structure alone cannot make `dot` produce a fixed grid. | Finding |
| GVZ-014 | Moving nodes inside a finished `dot` SVG breaks the edges, because edge paths do not follow the moved nodes. | Finding |
| GVZ-015 | `neato` ignores cluster subgraphs, so a `neato` drawing has no cluster boxes of its own. | Finding |
| GVZ-016 | Cluster fillers, invisible layout edges and rank-ordering experiments are no longer part of the code. | Superseded |
| GVZ-017 | Extracting coordinates from a `dot` layout and correcting them in the SVG was considered as a hybrid. It was not adopted. | Superseded |

Decision that followed (GVZ-003, GVZ-004): `neato` places and routes, the SVG post-processing draws the clusters.

---

## Grid Renderer: `neato -n`

| ID | Rule | Status |
|---|---|---|
| GVZ-020 | Every visible node receives `pos="x,y!"` from the virtual grid. With `-n`, neato uses these positions as given and only computes edge routes. | Established |
| GVZ-021 | Cluster rows (Category `CLUSTER`) are never drawn as nodes. | Established architecture |
| GVZ-022 | Edges are drawn before nodes (`outputorder=edgesfirst`) with spline routing. | Current design |
| GVZ-023 | Duplicate node pairs are drawn once. An edge whose end is not drawn (a hidden node, or a cluster without a box) is skipped. | Current design |
| GVZ-024 | Neato re-normalises the drawing so its bounding box starts at the origin. Coordinates in the SVG therefore differ from the model by a constant offset. The offset is measured from the drawn node shapes (median over all nodes) and is never assumed. A warning is given if nodes disagree by more than 1 pt. | Current design |

### Grid geometry

Units are points (72 pt = 1 inch). Values come from `[dot_view]` in the configuration.

| Quantity | Formula | Current value |
|---|---|---|
| Column spacing | (node width + `ranksep`) x 72 | 756 pt |
| Row spacing | (node height + `nodesep`) x 72 | 115.2 pt |
| Node size | width x 72, height x 72 | 252 x 72 pt |
| Position of a node | x = column x column spacing; y = -row x row spacing (DOT y points up) | |
| Position in the SVG | x + dx, -y + dy, with (dx, dy) measured (GVZ-024) | |

| ID | Rule | Status |
|---|---|---|
| GVZ-025 | Node size, `ranksep`, `nodesep` and `pad` are Parameters. They also determine the grid spacing, so changing them changes the whole grid. | Parameter |
| GVZ-026 | A research centre is a rounded box with a double border, two node heights plus the gap between them tall (187.2 pt), centred half a row below its grid row so that it fills the two rows reserved for it. | Established |
| GVZ-027 | Research centres were first drawn as circles. Their bounding circles overlapped neighbouring nodes, and neato fell back to straight edges ("some nodes with margin touch"). The double-bordered box replaced them. | Finding |

---

## Node and Edge Styling

| ID | Rule | Status |
|---|---|---|
| GVZ-030 | Node fill is the domain colour. The border is neutral grey so that it is visible on every fill. Category decides the shape: key technologies are double octagons, research centres double-bordered boxes, all others rounded boxes. | Current design |
| GVZ-031 | A cluster box is the domain colour darkened by a fixed factor, so that it is visibly but slightly darker than its nodes. The simple and grid views use the same colours. | Established (factor is a Parameter, currently 0.82) |
| GVZ-032 | Domain colours and order are configuration, not data. | Established |

| Edge | Meaning | Style |
|---|---|---|
| Between nodes, single entry | AND | Solid, black |
| Between nodes, OR group | Alternatives | Dashed, one colour per group, cycled through a palette of eight |
| Leaving a whole cluster | Any one member of the cluster | Dashed, black |
| Entering a whole cluster | Every member needs it | Solid, black |

The style of the "leaving a cluster" edge is `[edge_views.ANY]`. Only its line style is overridden, so dimming can still change its colour.

---

## Cluster Boxes

Boxes are added by SVG post-processing, from the virtual grid.

| ID | Rule | Status |
|---|---|---|
| GVZ-040 | One box per domain/tier cluster that has technologies. | Established |
| GVZ-041 | In the band tiers (currently tiers 1 to 6) a box is as tall as the largest cluster of its domain in those tiers, so the boxes of a domain line up across tiers. In all other tiers a box is as tall as its own nodes. | Established (tier range is a Parameter) |
| GVZ-042 | Box width = node width + 2 x margin. Box height = (rows - 1) x row spacing + node height + 2 x margin. The margin is `[cluster_view]` margin (currently 30 pt). | Current design |
| GVZ-043 | A box is drawn as a rounded, dashed rectangle with the border colour and width from `[cluster_view]`. Corner radius is `[postprocess]` `corner_radius`. | Current design |
| GVZ-044 | Boxes are inserted directly after the white page background and therefore lie behind every edge and node. | Current design |
| GVZ-045 | The canvas is widened (viewBox, width, height, translation, background) so that the boxes keep the same padding around them as Graphviz gave the nodes. | Current design |
| GVZ-046 | In a filtered view a box keeps its full footprint, and a cluster with no remaining node gets no box. A cluster without any highlighted node is dimmed: its fill is the dimmed node fill darkened by the same factor. | Current design (the author is testing the effect) |
| GVZ-047 | A research centre or key technology has a double border that protrudes about 4 pt beyond its nominal size, so the margin inside boxes that contain one looks 4 pt tighter. Box widths are kept uniform. | Open (being tested) |
| GVZ-048 | The dash pattern (5,2) of box borders is fixed in the code, not configuration. | Current design |

---

## Arrows to and from Clusters

The meaning of dependencies on clusters is defined in topic 20 (VIS-030 to VIS-032): a dependency on a cluster means any one member; a dependency listed on a cluster means every member.

| ID | Rule | Status |
|---|---|---|
| GVZ-050 | An arrow that enters a cluster ends on the left edge of its box, and an arrow that leaves a cluster starts on the right edge, both at the vertical middle of the box. | Current design |
| GVZ-051 | Neato routes to small invisible anchor points placed on those box edges (`__anchor_<box id>_L` and `_R`). Anchors exist only for the boxes that edges actually use. | Current design |
| GVZ-052 | A dependency between two clusters is one arrow from box to box. | Current design |
| GVZ-053 | Drawing arrows to the box edge instead of to individual members replaces, in the v8.8 snapshot, 28 arrows from the Basic Research Facility into tier 1 with 6, and avoids 108 of the 354 node-to-node arrows that full expansion would need. | Finding |
| GVZ-054 | Arrows are routed by neato, so they avoid nodes the same way other edges do. Arrows drawn by post-processing would cross nodes and are not used. | Established |

Verified on the v8.8 data: every cluster-arrow end lies within 1.2 pt of the box edge at mid-height.

---

## Filtered Views in SVG

| ID | Rule | Status |
|---|---|---|
| GVZ-060 | Grey dimming gives non-highlighted nodes and edges a flat grey; fade blends the domain colour towards white; none removes them. The colours and the blend are `[dim.*]` in the configuration. | Current design |
| GVZ-061 | An edge is highlighted only if both of its ends are. A cluster end counts as highlighted if any member is. | Current design |
| GVZ-062 | With `none`, removed nodes leave their place empty, so all views of the same data share one grid. | Current design (the author is testing the effect) |
| GVZ-063 | The simple view is rendered before any filter is applied and is therefore never affected by it. | Established |

---

## SVG Structure Conventions

These are conventions of the generated files, so that later tools (an interactive page, exports) can rely on them.

| Element | Convention |
|---|---|
| Graph group | `g` with class `graph`; its `transform` carries the translation. All coordinates below are inside it. |
| Cluster layer | `g` with id `clusters`, first child after the page background. |
| Cluster box | `g` with id `cluster_<Domain>_<tier>` (non-word characters replaced by `_`) and class `cluster`, containing `title` ("Domain - Tier N") and a `rect`. |
| Node | `g` with class `node`; its `title` is the Tech_ID. |
| Edge | `g` with class `edge`; its `title` is `source->target`. Cluster ends use the anchor names above. |

| ID | Rule | Status |
|---|---|---|
| GVZ-070 | The conventions above are stable. Changing them is a change to the output format. | Current design |
| GVZ-071 | Output file names: `tech_tree_simple.dot/.svg` and `tech_tree_grid[_<view>_<value>].dot/.svg`. The value is lower-cased with `.`, space, `&`, `/` and `\` replaced by `_`. Folders come from the configuration. | Current design |
| GVZ-072 | DOT files are written by the program and are independent of the Graphviz version. SVG files are produced by Graphviz and can differ between versions. | Finding |

---

## Verification

| ID | Rule | Status |
|---|---|---|
| GVZ-080 | Rendered grid SVGs are checked from the finished file: every node lies inside exactly one box; no boxes overlap; each domain has one box height across the band tiers; cluster-arrow ends lie within 4 pt of the box edge; the canvas keeps the padding. | Current design |
| GVZ-081 | The DOT output is compared exactly with golden files. | Current design |
| GVZ-082 | A visual check of the result is made in a real browser engine, because the tool environment has no SVG rasteriser of its own. | Current design |

---

## Parameters

| Parameter | Where | Current value |
|---|---|---|
| Node width, height | `[dot_view.node]` | 3.5 in, 1.0 in |
| `ranksep`, `nodesep`, `pad` | `[dot_view.graph]` | 7.0 in, 0.6 in, 0.5 in |
| Cluster margin | `[cluster_view]` | 30 pt |
| Cluster darkening | `[colors]` `cluster_darken` | 0.82 |
| Corner radius | `[postprocess]` | 12 |
| Band tiers | `[postprocess]` | 1 to 6 |
| Free rows between clusters | `[layout]` `row_offset` | 1 |
| OR group colours | `[colors]` `or_groups` | eight colours, cycled |
| Dimming | `[dim.grey]`, `[dim.fade]` | see configuration |
| Dash pattern, anchor size | Code | 5,2 and 0.02 in |

---

## Known Limitations and Open Questions

| ID | Item | Status |
|---|---|---|
| GVZ-090 | Neato's general-purpose edge router is not tuned for layered graphs. Long edges curve across the grid, edges can pass underneath nodes, and crossings are not minimised. The empty rows between clusters leave room for corridors, but routing does not use them deliberately. | Open |
| GVZ-091 | Should arrows be anchored somewhere other than the vertical middle of a box edge, for example to reduce crossings? | Open |
| GVZ-092 | The simple view still attaches cluster arrows to a representative node (the first member). | Open (see VIS-103) |
| GVZ-093 | Hidden-node footprint in `--dim none` views (GVZ-046, GVZ-062). | Open (being tested) |
| GVZ-094 | The 4 pt protrusion of double borders (GVZ-047). | Open (being tested) |
| GVZ-095 | Tier column headers, domain labels and a legend in the grid view. | Exploration |
| GVZ-096 | An interactive page built on the SVG conventions (filtering, prerequisite exploration, research-state tracking). | Exploration (DP-015) |
| GVZ-097 | A renderer other than Graphviz, or a custom router, if neato's routing proves insufficient. | Exploration |

---

## Relationship to Other Topics

- **20-visualisation-code** defines the canonical graph, the virtual grid, the views, the configuration and the tests that this topic builds on, and the meaning of dependencies on clusters.
- **Design Principles** supply DP-013 (visual clarity), DP-014 (separate logic and presentation), DP-015 (interactive future compatibility) and DP-045 (one canonical graph, multiple derived views).
