# Topic: Domain Design

Last updated: 2026-11-09  
Status: Active

## Purpose

Define and maintain the domain structure used by the Axis & Allies Global 1940 R&D technology tree.

Domains provide the primary technological classification of nodes and also structure the visual technology tree. They must distinguish technological identity from cross-domain relationships such as paths, resources, facilities, and prerequisites.

The current domain structure is established in the technology-tree configuration. The conceptual boundaries and classification of every technology have not yet been fully audited.

## Current Domain Structure

The current technology-tree configuration defines eight domains:

| Code | Domain | Current conceptual scope |
|---|---|---|
| A | Air | Aircraft, aviation, air warfare and related aviation systems |
| L | Land | Ground warfare, tanks, armour, artillery and related land capabilities |
| N | Naval | Surface ships, submarines, naval propulsion, naval weapons and naval warfare |
| P | Programs | Large-scale or exceptional technological/development programmes |
| R | Research | General research and research-related technological development |
| M | Manufacturing | Industrial production, manufacturing, logistics, transportation and supporting industrial infrastructure |
| I | Intelligence | Intelligence, reconnaissance, espionage, counter-intelligence and information capabilities |
| E | Energy | Physics, energy technologies, nuclear technology and related physical-science capabilities |

The exact domain code is part of the technology data model.

The domain is also used by the Graphviz technology-tree presentation to create domain/tier clusters. It is therefore both a model property and a visual classification.

## Current Domain Names

The current names are:

- `Air`
- `Land`
- `Naval`
- `Programs`
- `Research`
- `Manufacturing`
- `Intelligence`
- `Energy`

Do not use the older names:

- `Energy And Physics`
- `Logistics And Industry`
- `Resource`

as current domain names.

`Resource` remains an important data-model/category concept, but is no longer a current technological domain.

## Core Domain Principle

A technology should normally be assigned to the domain representing its **primary technological capability**, rather than every field it interacts with.

Cross-domain relationships should normally be represented through:

- dependencies;
- paths;
- resources;
- facilities;
- modules;
- other explicit relationships.

A technology participating in multiple technological paths does not therefore need multiple domains.

The domain answers:

> What is the primary technological identity of this technology?

It does not answer:

> What other systems does this technology interact with?

## Domain vs Path

A domain is the primary classification of a technology.

A path is an analytical/strategic technological route.

Paths may cross domains, and a technology may belong to multiple paths.

Path membership therefore does not redefine domain membership.

## Domain vs Historical Organization

Domains represent game-design technological/functional areas, not historical ministries, armed forces or research organizations.

The question for classification is:

> What technological capability does this node represent in the game?

not:

> Which historical organization developed it?

Historical inspiration is relevant, but does not determine domain membership by itself.

## Air / Land / Naval

Air, Land and Naval are the major military technology domains.

### Air

Primarily covers:

- aircraft;
- aviation;
- air combat;
- air power;
- aircraft performance and armament;
- related aviation systems.

### Land

Primarily covers:

- ground warfare;
- tanks;
- armoured vehicles;
- artillery;
- ground combat systems;
- related land-war capabilities.

Example: Landkreuzer P.7 remains associated with the Land/TANK route despite its unusual size and character.

### Naval

Primarily covers:

- surface warships;
- submarines;
- naval propulsion;
- naval weapons;
- carriers;
- naval warfare systems.

A nuclear submarine remains primarily Naval because its primary capability is a submarine platform, even though nuclear propulsion creates a relationship with Energy.

## Energy

The current domain name is **Energy**, replacing the older `Energy And Physics` terminology.

Energy covers physical-science and energy-related technological capabilities, particularly:

- nuclear physics;
- atomic energy;
- nuclear technology;
- advanced energy technologies;
- related physical-science breakthroughs.

It must not become a catch-all for everything involving nuclear weapons.

The distinction remains:

- nuclear/atomic technology → Energy;
- nuclear submarine → Naval;
- nuclear propulsion represented as part of a naval platform → primarily Naval;
- uranium/heavy water → Resource/category rather than Energy domain merely because they are used by nuclear technology.

## Manufacturing

The current domain name is **Manufacturing**, replacing the older `Logistics And Industry` terminology.

Manufacturing represents the industrial and logistical capability itself, including:

- industrial production;
- manufacturing;
- logistics;
- transportation;
- supporting industrial infrastructure;
- industrial processes.

