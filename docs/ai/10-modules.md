# Topic: Modules

Last updated: 2026-11-09
Status: Active

## Purpose

Define the modular architecture of the Axis & Allies Global 1940 R&D system and document the rules governing optional modules.

The module architecture allows the core R&D system to remain stable while optional systems add technologies, facilities, resources, capabilities, or specialised rules.

The module framework must support:

- the core R&D system operating independently;
- optional modules being enabled or disabled without redesigning the core;
- modules introducing their own technologies, facilities, resources, and/or rules;
- interaction between modules where explicitly designed;
- future expansion without changing the fundamental R&D architecture;
- compatibility with both Global 1940 and Global 1940 Halifax.

---

## Core Module Architecture

The R&D system is explicitly modular.

| ID | Rule | Status |
|---|---|---|
| MOD-001 | The R&D system is modular. | Established |
| MOD-002 | Optional modules can be added without altering the core research framework. | Established |
| MOD-003 | A module can introduce its own technologies, facilities, resources or rules. | Established |
| MOD-004 | Core R&D remains playable without optional modules. | Established |
| MOD-005 | Module-specific eligibility and effects are only active when the relevant module is enabled. | Established architecture |
| MOD-006 | Exact module activation/configuration procedure. | Open |

The modular architecture is a structural principle, not merely a list of optional expansions.

A module should therefore be capable of being added without requiring changes to unrelated core R&D rules.

---

## Core vs Optional Modules

The architecture distinguishes between:

### Core R&D

The core system contains the fundamental research framework:

- Research Points;
- research attempts;
- technology eligibility;
- prerequisite logic;
- technology acquisition;
- research timing;
- research resolution;
- technology effects;
- the canonical technology tree.

Core R&D must remain playable without optional modules.

### Optional Modules

Optional modules extend the system with specialised mechanics.

Examples currently include:

- Oil;
- Zombies;
- Nuclear;
- other resource/mechanical extensions as they are developed.

A module may add one or more of:

- technologies;
- facilities;
- resources;
- unit capabilities;
- eligibility conditions;
- production rules;
- strategic effects;
- specialised rules.

---

## Module Activation

The architecture establishes that module-specific rules only apply when their module is enabled.

However, the exact player-facing procedure for configuring/enabling modules has **not yet been formally established**.

This remains:

**MOD-006 — Open**

The eventual rule should define, at minimum:

- how players determine which modules are active;
- whether modules are selected before the game;
- whether module selection is globally agreed or individually configurable;
- how module dependencies are handled;
- how module-specific technologies/facilities/resources enter the game;
- how configuration is represented for automated implementations such as TripleA.

No detailed activation procedure should be invented until this is explicitly designed.

---

## Module Independence

Optional modules should be independently understandable and removable wherever practical.

The core R&D framework should not contain assumptions that require a particular optional module.

Likewise, module-specific rules should not silently alter core R&D behaviour unless the module explicitly defines such an interaction.

This produces a layered architecture:

```text
Core R&D
│
├── Optional Module A
│   ├── Technologies
│   ├── Facilities
│   ├── Resources
│   └── Special Rules
│
├── Optional Module B
│   ├── Technologies
│   ├── Facilities
│   ├── Resources
│   └── Special Rules
│
└── Optional Module C
    ├── Technologies
    ├── Facilities
    ├── Resources
    └── Special Rules
```

---

## Module Interaction

Modules may interact with the core R&D system and with other modules where such interaction is deliberately designed.

An interaction should be represented explicitly rather than becoming an implicit dependency.

Examples already established in the project include:

- Oil having effects on existing R&D technologies;
- Zombies being able to interact with existing R&D technologies;
- Nuclear mechanics being represented through the broader R&D technology/facility/resource architecture.

A module therefore does not need to be completely isolated from the core tree.

The architectural requirement is instead that the dependency is explicit and conditional on the relevant module being enabled.

---

## Modules and the Technology Tree

Optional modules may introduce technologies into the canonical technology graph.

Module technologies follow the same fundamental R&D architecture unless the module explicitly requires additional mechanics.

The module architecture therefore does **not** imply separate technology trees.

Instead:

