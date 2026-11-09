# Topic: Visualisation Code

Last updated: 2026-11-09
Status: Active

## Purpose

Document the architecture, conventions and rules of the tooling that turns the authoritative Tech List CSV into readable views of the Axis & Allies Global 1940 R&D technology tree.

The tooling exists to support two uses of the same tree:

- **tuning and balancing** the tree (filters, prerequisite chains, data checks);
- **reading** a tree of roughly 175 technologies across nine tiers (overview and filtered views for players).

The tooling must support:

- generating every view from the one authoritative data file;
- keeping the technology data independent of how it is drawn;
- several renderers (text, Graphviz overview, fixed-grid SVG) and future outputs without restructuring;
- checking the data for mistakes the picture would hide;
- being tested, so that changes to the code can be proven not to change the output.

Rendering details specific to Graphviz and SVG are documented in **21-graphviz-svg**.

### Status legend

| Status | Meaning |
|---|---|
| Established | Deliberately decided by the project owner. |
| Established architecture | Part of the settled architecture (including principles from the Design Principles table). |
| Current design | Implemented and in use, but not formally decided as a rule. |
| Parameter | A value that may change through balancing or taste; held in configuration. |
| Open | Unresolved. Nothing should be invented until it is designed. |
| Exploration | An idea that is not yet a project requirement. |

---

## Scope

In scope: reading the Tech List, the canonical graph, views and filters, the virtual grid, the renderers as a system, configuration, data checks, tests, the command line and its outputs.

Out of scope: the game rules themselves (they are defined in the R&D rule topics), and Graphviz/SVG specifics (topic 21).

---

## Architectural Principles

| ID | Rule | Status |
|---|---|---|
| VIS-001 | The CSV defines the technology tree. Renderers define how it is viewed. | Established architecture |
| VIS-002 | The complete graph is built once from the data (the canonical graph). Views, filters and highlights are derived from it, never separate copies of it. | Established architecture (DP-045) |
| VIS-003 | The canonical graph contains no layout or Graphviz details. | Established architecture |
| VIS-004 | The virtual grid (where each technology sits, as column and row) knows nothing about Graphviz or any other renderer. | Established architecture |
| VIS-005 | A node may exist in the canonical graph without being drawn (for example cluster rows). Semantic existence and visual existence are different things. | Established architecture |
| VIS-006 | The simple overview renderer is a stable reference view. Experiments with other renderers must not alter it. | Established |
| VIS-007 | The simple view always shows the full tree. View flags affect only the grid view. | Established |
| VIS-008 | Experimental techniques are tried one at a time, so that a change in the result can be attributed to one cause. | Established |
| VIS-009 | Graphviz, DOT and SVG are tools, not the architecture. The pipeline must stay usable if Graphviz is replaced or supplemented. | Established architecture |
| VIS-010 | Presentation settings live in a configuration file, not in the code. | Established |
| VIS-011 | The configuration file is the single source of truth: the program has no built-in defaults, and a missing setting stops the run and names the setting. | Established |
| VIS-012 | Input and output locations are configuration. The Tech List to read can be replaced for one run on the command line. | Established |
| VIS-013 | Importing the code as a library has no side effects. The command line is a thin layer on top of it. | Current design |
| VIS-014 | Settings are loaded into module-level values, so one process uses one configuration at a time. | Current design |

Related Design Principles: DP-002 (data-driven structure), DP-003 (single source of truth), DP-013 (visual clarity), DP-014 (separate logic and presentation), DP-015 (interactive future compatibility), DP-019 (automation-friendly), DP-045 (one canonical graph, multiple derived views).

---

## Pipeline

```text
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
     |              |  column (tier) / row for each technology       |
     |              |      *** KNOWS NOTHING ABOUT GRAPHVIZ ***      |
     |              +-----------------------+------------------------+
     |                                      |
     |                          RENDERER ENTRY POINTS
     |                                      |
     |   render_text()          terminal + text file
     |   render_simple_svg()    Graphviz dot, always the full tree
     |   render_grid_svg()      view filter, then neato -n, then SVG
     |                          post-processing
     |
     +--- paths (txt_dir, dot_dir, svg_dir, tech_list) <--- config
```

