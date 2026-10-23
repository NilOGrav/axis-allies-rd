"""Axis & Allies R&D tech tree tools.

The CSV defines the technology tree. The config file defines how it
is shown. Renderers turn the one canonical graph into views.

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

Modules: settings (config), data (CSV and graph), views (styling and
filters), layout (virtual grid), render_text, render_dot (simple),
render_grid and svg_postprocess (grid), output (file locations), util.
"""
