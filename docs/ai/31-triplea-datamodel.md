# Topic: TripleA Data Model

Last updated: 2026-11-10
Status: Active

## Purpose

This topic records the current understanding of TripleA's game/data model and how it may relate to the project's planned canonical Axis & Allies Global 1940 model.

The objective is to determine what can be reused from TripleA, what must be adapted, and what game semantics are missing from TripleA's declarative data and therefore require procedural implementation.

This document is AI project memory. It is not the authoritative Axis & Allies rules specification.

## Current design

The project should use TripleA's existing game definitions, maps, data structures and implementations as **input/reference material**, but should not make the project's canonical data model depend directly on TripleA Java runtime classes.

The intended relationship is:

    Axis & Allies canonical model
                |
         TripleA adapter
                |
          TripleA engine
                |
           playable game

The canonical model describes the game/rules concepts independently.

The adapter translates between that model and TripleA's existing engine representation.

This allows the canonical model to remain usable independently of TripleA and prevents TripleA implementation details from becoming the permanent definition of the game's data model.

## Established decisions

### DATAMODEL-001 — Reuse TripleA concepts where useful

TripleA already provides useful representations for many core game concepts.

These should be investigated for reuse rather than duplicated unnecessarily.

Relevant areas include:

- territories;
- territory connections;
- players;
- alliances;
- resources;
- unit types;
- unit properties;
- production;
- starting ownership;
- starting unit placement;
- starting resources;
- turn sequence/delegates;
- game attachments;
- map/game configuration.

### DATAMODEL-002 — Do not make the canonical model TripleA-dependent

The canonical model must not consist of references to TripleA Java classes.

TripleA-specific classes are an implementation layer.

### DATAMODEL-003 — XML is not the complete rules model

TripleA game XML/map definitions are not sufficient by themselves to reconstruct every game rule.

Some semantics are implemented procedurally by TripleA's Java code, including behaviour associated with delegates and other engine mechanisms.

A complete model audit therefore needs both:

1. TripleA declarative game/map data.
2. TripleA Java implementation behaviour.

### DATAMODEL-004 — Distinguish game definition from game state

The architecture should distinguish between:

- static definition/configuration of a game;
- mutable state of an individual running game;
- rules that determine legal transitions between states.

This distinction is important for both the canonical model and the eventual TripleA adapter.

### DATAMODEL-005 — Global 1940 is the first important mapping target

The data-model investigation should use an explicit Global 1940 baseline rather than attempting to merge every TripleA game/variant into one initial model.

Variant differences should be represented explicitly where necessary.

## Conceptual mapping

The following is the current working mapping. It is a starting point for audit, not a claim that every field maps one-to-one.

| Canonical concept | TripleA representation to investigate | Current assessment |
|---|---|---|
| Territory | Territory / map data | Strong candidate for reuse |
| Territory connection | Map connection data | Strong candidate for reuse |
| Player | Player data | Strong candidate for reuse |
| Alliance | Alliance/relationship configuration | Reuse concept; exact semantics to audit |
| Resource | Resource definitions/state | Strong candidate; exact production semantics to audit |
| Unit type | Unit type definitions | Strong candidate for reuse |
| Unit capability | Unit properties + procedural rules | Requires deeper audit |
| Production | Production rules/attachments | Requires audit |
| Starting setup | Map/game XML setup | Strong candidate for import |
| Turn sequence | Sequence/delegate configuration | Reuse concept; implementation needs abstraction |
| Technology | Existing technology/game-specific structures where present | Requires audit; not assumed equivalent to R&D model |
| Facility | Unit/attachment/configuration mechanisms depending on implementation | Requires explicit canonical mapping |
| Research Centre | No assumption of direct one-to-one representation | Needs canonical representation and adapter |
| Strategic resource infrastructure | Combination of territory, unit/facility, attachments and rules | Needs audit |
| Special rule | Attachments and/or Java implementation | Often procedural |
| Rule condition | Conditions/attachments and procedural checks | Needs audit |
| Rule effect | Attachments, delegates and state changes | Needs audit |
| Game state | Central GameData and associated state objects | Important reuse candidate, but architectural coupling must be examined |
| Save state | TripleA save-game serialization | Compatibility constraint |
| Network state | TripleA network/state synchronization mechanisms | Compatibility constraint |

## Important architectural distinction

The project should distinguish at least three things:

### 1. Canonical entity

What the game/rule system says exists.

Examples:

- territory;
- player;
- unit;
- facility;
- technology;
- resource;
- research centre.

### 2. Canonical rule

What is permitted or what happens when a state transition occurs.

Examples:

- a unit may move through a particular connection;
- a player may purchase a technology;
- a facility may be constructed;
- a resource may be produced;
- a combat result may change unit state.

### 3. TripleA implementation

The Java classes, attachments, delegates, XML structures and state machinery that make the rule executable in TripleA.

These three layers should not be collapsed into one model.

## Canonical model direction

The eventual canonical model should be capable of representing more than the R&D system alone.

At minimum, the architecture should be able to describe:

