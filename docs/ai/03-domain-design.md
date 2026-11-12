# Topic: Domain Design

Last updated: 2026-11-09
Status: Active

## Purpose

Define and maintain the domain structure used by the Axis & Allies Global 1940 R&D technology tree.

Domains provide the primary technological classification of nodes and also structure the visual technology tree. They must distinguish technological identity from cross-domain relationships such as paths, resources, facilities, and prerequisites.

The domain structure is currently considered stable enough for implementation, but its boundaries have not yet been formally audited against every technology node. A dedicated domain-definition and boundary review is planned for the later balancing phase.

## Current Domain Structure

| Code | Domain | Current conceptual scope |
|---|---|---|
| A | Air | Aircraft, aviation, air warfare and related aviation systems |
| L | Land | Ground warfare, tanks, armour, artillery and related land capabilities |
| N | Naval | Surface ships, submarines, naval propulsion, naval weapons and naval warfare |
| I | Intelligence | Intelligence, reconnaissance, espionage, counter-intelligence and information capabilities |
| E | Energy | Nuclear physics, atomic energy, advanced energy and fundamental physical-science technologies |
| M | Manufacturing | Industrial production, manufacturing, logistics, transportation and supporting infrastructure |
| P | Programs | Large-scale or exceptional technological/development programmes |
| R | Research | Technology to boost the research capabilities |

The domain is a property of the technology model and is not merely a Graphviz presentation category.

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

Air, Land and Naval are the clearest military domains.

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

A nuclear submarine remains primarily Naval because its primary capability is a submarine platform, even though nuclear propulsion creates an Energy And Physics relationship.

## Energy And Physics

Energy And Physics covers fundamental or enabling physical science, particularly:

- nuclear physics;
- atomic energy;
- nuclear weapons research;
- advanced energy technologies;
- related physical-science breakthroughs.

It must not become a catch-all for everything involving nuclear weapons.

The distinction is:

- nuclear physics → Energy And Physics;
- nuclear submarine → Naval;
- nuclear propulsion used as a naval capability → potentially Naval;
- uranium/heavy water → Resource.

## Logistics And Industry

This domain represents industrial and logistical capability itself, including:

- industrial production;
- manufacturing;
- logistics;
- transportation;
- supporting infrastructure;
- industrial processes.

A cross-domain industrial effect does not require the technology to be duplicated into Air, Land and Naval.

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

The current Occultism Germany P.3–P.6 programme is therefore retained under Programs for now rather than creating a new `Specials` domain solely for it.

## Resources

Resources are not conceptually equivalent to technological domains.

Resources are strategic/material inputs that can be used by technologies across multiple domains.

Examples include:

- uranium;
- heavy water;
- other strategic materials.

Resource requirements are distinct from:

- technology prerequisites;
- facility requirements.

The current `Resource` classification exists in the tree and data model, but its status as a true peer technological domain remains a design question for the later domain audit.

## Research Centres and Facilities

Research Centres require a distinction between **general research infrastructure** and **domain-specific research infrastructure**.

### Domain-specific Research Centres

A Research Centre can belong to a specific technological domain.

Examples:

- Naval Research Centre → Naval;
- Air Research Centre → Air;
- other domain-specific Research Centres → their respective domains.

These facilities can interact with technological eligibility and therefore have a meaningful relationship with the domain structure.

A Research Centre's domain does **not** mean that every technology it supports belongs to that domain; the technology's own primary capability remains the classification criterion.

### General Research Facilities

Some research infrastructure is inherently general rather than domain-specific.

Current examples:

- Basic Research Facility;
- University.

These currently represent only two general R&D nodes and do not justify creating a separate technological domain merely to contain them.

Their potential role in a general Research Point (RP) economy remains an open design area.

## `RCENTER` Data-Model Category

`RCENTER` is a data-model category for Research Centre nodes.

It is not itself a technological domain.

A node may therefore be:

- category = `RCENTER`;
- domain = `Naval`;

for a Naval Research Centre.

This distinction must be preserved.

## Current Classification Model

The conceptual structure is currently:

