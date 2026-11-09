# AI Project Memory

This directory contains **topic-based project memory for AI assistants** working on the Axis & Allies R&D project.

Its purpose is to make the project understandable and transferable between different AI assistants and different working sessions without requiring the entire project history to be reconstructed.

This is **context and handover documentation**, not the authoritative game-design source.

---

## 1. How to use this directory

When starting work on the project:

1. Read this `README.md`.
2. Identify the topic relevant to the task.
3. Read the corresponding topic file(s).
4. Read `99-open-questions.md` if the task touches an unresolved design area.
5. Check the actual project files referenced by the topic documentation before making changes.
6. Use the current project data/design files as the authority for concrete implementation details.

Do **not** automatically read every file in `docs/ai/`. The topic files are intentionally separated so that an AI can load only the context relevant to the current task.

### Topic files

| File | Topic |
|---|---|
| `00-project-context.md` | Global project context, architecture and terminology |
| `01-research-system.md` | Core R&D / research mechanics |
| `02-technology-tree.md` | Technologies, prerequisites, domains, paths and technology-tree structure |
| `03-domain-design.md` | Domain structure in detail |
| `04-resources.md` | Strategic resources and resource mechanics |
| `05-facilities.md` | Facilities, Research Centres and infrastructure |
| `10-modules.md` | Modular architecture and optional modules |
| `11-module-oil.md` | Oil module |
| `12-module-nuclear.md` | Nuclear module |
| `13-module-zombie.md` | Zombie module |
| `20-visualization-code.md` | Code architecture to deliver different visualisation based on a csv technology list |
| `21-graphviz.md` | Graphviz/SVG generation and visual tree architecture |
| `30-triplea.md` | TripleA data model and implementation |
| `99-open-questions.md` | Cross-topic unresolved questions |
| `HANDOVER.md` | Temporary current-session handover |

---

## 2. Authority hierarchy

AI memory exists to provide context. It does **not** override the actual project.

Use the following priority order when information conflicts:

1. **Explicit current project data/design files**
2. **Explicit established decisions documented in the project**
3. **Current topic files in `docs/ai/`**
4. **Older project discussion/history**
5. **AI inference or general knowledge**

The AI must not silently resolve a conflict by choosing whichever source seems more reasonable.

If the authoritative source is unclear, identify the conflict and mark it as an open question rather than inventing a resolution.

### Important distinction

The following are not equivalent:

> “This was discussed.”

> “This was proposed.”

> “This is currently being considered.”

> “This was decided.”

Only the last one represents an established decision.

---

## 3. Status vocabulary

Use these status labels consistently.

| Status | Meaning |
|---|---|
| **Established** | Explicitly decided and accepted as part of the design |
| **Current** | Current working parameter/design, but potentially subject to revision |
| **Proposed** | Suggested but not accepted as a decision |
| **Open** | Known unresolved question |
| **Historical** | Former design or discussion retained for context |
| **Superseded** | Replaced by a newer decision |

Do not convert a `Proposed`, `Open`, `Historical`, or `Superseded` item into `Established` merely because it appears plausible.

If something is uncertain, preserve the uncertainty.

---

## 4. What belongs in a topic file

Each topic file should be sufficiently self-contained that another AI can understand the current state without reading the entire conversation history.

Use the following structure where practical:

```markdown
# Topic: [Name]

Last updated: YYYY-MM-DD
Status: Active

## Purpose

What this part of the project is responsible for.

## Current design

The current agreed architecture and behaviour.

## Established decisions

- ...

## Current implementation

- ...

## Open questions

- ...

## Known constraints

- ...

## Relevant project files

- ...

## Important terminology

- ...

## Recent changes

- ...

## Do not assume

Important things discussed but NOT decided.

## Next intended work

- ...
```

The exact sections may be adapted when a topic needs a more useful structure.

---

## 5. Do not duplicate authoritative data unnecessarily

The AI-memory files should explain **how the project works and what decisions have been made**.

They should not become a second copy of the complete technology database, facility database, resource database, or TripleA configuration.

For example:

- `02-technology-tree.md` should document the technology-tree architecture, domain rules, prerequisite logic, important decisions and implementation conventions.
- The actual technology definitions should remain in the project's authoritative data files.
- `04-facilities.md` should document the facility architecture and rules, while the actual facility records remain in the appropriate data source.
- `05-graphviz.md` should document the Graphviz architecture rather than duplicating generated SVG data.

