# Topic: Modules

Last updated: 2026-11-17  
Status: Active

## Purpose

This handover defines the **generic module framework** of the Axis & Allies Global 1940 R&D system.

It establishes how optional modules relate to the core R&D system, how module-specific content is activated and integrated, and what parts of the architecture are intentionally shared.

Detailed rules for individual modules belong in their respective module handovers. This document therefore provides only short module summaries and must not become a second source of truth for their detailed mechanics.

---

# 1. Module Framework

## 1.1 Module rule overview

| ID | Rule | Status |
|---|---|---|
| MOD-001 | The R&D system is modular. | Established |
| MOD-002 | Optional modules can be added without altering the core research framework. | Established |
| MOD-003 | A module can introduce its own technologies, facilities, resources or rules. | Established |
| MOD-004 | Core R&D remains playable without optional modules. | Established |
| MOD-005 | Module-specific eligibility/effects are only active when the module is enabled. | Established architecture |
| MOD-006 | Exact module activation/configuration procedure. | **Needs explicit rule** |
| MOD-007 | Enabled/disabled modules should be represented through game configuration/data rather than scattered hard-coded logic. | **Open** |
| MOD-008 | Need for a generic mechanism for module dependencies/inter-module compatibility. | **Open** |
| MOD-009 | Exact precedence/order of module activation versus other eligibility conditions. | **Open** |

MOD-001 through MOD-005 describe the established modular architecture.

MOD-006 through MOD-009 identify remaining framework-level questions. They are deliberately kept separate from module-specific open questions.

---

## 1.2 Core vs Optional Modules

The core R&D system must remain complete and playable without optional modules.

Optional modules extend the system rather than replacing its core research framework.

A module may introduce:

- technologies;
- facilities;
- resources;
- technology effects;
- eligibility conditions;
- other module-specific rules.

The module does not need to use all of these categories.

---

# 2. Module Activation

Module-specific content is conditional on the module being enabled.

When a module is disabled:

- its technologies are not active;
- its module-specific eligibility conditions are not active;
- its module-specific effects are not active;
- its module-specific facilities/resources/rules are not active unless another explicit rule says otherwise.

### Activation procedure

The exact procedure for activating/configuring modules has not yet been formally established.

This is **MOD-006** and remains an open framework rule.

The eventual implementation should allow the active game configuration to determine which modules are enabled.

---

# 3. Module Integration with Core R&D

## 3.1 Common R&D framework

An enabled module integrates into the existing R&D architecture rather than automatically creating a separate research system.

The existing R&D framework remains responsible for:

- research points;
- research attempts;
- research eligibility;
- prerequisite logic;
- research resolution;
- technology acquisition.

Module content can extend these systems with module-specific conditions or effects.

---

## 3.2 Technology integration

An enabled module may add technologies to the canonical technology structure.

Module technologies follow the same fundamental research architecture unless the module explicitly establishes an exception.

Module technologies can therefore:

- have prerequisites;
- belong to technological domains;
- participate in technological paths;
- unlock capabilities;
- interact with existing technologies.

The generic module framework does not prescribe the detailed mechanics of individual module technologies.

---

# 4. Module Eligibility

Module technologies can have module-specific eligibility conditions.

The general eligibility architecture already supports optional technologies/modules having their own conditions.

The important distinction is:

> A module-specific eligibility condition only exists for the game when that module is enabled.

The precise ordering between:

- module activation;
- technological prerequisites;
- Research Centre requirements;
- resource conditions;
- national restrictions;

remains an eligibility-system question.

This is represented by **MOD-009** rather than being resolved here.

---

# 5. Modules and Facilities

An enabled module may introduce physical facilities or infrastructure.

Facilities remain distinct from technologies.

Researching a technology that enables construction of a facility does not automatically mean that the physical facility exists or has been constructed unless the technology explicitly says so.

Similarly, a module facility is not automatically an RP generator merely because it is associated with research.

The generic facility architecture therefore remains separate from the module framework.

---

# 6. Modules and Resources

An enabled module may introduce resources or resource-related mechanics.

The generic resource architecture permits:

- geographically associated resources;
- territory/sea-zone control affecting access;
- abstract national resources;
- infrastructure-dependent production;
- R&D enhancement of resource infrastructure or production.

Individual resource modules define their own production and consumption rules.

Therefore, the module framework does not prescribe the detailed mechanics of any particular resource.

---

# 7. Module Interaction

Modules may interact with the core R&D system and with other game systems.

Such interaction must be defined by the relevant module rather than assumed globally.

Examples include:

- existing technologies modifying module effects;
- module technologies unlocking capabilities;
- module facilities providing capabilities;
- module resources forming eligibility or production requirements;
- module technologies interacting with existing facilities or units.

An interaction is not automatically a new generic module rule. It belongs to the module that defines it unless it establishes a reusable framework rule.

---

# 8. Module Independence

Optional modules should remain independently understandable and playable where their design permits it.

The core R&D system must not depend on an optional module.

Likewise, enabling a module should add its intended content without requiring unrelated modules unless an explicit dependency between modules has been designed.

