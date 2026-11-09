# AI Handover

Last updated: 2026-11-07

## Purpose

This file provides the **current session handover** for the next AI working on the Axis & Allies R&D project.

It is intentionally temporary and should not become a second source of truth for the project's rules or technology data.

For the permanent AI-memory structure, read:

- `docs/ai/README.md`
- the relevant numbered topic file(s)

---

## Project

**Axis & Allies 1940 Global R&D / Technology Tree**

The project develops a modular R&D system for Axis & Allies 1940, including:

- research mechanics;
- technology trees;
- technological paths;
- domains;
- Research Centres and other facilities;
- strategic resources;
- units and capabilities;
- optional modules;
- Graphviz/SVG visualisation;
- eventual TripleA implementation.

The system is intended to support the applicable Global 1940 variants, including the Halifax variant.

---

## Source of truth

The **CSV files are the authoritative source for the current rules, design principles, and technology definitions**.

When working on the project:

> **Do not reconstruct rules or technology data from this handover or from AI memory when the authoritative CSV contains the relevant information.**

The AI-memory files exist to provide context, architecture, history, terminology, decisions, and pointers to the authoritative project data.

If an AI-memory document conflicts with the current authoritative CSV data, the CSV takes precedence.

The current ODS/design documents may provide additional design context, but the current CSV data should be treated as authoritative for the corresponding rules, design principles, and technology definitions.

---

## Important working principle

Do not duplicate detailed rules or technology definitions here.

For example, this file should **not** maintain:

- research costs;
- research resolution tables;
- technology prerequisites;
- technology effects;
- facility statistics;
- resource values;
- unit effects;
- technology IDs and definitions.

Those belong to the authoritative project data.

This prevents the AI-memory system from becoming stale when the design changes.

---

## Current work context

The project has been developing the AI-memory / handover structure itself.

The agreed permanent structure is:

```text
docs/ai/
├── README.md
├── 00-project-context.md
├── 01-research-system.md
├── 02-technology-tree.md
├── 03-resources.md
├── 04-facilities.md
├── 05-graphviz.md
├── 06-triplea.md
├── 07-modules.md
├── 08-oil.md
├── 09-nuclear.md
├── 10-zombie.md
├── 99-open-questions.md
└── HANDOVER.md
```

`README.md` defines the purpose, authority hierarchy, status vocabulary, and update rules for this system.

The numbered files are the permanent topic-based project memory.

`HANDOVER.md` is the temporary session bridge.

---

## Current architectural context

The project has evolved beyond a simple technology list into a connected data model involving technologies, facilities, resources, research eligibility, paths, domains, modules, and implementation.

Important architectural distinctions include:

- technology;
- resource;
- facility;
- Research Centre;
- technological path;
- domain;
- module.

These should not be silently collapsed into one another.

The permanent topic files contain the relevant architectural context. Check those files rather than reconstructing the architecture from this handover.

---

## Terminology

Use the **current terminology in the authoritative project data**.

Do not rely on terminology appearing in older conversations, older AI-memory text, or previous handovers if the current data uses different terminology.

In particular, terminology changes should be made in the authoritative source first and then reflected in the AI-memory documentation where appropriate.

---

## Current unresolved work

The project contains a number of areas that have been discussed but may still require explicit resolution.

The authoritative status should be checked in:

```text
docs/ai/99-open-questions.md
```

Do not resolve an open question merely because a plausible solution exists.

---

## Working procedure for the next AI

Before making a substantive project change:

1. Read `docs/ai/README.md`.
2. Identify the relevant topic.
3. Read the relevant topic file(s).
4. Check the authoritative CSV data.
5. Check the relevant implementation files if the task concerns code.
6. Distinguish established decisions from open questions and proposals.
7. Make the requested change.
8. Update the relevant permanent AI-memory topic if the project state materially changed.
9. Update this `HANDOVER.md` if the change is relevant to the next session.

Do not use this file as a substitute for checking the authoritative project data.

---

## Next intended work

The next AI should continue from the actual current repository state and the user's latest request.

When a session completes a meaningful piece of work:

- update the relevant permanent topic file;
- update `99-open-questions.md` if an open question was resolved or changed;
- replace this handover with a concise summary of the new session state.

---

## Handover maintenance

This file should remain short enough to be useful.

When information in this file becomes permanent project knowledge:

1. Move the information to the appropriate topic file.
2. Remove the duplicated detail from `HANDOVER.md`.
3. Leave only the information needed to orient the next session.

The objective is:

> **Permanent topic files remember the project.  
> `HANDOVER.md` remembers where the last session left off.  
> The authoritative CSVs define the current rules and technology data.**
