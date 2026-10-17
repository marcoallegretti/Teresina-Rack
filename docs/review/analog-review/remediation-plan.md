# Minimal analog schematic correction plan

No repository file has been edited. Apply only after asserting UUID, type, coordinate and old field value against the live file; do not globally replace +5V labels. Net connectivity, not visual appearance, is the independent acceptance criterion.

## Exact changes

These four objects are **local `label` instances** on the existing single schematic, not global labels or power symbols. Change their text from `+5V` to the existing exact name `+3V3A`; retain every UUID, coordinate, rotation and rendering property.

| Target | Label UUID | x,y,rotation |
| --- | --- | --- |
| U13 pin4 | 95807d3e-ccf7-45d6-ba80-fe20c4f80e11 | 917.46,692.38,0 |
| U14 pin4 | 540ca892-f44c-4037-82ae-2b3b5544231e | 1057.46,692.38,0 |
| C141 pin1 | 56ed39c5-dd65-4fe5-9c8e-13e9cc904794 | 1610,564.19,0 |
| C142 pin1 | e2b44745-aeb0-4e77-8267-9b5725796231 | 1340,580.19,0 |

Supply unit symbol UUIDs: U13 unit5 `df1b5a3e-9a4b-439a-aed9-603ce0cb7399` at920,700; U14 unit5 `80fa3a46-c0c3-41a4-ab64-338195ae68d7` at1060,700. Their supply pins are directly labelled, so no symbol-library, instance, pin UUID, wire or property change is required. Keep U15 unit5 `bca5bd90-f7c9-467c-95b7-048ce2ea04a5` at1200,700 and its +5V label `caf0a015-b37a-452f-b891-debcf5701328` at1197.46,692.38 unchanged.

**Capacitor ownership qualification:** The raw schematic contains no dedicated ownership group/wire/text for C141/C142/C143; each is a standalone capacitance with direct rail/GND labels. Thus existing ownership cannot be established from schematic topology. This plan deliberately assigns C141→U13, C142→U14, C143→U15 as new design intent. It does not claim that nearest existing PCB placement verifies that ownership. Leave C143 supply label `25f55a6a-68f8-4629-b3d3-d30466b139f6` at1385,580.19 on +5V. C141/C142/C143 symbol UUIDs are `5a3cf810-8c1a-40b7-9394-810c2b93b2a3`, `e17a0658-9004-4a3a-85ce-3ff05d5b3bf1`, `b96f402c-cc4c-42b7-a3f4-12b7fb86c2d7`. Keep their values/MPNs unchanged. Their positions must be reassigned near their intended supply pins in the later PCB redesign.

For R162 symbol `6ab9825f-a97e-4094-ac07-61284422f3ca` at1475,552 and R163 `9295a905-124c-4d97-89a3-a892a05322d6` at1520,552, change exactly three property values: `Value`1K→100R; `MPN`0402WGF1001TCE→RC0402FR-07100RL; `LCSC`C11702→C106232. Keep `Resistor_SMD:R_0402_1005Metric`, physical pin order, positions, UUIDs and all net wiring. The attached datasheet field is empty now; populating it is optional metadata and must not occur accidentally as part of this six-field minimal patch.

The replacement reuses the exact R158/R159 order code. Independently fetched exact LCSC product JSON identifies YAGEO100Ω,±1%,62.5mW,50V,0402; YAGEO RC-series PDF ordering p2, dimension p4 and rating p5 agree with1.00x0.50mm/1⁄16W package. `C106232-product.json`, `C106232.pdf` and its text preserve evidence. Therefore this is a correct same-package replacement, not an inferred resistor-code substitution. Normal5V output into10kΩ dissipates approximately25µW in100Ω, comfortably below rating. Cable faults, prolonged shorts and opamp current/temperature still need validation at board level.

## Existing analog supply and incremental load

Existing `+3V3A` is a local net feeding MCU VDDA(R1) and VREF+(P1), with C15/C16/C17/C31/C34/C53/C54/C62 decoupling. FB5 pin1 comes from +3V3 and pin2 supplies +3V3A. FB5 is symbol `ceb7e2af-3471-4235-855c-8deb27178589` at205,800; source-side label is +3V3 and downstream +3V3A label `8880bd56-c332-4e99-9368-7bd04c0eeef2` at205,803.81. FB1 pin2 is also +3V3A, but pin1 is A_OUT connected only to C50, so it is not a second source or parallel supply path.

The current FB5 BOM points to CR0805FR600P05Z/C175716, a0.6Ω125mW resistor, as independently documented by the power/BOM reviewer; it is not a600Ω@100MHz ferrite. That mismatch needs its own reviewed replacement. For present DC load analysis use actual0.6Ω, up to0.606Ω at1% tolerance, rather than fictitious600Ω.

Eight MCP6004 channels add about0.8mA typical quiescent consumption. A conservative25°C proxy using the datasheet170µA maximum per channel measured at5.5V gives1.36mA. Normal virtual-ground feedback sourcing at3.3V is at most8×3.3/33k=0.8mA; sum2.16mA, incremental drop1.309mV through0.606Ω. This quiescent proxy is not a full-temperature guaranteed maximum at3.3V. MCU ADC supply current is firmware/revision/mode dependent; example datasheet revV PDFp265 single-ended16bit25MHzBOOST11 gives720µA typical per ADC. Three ADCs plus two DACs at worst-code490µA VDDA/channel and170µA VREF/channel give an illustrative3.48mA MCU analog burden. Adding2.16mA gives5.64mA and approximately3.418mV across the actual0.606Ω element; resistor loss about19.3µW. ADC-reference conversion spikes and opamp sampled-capacitor drive are not represented by this static estimate.

The incremental static current is therefore small and does not indicate a DC current-capacity problem. This supports correcting the CV rail topology to match the official reference. It does **not** certify reference noise, ADC accuracy, supply startup, full-temperature/current extremes, sampled-load transients or the final ferrite choice. Those remain layout/PDN and bench checks, and replacing FB5 must retain adequate DC-current and DCR margins. Existing analog rail has local/bulk capacitance well above the MCP requirement of≥1µF within100mm, but the per-IC100nF loop must meet the2mm placement criterion in the later PCB redesign.

## Independent acceptance after applying

Export fresh native XML before and after. Require the only connection deltas to be removal of U13.4/U14.4/C141.1/C142.1 from `/+5V` and their addition to `/+3V3A`; all other component-pin nets and all native library pin functions must remain identical. Require only six resistor value/order-field changes. Run native ERC and relevant schematic analyzers, compare with baseline, and review introduced/existing issues. Recompute the nominal CV transfer using native values; resistor/capacitor topology must be unchanged. Preserve backups and a textual diff. PCB parity is deliberately pending while layout redesign proceeds; do not present this schematic-only fix as a manufacturable synchronized design.
