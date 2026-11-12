# Topic: GitHub

Last updated: 2026-11-12
Status: Active

## Purpose

Define how GitHub is used as the repository, version-control system, project workspace, documentation location, and portable memory layer for the Axis & Allies 1940 Global R&D project.

This topic covers GitHub repository structure, version control, AI handover documentation, project documentation practices, and the distinction between authoritative project data and AI memory.

GitHub is part of the project's working infrastructure; it is not itself the source of truth for every type of project information.

## Current design

The project is maintained in the GitHub repository:

`https://github.com/NilOGrav/axis-allies-rd`

The repository contains the project's software, data, documentation, reference material, design history, generated artefacts, and AI handover documentation.

GitHub provides:

- version control;
- collaboration between human and AI contributors;
- a persistent project history;
- issue and project tracking;
- portable AI context through `docs/ai/`;
- a stable location for authoritative project files.

The repository should remain understandable to both humans and colleague AIs without requiring access to previous conversations.

## Established decisions

### Repository as project memory

GitHub is used as a persistent, versioned memory store for the project.

AI memory is organised by topic rather than as one large undifferentiated project summary.

Permanent AI-memory documents are stored under:

`docs/ai/`

The current structure is:

    docs/
    └── ai/
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
        ├── 40-github.md
        ├── 99-open-questions.md
        └── HANDOVER.md

The numbered topic documents are intended to become the permanent memory of their respective areas.

### Topic documents

Topic documents record the current state of a project area, including:

- purpose;
- current design;
- established decisions;
- current implementation;
- open questions;
- known constraints;
- relevant project files;
- terminology;
- recent changes;
- things that must not be assumed;
- intended next work.

Topic documents should preserve uncertainty rather than silently resolving it.

### HANDOVER.md

`docs/ai/HANDOVER.md` is a temporary session-oriented handover.

It records where the previous working session stopped and what the next AI should do.

It is not intended to become a second permanent source of truth.

Information that becomes permanent should be moved into the relevant topic document.

### AI-memory authority

AI-memory documents provide project context, architecture, history, decisions, and pointers.

They do not override authoritative project data.

When an AI-memory document conflicts with current authoritative project data, the authoritative project data takes precedence.

Current terminology in authoritative project files takes precedence over terminology preserved from older discussions.

AI inference must not be presented as an established project decision.

### Authoritative data

For the current R&D design, the authoritative CSV files define the current:

- rules;
- design principles;
- technology definitions.

AI-memory documents should therefore refer to authoritative data rather than duplicating detailed rules and technology definitions unnecessarily.

The ODS and other design documents can provide additional context where applicable, but should not silently override the current authoritative CSV data.

### Git workflow

Normal repository work follows the standard Git workflow:

    git pull
    git status
    git add .
    git commit -m "..."
    git push
    git status

Changes must be committed before they are pushed.

`git status` should be used before and after changes to understand the repository state.

Pull before beginning significant work where remote changes may exist.

### Branching

The main working branch is `main`.

Unless a specific task requires another branch, work is performed against the main project branch using the established repository workflow.

### Issues and project tracking

GitHub Issues are suitable for explicit TODOs, bugs, unresolved implementation problems, and follow-up work.

GitHub Projects may be used for broader Kanban-style tracking when useful.

Open design questions should not be silently converted into implementation tasks that imply a decision has already been made.

## Current implementation

The repository contains the project's software and data pipeline, including the technology-tree implementation and Graphviz generation.

Important project areas include:

- `data/` — project data;
- `src/` — implementation;
- `docs/` — project documentation and AI memory;
- `docs/reference/` — third-party/reference material where applicable;
- `archive/` — historical material where applicable.

The exact current repository contents should be checked rather than assumed from this document.

## Licensing

The repository uses a split licensing model because the project contains both original work and third-party Axis & Allies-derived/reference material.

Current intended licensing:

| Content | License |
|---|---|
| Original Python/software | MIT |
| Original research/design CSV/data | CC BY 4.0 |
| Original documentation | CC BY 4.0 |
| Original `docs/ai/` handover documents | CC BY 4.0 |
| Generated representations containing solely original project content | CC BY 4.0 |
| Third-party Axis & Allies material | Not covered by project licenses |
| Third-party dependencies | Their respective licenses |

Relevant repository files:

