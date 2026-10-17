# Teresina-Rack redesign plan

The target is an independently reproducible, JLCPCB-manufacturable module that fits Daisy Patch SM carriers and supports recompiled libDaisy applications through a narrowly scoped Teresina firmware variant. Official references and manufacturer datasheets have now been obtained. Requirements and component selection remain provisional until the findings in [production-review.md](production-review.md) are resolved. This plan does not approve the existing layout or a new layer count.

The firmware reference is official libDaisy v9.0.0 at `08087203debc646d3710ec8caa35bac6cf20ab5e`, together with the pinned official v6.4 bootloader source. Following the user's revised proposal, a small Teresina firmware variant is the prototype path. The refresh correction is implemented and crossbuilt; physical validation remains open. Continue core and four-layer design with the ISSI candidate under this explicit profile, qualifying Rev V procurement and oscillator/timing bounds before production freeze. See [firmware-policy.md](firmware-policy.md). A passing short memory test cannot replace a manufacturer's retention guarantee or establish stock-binary compatibility.

## Requirements and evidence

Keep the board outline, mating pad coordinates/numbering, pin functions and installed mechanical envelope equal to the official module. Preserve memory geometry, codec/GPIO/channel mapping, analog transfer functions and supported boot behavior. Document the firmware profile's clock/refresh changes and timing limitations. Circuit implementation may differ where those contracts are met.

Before making electrical changes, collect and index:

