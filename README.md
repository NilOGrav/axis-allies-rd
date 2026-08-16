# Axis & Allies 1940 Global – R&D System

Development repository for the custom Research & Development system for
Axis & Allies 1940 Global.

## Project structure

- `src/` — current Python source code
- `data/research/` — current research spreadsheets and CSV data
- `data/config/` — configuration data
- `graph/dot/` — Graphviz source files
- `graph/generated/` — generated graph output
- `assets/` — visual assets
- `docs/` — rules and project documentation
- `tests/` — automated tests
- `archive/` — historical versions of scripts and tech sheets
- `output/` — generated project output

## Tools

The project uses:

- Python
- Graphviz
- LibreOffice Calc
- SVG

## Development

The repository is maintained using Git and GitHub.

The `main` branch contains the current working version.
Historical development versions are preserved under `archive/`.

Usage:
$ python3 tech_tree.9.1.py Axis\ \&\ Allies\ Research\ \&\ Development\ -\ tech\ tree\ v7.8.csv
$ dot -Tsvg tech_tree.dot -o tech_tree.svg 