- `LICENSE`
- `LICENSE-DATA`
- `NOTICE`
- `docs/licensing.md`

The project does not claim ownership of Axis & Allies names, trademarks, official artwork, rulebook text, maps, scans, or other third-party material.

The project is an independent/fan-created project and is not presented as official, endorsed, sponsored, or affiliated with the rights holders.

Before applying a project license to an individual file, its origin should be considered. Mixed or third-party material must not accidentally be relicensed as original project content.

## Known constraints

### Do not use AI memory as a substitute for project data

An AI should not reconstruct current technology definitions or rules from an old conversation when the authoritative project data is available.

### Do not duplicate authoritative data unnecessarily

AI-memory documents should explain architecture and decisions, but should not become parallel copies of the complete CSV datasets.

Duplication creates a risk that an old AI-memory statement survives after the actual project data has changed.

### Preserve historical context

Older decisions and terminology can be useful for understanding why the project developed in a particular direction.

However, historical information must be identified as historical when it is no longer current.

### Do not silently resolve open questions

If the project has not decided an issue, the AI-memory document should record it as open rather than selecting an answer by inference.

Cross-topic unresolved questions belong in:

`docs/ai/99-open-questions.md`

Topic-specific unresolved questions should remain in their relevant topic document.

### Avoid repository-path assumptions

Instructions should refer to the repository directory or repository name rather than assuming a particular local filesystem path.

## Relevant project files

### AI memory

- `docs/ai/README.md`
- `docs/ai/HANDOVER.md`
- `docs/ai/00-project-context.md`
- `docs/ai/99-open-questions.md`
- topic-specific documents under `docs/ai/`

### Licensing

- `LICENSE`
- `LICENSE-DATA`
- `NOTICE`
- `docs/licensing.md`

### Project data and implementation

- `data/`
- `src/`
- `docs/`

The exact current filenames and data layout should be verified from the repository when performing implementation work.

## Important terminology

**Authoritative data**  
The project files that define the current design/rules/data for their respective subject.

**AI memory**  
Persistent contextual documentation intended to allow colleague AIs to understand the project without access to previous conversations.

**Topic handover**  
A permanent topic document under `docs/ai/` containing the current state of one project area.

**Session handover**  
`docs/ai/HANDOVER.md`, which records temporary working state between AI sessions.

**Historical**  
Information retained for context but no longer necessarily part of the current design.

**Established**  
A decision explicitly made and accepted as part of the project.

**Current**  
The current working design or parameter, which may still be revised.

**Proposed**  
A suggestion that has not yet been accepted.

**Open**  
An unresolved question or decision.

**Superseded**  
A previous decision or design that has been replaced.

## Recent changes

The project has established `docs/ai/` as the persistent AI-memory structure.

The permanent-memory approach was deliberately separated from `HANDOVER.md` so that:

- topic files contain lasting knowledge;
- `HANDOVER.md` contains temporary session state;
- `99-open-questions.md` contains cross-topic unresolved issues.

A split licensing model was also established for software, original data/documentation, and third-party material.

## Do not assume

- That every file in the repository is original project material.
- That every file is covered by MIT.
- That every file is covered by CC BY 4.0.
- That Axis & Allies-derived material can be relicensed by the project.
- That AI-memory documents override current CSV data.
- That historical AI-memory terminology remains current.
- That an unresolved question has been decided merely because an AI proposed a solution.
- That the repository structure described here is immutable; verify actual current files before implementation work.
- That generated files are automatically original merely because they were generated by project tooling.

## Next intended work

- Keep `docs/ai/40-github.md` synchronized with material changes to the project's GitHub workflow or repository-memory architecture.
- Update the relevant topic document when a GitHub-related architectural decision becomes established.
- Keep licensing documentation synchronized when new categories of project material are added.
- Audit repository areas such as `assets/`, `archive/`, and `docs/reference/` when necessary to ensure third-party material is not unintentionally covered by project licensing.
- Continue using topic-specific AI-memory documents rather than expanding this document into a general project summary.

## Working principle

GitHub stores the project's versioned work and its persistent AI context.

The repository's authoritative project data defines the current design.

The `docs/ai/` documents explain the project to future humans and AIs.

`HANDOVER.md` records where the current working session left off.

These roles should remain separate so that project memory remains useful without becoming a competing source of truth.
