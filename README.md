# Axis & Allies 1940 Global – Research & Development System

This project adds a modular **Research & Development (R&D) system** to Axis & Allies Global 1940. It is a civilization-style system where you research technologies, which open up new technologies on turn. The technologies offer perks in different areas. This is the development repository where all the materials for the game are gathered, including add-ons and the possibility to in- or exclude them:

- CORE: the technology tree including deleopment paths in different domains: Land, Naval, Air, Production, Energy and Intelligence.
- NUCLEAR: Develop the nuclear bomb and a means to drop it.
- OIL: Finding and refining oil to allow your logistics to function.
- OCCULTISM: Alternate history module to include the myths about Germany's occult research.
- ToDo - ZOMBIES: Alternate reality module to integrate Axis & Allies & Zombies into Axis & Allies 1940 Global.


## Gameplay

Players can invest in technologies that unlock new capabilities, units, facilities, resources, and strategic options, during their Purchase and Repair phase, for 1 Research Token. Technology will become effective during the Deployment phase. Contrary to the stock R&D mode there is far less luck involved, but still a bit: on a D6 roll 1 means failure, 2-5 means choosing a valid tech (when all dependencies are met) and 6 means choosing a valid tech for free (you may keep your Research Token). Research is deliberately separated from production and construction:

* **Research Points (RP)** represent individual research attempts. Each attempt costs 1 RP and targets an eligible technology.
* **Technology prerequisites** determine which technologies are available for research. Eligibility is checked at the start of the turn, preventing research from cascading through the tree in a single turn.
* **Research is uncertain but strategic:** players choose their research targets, with successful research advancing their technological capabilities while breakthroughs can preserve the invested RP for the following turn.
* **Technologies unlock capabilities rather than automatically providing physical assets.** Facilities and bases must generally be constructed or purchased separately.
* **Facilities are physical game pieces** placed on the map. They provide specialised capabilities and can be damaged, captured, and rendered inoperative according to their rules.
* **Air Bases and Naval Bases** are distinct from other facilities and provide operational capabilities such as extended unit range, scrambling, servicing, and repairs.
* **Resources** such as Oil, Aluminium, Steel, Heavy Water, Uranium, and Vril are separate from technologies and may form part of optional strategic-resource modules.
* The technology tree is designed with **multiple technological routes and national specialisation**, allowing players to pursue different strategic approaches rather than a single optimal progression.

The system is modular: the core R&D rules can be used with optional expansions such as strategic resources, additional facilities, and other technology modules. It is designed for compatibility with both **Global 1940** and **Global 1940 Halifax**.


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

The repository is maintained using Git and GitHub. The `main` branch contains the current working version. Historical development versions are preserved under `archive/`.

Since of v10.2 Github is handling the version history.


## Usage

`$ python3 src/tech_tree.py --help`
 
```
usage: tech_tree.py [-h] [--view {full,module,domain,path,chain}] [--filter VALUE] [--dim {grey,fade,none}]
                    [--hide-resource] [--notxt] [--nodot] [--nosvg] [--nosimple] [--nogrd]
                    input_file

Axis & Allies R&D Tech Tree Generator

positional arguments:
  input_file            CSV data file path

options:
  -h, --help            show this help message and exit
  --view {full,module,domain,path,chain}
                        View type: full (default), module, domain, path, or chain. Use --filter to specify the
                        value.
  --filter VALUE        Value for --view: module name (NUCLEAR), domain name (Air), or node ID for chain view
                        (P.9.NU).
  --dim {grey,fade,none}
                        How to display non-highlighted nodes: grey (flat grey), fade (washed-out domain colour),
                        none (remove entirely). Default: grey.
  --hide-resource       Exclude all Resource domain nodes from the output.
  --notxt               Skip text file output.
  --nodot               Skip writing DOT files (both renderers).
  --nosvg               Skip SVG generation (both renderers).
  --nosimple            Skip the simple Graphviz dot renderer entirely.
  --nogrd               Skip the grid neato renderer entirely.
```

`$ python3 src/tech_tree.py data/research/Axis\ \&\ Allies\ Research\ \&\ Development\ -\ tech\ tree\ -\ Tech\ List.csv `

This will generate a dot-file (in .) from the csv-file, which is than converted to a svg-file (also in .) that contains the Tech tree.