The data check (`--check`) is a separate path: it reads the raw CSV rows, before any graph is built, and writes no files.

| Stage | Module | Responsibility |
|---|---|---|
| Configuration | `settings` | Read and validate `tech_tree.toml`; publish the values. |
| Data | `data` | Read the CSV; build the canonical graph, including cluster endpoints with their member lists. |
| Styling and views | `views` | Per-node and per-edge appearance; hiding domains; highlighting (module, domain, path, chain); dimming. |
| Layout | `layout` | The virtual grid. |
| Renderers | `render_text`, `render_dot`, `render_grid`, `svg_postprocess` | Turn graph and layout into files. |
| Output | `output` | Where files go and which of them are written. |
| Data check | `check` | The data lint. |

---

## Code Organisation

| Path | Content |
|---|---|
| `src/tech_tree.py` | Command line entry point (`main`). |
| `src/tech_tree.toml` | The configuration. |
| `src/rdtree/` | The code, one module per stage (see Pipeline). |
| `src/README.md` | User documentation of the tool. |
| `tests/` | Test suite, fixture tree, frozen test configuration, golden DOT files. |
| `output/` | Generated files (folders from the configuration). Generated output is not source. |

Requirements: Python 3.11 or newer (the configuration is read with `tomllib`) and Graphviz (`dot`, `neato`) on the path. No Python packages are required.

---

## Input: the Tech List CSV

| ID | Rule | Status |
|---|---|---|
| VIS-020 | The Tech List CSV is the authoritative source for technologies, domains, tiers, modules and dependencies. | Established architecture (DP-003) |
| VIS-021 | The file is comma-separated UTF-8. A byte-order mark is accepted. Text cells that contain commas are quoted. Completely empty rows are skipped. | Current design |
| VIS-022 | Required columns: `Tech_ID`, `Name`, `Domain_code`, `Domain`, `Tier`, `Module`, `Category`, `Path`, `DepGroup1` to `DepGroup4`. Other columns are ignored by the tooling. A missing column is reported with a hint (for example a semicolon-separated file or an old `ID` column). | Current design |
| VIS-023 | The set of domains is taken from the data. The configuration only decides the order and colour of domains. A domain in the data but not in the configuration is placed last with the default colour; a configured domain absent from the data is ignored. Both give a warning. | Established |
| VIS-024 | Domain order and domain colours are presentation, not data, and belong in the configuration. | Established |
| VIS-025 | Resources are not part of the Tech List. The former Resource domain no longer exists there; resources live in their own sheet. | Established |
| VIS-026 | Clusters are determined by the data (domain and tier), not reconstructed from Tech_ID text. | Established architecture |
| VIS-027 | A technology belongs to the domain named in its row. The prefix of its Tech_ID is not authoritative. | Established architecture |

### Dependency syntax

Each `DepGroup` cell is one group. Groups are combined with AND. Inside a cell, `|` separates alternatives (OR).

```text
DepGroup1: A.1.01|A.1.02     DepGroup2: E.2.01
meaning:   (A.1.01 OR A.1.02) AND E.2.01
```

This is the established AND/OR logic of the Design Principles (DP-012).

---

## Dependencies on Clusters

A cluster is all technologies of one domain in one tier. A row with Category `CLUSTER` (Tech_ID of the form `X.<code>.<tier>`) stands for that cluster in a dependency.

