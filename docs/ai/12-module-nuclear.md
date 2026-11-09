# Topic: 13-module-nuclear
Last updated: 2026-11-09
Status: Active

## Purpose
Define and maintain the Nuclear / “Going Nuclear” module for the Axis & Allies Global 1940 R&D system, including nuclear-related technologies, facilities, resources, production capabilities, delivery systems, prerequisites, and their interaction with the wider R&D architecture.

## Current status

The nuclear module is **partially defined**. The technology path, major facilities, and several resource relationships are established, but the complete nuclear production/delivery model still requires reconciliation with the dedicated `XP GOING NUCLEAR v3` design.

## Established design decisions

### Nuclear facilities

- Nuclear facilities are physical **Facilities**, not technology nodes.
- `Nuclear Power Plant` is unlocked by `E.2.02 Reactor Theory`.
- `Nuclear Reactor` is unlocked by `E.5.01 Uranium Processing`.
- `E.6.03 Nuclear Reactor` is a placeholder technology and should be removed; the reactor itself is a facility.
- A Nuclear Reactor is associated with the TANK path because of the `P.7.NU` Landkreuzer-related architecture.

### Nuclear Power Plant

`E.2.02 Reactor Theory`:

- unlocks construction/use of the Nuclear Power Plant;
- Nuclear Power Plant provides `+1 IPC per turn`.

`E.5.01 Uranium Processing`:

- unlocks the Nuclear Reactor;
- a Nuclear Power Plant in the same territory as the Nuclear Reactor produces `2 IPC per turn`.

The intended effect wording is:

> “Increases the Nuclear Power Plant's production to 2 IPC per turn within the same territory.”

### Uranium

Uranium is a strategic resource.

Known uranium locations:

- Western US
- Slovakia
- Belgian Congo
- Yukon
- Xinjiang

`P.7.NU Nuclear Reactor` provides uranium production capability.

The current production relationship is:

- `3 IPC → 1 Uranium`

An initial uranium mine is expected to function as the practical gate for uranium production, although the complete facility/resource implementation remains to be finalized.

### Atomic bomb production

`P.8.NU` gives the Nuclear Reactor an Atomic Bomb production capability.

Current resource requirement:

- `2 Heavy Water`
- `1 Uranium`

The exact production procedure, capacity, storage, and timing still require confirmation against the dedicated nuclear design.

### Nuclear submarines

Nuclear submarines are treated primarily as **extended-range / nuclear-propulsion naval units**, not as atomic-bomb delivery systems by default.

The current nuclear submarine research route is:

`E.2.02 → E.4.01 → N.4.01 → N.5.02 → N.6.01`

This route needs to remain distinct from the nuclear-warhead production/delivery path.

Ballistic Missile Submarines can deliver atomic payloads.

`E.5.02 Rocket Development Program` is **not** the nuclear-submarine technology.

## Technology / capability architecture

Nuclear technologies should be represented using the general R&D capability/effect architecture rather than hard-coded nuclear-specific rules wherever possible.

The intended distinction is:

- technology = researchable/unlockable element;
- facility = physical infrastructure;
- resource = geographically/economically constrained material;
- capability = reusable rule/mechanic;
- effect = atomic modification/unlock of a capability for a subject.

A technology may therefore introduce a new nuclear facility/unit/capability, modify an existing capability, or establish a conditional rule.

## Open issues

The following points remain unresolved and must not be treated as final:

- Exact purpose and effects of `P.9.NU`.
- Exact atomic-bomb delivery procedure.
- Exact relationship between `P.8.NU`, `P.9.NU`, and Ballistic Missile Submarines.
- Complete uranium-mining / uranium-production implementation.
- Heavy Water acquisition and production.
- Nuclear Reactor construction cost and construction rules.
- Nuclear facility damage, repair, capture, and destruction rules.
- Atomic bomb storage, transport, and deployment rules.
- Whether additional delivery platforms beyond Ballistic Missile Submarines are supported.
- Exact prerequisites and eligibility gates for the complete nuclear chain.
- Final reconciliation with `XP GOING NUCLEAR v3`.

## Data-model implications

The nuclear module must remain compatible with the wider project architecture:

- `Facility` is the umbrella category; Nuclear Power Plant and Nuclear Reactor are facilities.
- `RCENTER`, `Installation`, and `Base` are facility subcategories; the nuclear facilities should use the appropriate subcategory once finalized.
- Facilities do not automatically generate Research Tokens unless explicitly assigned such a capability.
- Resources remain separate from facilities and technologies.
- Research eligibility is controlled by the technology tree and prerequisite structure.
- Research does not create/construct the physical facility automatically unless the relevant rules explicitly say so.
- No same-turn research chain should be assumed.

## Source of truth

The latest nuclear-specific design must be reconciled with:

- the current R&D ODS / technology design;
- the project Documentation & Design Log;
- `XP GOING NUCLEAR v3`;
- the finalized capability/effect data model.

Where these sources conflict or remain incomplete, the nuclear module should be marked **open** rather than silently resolved.

## Next work

1. Reconcile the nuclear module against `XP GOING NUCLEAR v3`.
2. Establish the complete nuclear technology dependency chain.
3. Define the remaining nuclear resources, especially Heavy Water.
4. Finalize Nuclear Reactor and Nuclear Power Plant facility rules.
5. Finalize Atomic Bomb production and delivery.
6. Map the finalized nuclear technologies to atomic capabilities/effects.
7. Remove obsolete placeholder technology entries such as `E.6.03`.
8. Update the master technology/effect data only after the above points are settled.
