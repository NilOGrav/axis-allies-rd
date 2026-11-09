# Topic: Research System

Last updated: 2026-11-09
Status: Active

## Purpose

Define the core R&D research mechanism and the research-resource economy for the Axis & Allies R&D system, including Research Tokens, research assignment and resolution, technological eligibility, research-capacity sources, and the relationship between the technology tree and the research economy.

## Current design

The research system uses a separate resource called **Research Token (RT)**.

An RT represents a discrete research opportunity, not accumulated progress toward a technology.

The current conceptual architecture has three layers:

1. **Technological structure** — determines what technologies are eligible through tiers, dependencies, AND/OR routes, infrastructure, resources, and other prerequisites.
2. **Research economy** — determines how much research capacity a nation has, primarily through IPC investment and later through research-capacity sources and National Objectives.
3. **Research resolution** — determines whether an assigned research attempt acquires its target technology.

Current flow:

```
Research Token
    ↓
Research attempt
    ↓
Eligible discrete technology
    ↓
Research resolution
    ↓
Technology acquired or attempt fails
```

Every technology currently costs exactly **1 RT** for a research attempt.

The current baseline IPC conversion is **5 IPC → 1 RT**. This is a current working parameter and remains subject to balancing.

RT can be saved between turns.

## Established decisions

- The research resource is called **Research Token (RT)** rather than Research Point (RP).
- One RT funds one research attempt.
- Every technology currently has the same research cost: **1 RT**.
- RT are discrete research opportunities, not progress bars or percentage completion.
- RT pools are public information.
- Research targets are secret.
- Research assignments are made at the **start of the player's turn**, alongside normal unit purchases.
- The player secretly selects the target technology when assigning the RT.
- The number of RT committed is public; the identity of the target technology is not.
- Research resolves during the **deployment phase**.
- At resolution, the player reveals the target and determines the research result.
- Multiple RT can be assigned in the same turn; there is no general one-technology-per-turn limit.
- Research eligibility is determined from the technological state **at the start of the turn**, when research is assigned.
- Technologies acquired during the current turn cannot make additional already-assigned research attempts eligible during that same turn.
- This prevents same-turn research chains such as using several RT to acquire a technology and immediately use that new technology as a prerequisite for another research attempt.
- Multiple RT therefore primarily increase **research breadth** rather than allowing accelerated **research depth**.
- Research resolution currently uses a d6:
  - **1 = failure:** the RT is lost, no technology is acquired, and the attempted technology remains secret.
  - **2–5 = success:** the target technology is acquired and the RT is consumed.
  - **6 = breakthrough:** the target technology is acquired and the RT is retained for the following round.
- A breakthrough does not create an additional research attempt during the same turn.
- The secrecy of the target is preserved on failure.
- The technology tree, rather than escalating RT costs, is intended to provide much of the progression and pacing through meaningful prerequisites and technological journeys.
- Stronger or later technologies are therefore not currently made more expensive by assigning them more RT.

## Research economy

The research economy should remain small and integrated with the existing technology tree.

Research-capacity technologies/facilities are intended to be **sparse convergence points** within the existing tree rather than a separate parallel research tree.

A small number of RT generators may be distributed across different technological paths.

Where appropriate, their prerequisites can deliberately use **mutually exclusive or competing keystones/routes**. This prevents a nation from collecting every RT generator and becoming an unrestricted research powerhouse, while still allowing different nations and strategies to obtain meaningful research capacity through different paths.

Conceptually:

```
Existing technology paths
        ↓
Competing / alternative prerequisites
        ↓
Research-capacity technology or facility
        ↓
RT generation
```

The intended design is approximately **one major RT-generating element per tier**, but the exact technologies, prerequisites, yields, and tier placement are not yet fully defined.

The **University** is an example of this type of research-capacity element. Its exact tier, prerequisites, implementation and RT yield remain subject to the detailed design work.

RT generators should primarily depend on technologies already present in the main technology tree rather than creating an independent chain such as Research Administration → Scientific Management → University → Advanced University.

## National Objectives

National Objectives may provide additional RT as rewards for achieving strategic conditions, following the general role of National Objectives in the base Axis & Allies game.

The objective system and persistent RT generators serve different functions:

- **RT generators:** persistent research capacity resulting from technological/institutional investment.
- **National Objectives:** strategic/event-driven injections of research capacity.

National Objectives should not necessarily refer directly to research. They may reward strategic conditions, resources, territories, capabilities, or other national goals, with the resulting RT feeding into the general research economy.

Exact National Objectives and RT amounts remain to be designed.

