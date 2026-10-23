# R&D tech tree tools

Generates views of the Axis & Allies 1940 Global R&D technology tree from
the Tech List CSV: a text listing, a Graphviz overview ("simple" view) and
a fixed-grid view ("grid" view) with filters for modules, domains, paths
and prerequisite chains.

The CSV defines the tree. `tech_tree.toml` defines how it looks. The
program has no built-in defaults: everything about presentation and file
locations is in the config file.

## Requirements

- Python 3.11 or newer (the config file is read with `tomllib`)
- Graphviz with `dot` and `neato` on the PATH
- No Python packages to install

## Quick start

From anywhere:

```
python src/tech_tree.py
```

reads the Tech List named in `tech_tree.toml` and writes everything to
`output/` in the repository root. More examples:

```
python src/tech_tree.py --file other_list.csv
python src/tech_tree.py --view domain --filter Energy --dim fade
python src/tech_tree.py --view module --filter NUCLEAR --dim none
python src/tech_tree.py --view chain  --filter P.9.NU
python src/tech_tree.py --view path   --filter FIGHTER --dim grey
python src/tech_tree.py --hide-domain Programs --nosimple
```

## Command line options

| Option | Meaning |
|---|---|
| `--file CSV` | Tech List to read for this run. Default: `paths.tech_list` in the config. Relative to the current directory. |
| `--config FILE` | Config file. Default: `tech_tree.toml` next to `tech_tree.py`. |
| `--view {full,module,domain,path,chain}` | Which nodes to highlight in the grid view. Default `full`. |
| `--filter VALUE` | The module name, domain name, path name, or node id (for `chain`) to highlight. |
| `--dim {grey,fade,none}` | What happens to everything else: flat grey, faded domain colour, or removed. Default `grey`. |
| `--hide-domain NAME` | Leave a domain out of every output. May be repeated. |
| `--notxt` / `--nosimple` / `--nogrd` | Skip the text file / simple view / grid view. |
| `--nodot` | Do not keep DOT files (Graphviz still gets a temporary one). |
| `--nosvg` | Stop after writing DOT files. With both `--nodot` and `--nosvg`, nothing is written. |

The simple view always shows the full tree; `--view`, `--filter` and
`--dim` only affect the grid view. A filtered grid view gets a suffix in
its file name, e.g. `tech_tree_grid_chain_p_9_nu.svg`; the simple view
files never do.

## Output

| File | Content |
|---|---|
| `txt_dir/tech_tree.txt` | The resolved layout as text (also printed). |
| `dot_dir/tech_tree_simple.dot`, `svg_dir/tech_tree_simple.svg` | Graphviz overview with clusters as boxes. |
| `dot_dir/tech_tree_grid[_view_value].dot`, `svg_dir/tech_tree_grid[_view_value].svg` | The grid view. |

The directories come from the config and are created when missing. You
probably want `output/` in `.gitignore`.

## Configuration: `tech_tree.toml`

Every setting is required; a missing one is reported by name at start-up.

| Section | What it controls |
|---|---|
| `[paths]` | `root` (relative to the config file), then `tech_list`, `txt_dir`, `svg_dir`, `dot_dir` (relative to `root`). |
| `[layout]` | `row_offset` (free rows between clusters), `late_tiers_from` (tiers from here on are centred on their domain). |
| `[[domains]]` | One entry per domain: `name` and `color`. **The order of the entries is the vertical order of the domain bands.** |
| `[colors]` | Default colour for unknown domains, how much darker cluster boxes are than nodes, colours cycled through for OR groups. |
| `[dim.grey]`, `[dim.fade]` | How non-highlighted nodes, edges and cluster boxes look in a filtered view. |
| `[dot_view]` | Graphviz graph and node attributes. Width, height, `nodesep` and `ranksep` also set the grid spacing. |
| `[edge_views.*]` | `AND` (solid), `OR` (dashed, coloured per group), `ANY` (edge leaving a whole cluster). |
| `[node_views.*]` | Node style per `Category`; `DEFAULT` is used for any category without its own entry. |
| `[cluster_view]` | Style, colour, margin of the cluster boxes. |
| `[postprocess]` | Which tiers are drawn as full domain bands (`band_tiers_from` / `band_tiers_to`) and the box corner radius. |

The CSV decides which domains exist. A domain in the CSV but not in the
config is placed at the bottom with the default colour; a configured
domain that is not in the CSV is ignored. Both give a warning.

## The Tech List CSV

Comma-separated, UTF-8 (a byte-order mark is accepted), text cells quoted
where they contain commas. Required columns: `Tech_ID`, `Name`,
`Domain_code`, `Domain`, `Tier`, `Module`, `Category`, `Path`,
`DepGroup1` to `DepGroup4`. Other columns are ignored by these tools.
Completely empty rows are skipped.

**Dependencies.** Each `DepGroup` cell is one group. Groups are combined
with AND. Inside a group, `|` separates alternatives (OR):

