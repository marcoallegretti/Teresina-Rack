# Four physical carrier headers — 13 October 2026

Preferred candidate: **4× Harwin M20-9980545**, LCSC **C3338551**,155 retail units at retrieval. This is a genuine10-pin2×5 vertical male2.54 mm header, gold over nickel, brass pins and blackPA6T UL94V-0 housing. Exact Harwin drawingDRG-00478/M20-998XXXX issue24 and manufacturer material/composition/process documents were obtained directly from the official product page; the LCSC mirror family specification independently agrees. No CAD changes or JLC assembly availability claim is made.

## Dimensions and assembly limits

The manufacturer drawing gives6.10 mm mating post above the insulator (general tolerance±0.25 mm),2.54±0.10 mm insulator,3.00±0.25 mm solder tail below insulator,0.64±0.02 mm square pins,2.54±0.10 mm pitch/row separation. Body length for five positions is12.70±0.50 mm; width5.08±0.20 mm. The order suffix05 denotes five contacts per row and45 denotes gold;46 is tin. The drawing lists this size/finish combination as active. Manufacturer family specification rates3 A per contact and300 mating operations for gold. Material/process document explicitly specifies260°C for10 s peak reflow/solder heat for this finish; use the manufacturer's complete profile, not an unreviewed production process assumption.

With the insulator seated on the component-side board surface:

- Nominal top height is8.64 mm; dimensional maximum8.99 mm. Against the stated9.30 mm top envelope, this leaves0.31 mm for assembly stand-off/clearance. The insulator must sit flush or within a validated stand-off limit; arbitrary sockets/spacers are not allowed.
- On nominal1.60 mm PCB, nominal solder-tail protrusion is1.40 mm. Taking maximum3.25 mm tail and minimum1.44 mm board (JLC±10% thickness), maximum protrusion is1.81 mm, below the stated2.75 mm bottom envelope by0.94 mm.
- Body/bank placement must retain all forty exact official hole-center positions. Reserve maximum13.20×5.28 mm plastic footprint for each bank, plus assembly courtyard margin. These wider front bodies and the new SMA diodes require fresh placement checks.
- **Mating post length is not a guaranteed engagement depth.** Actual reference-carrier socket insertion depth, contact wipe, seating gap and pin-stack alignment require a physical carrier/fixture test. No complete female-carrier interface drawing was established in this header review.

## Finished-hole requirement

Harwin recommends **finished PTH Ø1.02±0.05 mm**, not just a nominal drill. The current official-layout pads are1.8796 mm diameter with1.016 mm CAD drill. Under JLC's general+0.13/−0.08 mm through-hole tolerance, finished1.016 mm holes can be0.936–1.146 mm, outside Harwin's recommended0.970–1.070 mm range. The maximum square-pin diagonal is `0.66*sqrt(2)=0.93338 mm`; minimum generic-hole clearance would be only2.62 µm in diameter, before pattern registration/assembly variation. This is not an accepted production-fit margin.

Retain the hole-center coordinates and carrier net functions, and specify nominal1.02 mm **finished hole with±0.05 mm process acceptance**, or obtain an independently justified manufacturer/assembler alternative. JLC's capability table offers±0.05 mm precision/press-fit holes for circular multilayerENIG holes0.55–2.0 mm and requires an order remark identifying holes. An order/DFM acceptance is necessary; selecting that capability text alone is not a quotation. Changing nominal1.016→1.02 mm preserves mechanical pin positions and leaves0.4298 mm nominal annular ring with existing1.8796 mm lands, comfortably above the published multilayerPTH0.20 mm recommendation. Do not keep the generic tolerance and waive the mismatch.

## Refactoring the abstract J5

Create four physical component references: J5=A bank, J6=B bank, J7=C bank, J8=D bank. Each gets quantity1, exact manufacturerMPN/LCSC, physical footprint and assembly placement. J5 in the baseline is one40-pad abstract module footprint; merely giving it a quantity4 MPN does not provide four assembly placements.

`header-pad-permutation.json` derives a valid standard2×5 odd/even numbering permutation from the raw forty pad coordinates. The same per-bank relation is:

| New physical pad | Legacy module pad suffix |
|---|---|
|1|10|
|2|1|
|3|9|
|4|2|
|5|8|
|6|3|
|7|7|
|8|4|
|9|6|
|10|5|

For exampleJ5.2 carries the formerA1−12 V net, J5.1 carries formerA10+3V3, and J6.2 carries formerB1 audio-right output. Apply the appropriateA/B/C/D prefix to every legacy suffix and preserve the original net at its **physical coordinate**. The standard footprint's odd/even numbering is not the original counterclockwise module numbering; a blind serial1→1 mapping would swap interface signals.

Raw baseline bank centers, in board coordinates, areJ5(A)=(7,6),J6(B)=(62,7),J7(C)=(62,33),J8(D)=(7,34) mm. Math rotations in the JSON describe a geometric transform only; verify KiCad's actual transform convention and all forty exported pad coordinates independently. Centered per-bank footprints are preferable for unambiguous manufacturingCPL center positions; standard library origins can be at pin1 and need a placement offset. Include an assembly drawing with the legacybank/module pin names, orientation, component side and flush seating requirement.

Provide four physical rows/designators in the production BOM and complete placement records. JLC StandardTHT assembly requires actual part allocation/process review; it is **not confirmed** by LCSC retail155. A valid fallback is JLC SMT-only assembly plus four manually installed headers. For that variant, omit all four manual parts from the JLC machine-uploadBOM/CPL pair and supply a separate exact manual-assemblyBOM/drawing; retain complete placements in the canonical assembly data.

Manual fallback: install the four headers simultaneously in an unpowered compatible carrier or accurate alignment fixture; seat the module to the defined frame without forcing bent pins; tack one joint per bank, check flushness andparallelism, finish joints using a manufacturer-compliant solder process, clean/inspect, then check all forty nets and adjacent pin isolation before powering. Remove the carrier/fixture before electrical tests. Verify front/bottom envelope with a gauge and repeat mating/insertion checks. This is a documented assembly route, not evidence of completed hardware validation.

## Alternatives investigated

SamtecTSW-105-07-G-D/C7074471 has417 retail units and nominal8.38 mm front height/0.94 mm bottom protrusion. The exact manufacturer catalog statesTSW usesPBT and **“No, Lead Wave Only”** for lead-free solderability; do not assume JLC's usual lead-free process is supported. Its recommended pattern is1.02 mm holes. High-temperatureLCP HTSWvariants located in LCSC had0stock or different/special options; they were not substituted silently. HarwinM20-9980546 tin version/C3327032 has0retail stock. Harwin goldM20-9980545 is preferred here, with the remaining hole/assembly/carrier-fit gates explicit.

Sources: [Harwin official product](https://www.harwin.com/products/M20-9980545), [exact drawing](https://content.harwin.com/asset/1590d228-db5c-4836-ab0c-0f146730b624/DRG-00478-Technical-Drawing-Datasheet-M20-998-pdf.pdf), [family specification](https://content.harwin.com/asset/92486137-0a45-4017-9b78-1edaa8709008/C001-C001XX-Component-Specification-M20-Series-2-54mm-pitch-PCB-connectors.pdf), [material/process record](https://content.harwin.com/asset/4bb177ac-7693-48b4-863e-81a103be23b6/MC-00173-Material-composition-for-M20-998-series.pdf), [LCSC exact part](https://www.lcsc.com/product-detail/C3338551.html). Retained native geometry, source PDFs and product metadata are under this review directory.