```text
Canonical R&D Graph
│
├── Core technologies
│
├── Module technologies
│   ├── Oil
│   ├── Nuclear
│   ├── Zombie
│   └── future modules
│
└── Cross-module dependencies/interactions
```

The exact visual representation of module-specific technologies remains a presentation/data question and should follow the existing canonical-graph architecture.

---

## Modules and Eligibility

Module-specific eligibility conditions may exist.

The established eligibility architecture includes:

- technology prerequisites;
- AND/OR prerequisite logic;
- Research Centre requirements;
- resource requirements where explicitly specified;
- national restrictions where explicitly specified;
- module-specific conditions.

A technology belonging to an optional module must not become eligible when that module is disabled.

Thus module activation is effectively one of the conditions determining whether module-specific content exists in the active research system.

---

## Modules and Facilities

A module may introduce physical facilities.

Facilities remain conceptually distinct from technologies and resources.

Research facilities such as Research Centres are part of the broader R&D architecture, while module-specific facilities may belong to the module that defines them.

A module's facility rules must therefore specify their own:

- construction/acquisition;
- ownership;
- capture;
- destruction;
- repair;
- operational effects;
- relationship to technology eligibility.

The existence of a facility does not automatically make it an RP generator.

---

## Modules and Resources

A module may introduce strategic resources.

Resources are distinct from technologies.

The generic resource architecture establishes that:

- resources can be geographically located;
- control of resource-producing territory can affect access;
- some resources require infrastructure;
- R&D can enhance resource infrastructure or production;
- individual resource modules define their own production and consumption rules.

Consequently, resource-specific mechanics should normally be documented within the relevant module while relying on the common resource architecture where applicable.

---

# Current Modules

## Oil Module

Oil is an optional module extending the R&D/resource system with geographically associated oil production and physical infrastructure.

Known architecture includes:

- Oil as a strategic resource;
- geographically associated oil locations;
- naturally active oil locations;
- oil locations requiring infrastructure;
- Oil Derricks;
- Oil Platforms;
- infrastructure affecting production;
- naval control affecting Oil Platform access.

The detailed Oil rules belong to the Oil module handover rather than this module-framework document.

---

## Nuclear Module

The Nuclear system contains enough specialised interactions to constitute a distinct module/rule family.

It interacts with:

- Energy and Physics technologies;
- Nuclear Power Plants;
- Nuclear Reactors;
- Uranium;
- Heavy Water;
- nuclear submarines;
- ballistic missile submarines;
- Atomic Bombs.

Important architectural distinction:

**Nuclear Reactor is a physical facility, not a technology node.**

The nuclear system also demonstrates why modules may need to combine technologies, facilities, resources, units, and specialised effects rather than being limited to technology nodes.

Detailed nuclear mechanics belong to the Nuclear module/rule family.

---

## Zombie Module

The Zombie system is an optional module designed specifically for Global 1940.

Established direction:

- it can operate as a standalone Global 1940 Zombie expansion;
- it can integrate with R&D when both systems are enabled;
- existing R&D technologies may provide contextual Zombie benefits;
- dedicated Zombie technologies are complementary rather than replacing the main technology tree;
- the official *Axis & Allies & Zombies* system is the mechanical baseline;
- the Global 1940 implementation adapts and expands that baseline for the larger map and longer game.

The exact interaction between Zombies and Desperate Measures remains unresolved.

Detailed Zombie design belongs to the Zombie module handover.

---

# Modules and Global / Halifax Compatibility

The core R&D rules are intended to apply consistently to:

- Global 1940;
- Global 1940 Halifax.

The modular architecture must therefore avoid assumptions that make optional modules inherently incompatible with either game variant.

Where a module requires variant-specific treatment, that should be explicitly documented as part of that module.

---

# Data Model Implications

The module architecture should be represented in the data model rather than hard-coded into the presentation layer.

At minimum, module-aware data may need to distinguish:

- core vs module technology;
- module ownership/association;
- module-specific prerequisites;
- module-specific facilities;
- module-specific resources;
- module-specific effects;
- enabled/disabled module state.

The existing project principle of **data-driven structure** applies.

Module configuration should therefore eventually be represented as data/configuration rather than requiring code
