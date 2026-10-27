# Production gate

This repository is **not fab-ready**. No BOM line may be labelled “orderable” unless it has an exact manufacturer part number, verified footprint and value, a source that can supply the required quantity, and a completed electrical/firmware compatibility check.

## Release blockers

- U3 `IS42S32160F-6BLI`: the pinned stock initialization gives a 168.3456 ms refresh sweep against the part's 64 ms limit. The prototype firmware patch in `docs/review/firmware/` is not a production qualification until built and exercised on hardware.
- U3 availability: the recorded LCSC source currently has zero inventory. A replacement has not been demonstrated compatible.
- J5: the carrier interface is an abstract custom footprint without a frozen manufacturer part number and pad drawing.
- `C72443`: the BOM assigns one LCSC code to both `KMR231NGLFS` switches and `0402WGF1002TCE` resistors. These are separate sourcing lines.
- C13/C14: the schematic value is 2.2 uF but the listed MPN `CL10A226MQ8NRNC` is 22 uF. The exact capacitor and local placement must be corrected in the source CAD.
- Current inventory gaps: C1523, C1549, C25744, C327329, C59461 and C98190 are unavailable in the recorded source snapshot.
- The electrical candidate still has unresolved ERC, placement, routing, DFM and first-article hardware checks.
- Baseline PCB DRC (KiCad 10) reports **414 violations**: 199 silkscreen-over-copper, 195 silkscreen overlaps, 16 edge-clearance violations, 2 courtyard overlaps and 2 back-layer text violations. It reports zero unconnected items, but that does not make the board production-ready.

## Release rule

Do not publish a component total as a manufacturing quote until every blocker above is closed and the source schematic, PCB, fabrication outputs, assembly outputs and firmware manifest are regenerated from the same approved revision.