| ID | Rule | Status |
|---|---|---|
| VIS-030 | A technology that depends on a cluster needs any one of the cluster's members. This is the same as an OR over all of its members. | Established |
| VIS-031 | A dependency listed on a cluster row means every member of the cluster needs it. | Current design (assumed from the research-centre rules; not separately confirmed) |
| VIS-032 | A cluster that depends on a cluster means: every member of the target needs any one member of the source. | Current design (follows from VIS-030 and VIS-031) |
| VIS-033 | The canonical graph keeps the endpoints of a dependency as sets of real technologies (the members), not only as one node. Analyses work on the meaning of a dependency, not on how it is drawn. | Current design |
| VIS-034 | The chain view follows all members of a cluster endpoint. It shows every technology that could be a prerequisite (the union of all alternatives), not the cheapest route. | Current design |
| VIS-035 | A cluster endpoint counts as highlighted in a filtered view if any of its members is highlighted. | Current design |
| VIS-036 | For Graphviz, a cluster endpoint also carries one representative real node (the first member). It exists only so the simple renderer can draw one arrow to a cluster box. It has no meaning for the rules. | Current design |

Snapshot (Tech List v8.8): 246 dependency edges, 223 between plain nodes and 23 through clusters (12 into clusters, including 2 between clusters, and 11 out of clusters feeding 6 technologies). Written out as node-to-node edges the total would be 354.

---

## Optional Modules in the Tooling

| ID | Rule | Status |
|---|---|---|
| VIS-040 | Each technology has a module: `CORE` or an optional module. | Established architecture |
| VIS-041 | Playing without an optional module removes its technologies. | Established |
| VIS-042 | A technology that stays in the game and depended on a removed technology is not blocked. A dependency group made only of removed technologies becomes obsolete and is dropped. A group with some alternatives remaining needs one of those. | Established (stated 2026-11-09) |
| VIS-043 | The data check tries every combination of switched-off modules against VIS-042. | Current design |

VIS-042 refines MOD-004 and MOD-005 of the Modules topic, which do not yet say what happens to a core technology that depends on a module technology. **Proposal for the Modules topic:** *MOD-007: when an optional module is disabled, a dependency group consisting only of technologies of that module is obsolete; a group with remaining alternatives requires one of them.* This is a proposal, not an established rule.

---

## Views

| ID | Rule | Status |
|---|---|---|
| VIS-050 | Views are derived from the canonical graph by highlighting a set of nodes: `full`, `module`, `domain`, `path`, `chain`. | Current design |
| VIS-051 | Everything outside the highlighted set is dimmed in one of three ways: flat grey, the domain colour washed out, or removed entirely. | Current design |
| VIS-052 | A domain can be left out of every output. | Current design |
| VIS-053 | A path is an analytical route, a technology can be on several paths, and paths are not exclusive research programmes. | Established architecture (DP-044) |
| VIS-054 | Output files of filtered grid views carry the view and value in the file name. Simple-view files never do. | Current design |
| VIS-055 | In a filtered view, hidden or dimmed nodes keep their place in the grid. All views of the same data stay directly comparable. | Current design (the author is testing the effect) |

---

## Layout: the Virtual Grid

| ID | Rule | Status |
|---|---|---|
| VIS-060 | Columns are tiers, in numeric order. Only tiers that exist in the data get a column. | Current design |
| VIS-061 | Rows are grouped in one band per domain, in the configured order. | Established |
| VIS-062 | A domain band is as tall as the largest cluster of that domain across the early tiers, so every cluster in a domain occupies the same number of rows. Clusters are aligned at the top of their band. | Established |
| VIS-063 | A domain that has no cluster in a tier still reserves its band in that column, so bands stay aligned across all columns. | Current design |
| VIS-064 | One free row separates clusters. | Parameter (`row_offset`) |
| VIS-065 | A research centre occupies two rows. | Established |
| VIS-066 | From the late tier onward, a domain whose largest cluster exceeds its early band is centred on its own band. The alignment node (1-based) is n/2 for an even number of rows n and (n+1)/2 for an odd number. | Established |
| VIS-067 | Other domains in the late tiers keep their natural band position. If the whole range is not free they shift down as one unit, never split, so that one free row remains between clusters. | Established |
| VIS-068 | Late-tier clusters overflow into neighbouring bands instead of reserving space for the overflow. The author calls this a pragmatic solution. | Current design |
| VIS-069 | The first tier that counts as late is configuration. | Parameter (`late_tiers_from`, currently 7) |

