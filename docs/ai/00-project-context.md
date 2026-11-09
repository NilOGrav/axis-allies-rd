# Topic: Project Context

Last updated: 2026-11-09  
Status: Active

## Purpose

Maintain the overall architecture and design principles of the Axis & Allies Global 1940 R&D project, including the separation between technologies, capabilities, facilities, resources, paths, modules, and rules.

The project is intended to provide a modular R&D framework for Global 1940 and Global 1940 Halifax while remaining compatible with the broader Axis & Allies game structure.

## Core Design Philosophy

The R&D system is modular.

Established principles include:

- The core R&D system remains playable without optional modules.
- Optional modules can be added without replacing the core research framework.
- Modules may introduce their own technologies, facilities, resources, and rules.
- Module-specific eligibility/effects are active only when the relevant module is enabled.
- Technologies, resources, facilities, paths, and modules are distinct concepts.
- Cross-domain relationships should be represented explicitly rather than forcing everything into the technology domain classification.

The architecture is intended to be data-driven rather than embedding every technology effect directly into procedural code.

## Core Conceptual Layers

The current design distinguishes:

### Technology

An acquired technological capability or progression step.

Technology determines progression and eligibility and may grant one or more effects.

### Capability

A reusable representation of a game rule or functional ability.

Capabilities should be generic where possible and parameterized where the rule differs by target, subject, value, condition, or other rule dimension.

### Subject

The object or object group to which a capability is attached.

`Subject` is not a capability variable.

For example, a capability effect can conceptually specify:

```text
Capability = Cannot Hit Units
Subject = Submarines
Target = AIR
```

The converse can be represented independently:

```text
Capability = Cannot Hit Units
Subject = AIR
Target = Submarines
```

This avoids creating separate capability names for every possible target relationship.

### Facility

Physical infrastructure or installation existing on the game map.

Facilities are separate from technologies.

Research Centres are a distinct facility category and may function as eligibility gates.

Facilities do not universally generate Research Tokens.

### Resource

A strategic resource or material used by the game system.

Resources are separate from technologies and facilities.

Some resources are geographically associated with territories or sea zones and may require infrastructure.

### Path

An analytical/technological route through the tree.

Paths may cross domains and do not themselves define eligibility.

### Domain

The primary technological classification of a technology.

Current domains:

- Air
- Land
- Naval
- Intelligence
- Energy And Physics
- Logistics And Industry
- Programs
- Resource

The domain model is not intended to reproduce historical research organizations.

## Domain Principle

The current best-established classification principle is:

> Put a technology in the domain representing its primary technological capability, not every field it interacts with.

A technology may therefore interact with several domains without belonging to all of them.

For example, a technology can involve:

- naval platforms;
- nuclear physics;
- industrial production;
- strategic resources;

while still having one primary domain.

Paths, dependencies, resources, facilities, and modules provide the additional relationships.

A formal exhaustive boundary definition for every domain has not yet been completed.

## Research Architecture

Research Tokens (RT) are the research resource.

Established core principles include:

- Each research attempt costs exactly 1 RT.
- Baseline conversion is 5 IPC → 1 RT.
- Unspent RT can be saved.
- RT are assigned to research at the start of the turn.
- Each assigned RT targets one eligible technology.
- Research targets are secret.
- RT assignment/availability is public while the target remains secret.
- Eligibility is evaluated using the start-of-turn state.
- Newly acquired technologies do not create additional eligibility during the same turn.
- Multiple RT can support simultaneous research attempts.
- Research resolves during Deployment.
- Roll 1 fails and the RT is lost.
- Roll 2–5 successfully acquires the technology.
- Roll 6 is a breakthrough.
- A breakthrough acquires the technology and retains the RT.
- Breakthrough RT cannot be used until the following round.

## Tree vs. Economy

An important architectural distinction is:

> **The technology tree controls eligibility; the research economy controls research capacity.**

The tree determines what can be researched.

Research Tokens determine how many research attempts can actually be made.

Facilities and resources can participate in the research economy where explicitly defined, without turning every facility or resource into a universal RT generator.

## Research Centres

Research Centres (`RCENTER`) are a distinct facility category.

They may act as technological eligibility/prerequisite gates.

Research Centres are not themselves technologies.

A Research Centre may explicitly generate RT where its rules say so, but facilities in general do not automatically generate RT.

## Facilities vs. Technologies

The following distinction is established:

```text
Technology
    = acquired technological capability / progression

Facility
    = physical infrastructure implementing or supporting capability
```

Researching a facility-related technology does not automatically construct the physical facility unless explicitly specified.

Likewise, possessing a facility does not automatically replace a technology prerequisite.

A physical facility should not be represented as a technology node merely to create a dependency.

## Units and Technologies

Technology can:

- unlock an existing unit type;
- introduce a new unit type;
- modify an existing unit;
- grant a capability to a unit;
- provide another explicit unit-related effect.

Unlocking a unit does not automatically provide one unless explicitly specified.

Unlocked units are subsequently purchased/constructed through the applicable normal mechanism.

This distinction is particularly important for technology-effect data.

## Resources and Technologies

Resources are distinct from technologies.

Strategic resources can be:

- geographically located;
- dependent on territory control;
- dependent on physical infrastructure;
- consumed by technological or military effects.

Individual resource modules define their own production and consumption rules.

The architecture should not assume that every resource is physically transported merely because it has a geographical source.

## Modules

Modules are optional extensions to the core architecture.

A module may introduce:

- technologies;
- facilities;
- resources;
- units;
- capabilities;
- rules.

Existing R&D technologies may also receive module-specific contextual effects.

The exact activation/configuration mechanism remains an open design item.

## Current Major Open Areas

The following remain unresolved or require consolidation:

- exact module activation/configuration procedure;
- formal domain boundary definitions;
- exact eligibility-check ordering;
- complete capability taxonomy;
- complete mapping of technology effects to capabilities;
- precise captured Research Centre behaviour;
- exact facility/technology interaction after capture;
- precise resource rules for all resource types;
- exact nuclear delivery dependency placement;
- minor-unit definition for Research Centre bonuses;
- some Oil terminology and mechanics;
- Zombie/Desperate Measures integration.

## Important Continuation Rules

A future AI should:

1. Preserve the separation of technology, capability, facility, resource, path, domain, and module.
2. Avoid creating new concepts merely to solve a single ambiguous technology.
3. Prefer parameterized generic capabilities where actual effects share the same rule structure.
4. Do not merge apparently similar capabilities until their actual rule semantics and parameters have been compared.
5. Treat unresolved items as open rather than silently deciding them.
6. Use the latest ODS/design data as the primary design source where available.
7. Treat exported CSVs as derived data unless specifically designated otherwise.
8. Apply the architecture consistently to both Global 1940 and Global 1940 Halifax.
9. Remember that Halifax changes the political/economic framework without changing the fundamental R&D architecture.