| Source | Required evidence |
|---|---|
| [Patch Submodule product](https://daisy.audio/products/patch-submodule) and official support resources | Datasheet revision, mechanical dimensions, carrier footprint, pinout, schematic and operating ranges |
| [libDaisy](https://github.com/electro-smith/libDaisy/tree/08087203debc646d3710ec8caa35bac6cf20ab5e) | Pin map, boot/QSPI behavior, SDRAM geometry/timings/refresh, ADC mapping, codec protocol and analog scaling assumptions |
| ST | STM32H750IBK6 ballout/package, hardware design guidance, power/VCAP/oscillator/FMC/USB requirements; LD1117 and exact TL074 variant where applicable |
| ISSI | IS42S32160F-6BLI and IS25LP064A-JBLE package, voltage, pinout and timing |
| TI | PCM3060PWR, TPS62170DSGR, LM4040C10IDBZR requirements |
| Microchip | MCP6004T-I/SL pinout, output swing, common-mode and stability |
| Exact passive/discrete suppliers | Inductor saturation/DCR/value, crystal load/ESR, ferrite DC rating, capacitor voltage/derating, protection and transistor package pinouts |
| JLCPCB/LCSC | Selected stackup and process capabilities, via filling/capping, assembly limits, stock, complete orderable MPNs and CPL convention |

Record URL, document revision, access date, checksum and cited page/table for each requirement. A failed source request remains an open item. [production-review.md](production-review.md) records current gaps.

## Schematic reorganization

Replace the large, poorly arranged working sheet with clear functional sheets after the pin-level review: carrier interface, MCU/clock/boot, SDRAM, QSPI, power, codec/audio, CV inputs, CV outputs/gates, and test/debug. Preserve reference identity or provide an explicit reference map. Use proper package-specific symbols with documented electrical pin types. Resolve net-name and footprint-identifier drift deliberately; do not suppress ERC/DRC to hide it.

Review every reference in [component-review.csv](review/component-review.csv). For each part, close package/pinout, value/tolerance/voltage, current/thermal, sourcing and layout ownership. Shared-rail capacitors must be assigned to actual supply balls/pins rather than whichever IC happens to be closest in the current layout.

## Floorplan and routing ownership

| Block | Placement plan | Acceptance gate |
|---|---|---|
| J5 and board outline | Freeze carrier geometry first; reserve the complete mating/component envelope | Coordinate-by-coordinate comparison with official drawing/footprint and installed header-height check |
| U1 MCU | Compact core region, with ball-specific supply capacitors and short VCAP/clock loops | Exact ballout, local decoupling loops, fanout/DRC and return-path review |
| U3 SDRAM | Evaluate same-side adjacent and coordinated opposite-side core placements; reduce the present long memory bus | Full bank/address/data/byte-lane mapping, pinout, skew/timing budget, fanout feasibility and return continuity |
| U2 QSPI | Beside the corresponding MCU escape area, with short SCK and local bypass | ROM/bootloader/stock firmware compatibility, complete pinout and timing review |
| Y1 and oscillator parts | Beside PH0/PH1 with a compact protected loop | Exact crystal CL/ESR/drive constraints and startup test plan |
| U6/L1 buck and input protection | Together near the power entry, with compact hot-loop geometry and separation from audio/reference nodes | Correct inductor, saturation/ripple, startup/current budget and conducted-noise review |
| U7 and +5 V distribution | Thermally planned power region, with defined exported current limits | Worst-case dissipation, dropout, reverse-current paths and local capacitance |
| U4 codec | At the digital/analog boundary, with separate local analog/digital bypass and short clock/control connections | Datasheet straps, 0x46 address, SAI directions, rails, VCOM and sequencing |
| U12 audio and associated R/C | Symmetric L/R channels beside codec analog pins and carrier audio banks; avoid buck/clock/memory paths | Full-channel MFB simulation, common-mode/rail headroom and loopback limits |
| U13–U15 CV/gate analog | Group by channel and matching connector bank; keep high-impedance summing nodes local | Per-channel transfer function, polarity, noise/filtering, protection and load checks |
| U16 reference and associated R/C | Quiet analog region; compact reference path and no shared switching return | Actual 10 V part, bias/headroom/load/noise budget and tolerance corners |
| Q1/Q2 gate inputs | Close to their carrier bank and protection network | Exact device pinout, threshold, input limits and polarity |
| J3/U8 USB | Review connector accessibility; place ESD in the entry path with a short ground return | USB FS/HS pin contract, impedance/return routing, VBUS modes and mechanical clearance |
| J4 reset/boot/SWD and indicators | Accessible service region within the carrier envelope | Cable/pin orientation, debug/programming access and boot-state behavior |
| All remaining passives | Pin/loop/channel-specific placement from the inventory, not a leftover-space placement pass | Datasheet and subcircuit ownership closed for every row |
| Fiducials, markings and test pads | Clear assembly/test access on both sides | Courtyard/paste/silkscreen, assembly registration and electrical test coverage |

The preferred production target is **four copper layers**. **Six layers** are an acceptable fallback if four cannot meet the design requirements. **Eight layers** are the final fallback, considered only after documented four- and six-layer trials fail. Twelve layers describe the existing board only and are outside the redesign target.

Evaluate candidates in the order **4 → 6 → 8**. For each candidate, review BGA escape geometry, coordinated MCU/SDRAM placement, bus routing and timing, continuous signal return paths, power distribution, analog isolation and the actual JLCPCB stackup/process. Compare fabrication and assembly costs, including via technology; fewer layers do not automatically mean a cheaper manufacturable board. Record the specific constraint that prevents a candidate from passing, together with the placement/fanout alternatives tried, before increasing the layer count.

Select the lowest layer count that passes the full independent review. Four-layer feasibility is not established yet. Initial disposable trials show a MCU escape with zero native clearance errors after accounting for drilled holes and allowing six filled/capped power-pad vias. SDRAM escape at the inherited placement remains incomplete. These are local escape studies with no connected planes or whole-board routing, not an accepted four-layer design. Six- and eight-layer trials have not been invoked. See [four-layer-trials.json](review/four-layer-trials.json).

If eight layers cannot meet the requirements, report the concrete blocker rather than returning to 12 layers. Do not cut layers from the existing routed file and assume the remaining copper is valid.

Assign each signal layer an adjacent reference; constrain memory, QSPI, SAI and USB by actual edge rates and timing budgets. Plan power islands and stitching around the reference scheme. Avoid fragmented ground, long analog feedback loops and unnecessary layer transitions. Define manufacturer limits and engineering sidecars before invoking a router.

## Implementation and independent review sequence

1. Close sources, BOM discrepancies and electrical requirements. Review all component/package pin maps and the complete carrier contract.
2. Produce a clean schematic with preserved electrical intent. Run native ERC/netlist, independent pin-to-net comparison and analog/power calculations.
3. Trial the core fanout and candidate stackups in the order four, six, then eight layers, using disposable files outside the checkout. Reject any output that fails native DRC, connectivity, return-path or timing review; document why the lower-layer candidate failed before escalating.
4. Place complete functional groups, then review actual supply/signal loops and mechanical envelopes. Freeze no unreviewed placement.
5. Route critical clocks/memory/USB and analog feedback first, then remaining nets, using KiCadRoutingTools. Do not invoke the prohibited legacy MCP autorouter. For every operation retain before/after evidence and run zone-refilled native DRC, independent connectivity and copper-hygiene checks.
6. Investigate every new warning/error against raw geometry and sources. Do not waive errors merely because a tool generated the geometry. Remove obsolete copper only after proving connectivity and required return paths remain intact.
7. Finish silkscreen, assembly/test access and manufacturing notes. Re-export and cross-check Gerbers/drills/BOM/CPL from the final accepted files.
8. Perform the final per-part, firmware, mechanical, DFM, SPICE, EMC-risk and thermal review, with explicit coverage and source citations. Keep failed, skipped and unrun checks separate from passes.

## Production acceptance

The final deliverable must contain editable KiCad sources/libraries/rules, reproducible validation commands, source/requirements matrix, complete BOM/CPL, fabrication notes/stackup, Gerbers/drills, assembly drawings, test firmware/procedure and an evidence-based review with no unexplained critical findings.

First-article validation must exercise power consumption/startup, USB DFU and software boot entry, SWD, QSPI boot/read/write, full SDRAM address/data patterns, audio across supported sample rates, all CV/ADC/gate paths and actual carrier fit. Test limits must come from the requirements matrix. Analytical agreement and clean layout checks cannot replace those physical results when declaring the module production-ready.

Do not add attribution trailers, watermarks or attribution in branch/commit names or repository text. Keep work in the existing checkout, preserve prior changes and do not publish or order hardware without the user's authorization.