Where exact data matters, point to the relevant project file.

---

## 6. Preserve uncertainty

One of the most important purposes of this memory system is to prevent unresolved design questions from being accidentally turned into rules.

If a question is unresolved:

- keep it explicitly marked **Open**;
- record competing possibilities when useful;
- do not choose one without an explicit decision;
- do not write the chosen possibility as though it were already established.

This is especially important for areas where the project documentation already identifies gaps in the rule inventory.

An AI should prefer:

> “This is currently unresolved.”

over:

> “The rule is probably X.”

---

## 7. Distinguish design from implementation

The project has several layers that should not be conflated.

For example:

- **Technology** is not the same as a facility.
- **Resource** is not the same as technology.
- **Research Centre** is a facility/data-model category, not automatically a technology.
- **Graphviz presentation** is not the underlying technology-tree data model.
- **TripleA implementation** is not the same thing as the game-design rule.
- **Optional modules** should not silently become part of the core rules.

When documenting a decision, state which layer it belongs to.

---

## 8. Project variants

The project supports multiple Axis & Allies contexts, including:

- Europe 1940
- Pacific 1940
- Global 1940
- Global 1940 Halifax

The core R&D architecture is intended to apply consistently across the applicable variants.

Variant-specific behaviour should therefore be documented as applicability or configuration where appropriate rather than creating unnecessary separate technology trees or incompatible identifiers.

Stable IDs should not encode a scenario/variant unless the underlying entity is genuinely variant-specific.

---

## 9. Modules

Optional systems are modular.

A module may introduce its own:

- technologies,
- facilities,
- resources,
- rules,
- prerequisites,
- effects.

Core R&D should remain playable without optional modules.

Module-specific content must not be silently treated as core content.

If a module interaction is not yet defined, record it as an open question rather than assuming how the systems should interact.

---

## 10. Updating AI memory

Update the relevant topic file when an important design decision is made.

Prefer updating the **single topic file that owns the information** rather than copying the same decision into multiple files.

When a decision supersedes an earlier one:

1. Update the current section.
2. Mark the old decision as `Superseded` or `Historical` where retaining it is useful.
3. Record the newer decision.
4. Update `99-open-questions.md` if the decision closes an open question.
5. Update `HANDOVER.md` only when the change is relevant to the current session.

Do not create duplicate summaries merely because a decision is important.

---

## 11. Keeping `HANDOVER.md` useful

`HANDOVER.md` is different from the numbered topic files.

It is a **temporary session handover document**.

It should answer:

- What was being worked on?
- What changed during the session?
- What decisions were made?
- What files were changed?
- What remains unresolved?
- What should the next AI do?
- Is there anything important the next AI should verify before continuing?

Once its information has been incorporated into the appropriate permanent topic files, obsolete handover material should be removed or replaced.

The numbered topic files are the long-term memory.

`HANDOVER.md` is the short-term bridge between sessions.

---

## 12. Open questions

`99-open-questions.md` contains cross-topic unresolved questions that deserve visibility.

A question should remain there until it is actually resolved.

When resolving an open question:

1. Record the decision in the appropriate topic file.
2. Remove or mark the corresponding item as resolved in `99-open-questions.md`.
3. If the decision materially affects another topic, update that topic as well.

Do not use `99-open-questions.md` as a general TODO list. It is specifically for **design questions whose answer has not yet been established**.

---

## 13. AI behaviour rules

An AI working on this project should:

- preserve established decisions;
- distinguish fact, current design, proposal and inference;
- check the relevant project files before changing implementation;
- keep unresolved questions explicitly unresolved;
- avoid silently redesigning the system;
- avoid inventing missing rules;
- prefer existing project terminology;
- preserve stable IDs unless an explicit change is required;
- document important decisions in the appropriate topic file;
- update AI memory when the current design materially changes;
- keep implementation details separate from game-design decisions.

An AI should **not**:

- treat its own previous answer as authoritative;
- treat an old conversation as more authoritative than current project data;
- infer a missing rule and record it as established;
- silently reconcile contradictory design documents;
- duplicate large authoritative datasets into AI memory;
- turn optional-module content into core rules;
- remove an open question merely because a plausible answer exists.

---

## 14. Working principle

The purpose of this directory is not to make an AI believe it already knows everything about the project.

The purpose is to let an AI quickly determine:

> **What is established, what is current, what is uncertain, where the actual source lives, and what should be worked on next.**

When in doubt, preserve the distinction between those categories.
