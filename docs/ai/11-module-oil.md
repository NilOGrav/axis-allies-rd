# Topic: Oil Module

Last updated: 2026-11-09
Status: Active

## Purpose

The Oil module introduces Oil as an optional strategic resource system for Axis & Allies Global 1940.

The module is intended to support two use cases:

1. Integration into the project's broader R&D system.
2. Standalone use as a drop-in optional expansion for vanilla Axis & Allies Global 1940.

The module is designed to create strategic value around geographically concentrated oil resources without introducing excessive physical resource-transport or per-unit fuel bookkeeping.

## Current design

Oil is a separate national resource/currency alongside IPCs.

Oil is produced from oil-bearing territories and spent according to the operational rules of the Oil module. Oil does not need to be physically transported between territories or represented by individual resource shipments.

Some oil-bearing territories have a predefined production value greater than 1 Oil per turn.

Oil production may be naturally available at certain starting oil locations, while other oil locations can require development through Oil infrastructure.

The current established infrastructure concept includes Oil Derricks for land-based extraction and Oil Platforms for offshore extraction.

## Established decisions

- Oil is a distinct resource from IPCs.
- Oil is also distinct from technologies and facilities in the data model.
- Oil is an abstract national resource rather than a physically transported commodity.
- Geography remains strategically important because Oil production is tied to specific territories.
- Oil-bearing territories may have different production values.
- A territory's Oil production value is collected as a whole rather than requiring one infrastructure unit per Oil produced.
- **One Oil Derrick is sufficient to exploit the complete producible Oil value of a territory.**
- A territory producing 2 Oil therefore requires one Derrick, not two.
- A territory producing 1 Oil also requires one Derrick where a Derrick is required.
- Multiple Derricks are not required merely because a territory produces multiple Oil per turn.
- Some oil-producing locations can produce without first requiring an Oil Derrick.
- Oil infrastructure and technologically enhanced extraction are conceptually distinguishable.
- Oil is intended to remain an optional module rather than becoming an implicit part of the core R&D system.
- The Oil module should be capable of existing independently from the R&D system.

## Current implementation

The Oil concept currently distinguishes:

### Land oil

Oil-bearing land territories can have a defined Oil production value.

Where development is required, an Oil Derrick activates the territory's available production.

The Derrick represents the infrastructure required to exploit the oil field rather than representing an individual unit of Oil production.

### Offshore oil

Oil Platforms provide the corresponding infrastructure concept for offshore oil extraction.

The detailed distinction between ordinary and R&D-enhanced Oil Platforms remains part of the wider module design.

### R&D interaction

The Oil module is intended to interact with the R&D system through technologies that can improve or unlock extraction capabilities.

The precise implementation of these interactions should remain in the authoritative research/design data rather than being duplicated here.

## Open questions

- Exact rules for which oil territories produce naturally and which require infrastructure.
- Exact Oil production values for all oil-bearing territories, unless established in the authoritative resource data.
- Exact cost and construction rules for Oil Derricks.
- Exact cost and construction rules for Oil Platforms.
- Exact distinction between ordinary/basic oil infrastructure and technologically enhanced infrastructure.
- Exact technological prerequisites for advanced land and offshore extraction.
- Exact operational situations in which Oil is consumed.
- Exact Oil storage/capacity rules, if any.
- Exact consequences of insufficient Oil.
- Exact interaction between Oil and other optional modules.
- Exact TripleA implementation of Oil as a resource.

These questions must not be resolved merely by inference from earlier proposals.

## Known constraints

- The module should avoid unnecessary micromanagement.
- Physical transportation of Oil is not part of the established concept.
- Oil must remain semantically distinct from technologies.
- Oil infrastructure must remain distinguishable from technologies and from Research Centres.
- Optional Oil rules must not silently become core R&D rules.
- Detailed numerical rules should be taken from the current authoritative design data when available.
- Previously discussed illustrative costs, penalties, storage limits and specific technologies are not automatically established decisions.

## Relevant project files

- `docs/ai/README.md` — AI handover/memory methodology.
- `docs/ai/03-resources.md` — resource architecture and terminology, when present in the current repository.
- `docs/ai/04-facilities.md` — facility architecture and infrastructure terminology, when relevant.
- `docs/ai/08-oil.md` — permanent Oil topic memory, when present/current.
- `docs/ai/99-open-questions.md` — unresolved cross-topic design questions.
- `data/research/` — authoritative R&D design data, including the current ODS where applicable.
- `data/research/` — current Oil-related design data if incorporated into the research dataset.

## Important terminology

- **Oil** — the strategic resource/currency introduced by this module.
- **Oil production value** — the amount of Oil a resource territory can produce per turn.
- **Oil Derrick** — land-based oil extraction infrastructure.
- **Oil Platform** — offshore oil extraction infrastructure.
- **Oil-bearing territory** — a territory containing a defined Oil resource.
- **Natural/starting production** — Oil production that does not require prior construction of an Oil Derrick.
- **R&D-enhanced extraction** — technologically enabled or improved oil extraction; exact implementation remains to be established.

## Recent changes

- Established that Oil-bearing territories may produce more than 1 Oil per turn.
- Established that **one Oil Derrick activates the complete Oil production value of a territory**, rather than requiring one Derrick for every Oil produced.
- Confirmed that this rule is intended to reduce infrastructure micromanagement while preserving the strategic value of Oil-producing territories.
- Confirmed that Oil remains an optional module usable both with the R&D system and as a standalone G40 expansion.

## Do not assume

The following have been discussed or proposed but should not be treated as established unless confirmed elsewhere in the authoritative project data:

- Specific Oil Derrick costs.
- Specific Oil Platform costs.
- Specific Oil production values beyond values explicitly established in the current design data.
- Oil storage limits.
- Specific operational Oil consumption costs.
- Specific penalties for Oil shortages.
- Emergency fuel rules.
- Specific Oil technologies.
- Specific research costs for Oil technologies.
- Specific rules for convoy disruption or strategic bombing of Oil production.
- Specific TripleA implementation details.

In particular, the earlier exploratory Oil rule proposals should not be promoted to established design merely because they appeared in previous discussion.

## Next intended work

- Maintain the Oil module as a separate permanent topic in the AI-memory structure.
- Transfer established Oil decisions into the appropriate authoritative project data.
- Define the remaining Oil resource and infrastructure rules.
- Define the precise interaction between Oil and R&D technologies.
- Define the standalone vanilla-G40 Oil rules independently enough that the module does not depend on the full R&D system.
- Record unresolved cross-topic questions in `99-open-questions.md` where appropriate.
- Keep this topic handover focused on architecture, decisions and implementation conventions rather than duplicating the complete Oil dataset.
