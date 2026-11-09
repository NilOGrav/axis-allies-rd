# Topic: Facilities and Installations

Last updated: 2026-11-09  
Status: Active

## Purpose

Define the physical facility/installation layer of the Axis & Allies Global 1940 R&D system, including Research Centres, Bases, industrial/research infrastructure, construction, ownership, damage, repair, and interaction with technology.

Facilities are physical game elements and are distinct from technologies, resources, and capabilities.

## Core Facility Architecture

Established principles:

- Facilities are physical game pieces.
- Facility types have individually defined functions.
- Facilities are associated with territories and ownership.
- Facility functions are individually defined.
- Technologies may unlock the ability to build/purchase facilities.
- Unlocking a facility does not construct it.
- Unlocking, purchasing/building, placing, and operating a facility are separate events.
- Facility possession does not replace a technology dependency.
- Facilities can be damaged where applicable.
- Facility damage can affect operation.
- Damage does not remove the underlying technology.
- Loss of a facility does not remove the technology that unlocked it.
- Facility data is maintained separately from technology data.
- Facility costs are individually defined.
- Technology research cost and facility construction cost are separate.
- A territory may contain at most one facility of each facility type.

A physical facility should not be represented as a technology node merely to create a dependency.

## Facility Categories

The project uses **Facility** as the umbrella concept.

Within that umbrella, physical categories include:

- RCENTER — Research Centre
- Installation
- Base

“Installation” is used as a subcategory rather than treating Facility and Installation as competing top-level concepts.

## Research Centres

Research Centres (`RCENTER`) are a specialised Research Centre facility category.

They are distinct from ordinary installations and bases.

Research Centres may:

- act as technology eligibility gates;
- provide explicitly defined research-related functions;
- provide a specified one-time establishment bonus;
- explicitly generate Research Tokens where their individual rules say so.

Research Centres do not automatically generate RT merely because they are research facilities.

### Research Centre Eligibility

A Research Centre can act as a technology prerequisite/eligibility gate.

Other facilities do not normally act as technology prerequisites unless explicitly specified.

The exact interaction between captured Research Centres and technology eligibility remains open and requires explicit rule text.

## Bases

Air Bases and Naval Bases are distinct functional facility types.

### Air Base

Known functionality includes:

- increasing applicable air range;
- enabling scrambling where the rules permit.

If an Air Base becomes inoperative, it loses its applicable abilities until repaired.

### Naval Base

Known functionality includes:

- servicing applicable sea zones;
- increasing applicable sea-unit range;
- conducting repairs.

If a Naval Base becomes inoperative, it loses these applicable abilities until repaired.

### Damage Threshold

Bases become inoperative at **3 or more damage points**.

There are no established intermediate functional thresholds.

Damage reduces the applicable Base abilities until the Base is repaired.

## Seaplane Base

A Seaplane Base may combine air and naval functionality if the relevant data establishes that combined role.

The exact final treatment should follow the facility data rather than being inferred solely from the name.

## Bombing Exposure

Facilities and Bases have different bombing exposure.

Established architecture distinguishes:

- Facilities/installations that can be targeted by Strategic Bombing.
- Bases that can be targeted by Tactical and Strategic Bombing.

The exact bombing eligibility of each individual facility type remains data-defined.

## Facility Damage and Repair

Established rules:

- Facilities can receive damage from applicable attacks/effects.
- Facility damage affects operational capability according to facility rules.
- Facility damage does not destroy the associated technology.
- Bases become inoperative at 3+ damage.
- Damaged Bases lose applicable abilities until repaired.
- Repair restores operation according to the applicable repair rules.

The exact repair procedure and any facility-specific repair exceptions still need to be checked against the final intended Global 1940 rules.

## Capture and Ownership

Facilities are associated with the territory in which they are located.

When territory ownership changes:

- facility ownership can change with the territory;
- capturing a facility does not transfer the former owner's technologies;
- capturing a facility does not remove the former owner's technologies;
- captured facility operational status follows the facility's own rules.