A cross-domain industrial effect does not require the technology to be duplicated into Air, Land and Naval.

The purpose of Manufacturing is therefore broader than simply “technologies that improve unit production”. It represents the underlying production and industrial capability.

## Intelligence

Intelligence represents technological/organizational capabilities based around:

- intelligence gathering;
- reconnaissance;
- espionage;
- counter-intelligence;
- information advantages.

It is a distinct capability area rather than a subcategory of Air, Land or Naval.

## Programs

Programs represent large-scale, exceptional or otherwise non-standard development programmes rather than necessarily conventional technological disciplines.

Programs must **not become a generic miscellaneous category**.

If a node represents a normal technological capability that clearly belongs to another domain, it should normally use that domain instead.

The current Occultism Germany P.3–P.6 programme remains associated with Programs rather than requiring a generic `Specials` domain.

## Research

**Research** is now an explicit domain in the current technology-tree configuration.

This replaces the earlier assumption that general research infrastructure should necessarily remain outside the domain structure.

The Research domain represents research-oriented technological development and the R&D infrastructure/technology represented by the corresponding tree nodes.

The exact boundary between:

- Research as a technological domain;
- Research Centres as facilities/data-model categories;
- general research infrastructure;
- research-economy effects;

must remain consistent with the relevant facility and research-system definitions.

A Research Centre (`RCENTER`) is **not itself a domain**.

A Research Centre may nevertheless be associated with a domain where the facility is domain-specific.

## Resources

`Resource` is no longer treated as one of the current technology domains.

Resources remain a distinct conceptual/data-model layer.

Resources are strategic/material inputs that can be used by technologies across multiple domains.

Examples include:

- uranium;
- heavy water;
- oil;
- other strategic materials.

Resource requirements are distinct from:

- technology prerequisites;
- facility requirements.

The current data model also uses `RESOURCE` as a category for resource-related technology-tree nodes. This category must not be confused with the current domain list.

Thus:

```text
Domain = Energy
Category = RESOURCE
```

is conceptually possible where the data model requires both classifications, without making Resource a domain.

### Research Centres and Facilities

Research Centres require a distinction between **facility category** and **domain**.

### `RCENTER` Data-Model Category

`RCENTER` is a data-model category for Research Centre nodes.

It is not itself a technological domain.

A node may therefore conceptually be:

```text
Category = RCENTER
Domain   = Naval
```

for a Naval Research Centre.

Likewise, a Research Centre may be associated with Research or another domain where appropriate.

The facility's domain does not redefine the domain of every technology it supports.

#### Domain-specific Research Centres

A Research Centre can be associated with a specific technological domain.

Examples may include:

- Naval Research Centre → Naval;
- Air Research Centre → Air;
- other domain-specific Research Centres → their respective domains.

These facilities can interact with technological eligibility and therefore have a meaningful relationship with the domain structure.

### General Research Infrastructure

<<<<<<< HEAD
Research-related facilities that are not themselves technological-domain nodes must remain distinguishable from the Research domain.

The exact mechanical relationship between general research infrastructure, Research Centres and the Research Token economy remains a separate design question.
=======
#### General Research Facilities

Some research infrastructure is inherently general rather than domain-specific.

Current examples:

- Basic Research Facility;
- University.

These currently represent only two general R&D nodes and do not justify creating a separate technological domain merely to contain them.

Their potential role in a general Research Point (RP) economy remains an open design area.

#### `RCENTRE` Data-Model Category

`RCENTRE` is a data-model category for Research Centre nodes.

It is not itself a technological domain.

A node may therefore be:

- category = `RCENTRE`;
- domain = `Naval`;

for a Naval Research Centre.

This distinction must be preserved.

## Current Classification Model

The current conceptual structure is:

```text
TECHNOLOGICAL DOMAINS
├── Air
├── Land
├── Naval
├── Programs
├── Research
├── Manufacturing
├── Intelligence
└── Energy

CROSS-CUTTING DATA-MODEL / GAME ELEMENTS
├── Resources
├── Facilities
├── Research Centres
├── Paths
└── Modules
```

The exact implementation representation of these concepts may differ from this conceptual structure.

The important distinction is that `Resource`, `Facility`, `RCENTER`, `Path`, and `Module` are not automatically additional technological domains.

## Current Decision: Do Not Add `Specials`

A `Specials` domain has **not** been added.

Reasons:

