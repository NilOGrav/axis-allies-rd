# Topic: Axis & Allies Global 1940 Zombies Module

Last updated: 2026-11-09
Status: Active

## Purpose

Design an optional Zombie module for **Axis & Allies Global 1940** that can:

1. Operate as a **standalone Global 1940 Zombies expansion**.
2. Integrate with the existing **A&A R&D system** when both modules are enabled.
3. Preserve the core gameplay identity and mechanics of the official *Axis & Allies & Zombies* expansion wherever practical.
4. Adapt and expand the Zombie event system where the much larger Global 1940 map and longer game require it.
5. Allow existing R&D technologies to provide contextual anti-Zombie benefits, analogous to the way the Oil module adds contextual effects to existing technologies.

The module should add the Zombie layer without replacing the underlying Axis & Allies or R&D systems.

---

## Current Status

The Zombie module is in **early design / architecture phase**.

The fundamental direction is established, but the actual Global 1940 card deck, detailed Zombie rules, dedicated Zombie technologies, and exact R&D/Desperate Measures relationship are not yet designed.

The current project Rule Inventory already identifies this module as ZOM and records:

- ZOM-001 — Zombie module is optional.
- ZOM-002 — Zombie mechanics are adapted specifically for Global 1940.
- ZOM-003 — Zombie system can operate as a standalone optional module.
- ZOM-004 — Zombie system can interact with R&D when the integrated version is enabled.
- ZOM-005 — Existing R&D technologies can contextualise Zombie effects.
- ZOM-006 — Dedicated Zombie technologies are complementary rather than replacing the main tree.
- ZOM-007 — Exact interaction with Desperate Measures remains unresolved.

---

## Core Design Principle

> **Preserve the AAZ Zombie gameplay loop; adapt and expand it for Global 1940 rather than replacing it with a fundamentally different Zombie system.**

The official *Axis & Allies & Zombies* rules should therefore be treated as the starting point and reference implementation.

Where possible, Global 1940 should behave like AAZ.

Deviations should be introduced only when justified by:

- Global 1940's substantially larger map;
- the greater number of powers and theatres;
- longer expected game duration;
- interaction with Global 1940-specific mechanics;
- interaction with the R&D system;
- or a clear improvement in gameplay variety while preserving the AAZ core.

---

## Standalone + R&D-Integrated Architecture

The Zombie module must support two modes:

### Standalone

The Zombie system functions without the R&D module.

It should contain everything required to introduce, manage, and fight Zombies.

### Integrated

When R&D is enabled, the Zombie module can interact with:

- existing technologies;
- dedicated Zombie-related research;
- Research Centres where appropriate;
- resources and other optional modules where an interaction is justified.

The integrated version should **not become a separate technology ecosystem disconnected from the main R&D tree**.

The existing R&D architecture already establishes that optional modules can introduce their own technologies, facilities, resources, or rules while remaining modular.

---

## AAZ as the Mechanical Baseline

The official *Axis & Allies & Zombies* system is the starting point.

The following general gameplay elements should therefore be investigated first and preserved where possible:

- Zombie event/card draw;
- Zombie appearance/spawning;
- Zombie movement;
- Zombie attacks against units;
- Zombie capture of territories;
- interaction between conventional combat and Zombies;
- infantry casualties becoming Zombies;
- removal/destruction of Zombies;
- Zombie-related territory and industrial-complex effects;
- the Desperate Times / Desperate Measures card structure.

Exact rules must be taken from the official AAZ rules/card set rather than reconstructed from memory.

The next design phase should therefore be a systematic **AAZ → Global 1940 conversion analysis**.

---

## Why a Global-Specific Deck Is Needed

The official AAZ deck should **not simply be copied unchanged** into Global 1940.

Global 1940 has a much larger map and substantially more territories than the AAZ/1942 environment.

A direct port risks producing events that are:

- geographically irrelevant for long periods;
- too widely dispersed to matter;
- excessively concentrated in particular areas;
- or repetitive over a long Global 1940 game.

There is also a second issue: the official Zombie deck has relatively limited event variety compared with the scope of a Global 1940 game.

Therefore the working direction is:

> **Retain AAZ's underlying Zombie mechanics while creating a more varied Global 1940 event deck.**

This is an adaptation/expansion of the card layer, not a replacement of the Zombie rules.

---

## Randomness and Geographic Selection

The preferred design philosophy is:

