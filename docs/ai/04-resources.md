# Topic: Strategic Resources

Last updated: 2026-11-09  
Status: Active

## Purpose

Define the strategic-resource layer of the Axis & Allies Global 1940 R&D system, including resource identity, geographical availability, infrastructure, production, consumption, conversion, storage, and interaction with technologies and facilities.

Resources are a distinct layer of the game system and must not be conflated with technologies or physical facilities.

## Core Resource Architecture

Established principles:

- Resources are distinct from technologies.
- Strategic resources can be geographically located.
- Control of resource-producing territory can affect access.
- Resources may be abstract national resources rather than physically transported commodities.
- Some resources require infrastructure for production.
- Basic resource infrastructure can exist independently of R&D enhancement.
- R&D can improve or enhance resource infrastructure or production.
- Individual resource modules define their own production and consumption rules.

The complete resource inventory is not yet considered exhaustive.

## Research Tokens vs. Strategic Resources

Research Tokens are the research resource used by the core R&D system.

They should not automatically be treated as equivalent to the strategic resources covered here.

Facilities may generate RT only where explicitly specified.

Strategic resources such as Oil, Uranium, Heavy Water, Steel, Aluminium, or Vril have their own mechanics and purposes.

## Resource Rule Status

The following resource categories have been identified but still require complete explicit rule inventories:

- Aluminium
- Steel
- Heavy Water
- Uranium
- Vril

The project documentation explicitly identifies the detailed production rules for these resources as an area requiring extraction and consolidation rather than assumptions.

## Oil Module

Oil has a sufficiently distinct rule structure to receive its own resource treatment.

### Established Oil Principles

- Oil is an abstract strategic resource.
- Oil production is geographically associated with territories and/or sea zones.
- Some oil locations are naturally active.
- Some oil locations require infrastructure development.
- Oil Derricks are physical infrastructure pieces.
- Oil Platforms are physical infrastructure pieces.
- Oil infrastructure affects Oil production according to the Oil module.
- Oil Platforms can be contested/captured through naval control of their sea zone.

### Oil Infrastructure

Current parameters:

- Oil Derrick construction cost: 6 IPC.
- Oil Platform construction cost: 8 IPC.
- Physical piece quantities are defined separately in the module data.

The distinction between naturally active Oil locations and locations requiring infrastructure still needs consistent final wording.

### Current Oil Locations

Current design identifies:

- Western United States
- Central United States
- Caucasus
- Romania
- Sumatra
- Java

as active Oil locations.

Other locations may require infrastructure before producing Oil.

### Oil Production Technologies

Known technology relationships include:

- Basic Drilling: Oil Derrick cost reduction and Oil Platform availability.
- Improved Refining: +1 Oil from one controlled Oil territory per turn.
- Advanced Drilling: Oil production increase, subject to the specified maximum.
- Offshore Extraction: advanced Oil Platforms produce 2 Oil per turn.
- Synthetic Fuel Production: converts IPC to Oil, with a 3 Oil/turn cap.
- Synthetic Oil Expansion: improves IPC-to-Oil conversion and removes the earlier cap.

These effects still need final normalization into the capability/resource data model.

### Oil Consumption

Known Oil-related technology effects include:

- Fuel Efficiency: can waive Oil cost for one land attack or air mission.
- Fuel Logistics: naval movement into hostile sea zones consumes Oil.
- Advanced Fuel Efficiency: reduces Oil cost by 50%, rounded up.
- Strategic Fuel Reserves: increases storage capacity and permits IPC payment to ignore specified Oil penalties.

The exact generic capability structure for resource-cost modifiers is still being developed.

### Oil Infrastructure Protection

Protected Oil Infrastructure has two known effects:

- Oil infrastructure requires two bombing hits to disable.
- Repair cost is reduced.

These effects should be represented through the general damage/repair/cost systems rather than creating Oil-specific copies of generic capabilities where possible.

## Nuclear-Related Resources

### Uranium

Uranium is a strategic resource required by the nuclear system.

Known Uranium mine locations:

- Western United States
- Slovakia
- Belgian Congo
- Yukon
- Xinjiang

The omission of Xinjiang from an earlier technology-list entry was identified as a data correction.

The Nuclear Reactor can acquire Uranium-production capability through P.7.NU.

### Heavy Water

Heavy Water is a strategic resource used by the Atomic Bomb production rule.

The current nuclear design establishes that Atomic Bomb production requires:

- Heavy Water
- Uranium

The complete Heavy Water production system remains to be fully inventoried.

## Resource vs. Facility

A resource and its infrastructure are separate concepts.

For example:

```text
Oil
    = strategic resource

Oil Derrick / Oil Platform
    = physical infrastructure enabling or increasing Oil production
```

Likewise, a Nuclear Reactor is a facility rather than a resource.

A technology can unlock or modify the ability to produce a resource without the resource itself becoming a technology.

## Resource Capabilities

The capability model is expected to express resource effects through generic capabilities such as:

- Resource Production
- Resource Conversion
- Resource Storage
- Resource Cost
- possibly Resource Yield Modifier

The final capability taxonomy should be based on the actual resource effects rather than prematurely creating resource-specific capability names.

## Current Open Questions

- Complete Aluminium rules.
- Complete Steel rules.
- Complete Heavy Water rules.
- Complete Uranium rules.
- Complete Vril rules.
- Exact resource eligibility/payment interactions.
- Exact Oil terminology for naturally active vs infrastructure-activated locations.
- Final representation of capped and percentage-based resource-production modifiers.
- Exact interaction between resource control and resource access.
- Complete resource data normalization.

## Important Continuation Rules

A future AI working on resources should:

1. Keep resources separate from technologies.
2. Keep resource infrastructure separate from the resource itself.
3. Do not assume physical transportation unless the specific resource module requires it.
4. Use territory/ownership relationships where the resource rules require geographical control.
5. Preserve resource-specific rules while using generic capabilities where the underlying mechanic is shared.
6. Avoid inventing missing production rules for Aluminium, Steel, Heavy Water, Uranium, or Vril.
7. Treat Oil as a strategic-resource module with additional infrastructure mechanics.
8. Ensure resource effects can be linked cleanly to technologies without making resources part of the technology tree itself.
