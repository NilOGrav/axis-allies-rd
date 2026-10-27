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
| `--check` | Only check the Tech List for mistakes and print a report; nothing is written. Exit status 1 if there are errors. See "Checking the data". |
| `--strict` | With `--check`: warnings also give exit status 1. |
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
| `[check]` | The level of every data check: `"error"`, `"warning"` or `"off"`. |

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

**Optional modules.** `Module` is `CORE` or an optional module (NUCLEAR,
OIL, ...). Playing without a module removes its technologies. A technology
that stays and depended on them is not blocked: a dependency group made
only of removed technologies becomes obsolete (it is dropped), and a group
with some alternatives left needs one of those. `--check` tries every
combination of switched-off modules.

## Checking the data

```
python src/tech_tree.py --check            # exit status 1 on errors
python src/tech_tree.py --check --strict   # ... and on warnings
python src/tech_tree.py --check --file other_list.csv
```

The checks work on the CSV rows themselves, before any graph is built, so
they also report the mistakes that would make building the graph fail.
Dependencies are read with the same meaning as in the views: a technology
that depends on a cluster needs any one of its members, a gate listed on a
cluster row applies to every member.

**How to judge the levels.** Rate a finding by its consequence for the
rules, not by how unusual it looks:

- **error**: the tree as written is broken or breaks a design rule. A
  technology can never become eligible, the data cannot be read
  unambiguously, or core R&D needs an optional module.
- **warning**: probably unintended, but the rules still work.
- **off**: observations that are normal in this tree.

The level of each check is set in `[check]` in `tech_tree.toml`; the
defaults below are a starting point.

| Check | Default | Finds |
|---|---|---|
| `duplicate_id` | error | The same `Tech_ID` twice. The later row silently replaces the earlier one. |
| `missing_field` | error | Empty `Tech_ID`, `Domain`, `Domain_code` or `Tier`, or a `Tier` that is not a whole number. |
| `unknown_reference` | error | A dependency naming something that does not exist, or a cluster row without technologies. |
| `unresearchable` | error | A technology that can never become eligible: a cycle, or a prerequisite that cannot be met. Computed with AND, OR and cluster meaning. |
| `module_combination_blocked` | error | A technology that cannot be researched when some optional modules are switched off (every combination is tried). See "Optional modules" below. |
| `module_loses_prerequisites` | warning | A technology whose every dependency group becomes obsolete when modules are switched off, so it is left without any prerequisite. |
| `redundant_dependency` | warning | A dependency group already implied by another group of the same technology (for example `(A\|B\|C)` next to `A`), or the same entry twice. A cluster-wide gate is never reported. |
| `tier_higher` | warning | A prerequisite that is only available from a later tier. |
| `tier_same` | warning | A prerequisite that is only available from the same tier. |
| `no_prerequisites` | warning | A tier 2 or higher technology without any prerequisite (its own or from a cluster gate). |
| `unknown_category` | warning | A `Category` with no entry in `[node_views]`; it would be drawn with `DEFAULT` (e.g. `RCENTER` for `RCENTRE`). |
| `id_mismatch` | warning | A `Tech_ID` that disagrees with `Domain_code` or `Tier`, or one `Domain_code` used by several domains. |
| `domain_config` | warning | Domains in the CSV and in `[[domains]]` that do not match. |
| `missing_name` / `missing_description` | warning | Empty `Name` / `Description`. |
| `unused_cluster_row` | off | A cluster row that nothing depends on and that has no dependencies itself. These are placeholders for future tiers. |

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

## Tests

```
python -m unittest discover -s tests          # from the repository root
python -m unittest tests.test_check -v        # one module
```

Only the standard library is needed (pytest runs them too). The tests use
a small fixture tree (`tests/fixtures/mini.csv`) and a **frozen copy** of
the config (`tests/fixtures/test.toml`), so tuning the real config does not
break tests of the code. The real config is only tested for being valid.

| Module | Covers |
|---|---|
| `test_settings` | Strict config: every missing or invalid setting is reported by name; path resolution. |
| `test_data` | CSV loading and its hints; cluster endpoints and their members; the chain view. |
| `test_layout` | Every technology placed once, bands, research centres, centred programme tiers. |
| `test_check` | Every data check, including the cases that must *not* be reported. |
| `test_render` | Golden DOT files (exact); cluster boxes, arrow anchors, dimming and canvas in the finished SVG. Needs Graphviz, skipped without. |
| `test_cli` | `main()` end to end: output folders and suffixes, `--file`, `--nodot`/`--nosvg`, `--hide-domain`, `--check`. |

Two tests also look at the real Tech List when it is present: the layout
invariants, and "no duplicate ids, missing fields, unknown references or
unresearchable technologies". Design questions such as module independence
are for you to judge, so they are not tests.

The DOT files are written by this program, not by Graphviz, so the golden
files in `tests/golden/` do not depend on your Graphviz version. After a
deliberate change to what the renderers write, run
`python tests/regen_golden.py` and review the diff.

## Where to add things

| To add | Where |
|---|---|
| A new output (JSON export, cards, web data) | A new `render_*.py` module that takes `graph` and the resolved layout, plus a call in `tech_tree.py`. |
| A new view type | `get_highlighted_nodes` in `views.py` and the `--view` choices in `tech_tree.py`. |
| A new setting | `tech_tree.toml`, and `REQUIRED_KEYS` in `settings.py` if the program cannot run without it. Also add it to `tests/fixtures/test.toml`. |
| A new data check | A check id in `CHECK_IDS` (`settings.py`), its level in `[check]` in both toml files, the logic in `check.py`, and a test in `test_check.py`. |