> **Let the shuffled card deck provide most of the randomness instead of repeatedly rolling for random individual map territories.**

Avoid unnecessary mechanisms such as:

> "Roll for a random European territory."

A huge territory lookup table would add procedural overhead without necessarily producing interesting decisions.

Instead, Zombie cards should preferably identify meaningful locations through **game-state conditions**.

Examples of the design direction—not final card rules—include effects referring to:

- territories containing enemy units;
- territories containing infantry;
- industrial complexes;
- capitals;
- contested territories;
- territories where major combat recently occurred;
- territories already containing Zombies.

This allows the Zombie system to remain strategically relevant to the actual Global 1940 game.

---

## Card Variety

The deck should contain more variety than the original AAZ deck while remaining mechanically simple.

Possible event families discussed during exploration include:

- Outbreak;
- Rising Dead / conversion effects;
- Horde;
- Migration;
- Panic;
- Military Disaster;
- Strategic Outbreak;
- Mutation / altered Zombie behaviour;
- Global events;
- unusual/wild-card events.

**These are design exploration categories, not established final categories.**

Do not treat a fixed number of card families, card types, or cards as decided.

Similarly, earlier estimates such as 50–70 cards are **not final parameters**.

The correct deck size should be determined after analysing the original AAZ deck and its card frequencies.

---

## Strategic Relevance of Zombie Events

A recurring design goal is that Zombies should interact with the actual war rather than merely appear randomly across the map.

Cards should therefore, where appropriate, create situations that matter to players strategically.

The event system should be capable of producing effects around:

- military concentrations;
- industrial capacity;
- capitals;
- active fronts;
- recent battles;
- supply/logistics-relevant locations;
- existing Zombie populations.

This should make the Zombie apocalypse follow the strategic situation rather than becoming an unrelated mini-game.

---

## R&D Integration

R&D integration is a first-class design objective.

Existing technologies should be able to acquire **additional contextual benefits against Zombies**, in the same general design philosophy already used by the Oil module.

For example, a conventional technology might retain its normal effect while gaining an additional anti-Zombie application when the Zombie module is active.

This means that a player who has invested in conventional research before or during the Zombie outbreak can be better prepared without necessarily having researched a dedicated Zombie technology.

The principle is:

> **Zombie interaction should extend the existing R&D system rather than invalidate or replace it.**

---

## Existing Technologies vs Dedicated Zombie Technologies

The current direction is to use both layers.

### Existing technologies

Existing technologies can gain Zombie-related secondary effects where appropriate.

These should be treated similarly to contextual Oil bonuses: the technology remains fundamentally part of its original domain, while the optional Zombie module gives it an additional application.

### Dedicated Zombie technologies

A limited number of Zombie-specific technologies may be added.

Their purpose should be to represent capabilities that conventional technologies cannot adequately represent, such as:

- understanding Zombie behaviour;
- preventing or reversing infection/zombification;
- specialised containment;
- advanced Zombie-specific countermeasures;
- long-term solutions.

Dedicated Zombie technologies should therefore be **complementary to the main R&D tree**, not a parallel replacement military tree.

The current Rule Inventory already records this as ZOM-006.

---

## Desperate Measures and R&D

The relationship between **Desperate Measures** and R&D is intentionally **not decided**.

Several possible relationships have been discussed:

1. Desperate Measures could provide temporary versions of capabilities represented permanently by R&D.
2. Desperate Measures could provide temporary emergency technological effects.
3. Desperate Measures could interact with or accelerate R&D.
4. Desperate Measures and R&D could remain separate layers that merely interact.
5. Some combination of the above may prove appropriate.

No option has been selected.

**Do not redesign or decide this prematurely.**

First analyse the actual AAZ Desperate Measures cards and determine what mechanical role they play.

The project Rule Inventory explicitly records the relationship as an open issue (ZOM-007).

---

## Relationship to Other Optional Modules

The Zombie module should follow the project's general modular philosophy.

The R&D system is explicitly designed so optional modules can add technologies, facilities, resources, and rules without altering the core research framework.

Potential future interactions with other modules should therefore be considered where mechanically meaningful, but should **not be invented merely for the sake of cross-module interaction**.

In particular:

- Oil may interact with Zombie-related logistics or existing technology effects if justified.
- Resources may interact with Zombie technologies where explicitly designed.
- Nuclear technologies may potentially have Zombie applications, but no such rules are currently established.
- Research Centres may potentially provide access to Zombie research if explicitly designed, but this is not yet decided.