A module may therefore be:

- standalone;
- integrated with core R&D;
- dependent on another module;
- capable of interacting with another module.

The exact relationship must be documented by the affected modules.

The generic framework question of whether a reusable dependency/compatibility mechanism is required is **MOD-008**.

---

# 9. Module Configuration and Data Model

The module architecture should remain data-driven.

The technology data model already contains a module association for technologies, allowing the canonical technology dataset to identify module-specific content.

Module configuration should eventually determine which optional content participates in the active game configuration.

This avoids hard-coding individual module combinations into the core R&D implementation.

The exact configuration mechanism remains open under **MOD-006** and **MOD-007**.

---

# 10. Current Modules — Summary Only

The following entries are intentionally summaries. They are **not** the authoritative detailed rule sets for the modules.

## OIL — Oil Module

Oil is an optional strategic-resource module.

Established concepts include:

- Oil is an abstract strategic resource.
- Oil production is geographically associated with territories and sea zones.
- Some oil locations are naturally active.
- Some oil locations require infrastructure development.
- Oil Derrick and Oil Platform are physical infrastructure pieces.
- Oil infrastructure affects oil production.
- Oil Platforms can be contested/captured through control of their sea zone.

Detailed Oil rules, terminology, production mechanics and remaining open questions belong in the **Oil Module handover**.

---

## NUC — Nuclear Module

Nuclear is an optional module integrating nuclear technology, facilities, resources and strategic capabilities into the R&D system.

Established/current concepts include:

- Reactor Theory unlocks Nuclear Power Plant construction.
- Nuclear Power Plants provide nuclear power production.
- Uranium Processing unlocks Nuclear Reactor construction.
- A Nuclear Reactor is a physical facility rather than a technology node.
- Nuclear technology can enable Atomic Bomb production.
- Heavy Water and Uranium are involved in Atomic Bomb production.
- Nuclear submarines use nuclear propulsion.
- Nuclear submarines and ballistic missile submarines are distinct capabilities.
- Nuclear delivery requires an eligible delivery system.

The exact dependency placement for nuclear delivery remains open.

Detailed Nuclear rules belong in the **Nuclear Module handover**.

---

## ZOM — Zombie Module

Zombie is an optional module adapted specifically for Global 1940.

Established concepts include:

- Zombie mechanics are adapted specifically for Global 1940.
- The Zombie system can operate as a standalone optional module.
- The Zombie system can interact with R&D when the integrated version is enabled.
- Existing R&D technologies can contextualise Zombie effects.
- Dedicated Zombie technologies complement rather than replace the main technology tree.

The exact interaction between Zombies, R&D and Desperate Measures remains unresolved.

Detailed Zombie rules belong in the **Zombie Module handover**.

---

# 11. Design Constraints

The following constraints apply to the module framework:

1. **Modular by design** — optional systems should be addable without redesigning the core R&D framework.
2. **Core independence** — core R&D must remain playable without optional modules.
3. **Conditional activation** — disabled module content must not affect the game.
4. **Data-driven configuration** — module participation should ultimately be represented as configuration/data rather than scattered hard-coded logic.
5. **Shared R&D architecture** — enabled module technologies should integrate into the canonical R&D system unless explicitly designed otherwise.
6. **Separation of concerns** — the generic module framework should not duplicate detailed rules belonging to individual modules.
7. **Distinct categories** — technologies, facilities and resources remain conceptually distinct even when introduced by the same module.
8. **No automatic RP generation** — module facilities/resources do not become RP generators merely by being associated with research.

---

# 12. Open Questions — Framework Only

The following are unresolved at the **generic module-framework level**:

| ID | Question | Status |
|---|---|---|
| MOD-006 | What is the exact module activation/configuration procedure? | Open |
| MOD-007 | How should enabled/disabled modules be represented in the game configuration/data model? | Open |
| MOD-008 | Is an explicit generic mechanism needed for module dependencies/inter-module compatibility? | Open |
| MOD-009 | What is the formal precedence/order of module activation versus other eligibility conditions? | Open |

Module-specific open questions must remain in the relevant module handover rather than being duplicated here.

---

# 13. Current Status

The generic modular architecture is **established**.

The core principles are:

- R&D is modular.
- Optional modules extend rather than replace the core framework.
- Modules may add technologies, facilities, resources and rules.
- Core R&D remains independent of optional modules.
- Module-specific effects and eligibility are conditional on module activation.
- Enabled module content integrates with the canonical R&D architecture.

The principal unresolved framework issue is the **formal module activation/configuration mechanism**.

Oil, Nuclear and Zombie are established module families, but their detailed mechanics are maintained separately.

---

# 14. Authority and Scope

This document is authoritative for the **generic module framework only**.

It is not authoritative for detailed Oil, Nuclear or Zombie mechanics.

For detailed module rules, consult the corresponding module handover.

The module framework must remain consistent with the wider R&D architecture, including the established distinction between:

- technological structure;
- research economy;
- research resolution;
- technology eligibility;
- facilities;
- resources;
- technology effects.