```
DepGroup1: A.1.01|A.1.02      DepGroup2: E.2.01      ->  (A.1.01 OR A.1.02) AND E.2.01
```

**Clusters.** A cluster is all technologies of one domain in one tier. A
row with `Category` = `CLUSTER` (id `X.<code>.<tier>`) stands for that
cluster in a dependency:

- A technology that depends on a cluster needs **any one** of its members
  (the same as an OR over all of them). The grid view draws this as a
  dashed arrow leaving the cluster's box.
- A cluster that depends on something means **every** member needs it. The
  grid view draws one solid arrow into the cluster's box instead of one per
  member.

**Categories** with their own style: `KEYSTONE`, `RCENTRE` (research
centre; takes two grid rows), `RESOURCE`, `CLUSTER` (never drawn). Any
other value uses `DEFAULT`.

**Path** is a comma-separated list; a technology can be on several paths.

## Reading the grid view

- Columns are tiers, left to right. Rows are grouped in one band per
  domain, in the configured order.
- Each cluster has a background box. Boxes in tiers `band_tiers_from` to
  `band_tiers_to` are as tall as the largest cluster of their domain, so
  the bands line up. Other tiers (the starting tier and the programme
  tiers) wrap their own nodes; large programme clusters are centred on
  their domain.
- Solid arrow between nodes: AND. Dashed coloured arrows: one OR group.
  Dashed black arrow leaving a box: any one technology in that cluster.
  Solid arrow entering a box: every technology in that cluster needs it.
- In a filtered view, clusters with nothing highlighted are dimmed like
  their nodes. With `--dim none` removed nodes keep their place in the
  grid, so all views stay comparable.

## Architecture

```
tech_tree.toml                              Tech List (CSV)
HOW it is shown                             WHAT exists
settings.py                                 data.load_data()
     |                                           |
     |                                           v
     |                                     build_graph()
     |                                           |
     |                                           v
     |              +------------------------------------------------+
     |              |                CANONICAL GRAPH                 |
     |              |                                                |
     |              |  What technologies exist, how are they         |
     |              |  related? A dependency endpoint is a node or   |
     |              |  a whole cluster (= any one of its members).   |
     |              +-----------------------+------------------------+
     |                                      |
     |                       +--------------+--------------+
     |                       v                             v
     +---- styling ---->  apply_view()            resolve_layout()
     |                                                     |
     |                                                     v
     |              +------------------------------------------------+
     +--- layout -->|                  VIRTUAL GRID                  |
     |              |                                                |
     |              |  Where should each technology be?              |
     |              |  column (tier) / row                           |
     |              |                                                |
     |              |      *** KNOWS NOTHING ABOUT GRAPHVIZ ***      |
     |              +-----------------------+------------------------+
     |                                      |
     |                          ============+============
     |                          RENDERER ENTRY POINTS
     |                          ============+============
     |                                      |
     |   render_text()
     |       terminal + txt_dir/tech_tree.txt
     |
     |   render_simple_svg()                    always the full tree
     |       Graphviz dot lays the tree out, clusters are subgraphs
     |       -> dot_dir + svg_dir
     |
     |   render_grid_svg()                      honours --view / --dim
     |       view filter (highlight, dim or hide)
     |       build_cluster_boxes()   one box per domain/tier cluster
     |       build_neato_model()     nodes pinned to the grid; an edge
     |                               into / out of a cluster attaches
     |                               to its box edge
     |       neato -n                positions fixed, edges routed
     |       SVG post-processing     boxes behind the nodes, canvas
     |                               widened to keep the padding
     |       -> dot_dir + svg_dir
     |
     +--- paths (txt_dir, dot_dir, svg_dir, tech_list) <--- config
```

The canonical graph never contains layout or Graphviz details; renderers
translate it. Edges keep their endpoints as sets of real technologies
(`members`), so analyses such as the chain view work on the meaning of a
dependency, not on how it is drawn.

## Using it as a library

Importing the package does nothing; call `settings.load` first.

```python
import sys; sys.path.insert(0, "src")
from rdtree import settings, data, views, layout

settings.load("src/tech_tree.toml")
graph = data.build_graph(data.load_data(settings.paths["tech_list"]))
graph = views.apply_view(graph)
placed = layout.resolve_layout(graph, settings.layout)["nodes"]
# graph["nodes"], graph["edges"], graph["domains"] ... placed[id] -> column/row
```

Settings are loaded into module attributes, so one process uses one
config at a time.

## Where to add things

| To add | Where |
|---|---|
| A new output (JSON export, cards, web data) | A new `render_*.py` module that takes `graph` and the resolved layout, plus a call in `tech_tree.py`. |
| A new view type | `get_highlighted_nodes` in `views.py` and the `--view` choices in `tech_tree.py`. |
| A new setting | `tech_tree.toml`, and `REQUIRED_KEYS` in `settings.py` if the program cannot run without it. |