---

## Design Constraints

The Zombie module should:

- remain recognisably *Axis & Allies & Zombies*;
- avoid unnecessary complexity;
- avoid requiring large territory lookup tables;
- make Zombies strategically relevant on the Global 1940 map;
- preserve the normal Axis & Allies game as the underlying game;
- preserve the modular nature of the R&D system;
- avoid creating an isolated Zombie technology tree;
- distinguish established rules from experimental design ideas;
- remain usable both standalone and with R&D enabled.

---

## Not Yet Decided

The following are explicitly open:

- exact AAZ mechanics to retain unchanged;
- exact Global 1940 changes required by map scale;
- exact Zombie card count;
- exact card-family structure;
- exact card distribution/frequency;
- exact card effects;
- exact Zombie spawning rules for Global 1940;
- exact regional/geographic treatment;
- exact interaction with industrial complexes;
- exact Zombie-controlled territory rules where Global 1940 creates edge cases;
- exact dedicated Zombie technology count;
- exact number of Zombie technology tiers;
- exact Zombie technology prerequisites;
- exact relationship between Desperate Measures and R&D;
- exact interaction between Zombie research and Research Centres;
- exact interaction with Oil and other optional modules;
- exact win/end conditions for a Global Zombie game.

Do not treat exploratory numbers or example mechanics from earlier discussion as settled rules.

---

## Important Non-Decisions

The following ideas were discussed but **must not be treated as current design decisions**:

### Infection Track

A multi-level Global Infection Track was proposed during early brainstorming.

It was not adopted.

Do not introduce one unless reconsidered explicitly.

### Large Dedicated Zombie Technology Tree

An initial proposal suggested approximately 13–18 Zombie technologies across three tiers.

This was subsequently reconsidered.

The current direction is toward a **limited number of dedicated Zombie technologies**, complemented by Zombie effects on existing technologies.

The final number remains open.

### Fixed 50–70 Card Deck

A 50–70-card Global deck was suggested as an exploratory estimate.

This is not a decided deck size.

### Specific Card Categories

Outbreak/Horde/Migration/etc. are exploratory categories only.

They should not be treated as the final deck taxonomy.

### Random Territory Tables

A numbered regional territory table / D100 approach was considered and rejected as the preferred direction.

The current preference is to use the card's effect and game state to determine meaningful locations.

---

## Recommended Next Work

The next major task is to perform a **systematic analysis of the official AAZ rules and card deck**.

Create a conversion matrix approximately along these lines:

| AAZ mechanic/card | Original rule/effect | Global 1940 compatible? | Required adaptation | R&D interaction |
|---|---|---|---|---|
| Zombie card timing | | | | |
| Zombie spawning | | | | |
| Zombie movement | | | | |
| Zombie combat | | | | |
| Infantry → Zombie | | | | |
| Zombie territory capture | | | | |
| Industrial complexes | | | | |
| Desperate Times | | | | |
| Desperate Measures | | | | |
| Special cards | | | | |

Then classify the existing cards by their actual mechanics.

This should establish:

1. What can be transferred directly.
2. What needs Global-specific adaptation.
3. What is too repetitive for the larger game.
4. What additional card variety is actually useful.
5. Which Desperate Measures effects naturally belong near R&D.
6. Which effects should remain purely card-based.

Only after this analysis should the Global deck and Zombie technologies be designed.

---

## Source of Truth / Related Project Memory

The project's Rule Inventory is maintained in the Documentation & Design Log and currently contains the ZOM rules listed above.

The general R&D architecture establishes modular optional systems and allows module-specific technologies/effects while preserving the core R&D framework.

The project-wide architecture also distinguishes technologies from facilities, resources, paths, and modules; cross-domain interactions should normally be represented through relationships rather than duplicating the technology node across domains.

---

## Continuation Rule

A future AI continuing this topic should:

1. Treat the official AAZ rules as the baseline.
2. Treat the existing ZOM entries in the Rule Inventory as established project state.
3. Treat Desperate Measures/R&D integration as unresolved.
4. Distinguish confirmed decisions from brainstorming.
5. Analyse the official AAZ cards before designing the Global deck.
6. Preserve the standalone + integrated architecture.
7. Avoid introducing a new Zombie subsystem unless the AAZ baseline and Global-scale analysis demonstrate that it is necessary.
8. Update this handover when a Zombie design decision becomes established.
