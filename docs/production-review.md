# Production review — 13 October 2026

Status: incomplete. The current design is not approved for production. This review establishes the baseline for a redesign; it does not approve the existing routing, BOM or manufacturer process.

Design baseline: `09a374a24c77c10cfc12c9ae37e69187168445db`. KiCad 10.0.7. Firmware reference: [libDaisy](https://github.com/electro-smith/libDaisy/tree/08087203debc646d3710ec8caa35bac6cf20ab5e), commit `08087203debc646d3710ec8caa35bac6cf20ab5e`. Input checksums and analysis totals are in [baseline-summary.json](review/baseline-summary.json).

## Findings and acceptance gates

| Priority | Finding | Evidence and required next step |
|---|---|---|
| Firmware qualification | ISSI candidate requires the Teresina firmware profile; unchanged stock binaries are unsupported | Stock COUNT2054 gives a 168.3456 ms row sweep against ISSI's 64 ms requirement. An opt-in prototype now corrects refresh and clock/init settings and crossbuilds. Continue design with its explicit constraints; physical qualification remains a production gate. [Decision and limits](firmware-policy.md); [original counterexample](review/core-review/bounded-acceptance.md). |
| ADC protection | U13/U14 CV amplifiers run from 5 V instead of the official 3.3 V analog rail | Negative CV overrange can demand 5.61 V at an MCU ADC input. A reviewed schematic-only candidate moves these supplies and assigned bypass capacitors to +3V3A. Supply sequencing, fault behavior and PCB synchronization remain open. |
| Wrong ordered parts | Ferrites are actually resistors; L1 is 22 µH/300 mA rather than 2.2 µH; five capacitor MPNs are 22 µF rather than 2.2 µF | Exact manufacturer/LCSC evidence in [power review](review/power-fab-review/review.md) and [inventory audit](review/power-fab-review/nominal-inventory-audit.json). Correct the complete BOM after circuit requirements are frozen. |
| Package mismatch | Y1 is four-pad 3225, but footprint is two-pad 3215; D1/D2/D5 are SOD323 in SOD923 footprints | Exact manufacturer drawings corroborate ordering metadata. Rebuild symbol/land patterns and crystal case-ground connections; rotation cannot correct these mismatches. |
| Power and thermal | U7 input rating, output stability capacitor and high-load dissipation are inadequate for acceptance | LD1117 operating maximum 15 V; 18 V absolute exception only below 20 mA. Output capacitor is beyond a ferrite 24 mm away. Several-watt load case needs a redesigned power cell and qualified budget. |
| Layout | VCAP, HSE, opamp bypass and buck feedback parts are remote | Source-backed placement requirements contradict earlier waivers. Full placement/routing must be rebuilt; additional layers cannot repair these loops. |
| Mechanical/assembly | J5 has no exact assembly part or installed-height definition | All 40 local pad geometries match the official footprint, but header height, physical fit, USB notch/access and component envelope remain unqualified. |
| Manufacturing | No accepted complete stackup, timing/current sidecars or assembly allocation | Manufacturer four-layer process and candidate stackups are now sourced. Local escape pilots are insufficient for full-board routing, return paths, assembly or order approval. |

## Sources and verification basis

The earlier 403 network blocker is resolved. Official [PatchSM documentation](https://docs.daisy.audio/hardware/PatchSM/), [datasheet v1.0.5](https://daisy.nyc3.cdn.digitaloceanspaces.com/products/patch-sm/ES_Patch_SM_datasheet_v1.0.5.pdf), [Rev3 schematic](https://daisy.nyc3.cdn.digitaloceanspaces.com/products/patch-sm/ES_Daisy_Patch_SM_Schematic.pdf), pinout CSV, CAD footprint, manufacturer PDFs and current JLCPCB capabilities were obtained. Valid manufacturer-branded distributor mirrors were used where direct URLs returned HTML. HTML challenge responses were excluded as datasheets. URLs, hashes, cited tables and verification boundaries are in the linked subsystem reviews and replacement manifest; retained PDFs are under `/workspace/cloud-setup/redesign`.

The official schematic is reduced and omits the shared MCU/SDRAM core. It cannot establish the original RAM MPN. The datasheet lists ±6…17 V as absolute limits and ±12 V as typical operation; it does not guarantee full analog performance at 6 V. Likewise 800 mA/500 mA rail outputs are absolute, workload-dependent limits, not guaranteed external current in addition to internal consumption.

Read-only independent reviews cover [digital core](review/core-review/core-review.md), [analog](review/analog-review/review.md) and [power/fabrication](review/power-fab-review/review.md). Manufacturer pin tables, raw CAD/netlists and pinned firmware were compared, rather than treating analyzer agreement as physical correctness. They confirm 299 used core pads (201 MCU, 90 SDRAM, 8 QSPI), codec/analog pin maps, regulator pin maps and the 40-pad mating geometry. These confirmations are bounded findings, not an all-components production sign-off. Q1/Q2 still need exact supplier/MPN confirmation; the current symbol follows conventional BCE SOT23 mapping but a generic part-family name is insufficient.

## Overview and previous review delta

The files contain a 68 × 40 mm, 12-copper-layer board with 214 footprints, 5,172 track segments and 829 vias. The native schematic netlist contains 209 assembled component references; the extra PCB references are five fiducials. Existing README component totals should not be used as the assembly count.

The production redesign targets four layers, with six an acceptable fallback and eight the final fallback. Twelve layers remain a description of this baseline, not an accepted redesign option. The lower-layer alternatives require fresh placement/fanout trials and independent manufacturing, timing and return-path review; their feasibility has not yet been established.

Repository electrical/layout sources remain unchanged. Schematic remediation candidates and disposable four-layer escape trials were created outside the checkout. The earlier schematic/PCB analysis outputs were reused because the source checksums and tool revisions are unchanged. Additional work includes a native-netlist comparison, libDaisy comparison, parasitic extraction, SPICE, EMC, thermal, Gerber and lifecycle analyses. The previous claim that SPICE could not be reproduced is superseded: the analysis suite generates testbenches from the schematic analysis. Its simulation coverage is limited as described below.

`DESIGN.md` contains stale references to Alliance RAM, eight layers, castellated pads and an unfinished PCB. It is historical working material, not an authoritative compatibility contract. The current file names, properties and netlist take precedence for baseline inventory; official sources take precedence for correctness.

## Components and sourcing

[component-review.csv](review/component-review.csv) inventories every one of the 214 PCB references, with MPN/LCSC fields, current footprint/side/position, connected nets, circuit review group and required placement review. Group assignments for shared rails and analog channels are provisional until the pin-level review is complete. Existing coordinates are recorded for traceability, not approved as the new placement.

The schematic analyzer identifies 56 of 57 unique parts with MPNs, or 208 of 209 assembled references. A datasheet acquisition dry run identifies 56 unique parts with identifiers. Manufacturer fields are generally empty. Q1/Q2 carry the string `MMBT3904(RANGE:100-300)` and a PZT3904 datasheet URL; this is not sufficient evidence for the exact SOT-23 part. U12 carries TL074IDT while the attached URL points to the TL071 family: use the actual ordered manufacturer's TL074 variant.

The lifecycle audit executed for 51 parts using the LCSC-only source. All returned `unknown`; the runner states that this source does not provide lifecycle status. This is an unresolved sourcing gap, not evidence that those parts are active or obsolete. Exact retail stock and price were checked for 51 native ordering codes and proposed replacements. These are retrieval-time figures, not JLC assembly allocations or reservations. The nominal inventory audit confirms R168/R169 incorrectly use a switch ordering code, and SW1/SW2 MPNs do not match their actual ordering code. Lifecycle remains unknown; no lifecycle sign-off follows from retail stock.

## Power tree and thermal review

The baseline topology is:

```text
Carrier +12 V / USB VBUS → protection → positive input rail
  ├─ TPS62170 buck → +3V3 → digital loads and filtered MCU analog rail
  └─ LD1117S50 → +5V → analog/CV loads and filtered PCM3060 +5VA
Carrier −12 V → protection → negative analog rail and −10 V reference network
```

This is a topology description, not a datasheet-approved power design. Recalculate buck inductor/ripple/saturation, startup, MLCC derating and each ferrite's DC/AC requirements. Trace the USB-only flashing mode, reverse current and simultaneous USB/rack power. Calculate the exported +5 V/+3V3 current budget separately from internal consumption.

The thermal analyzer assessed only U6, estimating 55.1 °C at 40 °C ambient using heuristic assumptions. It skipped two components, including U7. Its 100/100 score is therefore not approval of the power tree. U7 requires `(Vin − 5 V) × Iout` loss calculations, dropout checks and actual package/board thermal data. ST gives SOT223 reference θJA 110 °C/W and θJC 15 °C/W. At protected 11.7 V, 800 mA yields approximately 5.42–5.48 W including quiescent current. Actual board thermal resistance, airflow and internal/external load budget remain unqualified; a higher-current linear regulator alone does not solve this dissipation.

## Electrical consistency and firmware contract

[connectivity-audit.json](review/connectivity-audit.json) compares a fresh native KiCad XML netlist against the raw PCB, independently of the schematic analyzer:

- 821 functional pads agree after removing the schematic's root-sheet prefix.
- 36 intentional no-connect pads have no PCB net.
- 11 pad records are mechanical/fiducial or unnumbered.
- Five SDRAM NC pads use local `NC_U3_*` aliases instead of native `unconnected-*` names. Each alias has exactly one pad and no track, arc, via or zone. They are not functional pin swaps.
- No schematic component is missing a footprint. Five PCB-only fiducials account for the count difference.

The source comparison checks 74 digital net assignments against libDaisy: FMC, QSPI, SAI, codec I²C, LED, boot strap and USB FS. All agree with the current native netlist. The SDRAM driver's generated comment says PC0 for SDNWE, but its actual HAL initialization uses PH5; the check follows the executed initialization, not the stale comment. The 40 carrier pin declarations and corresponding connector/MCU nets are recorded, but the analog paths between them still require individual review.

These results do not establish physical package correctness, analog range accuracy, SDRAM timing margin or execution on hardware. Firmware compatibility must retain:

- Unmodified DaisyPatchSM pin/ADC channel mapping and gate polarity.
- SAI1 RX/TX directions and PE2/PE3/PE4/PE5/PE6, I²C2 PB10/PB11 and PCM3060 address 0x46.
- IS25LP064A behavior on the existing QSPI pins, memory-mapped execution and boot modes.
- SDRAM geometry: 13 row bits, 9 column bits, four internal banks, 32-bit data and CAS 3; initialization and refresh must meet the selected device's specifications.
- Qualified HSE/PLL behavior with documented Teresina clock changes, DAC voltage transfer functions, ADC bipolar polarity, reset and software DFU behavior.

The ISSI IS42S32160F-6BLI is a **prototype candidate pending hardware qualification**. Pinned stock HAL proves PLL2_R200 MHz, SDCLK divide-by-two, direct COUNT2054 and a COUNT+1 SDCLK counter. Startup manual refreshes do not multiply periodic refresh. The resulting168.3456 ms exceeds ISSI64 ms; room temperature provides no published relaxation. The old AllianceMSA comment names a 1.8 V part, also requiring64 ms, and must not be restored on 3.3 V. Two further Alliance candidates did not close unchanged-firmware retention; that bounded search does not prove no suitable memory exists.

The user subsequently proposed accepting a small Teresina firmware variant. Under that revised path, the refresh discrepancy ceases to block continued core/layout work: the opt-in prototype implements COUNT369 with a conservative32 ms target, fixes PLL2's reference range, uses Rev V CPU profiles with frequency headroom and rejects unsupported initialization paths. Public SDK headers remain unchanged; one identical application source crossbuilds against both SDKs. The modified library, three application execution targets, memory-test firmware and digital-only boot adapter crossbuild. Host tests reject17 invalid clock snapshots and check7936 refresh arithmetic cases. These checks establish a prototype implementation, not executed hardware behavior or broad application compatibility. See [firmware-policy.md](firmware-policy.md) for clock/timer differences, unsupported boot cases and required physical tests.

### Four-layer escape evidence

[Trial summary](review/four-layer-trials.json) records disposable full-footprint studies. All inherited tracks/vias/zones were removed; original placement was retained solely as an obstacle/end-point baseline. Trace width0.09 mm, via land/drill 0.30/0.15 mm and drill-to-copper 0.20 mm were source-backed starting constraints, with escalation disabled and DRC floors preserved.

| Trial | Native errors | Reported signal targets | Missing plane drops | Disposition |
|---|---:|---:|---:|---|
| MCU dogbone,0.09 mm clearance |33 hole-clearance|114/114|6|Rejected |
| MCU dogbone,0.125 mm clearance |0|114/114|6|Incomplete |
| MCU with six filled/capped pad vias,0.125 mm |0|114/114|0|Local escape evidence only |
| SDRAM dogbone,0.125 mm |3 hole-clearance records at C204|57/57|11|Rejected at inherited placement |

Native DRC, independent copper hygiene and KRT DRC were run after each operation; the revised pilots also received independent connectivity checks. All retain 499 native unconnected items. Free terminal stubs and unconnected hypothetical-plane vias explain unfinished-copper warnings; they are not waived for a final board. Revised MCU hygiene found no narrow/soft joints or redundant cycles. The SDRAM output additionally intersects C206 paste with two vias, despite disallowing vias in the target BGA's pads. This exposes inherited placement interactions, not proof that four layers fail.

The synthetic GND/In1 and +3V3/In2 plane declarations are router predictions; no actual planes were added. They are not the accepted production reference scheme. JLC04161H-3313 is a sourced 1.6 mm candidate with 0.0994 mm outer-to-inner dielectric,1 oz outer/0.5 oz inner copper. A prospective outer-signal/power and two-inner-GND arrangement requires new power escape/distribution and continuous-return review. Via-in-pad requires explicit paid filled/plated-over fabrication on four layers. No cost quotation or full four-layer routability proof exists. Six and eight remain ordered fallbacks; neither has been selected.

### Reviewed remediation candidates

Reviewed stages are retained under `/workspace/cloud-setup/redesign/`. These are schematic-only candidates; they have not replaced or synchronized the historical repository PCB.

| Stage | Scoped reviewed result | Limit |
|---|---|---|
| `candidate` | U13/U14 and their explicit C141/C142 bypasses move to +3V3A; R162/R163 become exact sourced 100 Ω parts | Four native net moves, six field changes, 209 components; all other pins preserved |
| `bom-candidate` | Exact ferrites, capacitors, inductor and diode candidates correct 23 references/68 fields | All 850 pin nets/functions/types preserved; diode placements and operating corners require redesign |
| `electrical-candidate` | Both gate outputs use the official closed-loop 62 kΩ/120 kΩ feedback before 100 Ω isolation; exact transistor/audio supplier metadata | Two new resistors, five old-pin net moves; MCU PC14/PC13 and carrier channel mapping preserved |
| `core-candidate` | Y1 uses the four-pad 3225 symbol/footprint with grounded case pads; C13/C14 use reviewed 2.2 µF/25 V/X7R/0805 candidates | All 299 MCU/RAM/QSPI pin functions/nets preserved; original 18 pF loads remain unqualified |
| `organized-candidate` | Nine functional sheets; connected CV input, CV output/auxiliary ADC and gate circuits expose feedback paths | Native comparison preserves all 211 component fields except sheet metadata and explicit U3 documentary description, and all 856 pin nets/functions/types; other pages remain presentation drafts |

Independent [gate acceptance](review/analog-review/electrical-candidate-review.md) and [core acceptance](review/core-review/core-candidate-acceptance.md) approve those explicit schematic deltas only. No firmware changes or production approval follow. [Final independent analog review](review/analog-review/aux-and-analog-final-review.md) accepts the connected CV input, CV output/auxiliary ADC and gate pages; the other functional circuit pages remain drafts. The [gate fault proposal](review/analog-review/gate-protection-proposal.md) identifies a negative B-E clamp and larger 100 Ω output-resistor option, with exact-source and temperature/fault-current gaps. Neither was adopted in CAD.

An independently accepted [graphic-only SDRAM normalization](review/core-review/u3-grid-candidate-acceptance.md) aligns all 90 distinct physical pin endpoints, 85 wire stubs/labels and five NC markers to the connection grid. A neutral alias replaces the misleading Alliance identity and unsupported compatibility prose; physical Value/MPN/SKU/footprint and every physical pin function/net/type remain unchanged. Native ERC now reports the same three power-output conflicts and one U6 library mismatch. The 86 U3 off-grid records and U3 cache/library mismatch are removed through actual graphic/library correction. No severity suppression or exclusions were added. Six intrinsic-NC annotations were added and three incorrect connected MCU NC markers were removed during organization; physical pin assignments remain unchanged.

The [forced-PWM +5 V proposal](review/power-fab-review/forced-pwm-five-volt-architecture.md) replaces the thermally unsuitable LDO concept with a genuine TPS62135 trial. The input/output capacitor arrays account for exact manufacturer typical DC-bias curves: single proposed caps were rejected. Exact RGX 11-pin and Bourns footprints, effective capacitance/aging, low-input accuracy, hotplug, analog noise, active-discharge sequencing and USB/backfeed behavior remain gates. This power architecture has not been adopted in CAD.

The [header proposal](review/power-fab-review/header-proposal.md) identifies four real Harwin M20-9980545 headers and an exact physical-pin permutation preserving every legacy carrier function/position. Finished-hole tolerance, installed mating fit and assembly allocation remain necessary. No header replacement was silently applied.

See [replacement manifest](review/power-fab-review/proposed-replacements.json), [VCAP/crystal selection](review/core-review/core-component-selection.md), native comparison reports and scope manifests for exact sources and limitations. Shared-rail decoupling ownership, full connected schematic presentation, final PCB parity, fault protection and physical qualification remain open.


## Analog simulation and signal review

ngspice 47 executed 63 generated testbenches with PCB parasitic data: 43 RC filters, nine dividers, six decoupling networks, two transistor circuits, one crystal circuit, one regulator feedback network and one inrush case. All 63 completed with `pass`; none failed, warned or skipped.

This is limited mathematical/model coverage. There are no op-amp testbenches in that run, so it does not validate the differential MFB audio output, TL074 behavior, MCP6004 swing/saturation or complete CV transfer functions. The active tests use the generator's models rather than the exact ordered devices. The crystal test is not a demonstration of startup on the STM32 oscillator.

Additional channel-level benches were generated directly from the native XML netlist. [ideal-audio.cir](review/ideal-audio.cir) exercises both differential MFB outputs; [ideal-cv.cir](review/ideal-cv.cir) exercises all eight CV inputs and both CV outputs. These use ideal unsaturated opamps with open-loop gain 1e8 and 100 kΩ output loads, without exact device bandwidth, noise, rail limits, tolerances or PCB parasitics.

The 24 CV endpoint checks give 3.300 V, 1.650 V and 0 V for −5 V, 0 V and +5 V input, consistent with the independent equation `Vout = −(33k/100k) Vin + (33k/200k) × 10 V`. Both loaded DAC outputs give 5.000 V at 3.3 V input; the unloaded ideal result would be 5.005 V. Both audio channels give magnitude 2.16450 at 100 Hz and 2.11680 at 20 kHz, a 0.19355 dB reduction relative to 100 Hz. The DC gain agrees with `(39k/18k)/(1+100/100000)` for that load. See [analog-channel-summary.json](review/analog-channel-summary.json). No analog performance limit is approved without the official requirement and exact device evidence.

The redesign still needs source-backed device models or conservative behavioral limits, resistor/capacitor tolerance corners, rail/headroom limits and leakage/load assumptions. The PCM3060 supply, VCOM, I²C address 0x46, straps, pinout and SAI directions were checked against its PDF and firmware. Sequencing and device performance still require qualified models/measurements. Baseline ordered C100/C103 are 22 µF despite2.2 µF labels, moving the nominal input coupling corner from 1.0879 Hz to 0.1088 Hz; the ideal analyzer bench uses displayed values and does not validate the actual populated BOM.

## PCB, EMC and cleanliness

Native KiCad baseline DRC found zero errors and zero unconnected items, with 414 warnings. ERC found three documented power-output pin conflicts and 250 warnings. These are baseline observations, not an acceptance criterion that permits all inherited warnings.

KiCadRoutingTools' connectivity check reports all 200 routed nets connected and explicitly agrees with a KiCad zone-refill check that found zero missing links. Its advanced-tier DRC reports 308 findings. It skips the conditional 0.09 mm clearance rule, and 254 findings concern via barrels in paste openings without filled/capped declarations in the design file. The documented order process may account for these, but the fabrication package must specify and receive that process; using a baseline waiver would not prove it.

The generic `kct` JLCPCB profile reports 13,867 errors and 1,049 warnings. Its displayed limits include 0.127 mm trace/clearance and 0.300/0.600 mm via drill/diameter. Those are not the project’s claimed advanced limits. Do not treat that count as native electrical shorts, and do not relax the profile just to obtain a pass. Establish the selected fabrication limits from current manufacturer evidence first. Length matching, differential continuity and current-path checks were inactive because engineering sidecars were missing.

EMC analysis produced 79 findings, including 19 errors. The 0/100 risk score is not a compliance measurement. Its USB skew calculations identify asymmetry worth reviewing, but the attached 25 ps limit is not independently established for the actual FS application. It also applies a generic high-speed skew limit to differential analog codec outputs; those must instead be assessed for analog balance, filtering and common-mode rejection. Reference-plane and decoupling heuristics require inspection of actual filled copper, pin locations and device requirements. In particular, U8 is an ESD array and U16 a shunt reference: a generic IC decoupling rule is not automatically applicable.

Replan power/clock/SDRAM/audio return paths explicitly. The existing MCU and SDRAM projected centers are approximately 23 mm apart on opposite sides. Evaluate a closer memory/core placement with coordinated fanout before choosing layer count. Do not assume any convenient pair of solid planes gives every signal a continuous adjacent reference.

## Gerbers, manufacturing and testability

The baseline exported 34 Gerber files, plated/non-plated drills and CPL data. Gerber analysis reports two warnings based on paste-flash versus copper-flash counts. Copper flashes include vias and through-hole pads, so that ratio alone does not demonstrate missing SMD paste. Cross-check expected paste apertures against each assembled SMD pad before accepting or dismissing it.

An approved package must include an explicit stackup, fabrication notes, via protection, finish, drill tolerances, impedance requirements where applicable, sourcing-complete BOM, validated CPL rotations/sides, front/back assembly drawings and installed carrier-pin dimensions. Check component courtyards, silkscreen legibility and at least a reviewed fiducial strategy on both assembled sides. Provide access for power/current checks, SWD, memory tests, audio loopback and all CV/gate channels without changing the carrier interface.

## Review limits and next gate

Sources and subsystem pin audits are substantially improved, but the review is incomplete. No full corrected schematic/PCB, final placement, complete four-layer routing, controlled-impedance/timing analysis, power-current sidecars, approved assembly BOM/CPL, exact-device tolerance/noise/THD simulation, measured EMC/thermal results or first article exists. No hardware flashing or memory/audio/CV/gate/carrier-fit test was performed. Existing exports are baseline exports, not an order package. Applicable EMC/ESD, return-path and thermal analyses remain risk reviews, not standards certification.

Continue the corrected schematic, component sourcing and four-layer placement/routing work using the explicit Teresina firmware profile. Before production freeze, establish Rev V procurement, oscillator bounds, selected SDRAM timing/load constraints and complete power/mechanical/DFM closure. First-article firmware and physical testing remain release gates. The original counterexample continues to prevent an unchanged-stock-binary compatibility claim; it does not block the revised source-compatibility path.

All214 references are inventoried and51 ordering codes audited, but shared-rail capacitor ownership, complete sourcing/package details and final layout remain open. The repository schematic, PCB, project, custom library and rules retain their original bytes. Documentation now records 4 layers preferred, 6 acceptable fallback and 8 final fallback; 12 is baseline history only. Follow [redesign-plan.md](redesign-plan.md) after closing component/firmware requirements. Fabrication, publication and ordering are unperformed.