```text
TECHNOLOGICAL DOMAINS
├── Air
├── Land
├── Naval
├── Intelligence
├── Energy And Physics
├── Logistics And Industry
└── Programs

CROSS-CUTTING / SPECIAL CATEGORIES
├── Resources
└── General Research Infrastructure

DOMAIN-SPECIFIC INFRASTRUCTURE
├── Air Research Centre
├── Naval Research Centre
├── ...
└── other domain-specific Research Centres
```

The exact implementation representation of these categories may differ from this conceptual structure.

## Current Decision: Do Not Add `Specials`

A `Specials` domain has **not** been added.

Reasons:

1. Basic Research Facility and University are general R&D infrastructure rather than a technological field.
2. They are currently too few to justify a separate visual/technological domain.
3. Occultism P.3–P.6 already has a plausible home under Programs.
4. Creating `Specials` risks turning it into a miscellaneous bucket for nodes that do not fit elsewhere.
5. A new domain should represent a coherent technological area, not merely solve a small number of awkward classifications.

This decision is provisional and may be revisited if future design work produces a sufficiently coherent body of "special" technologies.

## Current Problem

Some existing technology nodes do not fit comfortably within the current domains.

This is recognized as a taxonomy issue rather than evidence that the entire domain architecture is wrong.

Typical causes include:

- platform + enabling technology overlap;
- weapon + scientific basis overlap;
- industrial technology with military consequences;
- resource/technology overlap;
- programme versus conventional technology;
- genuinely interdisciplinary technologies.

The intended solution is **not** to automatically create a new domain for every cross-domain case.

## Planned Domain Audit

A formal **Domain Definition & Boundary** review is planned for the later balancing phase.

For each domain, the review should establish:

| Domain | Core definition | Includes | Excludes | Borderline cases |
|---|---|---|---|---|
| Air | TBD | TBD | TBD | TBD |
| Land | TBD | TBD | TBD | TBD |
| Naval | TBD | TBD | TBD | TBD |
| Intelligence | TBD | TBD | TBD | TBD |
| Energy And Physics | TBD | TBD | TBD | TBD |
| Logistics And Industry | TBD | TBD | TBD | TBD |
| Programs | TBD | TBD | TBD | TBD |
| Resource | TBD | TBD | TBD | TBD |

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
- treat Resources as ordinary technologies;
- treat `RCENTER` as a domain;
- assume that a Research Centre's domain determines the domain of technologies it supports;
- redesign the domain taxonomy during routine technology-tree implementation.

## Open Questions

The following remain intentionally unresolved until the planned domain audit:

- Formal one-sentence definition for every domain.
- Exhaustive inclusion/exclusion criteria for every domain.
- Whether Resource should remain visually represented as a domain or become a separate model layer.
- Whether Programs should remain a domain or become another classification mechanism.
- Whether any current domain should be split.
- Whether any domains should be merged.
- Whether a new domain is justified by currently problematic nodes.
- Whether any technologies should support multiple domain classifications.
- Formal tie-breaker for genuinely interdisciplinary technologies.
- Exact mechanical relationship between general research infrastructure and the RP economy.
- Whether the general R&D nodes eventually justify a `General Research` domain or another classification.

## Important Rejected/Deferred Approach

Do not introduce `Specials` simply because:

- Basic Research Facility;
- University;
- Occultism P.3–P.6

do not fit neatly into the current conventional technological domains.

These are three different classification problems and should not be artificially grouped under a generic "Specials" label.

## Implementation Status

The current Graphviz architecture uses domain+tier combinations as visual clusters.

The domain is stored in the authoritative technology-node record and is therefore part of the model rather than being generated solely during presentation.

The current architecture should remain unchanged while the domain taxonomy is deferred for balancing review.

## Next Action

During the balancing phase, perform the Domain Definition & Boundary audit against the complete technology dataset.

Do not redesign the domains before that audit.

The audit should first determine whether each problematic node represents a genuine taxonomy gap or merely a cross-domain relationship that should be expressed through paths, prerequisites, resources or facilities.

## Source / Authority

The domain model is based on the project's accumulated R&D design discussions and the current technology-tree architecture.

The domain-design recap records the established principles, current domain structure, unresolved questions, and planned audit. It should be treated as the durable handover context for future AI sessions working on domain classification.
