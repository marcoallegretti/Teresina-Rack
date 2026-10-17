# Independent electrical candidate review

**Verdict:** Fresh candidate accepted for its scoped schematic correction. PCB parity, functional-sheet cleanup, routing and production acceptance remain pending. No CAD files were edited by this review.

Reviewed SHA256: `b2f87ee2049559ed1ed4f61d384682bda971ca9c31224ab6c06de133d95ceb64` for `../electrical-candidate/TeresinaRack.kicad_sch`, compared to the reviewed23-reference BOM candidate and `edit-plan.json`.

## Raw-file and native checks

- All original raw objects are byte-semantically identical in parsed structure except exactly five approved label texts and six approved component property objects. All library/root/title/wire/project content remains unchanged. Six added root objects are exactly two resistor symbols and four direct labels from the plan; no unexpected object was added or removed.
- R171 is at1340,620; R1721385,620. Every nonzero annotation/property position has the correct template translation, zero-position hidden metadata stays at0,0, pin/symbol/label UUIDs match the plan and are unique, and project instance references are correct. This checks the actual saved/reparsed file rather than source AST or metadata claims.
- Native XML contains211 components and854 component-pins. Exactly five existing pins change nets: R160.1 from+3V3 toGATEOUT_1_O; R160.2/R161.1/U15.9 fromVTH toGATEOUT_FB_1; U15.13 fromVTH toGATEOUT_FB_2. Every original pin identity/function/type and all other existing component-pin connections are preserved.
- Exactly four native pins are added: R171.1=GATEOUT_2_O, R171.2=GATEOUT_FB_2, R172.1=GATEOUT_FB_2, R172.2=GND. VTH disappears. Feedback1 is exactlyU15.9/R160.2/R161.1; feedback2 exactlyU15.13/R171.2/R172.1.
- Feedback comes from opamp outputs before isolation: GATEOUT_1_O is exactlyU15.8/R160.1/R162.1; GATEOUT_2_O exactlyU15.14/R171.1/R163.1. External gate1 remainsJ5.B5/R162.2; gate2J5.B6/R163.2. Thus both loops are closed noninverting120k/62k with100Ω output isolation, matching the visually reviewed official topology.
- MCU mapping remainsPC14/E1→GATE_OUT_1→U15.10 plus input, andPC13/D1→GATE_OUT_2→U15.12 plus input. No gate channel swap or firmware change occurred.
- Q1/Q2 change only Manufacturer and Datasheet. Native MMBT3904(RANGE:100-300)/C20526 selection, Value, SOT23 footprint and every pin net remain unchanged. Metadata now identifies exact JSCJ and matching manufacturer PDF.
- C100/C103 remain2.2µF declared, CL21B225KBYNNNE/C2762602,0805 from the reviewed BOM candidate. This stage only adds Samsung Manufacturer and the matching Datasheet query suffix. It does not revert the staged X7R50V part or change audio connections.

Machine-readable evidence: `electrical-candidate-independent-audit.json`.

## ERC triage and export correction

The earlier candidate was rejected: cloned resistor numeric coordinates retained old serialized strings, placing R171/R172 on CV output resistors rather than planned gate positions. It produced three dangling-label errors, a gate minus-input undriven error and two off-grid warnings. The corrected saved/reparsed candidate and fresh native/XML/ERC are the subject of this acceptance.

Current ERC has255 records:3 pre-existing pin_to_pin errors;246 endpoint_off_grid warnings;2 lib_symbol_mismatch warnings;3 no_connect_connected warnings;1 same_local_global_label warning. Compared with the253-record BOM baseline, exactly two off-grid warnings were added, one for each new resistor's pin1. No error was added or removed and no baseline record was removed. Project settings bytes, ignored-check list and included severity filters are unchanged, so no hidden waiver or severity downgrade caused the improvement. The inherited3 errors remain unresolved. The rough schematic coordinate/grid warning should be corrected during the planned functional hierarchy cleanup rather than hidden.

## Supported result and qualification limits

Both gates now implement the official closed-loop nominal transfer, rather than open-loop saturated comparators. Nominal gain is1.5166667; resistor tolerance, finite swing, supply/temperature variations, output loading, cable capacitance, shorts and physical loop layout remain tests, not verified performance. Exact JSCJ sourcing does not remove the6V reverse B-E limit and unprotected negative gate stress. X7R50V coupling parts restore nominal2.2µF BOM intent; effectiveC at DC bias, distortion/microphonics, transient voltage survival and exact original MLCC identity remain unqualified. Analog reference noise/sequencing and bypass relocation are still required. No production-ready claim follows from this scoped acceptance.