Tiers 0 and 7 to 9 differ in content from tiers 1 to 6 (base facilities and national programmes against research), which is why they are laid out differently.

---

## Configuration

`tech_tree.toml` holds everything about presentation and locations. Every setting is required.

| Section | Controls |
|---|---|
| `[paths]` | `root` (relative to the configuration file), then the Tech List and the text, SVG and DOT folders (relative to `root`). |
| `[layout]` | Free rows between clusters; first late tier. |
| `[[domains]]` | Domain name and colour. The order of the entries is the vertical order of the bands. |
| `[colors]` | Default colour for unknown domains; how much darker a cluster box is than a node; the colours cycled through for OR groups. |
| `[dim.grey]`, `[dim.fade]` | How non-highlighted content looks. |
| `[dot_view]` | Graphviz graph and node attributes; also the grid spacing. |
| `[edge_views.*]`, `[node_views.*]`, `[cluster_view]` | Styles of edges, nodes by category, cluster boxes. |
| `[postprocess]` | Which tiers are drawn as full domain bands; corner radius of boxes. |
| `[check]` | The level of every data check. |

The code tests use a frozen copy of this file, so tuning the real configuration cannot break tests of the code. The real configuration is only tested for being valid.

---

## Data Checks

`--check` reads the CSV rows, prints a report and exits with status 1 on errors (and on warnings with `--strict`). It writes no files.

| ID | Rule | Status |
|---|---|---|
| VIS-070 | Each finding is rated by its consequence for the rules, not by how unusual it looks. **Error:** the tree is broken or breaks a design rule. **Warning:** probably unintended, but the rules still work. **Off:** an observation that is normal in this tree. | Current design |
| VIS-071 | The level of every check is configuration, so it can be retuned without changing code. | Established |
| VIS-072 | The checks apply the same dependency meaning as the views (VIS-030 to VIS-032, VIS-042). | Established architecture |

| Check | Default | Finds |
|---|---|---|
| `duplicate_id` | error | The same Tech_ID twice; the later row would silently replace the earlier. |
| `missing_field` | error | Empty Tech_ID, Domain, Domain_code or Tier; a Tier that is not a whole number. |
| `unknown_reference` | error | A dependency naming something that does not exist; a cluster row without technologies. |
| `unresearchable` | error | A technology that can never become eligible (a cycle or an unmeetable prerequisite). |
| `module_combination_blocked` | error | A technology that cannot be researched when some optional modules are off (VIS-042). |
| `module_loses_prerequisites` | warning | A technology left without any prerequisite when modules are off. |
| `redundant_dependency` | warning | A dependency group implied by another group of the same technology, or an entry listed twice. A cluster-wide gate is never reported. |
| `tier_higher`, `tier_same` | warning | A prerequisite only available from a later or the same tier. |
| `no_prerequisites` | warning | A technology of tier 2 or higher without any prerequisite. |
| `unknown_category` | warning | A category with no entry in `[node_views]`. |
| `id_mismatch` | warning | Tech_ID disagrees with Domain_code or Tier; one Domain_code used by several domains. |
| `domain_config` | warning | Domains in the data and in the configuration do not match. |
| `missing_name`, `missing_description` | warning | Empty Name or Description. |
| `unused_cluster_row` | off | A cluster row that nothing depends on and that has no dependencies itself. |

---

## Tests

| ID | Rule | Status |
|---|---|---|
| VIS-080 | A change to the code must not change the output unless that is intended. Golden DOT files and a fixture tree guard this. | Established |
| VIS-081 | The DOT files are written by this program, not by Graphviz, so golden files do not depend on the installed Graphviz version. | Current design |
| VIS-082 | Rendered SVGs are checked geometrically from the finished file (see topic 21). | Current design |
| VIS-083 | The tests need only the Python standard library. Tests that need Graphviz or the real Tech List skip themselves when those are absent. | Current design |
| VIS-084 | The real Tech List is tested only for integrity (no duplicate ids, missing fields, unknown references, unresearchable technologies). Design judgements are the designer's, not tests. | Current design |