1. Awkward classification should not automatically produce a miscellaneous domain.
2. Programs already provides an appropriate home for genuine large-scale/special development programmes.
3. Research now exists as an explicit domain where research-oriented technologies require one.
4. Creating `Specials` risks turning it into a miscellaneous bucket for nodes that do not fit elsewhere.
5. A new domain should represent a coherent technological area, not merely solve a small number of awkward classifications.

This decision may be revisited if future design work produces a sufficiently coherent body of technology that cannot be represented by the existing domains.

## Current Problem

Some technology nodes may still not fit comfortably within the current domains.

This is recognized as a taxonomy/classification issue rather than evidence that the entire domain architecture is wrong.

Typical causes include:

- platform + enabling technology overlap;
- weapon + scientific basis overlap;
- industrial technology with military consequences;
- resource/technology overlap;
- programme versus conventional technology;
- research infrastructure versus research technology;
- genuinely interdisciplinary technologies.

The intended solution is **not** to automatically create a new domain for every cross-domain case.

## Planned Domain Audit

A formal **Domain Definition & Boundary** review should eventually establish, for each current domain:

| Domain | Core definition | Includes | Excludes | Borderline cases |
|---|---|---|---|---|
| Air | TBD | TBD | TBD | TBD |
| Land | TBD | TBD | TBD | TBD |
| Naval | TBD | TBD | TBD | TBD |
| Intelligence | TBD | TBD | TBD | TBD |
| Energy | TBD | TBD | TBD | TBD |
| Manufacturing | TBD | TBD | TBD | TBD |
| Programs | TBD | TBD | TBD | TBD |
| Research | TBD | TBD | TBD | TBD |

Every problematic node should then be classified as one of:

1. correctly classified;
2. incorrectly classified;
3. affected by an unclear domain boundary;
4. requiring a new domain;
5. better represented as Resource, Facility, Program or another category;
6. legitimately cross-domain but requiring only one primary domain.

## Design Constraints

Do not:

- create a new domain merely because a technology interacts with multiple domains;
- use Programs as a generic miscellaneous category;
- treat Resources as an ordinary technological domain;
- treat `RESOURCE` as equivalent to the Resource domain from the old model;
- treat `RCENTER` as a domain;
- assume that a Research Centre's domain determines the domain of technologies it supports;
- redesign the domain taxonomy during routine technology-tree implementation;
- use obsolete domain names in new data or documentation.

## Open Questions

The following remain intentionally unresolved until the planned domain audit:

- Formal one-sentence definition for every current domain.
- Exhaustive inclusion/exclusion criteria for every current domain.
- Formal boundary between Research-domain technologies and Research Centre facilities.
- Exact mechanical relationship between Research domain content and the research economy.
- Formal tie-breaker for genuinely interdisciplinary technologies.
- Whether every current domain should remain permanent.
- Whether any current domain should be split.
- Whether any domains should be merged.
- Whether a new domain is justified by currently problematic nodes.
- Whether any technologies should support multiple domain classifications.

## Important Terminology Rule

The current domain names are authoritative for new documentation and implementation:

```text
Air
Land
Naval
Programs
Research
Manufacturing
Intelligence
Energy
```

Do not reintroduce the obsolete names:

```text
Energy And Physics
Logistics And Industry
Resource
```

when referring to the current domain structure.

`Resource` remains valid as a resource/category concept; it is simply not one of the eight current domains.

## Implementation Status

The current Graphviz architecture uses domain+tier combinations as visual clusters.

The domain is stored in the authoritative technology-node record and is therefore part of the model rather than being generated solely during presentation.

The current configured domain order is:

```text
Air
Land
Naval
Programs
Research
Manufacturing
Intelligence
Energy
```

The CSV determines which domains actually exist; the presentation configuration defines their visual order and presentation properties.

## Next Action

During the balancing/classification phase, perform the Domain Definition & Boundary audit against the complete technology dataset.

Before changing domain membership, verify the actual current technology data.

The audit should first determine whether each problematic node represents:

- a genuine taxonomy gap;
- an incorrect classification;
- a cross-domain relationship that should instead be expressed through paths, prerequisites, resources or facilities;
- or a category distinction such as Resource, Facility or Research Centre.

## Source / Authority

The current domain names and visual domain configuration are defined by the project's technology-tree data/configuration.

The AI-memory document records the conceptual classification principles, current domain structure, unresolved boundaries, and implementation constraints.

Where this document conflicts with the current technology-tree data, the current project data takes precedence.