- players and alliances;
- territories and geography;
- resources/economies;
- units;
- unit capabilities;
- facilities;
- production;
- technology;
- research;
- prerequisites;
- conditions;
- effects;
- turn sequence;
- ownership;
- state transitions;
- optional modules.

R&D is therefore one subsystem of the broader canonical game model rather than the canonical model itself.

## TripleA-specific caveat: procedural rules

An important audit category is:

> "Can this rule be represented as data, or is it implemented by procedural engine code?"

Examples that need explicit investigation include:

- movement restrictions;
- canals;
- special combat abilities;
- production restrictions;
- placement restrictions;
- national rules;
- technology effects;
- facility effects;
- special unit behaviour;
- turn-phase behaviour;
- triggers and conditions.

The adapter/canonical model must account for rules that cannot simply be imported from XML.

## Recommended audit method

For each important Global 1940 concept, create an inventory row using:

| Field | Meaning |
|---|---|
| Canonical ID | Stable project-side identifier |
| Concept | Human-readable concept |
| TripleA source | XML, map data, Java class, attachment, delegate, etc. |
| Existing representation | What TripleA currently uses |
| Reuse strategy | Reuse / adapt / replace / canonical-only |
| Missing semantics | What is not represented by the existing source |
| Variant relevance | Global / Europe / Pacific / Halifax / optional module |
| Validation status | Unchecked / inspected / verified |
| Notes | Important implementation/design observations |

This audit should be performed before designing large amounts of engine-side replacement code.

## Example audit questions

For each concept ask:

1. Does TripleA already represent it?
2. Is the representation declarative or procedural?
3. Is the representation reusable independently of TripleA?
4. Does it contain enough information for the canonical model?
5. Does it combine multiple concepts that the canonical model should separate?
6. Does the canonical model need information TripleA currently does not store?
7. Is the behaviour variant-specific?
8. Is the behaviour implemented by a delegate, attachment or other procedural code?
9. Can the TripleA representation be adapted without changing TripleA internals?
10. Would changing the TripleA representation create save/network compatibility issues?

## Do not assume

The following are explicitly **not** established:

- that TripleA's current data model is the correct canonical model;
- that TripleA XML contains all game rules;
- that every canonical concept has a direct TripleA equivalent;
- that every TripleA concept belongs in the canonical model;
- that existing TripleA technology structures can directly represent the project's R&D technology model;
- that facilities should be represented as units merely because TripleA may use units for some physical pieces;
- that Research Centres already have an appropriate TripleA representation;
- that attachments are the correct long-term representation for all canonical rules;
- that the central TripleA GameData object should remain the canonical state container;
- that procedural Java rules can or should all be converted into declarative data.

## Open questions

- What is the complete set of Global 1940 concepts already represented by TripleA's game XML?
- Which important rules exist only in TripleA Java code?
- Which TripleA representations are sufficiently generic to reuse?
- Which representations are tied to historical TripleA implementation choices?
- What is the correct canonical representation of technologies and research?
- How should Research Centres and other facilities map into TripleA?
- How should technology effects map to unit capabilities and rule changes?
- How should conditional rules and effects be represented?
- How should mutable state be separated from static game definition?
- How should save/load be redesigned if the canonical state model differs from TripleA's existing GameData graph?
- Which TripleA XML constructs should be preserved for compatibility?
- Which semantics need a compatibility adapter rather than a direct translation?

## Relevant project files

- docs/ai/README.md — AI-memory conventions and authority hierarchy.
- docs/ai/20-triplea.md — TripleA architectural/recode direction.
- docs/ai/31-triplea-datamodel.md — this topic.
- docs/ai/99-open-questions.md — cross-topic unresolved questions.
- data/research/ — authoritative R&D design source.
- data/research/*.ods — current technology/R&D design data where applicable.

The upstream TripleA source, game definitions and Global 1940 map data must be inspected directly before implementation decisions are treated as verified.

## Recent changes

2026-11-10:

- The project explicitly separated the TripleA architecture/recode question from the TripleA data-model question.
- The working direction became: reuse TripleA where practical, but create an independent canonical model and adapter boundary.
- The need to inspect both declarative TripleA data and procedural Java implementation was established.
- A structured TripleA-to-canonical audit was defined as the next major investigation.

## Next intended work

1. Identify the exact Global 1940 TripleA game/map baseline to audit.
2. Inventory the game XML and map data.
3. Identify the corresponding Java classes, attachments and delegates for important rules.
4. Build the canonical-to-TripleA mapping table.
5. Mark each mapping as reusable, adaptable, replacement candidate, or canonical-only.
6. Record missing procedural semantics explicitly.
7. Use the resulting audit to guide the TripleA fork architecture work.

## Working principle

TripleA should be treated as a **valuable existing implementation and source of reusable game concepts**, not as the definition of the canonical game model.

The desired relationship is:

> **Canonical game model → adapter → TripleA implementation**

rather than:

> **TripleA Java classes → canonical model**

This keeps the project's rules and R&D architecture independent while still allowing the fork to exploit the substantial amount of working game-engine infrastructure already present.