## Research-capacity design principles

- Keep the number of RT generators small.
- Integrate RT generators into the existing technology tree.
- Prefer meaningful existing technological prerequisites over a separate research branch.
- Use competing or mutually exclusive prerequisite routes where useful to limit maximum RT generation.
- Preserve multiple viable paths to research capacity.
- Avoid allowing RT generation to snowball without meaningful technological opportunity cost.
- Research capacity should represent the ability to conduct more research, not bypass technological prerequisites.
- Additional RT sources should not change the fundamental one-RT-per-research-attempt model unless explicitly decided later.

## Known constraints

- The technology tree and research economy are separate layers and must not be conflated.
- Research Centres are a distinct facility/data-model category and are not automatically RT generators.
- A facility that generates RT may also serve another function, but those functions should remain conceptually distinct.
- RT generation is an economy mechanic; it does not itself make otherwise-ineligible technologies eligible.
- Start-of-turn eligibility prevents newly acquired technologies from creating same-turn research chains.
- Research targets must remain secret until research resolution.
- Failure must not reveal the attempted technology.
- The research economy should not be used to reintroduce arbitrary technology progress stages or percentage completion.

## Open questions

- Is **5 IPC → 1 RT** the final balanced conversion?
- What are the exact RT generators and their yields?
- Which tier contains the University?
- What exact prerequisites should each RT generator use?
- Which prerequisite groups should be mutually exclusive?
- Can RT be accumulated indefinitely, or should a holding limit eventually be introduced?
- Which National Objectives generate RT, and how much?
- Are there additional RT sources such as captured research assets, espionage, objectives beyond National Objectives, or special events?
- How should RT generation interact with Research Centres where a facility has both functions?
- Are any variant-specific RT sources required for Global 1940 versus Global 1940 Halifax?

## Relevant project files

- `docs/ai/README.md` — AI-memory structure, authority hierarchy and status rules.
- `docs/ai/02-technology-tree.md` — technology-tree architecture and prerequisite logic.
- `docs/ai/04-facilities.md` — facilities and Research Centres.
- `docs/ai/99-open-questions.md` — unresolved cross-topic questions.
- `data/research/` — authoritative research/technology design data; the latest ODS is the primary design source according to project memory.

## Important terminology

- **Research Token (RT):** the resource used to make a research attempt.
- **Research attempt:** one attempt to acquire one eligible technology using 1 RT.
- **Research target:** the secretly selected technology being attempted.
- **Research generator:** a defined source that provides recurring RT.
- **Research-capacity element:** broader term for a technology/facility that increases research capacity.
- **Research Centre:** a facility/data-model category that may act as a technological eligibility/prerequisite gate; it is not automatically an RT generator.

## Recent changes

- The research resource terminology changed from **Research Point (RP)** to **Research Token (RT)**.
- The uniform **1 RT per technology** model was established as the current research-cost model.
- The research assignment/resolution sequence was defined: secret assignment at turn start, public commitment, resolution during deployment.
- The start-of-turn eligibility snapshot was established to prevent same-turn technology chains.
- Research-capacity generation was narrowed to a small number of sparse elements distributed across the existing tree.
- Competing and mutually exclusive prerequisite routes were introduced as a design principle for limiting total RT-generating capacity.
- National Objectives were identified as a separate potential source of RT.
- Specific RT generators, prerequisites, yields, and National Objectives remain open for later design and balancing.

## Do not assume

- Do not assume the University is definitively Tier 3; this has only been discussed as a possibility.
- Do not assume any specific RT generator, prerequisite, yield, or National Objective is finalized unless it is explicitly established elsewhere.
- Do not assume all Research Centres generate RT.
- Do not assume RT has a maximum storage limit.
- Do not assume espionage, capture, strategic resources, or other future mechanics generate RT.
- Do not assume technology tiers have different RT costs.
- Do not turn proposed research-capacity routes into fixed technology-tree requirements without explicit design decisions.
- Do not treat the 5 IPC → 1 RT conversion as permanently balanced; it is a current working parameter.

## Next intended work

1. Define the small set of RT-generating technologies/facilities.
2. Place approximately one major research-capacity element per tier where appropriate.
3. Select existing tree technologies and keystones that provide their prerequisites.
4. Identify deliberate mutually exclusive/competing routes.
5. Define the University and its exact prerequisites/yield.
6. Design the National Objectives that provide RT.
7. Balance RT generation against the 1 RT per technology model and the existing technology-tree pacing.
8. Update the authoritative design data once these elements are established.
