# Teresina firmware compatibility decision

Proceed with a narrowly scoped Teresina variant of pinned Electro-Smith firmware. The RAM refresh discrepancy is a resolved configuration task in a prototype and a pending hardware qualification item. It does not prevent further schematic, placement or four-layer feasibility work. It still prevents claiming compatibility with unchanged stock binaries.

This is a change from the earlier unchanged-firmware requirement, following the user's proposal to accept a small firmware variant. It does not approve the current PCB or establish that a manufacturable redesign is complete.

## Evidence and scope

The reference SDK is [libDaisy v9.0.0](https://github.com/electro-smith/libDaisy/tree/08087203debc646d3710ec8caa35bac6cf20ab5e). The bootloader reference is [v6.4 source](https://github.com/electro-smith/DaisyBootloader/tree/8b279a8e25922b786c24a6cbd1d499cdc1e76934). Both revisions and their dependencies are pinned in the retained prototype under `/workspace/cloud-setup/redesign/firmware-candidate`.

| Item | Prototype behavior | Qualification boundary |
|---|---|---|
| SDRAM refresh | COUNT369 at nominal 100 MHz SDCLK; a conservative 32 ms row-sweep target, including a 20-cycle scheduling allowance and a provisional 1000 ppm lower-clock allocation | ISSI requires 64 ms through its specified 85 °C limit. Actual oscillator bounds, bus loading, timing and operation under load still need qualification. |
| PLL2 | M3/N37/FRAC4096 places the reference inside the configured 4–8 MHz range; nominal outputs remain unchanged | PLL reference and jitter behavior differ from upstream and need hardware checks. |
| CPU clock | Integer PLL profiles give 478.4 MHz Boost and 398.4 MHz Default | Upstream enum names remain; actual frequencies differ by about 0.33%/0.4%. Hard-coded clock assumptions need review. |
| Silicon/init | Rev V required; reject a live SDRAM controller before clock changes and SDRAM initialization; check initialization failures | Procurement must establish the silicon revision. Live reinitialization and SDRAM retention across reset are unsupported. |
| Boot adapter | Digital System/SDRAM/QSPI initialization, DCache off and TIM5 control callback; no analog initialization dependency for USB updates | Reset/DFU/storage logic is preserved. USB power, interrupt service timing and powered-rack output transients need bench tests. |
| Build selection | Opt-in SDK profile, strict 0/1 parser, object rebuild stamp and application relink dependency | A flag passed only to an application cannot change an already compiled stock SDK. Use matching SDK/bootloader builds. |

The unchanged public SDK headers and pin/channel mapping support a source-compatibility strategy. A single unchanged passthrough application has crossbuilt against both the stock and modified SDK; the modified SDK also links that application for internal flash, QSPI and internal SRAM. That is useful evidence, but it is not a representative compatibility survey or an executed audio test. The [final core review](review/firmware/firmware-final-review.md) verifies the scoped source/patch/artifact hashes, five linked images and default-off code equivalence. The [boot adapter review](review/firmware/bootloader-digital-review.md) checks its timer, cache and reset integration. Both accept only their stated prototype scope.

The existing microsecond timer conversions truncate a fractional-MHz timer frequency. At the candidate clocks, reported microseconds have approximately +0.084% Boost / +0.101% Default bias; nominal millisecond conversion remains exact. Timing-sensitive applications must account for this. More frequent refresh also consumes memory bandwidth; real DSP headroom must be measured. Keeping the API unchanged cannot guarantee identical performance.

## What can be postponed

The prototype already implements the refresh correction and clock/init guards. Deferring their physical validation until first-article bring-up is reasonable while the electrical design and layout continue. Leaving the required firmware behavior undefined until after the production layout is frozen would be weaker: a firmware investigation can uncover procurement, clock, supply or timing constraints, as this review already did.

Before a first-article design freeze, complete the manufacturer/controller/board memory timing and oscillator budget. The bounded refresh review does not qualify every memory timing; self-refresh is unsupported and its inherited exit delay has no positive frequency margin. Before a production release, validate the full 64 MiB with caches controlled, temperature/supply corners, sustained competing traffic and actual refresh/clock registers; test audio/CV/gates, USB-only and rack-powered updates, repeated reset/boot paths and representative applications. The supplied memory-test firmware is crossbuilt but has never run on hardware. Its 80 ms dwell uses periodic refresh and is not an isolated cell-retention characterization or a substitute for the datasheet guarantee.

## Compatibility promise

Target recompiled libDaisy applications using the Teresina SDK and compatible bootloader, with unchanged application source where its assumptions permit. Document and test any porting exceptions. Do not promise stock-binary compatibility or a percentage of compatible programs before measuring it.

The current prototype excludes pre-v6 external-memory boot paths, SDRAM-resident code/stack/data accessed before initialization, direct live boot handoffs, arbitrary clock reconfiguration and repeated board initialization. It preserves the supported reset-mediated v6 handoff. Upstream bootloader dependencies are upgraded to the same pinned v9 SDK as the application and require integration testing.

The subsequent [expanded replacement search](memory-replacement-search.md) found no documented RAM substitution meeting unchanged-firmware retention and the existing hardware contract. Etron EM63B325BK remains an unresolved catalogue lead, not an accepted substitute. The search does not prove global nonexistence.

Manufacturability and working firmware are separate acceptance gates. Continue the 4 → 6 → 8 layer policy and close power, BOM, footprint, mechanical, routing and assembly findings independently. A passing firmware build cannot approve the board for ordering.
