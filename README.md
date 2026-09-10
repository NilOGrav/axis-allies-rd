# Axis & Allies 1940 Global – R&D System

Development repository for the custom Research & Development system for
Axis & Allies 1940 Global. It is a civilization-style system where you research technologies, 
which open up new technologies on turn. There is also the possibility to in- or exclude add-ons:
- NUCLEAR: Develop the nuclear bomb and a means to drop it.
- OIL: Finding and refining oil to allow your logistics to function.
- OCCULTISM: To include the myths that Germany did occult resrearch.
- ToDo - ZOMBIES: to integrate Axis & Allies & Zombies into Axis & Allies 1940 Global

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
- neato
- SVG, CSV, DOT

## Development

The repository is maintained using Git and GitHub.

The `main` branch contains the current working version.
Historical development versions are preserved under `archive/`.

Since of v10.2 Github is handling the version history.

Usage:

$ python3 src/tech_tree.py data/research/Axis\ \&\ Allies\ Research\ \&\ Development\ -\ tech\ tree\ v8.Y.csv

This will generate a dot-file (in .) from the csv-file, which is than converted to a svg-file (also in .) that contains the Tech tree.

