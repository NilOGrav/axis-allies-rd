# Topic: TripleA Architecture / Recode

Last updated: 2026-11-10
Status: Active

## Purpose

This topic records the current project position on using TripleA as a foundation for the Axis & Allies R&D project, with particular attention to whether TripleA should be forked and incrementally refactored rather than rewritten from scratch.

This document is AI project memory. It is not an authoritative description of TripleA's implementation. Current TripleA source code and documentation must be checked before making implementation changes.

## Current design

The current direction is to **fork TripleA as a possible development platform and investigate/refactor its architecture incrementally**.

The project is **not** committing to a complete rewrite of TripleA.

The guiding approach is:

1. Establish a known-good TripleA baseline.
2. Audit the existing architecture and dependencies.
3. Identify concrete architectural boundaries that are missing, weak, or overly coupled.
4. Refactor one subsystem/vertical slice at a time.
5. Preserve existing game functionality while improving internal structure.
6. Replace individual subsystems only where refactoring proves insufficient.
7. Keep the project's canonical Axis & Allies/R&D data model independent from TripleA's Java implementation.

The purpose of the fork is therefore initially architectural research and controlled migration, not creation of an immediately independent replacement engine.

## Established decisions

### TRIPLEA-001 — Forking is a viable direction

A TripleA fork is considered a viable foundation for further work.

The fork should be treated as a controlled development branch of the existing engine rather than as a commitment to rewrite the entire codebase.

### TRIPLEA-002 — No full rewrite commitment

There is currently no decision to rewrite the entire TripleA codebase.

The project should gather evidence subsystem by subsystem before deciding that a component must be replaced.

### TRIPLEA-003 — Architecture comes before major feature integration

The first substantial work on the fork should investigate and improve architectural boundaries before deeply integrating the new R&D system.

### TRIPLEA-004 — Prefer incremental refactoring

Existing working functionality should be retained where practical.

Refactoring and replacement should happen incrementally so that regressions can be identified and the working game remains usable.

### TRIPLEA-005 — Separate game design from engine implementation

The canonical model must not become dependent on TripleA's internal Java classes.

TripleA should consume or adapt the canonical model rather than define the only representation of the rules.

### TRIPLEA-006 — Global 1940 is an important architectural test case

Global 1940 provides a sufficiently complex real game context to test whether the proposed architecture can represent:

- multiple players and alliances;
- territories and connections;
- units and unit capabilities;
- production and placement;
- turn phases;
- national restrictions;
- special rules;
- technologies;
- facilities;
- resources;
- optional modules.

### TRIPLEA-007 — Existing TripleA functionality is valuable even where architecture is imperfect

The existence of architectural debt is not sufficient reason to discard working TripleA functionality.

The project should reuse working concepts and implementations where they fit the target architecture.

## Evidence and architectural observations

The investigation has found evidence of substantial historical and current architectural debt, including:

- a central GameData model with broad responsibility;
- delegates that implement turn phases and may contain game/rule-specific behaviour;
- extensible attachments used to customize game behaviour;
- save-game compatibility constraints tied to Java serialization;
- network API compatibility constraints;
- historical discussion by TripleA maintainers/developers about modularization and overly broad or tightly coupled components.

TripleA is nevertheless already modularized to a significant degree and continues to receive refactoring and modernization work.

Therefore the evidence supports:

> "TripleA has meaningful architectural debt and some tight coupling."

It does **not** support:

> "TripleA must be completely rewritten before it can be used."

## Target architectural direction

The desired architecture should progressively establish clearer boundaries between at least:

- Game definition
- Canonical rules/model
- Mutable game state
- Rules execution
- Turn orchestration
- User interface
- AI
- Networking
- Persistence/save games
- TripleA compatibility/adaptation

These are target boundaries, not a claim that every component must become a separate Gradle module or service.

The important property is controlled dependency direction.

## Current implementation

The existing TripleA repository is the upstream reference implementation.

The project repository is separate:

- Axis & Allies R&D: NilOGrav/axis-allies-rd
- TripleA upstream: triplea-game/triplea

The current R&D repository contains the project's canonical design and AI-memory documentation. TripleA is an implementation/platform concern and should remain conceptually separate from the R&D design source.

## Known constraints

### Save-game compatibility

TripleA has compatibility constraints around Java serialization and the persisted game object graph.

Moving or renaming serialized classes or fields can therefore have consequences beyond normal source compatibility.

This must be investigated before large-scale movement of core game-state classes.

### Network compatibility

Changes to network-facing APIs and serialized state can affect compatibility.

Architectural refactoring must therefore consider multiplayer/network behaviour, not only local single-player execution.

### Existing rule implementation

Not all game semantics necessarily exist declaratively in game XML/map data.

Some rules are implemented procedurally in Java.

Consequently, an architecture audit cannot be limited to parsing TripleA XML.

## Do not assume

The following have **not** been decided:

- that TripleA's entire codebase must be rewritten;
- that every existing module is architecturally unsuitable;
- that the current GameData model must be completely discarded;
- that every game rule must be moved into declarative data;
- that the fork must permanently diverge from upstream;
- that the R&D system should be implemented directly inside existing TripleA attachment structures;
- that the final engine architecture must mirror the proposed target boundaries exactly;
- that the current TripleA implementation is the authoritative specification of Axis & Allies rules.

## Open questions

- How much of TripleA's existing architecture can be retained after a dependency audit?
- Which existing components should become stable architectural boundaries?
- Which components need refactoring versus replacement?
- How should canonical game/rules data be represented and imported into the engine?
- How should procedural TripleA rules be represented in the canonical model?
- How should save/load work after core game-state refactoring?
- What level of compatibility with existing TripleA maps and game definitions should be retained?
- Should the fork periodically rebase/merge upstream TripleA, and under what policy?
- Which Global 1940 rule systems should be used as the first architectural vertical slice?

## Relevant project files

- docs/ai/README.md — AI-memory conventions and authority hierarchy.
- docs/ai/20-triplea.md — this topic.
- docs/ai/31-triplea-datamodel.md — TripleA data-model investigation.
- docs/ai/99-open-questions.md — cross-topic unresolved questions.
- data/research/ — authoritative R&D design data, where applicable.

The upstream TripleA source and documentation should be checked directly for implementation details.

## Recent changes

2026-11-10:

- The project moved from discussing whether TripleA could be reused to considering an actual fork as a practical architecture-development path.
- The current position became incremental architectural refactoring rather than a presumed complete rewrite.
- The distinction between the TripleA engine architecture and the project's canonical Axis & Allies/R&D model was made explicit.
- A separate TripleA data-model topic was identified as necessary.

## Next intended work

1. Create a clean fork/branch of TripleA at a known-good upstream revision.
2. Build and run the unmodified baseline.
3. Run the existing tests and document baseline behaviour.
4. Produce an architecture/dependency inventory.
5. Identify the central coupling points and serialization/network constraints.
6. Select one contained vertical slice for architectural refactoring.
7. Use the TripleA data-model audit to determine what can be reused and what requires an adapter.
8. Revisit the fork/rewrite decision only after evidence from the first refactoring experiments.

## Working principle

The project should not ask:

> "Is TripleA good or bad?"

It should ask:

> "Which parts of TripleA provide a useful foundation, where are the architectural boundaries inadequate, and can those boundaries be improved incrementally without losing the existing engine's useful capabilities?"

That is the current architectural question.
