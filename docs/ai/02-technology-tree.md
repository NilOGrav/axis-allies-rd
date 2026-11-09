# Topic: Technology Tree

Last updated: 2026-11-09
Status: Active

## Purpose

Define and maintain the complete technology tree for the Axis & Allies Global 1940 R&D system, including technology identity, domains, tiers, prerequisites, paths, research eligibility, technology effects, unlocked game elements, and optional-module technologies.

The technology tree is the primary representation of the **technological progression and eligibility structure**. It is not itself the complete rule system: facilities, resources, units, capabilities, and other rules are represented separately and connected to technologies through explicit relationships.

## Current Status

The technology-tree architecture is established, but the current technology list still requires a **clarification/cleanup pass before technology effects can be mapped reliably into the capability model**.

A recent review identified an important source-data issue: some technology descriptions are ambiguous about whether a technology:

- modifies an existing unit;
- unlocks an existing game element;
- introduces a completely new unit or facility;
- adds a capability to that new element;
- or combines several of these effects.

Example: an Airship technology was intended to **introduce a new Airship unit**, give that unit the **Strategic Bombing** capability, and make the Airship immune to AAA while conducting Strategic Bombing. Earlier interpretation treated this primarily as a modification to existing strategic bombing rather than as the introduction of a new unit. The technology list therefore needs clearer wording before effect mapping is treated as authoritative.

## Core Technology Architecture

### Domains

The current technology model uses eight domains:

- A — Air
- L — Land
- N — Naval
- I — Intelligence
- E — Energy And Physics
- L&I — Logistics And Industry
- P — Programs
- R — Resource

Domain represents the technology's **primary technological identity**, not every subject with which it interacts.

Cross-domain relationships should normally be represented through:

- prerequisites;
- paths;
- resources;
- facilities;
- modules;
- or other explicit relationships.

Domains are therefore not historical organizational departments and are not intended to duplicate technologies merely because their effects span several fields.

### Paths

A path is an analytical/technological route through the tree.

Paths may cross domains, and a technology may contribute to multiple paths.

A path does not itself define research eligibility.

### Eligibility

Established eligibility principles include:

- A technology must be eligible before it can be selected.
- Prerequisites determine eligibility.
- Separate prerequisite groups combine as AND.
- Alternatives within a prerequisite group combine as OR.
- Eligibility is evaluated using the start-of-turn state.
- Newly acquired technologies do not create new eligibility during the same turn.
- Research Centres may act as eligibility gates.
- Ordinary facilities do not normally act as technology prerequisites.
- Resource requirements may form part of eligibility or payment where explicitly specified.
- Optional technologies/modules may have their own eligibility conditions.

The exact ordering of eligibility checks still needs formalization where multiple condition types interact.

## Technology Effects

Established architecture distinguishes technology acquisition from its effects.

A successfully researched technology permanently belongs to the researching player.

A technology may:

- unlock a capability;
- modify an existing capability;
- unlock a unit;
- introduce a new unit;
- unlock a facility/build capability;
- modify an existing unit;
- provide another explicit game effect;
- combine multiple effects.

Technology acquisition does **not** automatically:

- construct or place a physical facility;
- provide a unit;
- create additional same-turn research eligibility.

Technology effects remain available independently of the physical facilities used to implement them unless a specific rule says otherwise.

## Unit Introduction vs. Modification

This distinction must be made explicit in the cleaned technology list.

A technology can introduce a new unit with its own capabilities.

For example, an Airship technology should be expressible as:

1. Introduce the **Airship** unit.
2. Give Airship the **Strategic Bombing** capability.
3. Apply the specified AAA exception while that capability is being used.

This is different from simply modifying the Strategic Bombing capability of existing aircraft.

The source technology wording should therefore identify the **object being introduced or modified** and the **effect applied to it**.

## Capability Mapping

Technology effects will ultimately be represented through the capability system.

The intended conceptual model is:

```text
Technology
    │
    └── Effect
          │
          ├── Capability
          ├── Subject
          ├── Operation
          └── Parameters / Values
```

`Subject` identifies the object or object group receiving the capability/effect. It is not a capability variable.

Capabilities should be generic where the same rule structure can serve multiple targets. Parameters should represent meaningful rule dimensions rather than creating a separate capability name for every value or target.

The technology-effect mapping is still provisional and should not be treated as final until the source technology descriptions have been cleaned up.

## Current Technology Data Concerns

The technology list needs review for:

- ambiguous wording;
- distinction between unlock and modification;
- explicit identification of newly introduced units/facilities;
- explicit identification of capability assignments;
- conditions under which an effect applies;
- duration of effects;
- target/subject identification;
- cumulative versus replacement effects;
- duplicate or overlapping technology effects;
- unclear numerical parameters;
- inconsistent terminology.

The capability mapping should follow the cleaned source rather than silently interpreting ambiguous technology text.

## Nuclear Technology Architecture

The nuclear branch contains several established architectural distinctions:

- Nuclear Reactor is a physical facility, not a technology node.
- Nuclear Power Plant is a physical facility.
- Reactor Theory unlocks Nuclear Power Plant construction.
- Uranium Processing unlocks Nuclear Reactor construction.
- Nuclear Reactor can subsequently acquire uranium-production capability through P.7.NU.
- Atomic Bomb production is enabled through the nuclear technology chain.
- Atomic Bomb production requires Heavy Water and Uranium according to the current technology rule.
- Nuclear submarines use nuclear propulsion.
- Nuclear submarines are distinct from ballistic missile submarines.
- Ballistic missile submarines provide atomic-payload delivery capability.
- Nuclear delivery requires an eligible delivery system.
- Exact placement of the delivery-system dependency in P.8/P.9 remains open.

## Module Integration

The R&D architecture is modular.

Optional modules may introduce:

- technologies;
- facilities;
- resources;
- rules;
- effects.

Core R&D remains playable without optional modules.

Module-specific eligibility and effects are active only when the relevant module is enabled.

The exact module activation/configuration procedure remains unresolved.

## Important Continuation Rules

A future AI working on the technology tree should:

1. Treat the technology list as the source data to be clarified, not something to reinterpret silently.
2. Distinguish **new element introduction**, **unlock**, **modification**, and **conditional effect**.
3. Preserve the distinction between technology, unit, facility, resource, capability, and path.
4. Do not infer a capability merely because a technology description could be interpreted that way.
5. Flag ambiguous source wording instead of silently choosing an interpretation.
6. Treat the domain as primary technological identity rather than a list of all affected subjects.
7. Keep cross-domain relationships in paths, prerequisites, resources, facilities, or other explicit relationships.
8. Treat the capability-effect mapping as downstream of the cleaned technology list.
9. Preserve established rules while marking unresolved rules explicitly as open.
10. Update this handover whenever the technology-list structure or effect interpretation is materially changed.