The following remain open:

- whether/how a captured Research Centre satisfies the captor's technology eligibility requirements;
- how captured facilities interact with technology dependencies;
- any facility-specific capture restrictions.

These should not be silently resolved by assuming that physical possession equals technological ownership.

## Technology and Facility Relationship

The intended relationship is:

```text
Technology
    │
    └── unlocks ability to build/use
                    │
                    ▼
               Facility
                    │
                    └── provides physical function
```

Researching a facility-related technology does not automatically place the facility on the map.

Likewise, losing a facility does not remove the technology already researched.

A follow-up technology normally depends on the technology that unlocked the facility rather than simply requiring possession of the physical facility.

## Facility Construction

Facility costs are defined individually.

Construction cost is independent of research cost.

Technologies can unlock facility construction.

The act of unlocking a facility is therefore separate from:

1. researching the technology;
2. purchasing/building the facility;
3. placing it;
4. operating it.

## Research Facility Principle

Research Facilities are physical installations.

The generic term “research facility” should not be interpreted as meaning that every such facility automatically produces RT.

RT generation must be an explicit property of the particular facility.

## Nuclear Facilities

The nuclear architecture establishes several important facility distinctions:

- Nuclear Power Plant is a physical facility.
- Nuclear Reactor is a physical facility, not a technology node.
- Reactor Theory unlocks Nuclear Power Plant construction.
- Uranium Processing unlocks Nuclear Reactor construction.
- A Nuclear Reactor increases the Nuclear Power Plant's production to 2 IPC per turn within the same territory.
- The Nuclear Reactor can subsequently acquire uranium-production capability through P.7.NU.
- Atomic Bomb production is enabled through the nuclear technology chain and uses specified resources.

The placeholder E.6.03 Nuclear Reactor technology should not be treated as the facility itself; the facility is represented separately.

## Oil Infrastructure

Oil Derricks and Oil Platforms are physical infrastructure.

Current parameters:

- Oil Derrick: 6 IPC construction cost.
- Oil Platform: 8 IPC construction cost.
- Both have defined physical piece quantities.

Oil Platforms can be contested/captured through naval control of their associated sea zone.

Oil infrastructure is therefore represented as a physical facility/installation layer rather than as an Oil technology.

## Facility Data Model

Facility data should remain separate from technology data.

The facility model needs to represent, as applicable:

- facility identity;
- category;
- construction cost;
- placement restrictions;
- function;
- ownership;
- damage;
- operational threshold;
- repair;
- bombing exposure;
- technology requirement/unlock;
- eligibility function;
- resource-production function;
- establishment bonus;
- module scope.

Not every facility necessarily uses every field.

## Current Open Questions

- Exact captured Research Centre eligibility rules.
- Exact captured facility/technology dependency rules.
- Exact repair procedure where it differs from standard A&A repair.
- Exact definition of minor units eligible for Research Centre establishment bonuses.
- Complete facility taxonomy beyond the established RCENTER/Installation/Base structure.
- Exact facility-specific functions and costs for all remaining facilities.
- Final treatment of combined-function Seaplane Bases.
- Complete interaction between facility damage and specific facility capabilities.

## Important Continuation Rules

A future AI working on facilities should:

1. Keep facilities physically separate from technologies.
2. Do not represent a physical facility as a technology merely to create a dependency.
3. Do not assume that every Research Facility generates RT.
4. Treat RCENTER as a distinct facility category.
5. Keep facility unlock, construction, placement, ownership, operation, damage, and repair as separate concepts.
6. Do not assume captured facilities transfer technologies.
7. Do not assume captured Research Centres automatically satisfy eligibility until the open rule is explicitly resolved.
8. Preserve the established 3+ damage inoperative threshold for Bases.
9. Use the facility's explicit function rather than deriving function from its name.
10. Mark unresolved facility rules explicitly instead of filling them from general Axis & Allies assumptions.