The suite covers configuration, data and graph semantics, layout, every data check, rendering and the command line end to end. At the time of writing it has 97 tests. A deliberate-bug check (introducing known bugs one at a time into a scratch copy) was used to confirm that the tests detect them.

---

## Command Line

| Option | Purpose |
|---|---|
| `--file CSV` | Tech List for this run (default from configuration). |
| `--config FILE` | Configuration file (default `tech_tree.toml` next to the program). |
| `--check`, `--strict` | Data check only; strict also fails on warnings. |
| `--view`, `--filter`, `--dim` | Highlight in the grid view and how to dim the rest. |
| `--hide-domain NAME` | Leave a domain out of every output (repeatable). |
| `--notxt`, `--nosimple`, `--nogrd` | Skip an output. |
| `--nodot`, `--nosvg` | Do not keep DOT files (a temporary one is used); stop after the DOT files. |

Output files: `tech_tree.txt`, `tech_tree_simple.dot/.svg`, `tech_tree_grid[_<view>_<value>].dot/.svg`, in the configured folders.

---

## Exploration: Future Outputs

Nothing in this section is a project requirement.

| ID | Idea | Status |
|---|---|---|
| VIS-090 | Interactive website: filters, prerequisite exploration, module selection and research-state tracking, as anticipated by DP-015. | Exploration |
| VIS-091 | Blueprint-style printable technology cards. | Exploration |
| VIS-092 | A TripleA module. | Exploration (feasibility unknown) |
| VIS-093 | A JSON export of the canonical graph (nodes, positions, edges with member sets, colours) would be a common foundation for the three ideas above. | Exploration |
| VIS-094 | Tier column headers, domain labels and a legend in the grid view. | Exploration |

---

## Open Questions

| ID | Question | Status |
|---|---|---|
| VIS-100 | Should cluster dependencies stay as `X.*` rows in the data (originally created as helper items for DOT), or be replaced by an explicit notation in the dependency cells? The data should express game meaning, not renderer needs. | Open |
| VIS-101 | Is a quantifier other than "any one" needed for a dependency on a cluster (for example "two of four")? The tree has only AND and OR today. | Open |
| VIS-102 | Should hidden nodes keep the full footprint of their cluster box in `--dim none` views (VIS-055)? | Open (being tested) |
| VIS-103 | Should the representative node used for the simple view's cluster arrows follow a better rule than "first member"? | Open |
| VIS-104 | Should data errors stop a normal run, instead of only being reported by `--check`? | Open |
| VIS-105 | Exact module activation procedure (MOD-006) affects how module state would be represented in the tooling. | Open |

---

## Observations from the Data Checks (snapshot)

These are findings about the data at the time of writing (Tech List v8.8, 2026-11-09), not rules. They are for the designer to judge.

| Observation | Status |
|---|---|
| With VIS-042 applied, no technology is blocked in any combination of modules. | Observation |
| `N.2.05` has a tier-2 Tech_ID but is in tier 5. | Open |
| The Energy, Intelligence and Manufacturing research centres have no tier gate, while the Air, Land and Naval centres are gated by their tier-2 cluster. | Open |
| The rule "a research centre gates tier 4" is written as a cluster gate for Air, Land, Naval and Intelligence, and as direct dependencies on some technologies for Energy and Manufacturing. | Open |
| Ten technologies of tier 2 or higher have no prerequisite (`E.2.02`, `E.2.04`, `E.3.01`, `E.3.02`, `E.4.05`, `I.3.01`, `M.2.05`, `M.2.06`, `M.3.01`, `M.4.06`). Some may be intentional. | Open |
| `M.6.02` listed `M.5.02` both inside an OR group and on its own, so the OR changed nothing. Corrected by the author. | Resolved |

---

## Relationship to Other Topics

- **21-graphviz-svg** documents how the renderers draw the views.
- **Modules** defines the module architecture; VIS-040 to VIS-043 depend on it and propose MOD-007.
- **Design Principles** supply DP-002, DP-003, DP-012, DP-013, DP-014, DP-015, DP-019, DP-044 and DP-045.
