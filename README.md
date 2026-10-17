# Teresina-Rack

**Version 0.1.0-alpha0 — under engineering review; not fabricated or hardware-tested.** The current PCB is a 12-layer baseline with confirmed electrical, BOM, package and layout findings. It is not approved for production.

The goal is an open, self-fabricatable Daisy Patch SM-compatible Eurorack submodule: the same carrier interface and libDaisy application compatibility through a small Teresina firmware variant. Source compatibility and hardware behavior remain qualification targets. See [the firmware policy](docs/firmware-policy.md) and [production review](docs/production-review.md).

![Board top](docs/board-top.png)

| Top | Bottom |
|---|---|
| ![Top](docs/board-top.png) | ![Bottom](docs/board-bottom.png) |

![Perspective](docs/board-persp.png)

## Production target

**4 copper layers preferred; 6 acceptable if required; 8 the final fallback.** Evaluate in that order with new placement, BGA escape, timing, return-path and manufacturer review. Document the constraint and alternatives tried before increasing layer count. Twelve layers describe the existing file only and are outside the redesign target. See [the redesign plan](docs/redesign-plan.md).

Disposable four-layer MCU escape trials reached zero native clearance errors when six power-pad vias were filled/capped. The full board remains unrouted in those studies, and SDRAM escape at the inherited placement still fails. These results do not qualify a four-layer production design.

## Existing hardware

| Block | Baseline |
|---|---|
| Interface |68 × 40 mm, 40 through-hole mating pads; all 40 local pad geometries match official CAD |
| MCU |STM32H750IBK6, UFBGA176+25 balls, 480 MHz Cortex-M7 |
| RAM |IS42S32160F-6BLI prototype candidate, 64 MB, 3.3 V, 32-bit FMC; requires the Teresina refresh profile and hardware qualification |
| Flash |IS25LP064A, 8 MB QSPI |
| Codec |PCM3060, SAI1, I²C2 address 0x46 |
| Analog |TL074 audio, MCP6004 CV/gates, LM4040-10 V reference |
| Power |TPS62170 digital buck, LD1117 5 V stage; component selection/layout/budgets require correction |
| Files |209 schematic component references, 214 PCB footprints including five fiducials |

Manufacturer pin maps confirm the core/codec/analog signal assignments. 74 checked digital-net assignments agree with pinned libDaisy. Complete carrier fit, sequencing, analog performance and firmware execution still need first-article validation.

## Open compatibility findings

Official libDaisy v9.0.0 is the pinned firmware reference. Its stock refresh sweep is 168.35 ms against the proposed ISSI part's 64 ms requirement. An opt-in Teresina prototype now implements a conservative refresh profile and reviewed clock/init changes. Crossbuilds support a limited source-compatibility claim; stock binaries are unsupported and hardware tests remain unrun. See [the firmware decision](docs/firmware-policy.md) and [original retention check](docs/review/core-review/bounded-acceptance.md).

An [expanded memory-replacement search](docs/memory-replacement-search.md) found no datasheet-backed fix for unchanged firmware. Etron EM63B325BK is an unresolved catalogue lead; it has not been qualified or selected.

The review also confirms wrong ferrite/inductor/capacitor ordering data, crystal/diode footprint mismatches, CV amplifiers on the wrong supply, gate-output resistance differences and remote critical power/clock/decoupling loops. The earlier claims of an identical analog implementation and completed production validation are superseded by [the current findings](docs/production-review.md). Reviewed corrections are staged outside the checkout until the complete design can be synchronized.

## Validation

| Check | Baseline result and boundary |
|---|---|
| Native KiCad 10.0.7 DRC |0 errors, 0 unconnected, 414 warnings |
| Native ERC |3 power-pin conflicts, 250 warnings; unresolved |
| Native netlist→PCB |821 functional pad assignments agree; intentional NC aliases separately checked |
| Connectivity |200 routed nets connected; native zone-refill agreement |
| Copper hygiene |384 candidate findings; requires geometric review |
| SPICE |63 generated tests pass; ideal channel benches also executed; device/rail/tolerance coverage incomplete |
| EMC/thermal |Risk analyses executed; thermal budget incomplete; no compliance measurement |
| Fabrication export |34 Gerbers, PTH/NPTH drills, CPL; baseline only |

A clean native DRC does not resolve wrong ordered parts or prove stock-firmware retention, thermal safety, analog performance or carrier fit. See the full review for passed, failed and unrun checks.

## Development and fabrication

Use KiCad 10 for the project under `TeresinaRack/`. The configured cloud environment retains checksum-verified KiCad 10.0.7, ngspice 47, kicad-tools, KiCadRoutingTools and kicad-happy; reproducible setup/startup instructions are saved in environment settings. Interactive GUI editing and hardware programming were not validated in the headless environment.

Keep every routing operation's before/after evidence and run native DRC/refill, independent connectivity and copper hygiene before accepting it. Use the actual selected JLCPCB process, not an unrelated generic profile. Final fabrication requires an accepted stackup, explicit filled/capped-via process, corrected sourcing-complete BOM, CPL/assembly drawings, header dimensions and first-article plan. The current files and exports are not an approved order package.

```sh
kicad-cli pcb drc --format json -o drc.json TeresinaRack.kicad_pcb
kicad-cli sch erc --format json -o erc.json TeresinaRack.kicad_sch
```

Run from `TeresinaRack/` and inspect every report severity and unconnected item. Exit 0 alone does not establish a pass. Generated fabrication files belong in the ignored `fab/` directory.

## Repository layout

- `TeresinaRack/`: editable KiCad project, custom symbols and rules.
- `docs/production-review.md`: current evidence, blockers and review limits.
- `docs/redesign-plan.md`: requirements, 4 → 6 → 8 sequence and acceptance gates.
- `docs/review/`: inventory, calculations and independent subsystem evidence.
- `DESIGN.md`: historical working notes, superseded by the current review.
- `bom/`: baseline BOM working files; not approved production sourcing.

## Acknowledgements

- [Electro-Smith](https://electro-smith.com) — the Daisy platform, libDaisy, and the published
  Patch SM pinout/footprint that make a compatible open re-implementation possible.
- [kicad-happy](https://github.com/aklofas/kicad-happy) — schematic/PCB/EMC/SPICE analysis suite
  used for validation.

*This is an independent DIY project, not affiliated with or endorsed by Electro-Smith. "Daisy" and
"Patch SM" are their marks. Build at your own risk — check everything before powering your rack.*
