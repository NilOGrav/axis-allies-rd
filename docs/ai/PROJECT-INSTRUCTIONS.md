# Axis & Allies 1940 Global R&D — Project Instructions

This project develops the Axis & Allies 1940 Global R&D / technology-tree system, including research, technologies, resources, facilities, Graphviz, TripleA architecture, and optional modules such as Oil, Nuclear and Zombies.

## 1. Project memory

The GitHub repository is the project's persistent, versioned workspace and AI memory:

`https://github.com/NilOGrav/axis-allies-rd`

Persistent AI memory is stored in `docs/ai/`.

Relevant topic files should be read before substantial work. The structure includes:

- `00-project-context.md` — overall project context
- `01-research-system.md` — research system
- `02-technology-tree.md` — technology tree
- `03-resources.md` — resources
- `04-facilities.md` — facilities / Research Centres
- `05-graphviz.md` — visualisation
- `06-triplea.md` — TripleA
- `07-modules.md` — module framework
- `08-oil.md` — Oil
- `09-nuclear.md` — Nuclear
- `10-zombie.md` — Zombies
- `40-github.md` — GitHub / project-memory architecture
- `99-open-questions.md` — cross-topic unresolved questions
- `HANDOVER.md` — temporary session handover

Do not assume all files need to be read for every task. Read the topic(s) relevant to the task.

## 2. Authority and precedence

Use this precedence:

1. Current authoritative project data
2. Explicitly established project decisions
3. Current `docs/ai/` topic documents
4. `HANDOVER.md`
5. Historical discussions/documentation
6. AI inference

**Current authoritative CSV files define the current rules, design principles and technology definitions.**

AI-memory documents provide context and architecture but must not override current authoritative data.

When authoritative data conflicts with older documentation or conversation history, use the authoritative data.

The ODS and other documentation may provide additional context, but must not silently override current CSV data.

## 3. Status discipline

Always distinguish:

- **Established** — explicitly decided and accepted
- **Current** — current working design/parameter, potentially revisable
- **Proposed** — suggested but not accepted
- **Open** — unresolved
- **Historical** — retained for context, no longer current
- **Superseded** — replaced by a newer decision

Never present an inference or proposal as an established decision.

Do not silently resolve open questions.

## 4. Preserve project terminology

Use terminology from the current authoritative data and topic documents.

Do not reintroduce superseded terminology merely because it appeared in older conversations.

If historical terminology is relevant, identify it as historical.

## 5. Do not silently redesign

When analysing, documenting or implementing existing design:

- preserve established architecture;
- do not silently redesign it;
- do not turn an open question into a decision;
- distinguish existing design from proposed changes;
- identify inconsistencies rather than silently correcting them.

Project-specific concepts take precedence over generic alternatives.

## 6. Working method

For a substantial task:

1. Identify the relevant authoritative data/files.
2. Read the relevant `docs/ai/` topic document(s).
3. Check `99-open-questions.md` where relevant.
4. Inspect current project data/documentation.
5. Separate established facts, current design, proposals and inference.
6. Perform the requested work.
7. Identify newly established decisions or unresolved questions that belong in project memory.

Do not reconstruct current rules or technology definitions from memory when the authoritative files are available.

## 7. HANDOVER.md

`docs/ai/HANDOVER.md` is a temporary session bridge.

Use it to understand where the previous session stopped, recent decisions, unfinished work and intended next steps.

It is **not** a second permanent source of truth. Permanent knowledge belongs in the appropriate topic document.

## 8. Documentation

Permanent topic documents should preserve the project's handover method and normally contain:

- Purpose
- Current design
- Established decisions
- Current implementation
- Open questions
- Known constraints
- Relevant project files
- Important terminology
- Recent changes
- Do not assume
- Next intended work

Keep topic documents focused. Do not unnecessarily duplicate complete authoritative datasets.

## 9. Project variants

The core R&D rules apply to both Global 1940 and Global 1940 Halifax unless explicitly stated otherwise.

Do not introduce variant-specific IDs or architecture merely because the presentation differs.

## 10. Version control

Preserve existing repository work and avoid overwriting unrelated changes.

Normal Git workflow:

    git pull
    git status
    git add .
    git commit -m "..."
    git push
    git status

Do not assume a particular local filesystem path.

## 11. Licensing

Respect the established split licensing model:

- Original Python/software → MIT
- Original research/design data → CC BY 4.0
- Original documentation → CC BY 4.0
- Original `docs/ai/` documents → CC BY 4.0
- Generated representations consisting solely of original project content → CC BY 4.0 where applicable
- Third-party Axis & Allies material → not covered by project licenses
- Third-party dependencies → their own licenses

Do not assume every repository file is original project material or covered by one project license.

## 12. External information

Use external research when current verification or outside information is required.

Clearly distinguish external information from project-established information and AI inference.

External sources do not override established project decisions unless the project explicitly adopts the change.

## 13. Response discipline

For project work:

- be precise and concise;
- use current project terminology;
- distinguish fact, design and proposal;
- identify assumptions;
- identify unresolved issues;
- do not claim something is implemented when it is only designed or proposed;
- when documenting decisions, produce repository-ready text.

For design changes, consider their effect on the existing architecture before recommending them.

## Core rule

**Current authoritative project data and explicitly established decisions define the current design. `docs/ai/` provides persistent context. `HANDOVER.md` provides temporary session context. AI inference never silently becomes project fact.**
