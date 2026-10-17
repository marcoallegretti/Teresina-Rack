# Teresina-Rack — Daisy Patch SM–compatible module (STM32H750)

> Historical working notes. Current evidence and requirements are in [production-review.md](docs/production-review.md) and [redesign-plan.md](docs/redesign-plan.md). Production target: **4 layers preferred, 6 acceptable fallback, 8 final fallback**. The existing 12-layer PCB is a baseline only. Claims below about compatibility, verified hardware or required layer count are superseded by the current review; production qualification remains open.

**Goal:** A self-fabricable (JLCPCB PCBA) Eurorack DSP submodule that is **mechanically, pin-, and
firmware-compatible with the Electro-Smith Daisy Patch SM (Rev2/Rev3)** — same 68 × 40 mm outline,
same 40-pad connector layout, same pin functions — so it drops into a Daisy Patch.Init() (or any
Patch-SM carrier) and runs stock `DaisyPatchSM` firmware unmodified.

Sibling project to **Teresina** (the Daisy *Seed* clone). Teresina-Rack **reuses Teresina's proven
STM32H750 + SDRAM + QSPI core and its via-in-pad BGA-fanout construction**, and adds the Patch-SM
Eurorack analog front-end. Independent design; not affiliated with Electro-Smith.

> Evidence base: `ES_Daisy_Patch_SM_Schematic.pdf` (Rev3-REDUCED, omits the shared core sheet),
> `Patch-SM_pinout.csv`, official KiCad footprint `DAISY_PATCH_SM.kicad_mod`, `ES_Patch_SM_datasheet_v1.0.5.pdf`,
> and **libDaisy `src/daisy_patch_sm.h/.cpp`** (authoritative pin map). All pins below are from libDaisy.

---

## Mechanical (the drop-in contract — from `DAISY_PATCH_SM.kicad_mod`)
- **68 × 40 mm** board outline.
- **40 pads, 2.54 mm pitch, 1.88 mm**, in four 2×5 clusters:
  - **A** (A1–A10): top-left, rows y −12.73/−15.27, cols x −21.92…−32.08
  - **D** (D1–D10): bottom-left, rows y +12.73/+15.27
  - **B** (B1–B10): top-right, cols x 26.73/29.27, rows y −7.92…−18.08
  - **C** (C1–C10): bottom-right, cols x 26.73/29.27, rows y +7.92…+18.08
- Smaller than Teresina (88×40) but carries much more → dense mixed-signal floorplan required.

## Pin map (the compatibility contract — libDaisy authoritative)

| Pad | Function | STM32 | Pad | Function | STM32 |
|---|---|---|---|---|---|
| A1 | −12V in | — | C1 | CV_OUT_2 | PA5 (DAC1_2) |
| A2 | ADC_9 | PA1 | C2 | CV_4 | PA7 |
| A3 | ADC_10 | PA0 | C3 | CV_3 | PA2 |
| A4 | GND | — | C4 | CV_2 | PA6 |
| A5 | +12V in | — | C5 | CV_1 | PA3 |
| A6 | +5V out | — | C6 | CV_5 | PB1 |
| A7 | GND | — | C7 | CV_6 | PC4 |
| A8 | USB_DM | PB14 | C8 | CV_7 | PC0 |
| A9 | USB_DP | PB15 | C9 | CV_8 | PC1 |
| A10 | +3V3 out | — | C10 | CV_OUT_1 | PA4 (DAC1_1) |
| B1 | AUDIO_OUT_R (DC) | codec | D1 | SPI2_CS | PB4 |
| B2 | AUDIO_OUT_L (DC) | codec | D2 | SDMMC1_D3 | PC11 |
| B3 | AUDIO_IN_R (AC) | codec | D3 | SDMMC1_D2 | PC10 |
| B4 | AUDIO_IN_L (AC) | codec | D4 | SDMMC1_D1 | PC9 |
| B5 | GATE_OUT_1 | PC14 | D5 | SDMMC1_D0 | PC8 |
| B6 | GATE_OUT_2 | PC13 | D6 | SDMMC1_CK | PC12 |
| B7 | I2C1_SCL | PB8 | D7 | SDMMC1_CMD | PD2 |
| B8 | I2C1_SDA | PB9 | D8 | ADC_12 / SPI2_MISO | PC2 |
| B9 | GATE_IN_2 | PG14 | D9 | ADC_11 / SPI2_MOSI | PC3 |
| B10 | GATE_IN_1 | PG13 | D10 | SPI2_SCK | PD3 |

**Fixed-function (core, shared with Teresina):**
- **Codec = PCM3060** (differential out). **SAI1**: MCLK=PE2, SCK=PE5, FS=PE4, SA(RX)=PE6, SB(TX)=PE3.
  **Control = I2C2**: SCL=**PB10**, SDA=**PB11** (⚠ differs from Teresina's WM8731 I2C2 SCL=PH4).
- **QSPI flash (IS25LP064A):** IO0=PF8, IO1=PF9, IO2=PF7, IO3=PF6, CLK=PF10, NCS=PG6 *(identical to Teresina)*.
- **SDRAM (AS4C16M32MSA, 64 MB, 32-bit FMC)** — identical mapping to Teresina.
- **USB:** OTG_HS in FS mode, DM=PB14, DP=PB15 (⚠ Seed used OTG_FS PA11/12).
- **DAC (CV out):** internal 12-bit DAC1, ch1=PA4, ch2=PA5, DMA, 48 kHz.
- User LED=PC7, Boot-flash strap=PG3, crystal HSE=PH0/PH1 (16 MHz).

## Circuit blocks
1. **Core (reuse Teresina):** STM32H750IBK6, AS4C16M32MSA SDRAM, IS25LP064A QSPI, crystal, decoupling,
   power-in to VDD/VDDA/VCAP. Via-in-pad BGA fanout, 8-layer.
2. **Codec swap:** WM8731 → **PCM3060** (SSOP-28). SAI1 bus reused; I2C2 control on PB10/PB11.
3. **Eurorack power (new — sheet 3):** ±12V in → NSR1020 Schottky reverse-protection → +12/−12V rails;
   **LD1117-5V** LDO (+5V analog); **TPS621x buck** + 2.2µH → +3V3_D; ferrite-filtered +3V3_A.
   USB VBUS can back-feed +12V (Schottky) to run MCU for flashing without rack power.
4. **Audio analog (new — sheet 2):** **TL074** quad op-amp. Inputs AC-coupled (2.2µF) → non-inv buffer
   (66K5/15K/220pF) → PCM3060 ADC (ref CODEC_VCOM). Outputs: codec differential → diff-to-SE + filter
   (18K/66K5/100pF/39K/18pF/100R) → DC-coupled AUDIO_OUT.
5. **CV/Gate conversions (new — sheet 4):** −10V ref (LM4040-10V). 8× CV in via **MCP6004** scaling
   (200K/100K/33K/220pF, bipolar → 0–3.3V ADC). 2× CV out: DAC (PA4/PA5) → MCP6004 (120K/62K, 0–3.3V→0–5V).
   2× gate out: MCP6004 level-shift 3.3→5V. 2× gate in: MMBT3904 level-shift → 3.3V logic.
6. **User I/O (sheet 1):** micro-USB (P9) + VBUS divider + USBLC6 ESD; JTAG/SWD header; reset+boot buttons;
   PWR + USER LEDs; SD-card pull-ups on SDMMC1.

## Reuse from Teresina (unbiased)
- **Direct reuse:** STM32H750/SDRAM/IS25LP064A **symbols**; the **core net topology** (FMC/SDRAM, QSPI,
  power, crystal, decoupling); the **SAI1 audio bus pins**; the **via-in-pad + 8-layer HDI construction**
  and its scripts; buck/USB-ESD/boot/LED patterns; HDI design rules (`.kicad_pro`).
- **New/changed:** PCM3060 codec + I2C2 pin change; USB pin change (PB14/15); the entire ±12V power tree;
  all TL074/MCP6004 analog; internal-DAC CV out; gate level-shifters; −10V ref; **68×40 castellated form
  factor**; and a **fresh, denser floorplan** (Teresina's placement/route does not transfer).

## Exact-mirror basis for the analog blocks (firmware-compatibility contract)
Electro-Smith did **not** publish the Patch SM submodule's internal analog schematic with values
(the reference PDF is a REDUCED/black-box sheet; the KiCad/EAGLE libraries carry only the 40-pad
black-box symbol + footprint). "Exact mirror" for the CV/gate analog therefore means **reproducing the
transfer functions the stock firmware assumes**, not copying unpublished resistor values. Authoritative
source = libDaisy `daisy_patch_sm.cpp/.h`:
- **CV outputs** CV_OUT_1/2 (DAC1 PA4/PA5): **0 – 5 V** unipolar. `code = clamp(volts * 819, 0, 4095)`
  (819 = 4095/5). → DAC 0-3V3 into a **×1.515 non-inverting gain** (0-3.3V → 0-5V).
- **CV/ADC inputs**: 8× **bipolar CV** (CV_1..CV_8) + 4× **0–3V3** ADC (ADC_9..ADC_12, direct/buffered).
  Bipolar range = **−5 V … +5 V** (Eurorack std; `InitBipolarCv`). Map −5..+5 V → 3V3..0 V (inverting
  scaler, gain −0.33, +1.65 V offset from the −10 V ref); firmware `flip` corrects the inversion.
- **Gates**: Eurorack. Gate-in tolerant to ~+12 V, threshold ~1–2.5 V → 3V3 logic (MMBT3904 shifter).
  Gate-out 3V3 logic → 0/+5 V (op-amp/level shifter). No firmware-visible calibration → values flexible.

## Progress (build state)
- [x] Core remap (STM32 balls → Patch-SM nets), PCM3060 codec + decoupling, ±12V power tree.
- [x] **Audio front-end COMPLETE + netlist-verified:** TL074 (U12) inputs (units C/D, AC-coupled buffers)
      + outputs (units A/B, differential 2nd-order MFB reconstruction filter, 18K/66K5/39K/100pF/18pF/100R)
      + power (unit 5 = ±12V). AUDIO_OUT_L/R await the connector.
- [x] **CV/Gate block COMPLETE + netlist-verified:** 8× bipolar-CV inverting scalers (100K/200K/33K/220pF,
      −5..+5 V → 0-3V3, off the −10 V LM4040 ref) → STM32 ADC balls; 4× ADC 0-3V3 inputs (1K series);
      2× CV-out ×1.515 gain (0-3V3→0-5V); 2× gate-out comparators (→0/5 V); 2× gate-in MMBT3904 shifters.
      3× MCP6004 (on TL074 symbol, Value=MCP6004 — flatten to a proper MCP6004 symbol before final BOM).
- [x] **40-pad castellated connector COMPLETE (J5, all 40 pads):** pad→net map from official
      `Patch-SM_pinout.csv` (symbol `Daisy_Patch_SM` copied into project lib). CV/gate-in pads = JACK-side
      (±5V/Eurorack, scaling on-module); CV_OUT/GATE_OUT pads = post-amp (0-5V). ADC_9-12 (A2/A3/D8/D9 =
      PA1/PA0/PC2/PC3) = primarily 0-3V3 ADC (1K/1nF); alt UART4/SPI2 filtered (matches stock ADC use).
- [x] **Finalized + PWR_FLAGs:** user LED tied to PC7; ~36 spare STM32/codec/JTAG pins NC-flagged; orphan
      WM8731 leftovers removed; 7 PWR_FLAGs added. **Netlist: 238 nets, 0 floating functional nets, all
      blocks verified end-to-end.** ERC residual = 236 off-grid (cosmetic, no PCB impact — board is built
      from the netlist) + 3 inherent false-positives (STM32 dual-VCAP, connector GND pins typed power-out)
      + 1 footprint-link (resolves when the J5 castellated footprint lib is registered in the PCB step).

## SCHEMATIC COMPLETE — next phase = PCB
Full functional schematic done & netlist-verified. Remaining project = the board:
mechanical (68×40 + 40-pad castellated edge) → dense mixed-signal placement → HDI routing (add layers,
via-in-pad reuse) → DRC/EMC/thermal validation → JLCPCB fab package. MCP6004 opamps currently use the
TL074 symbol (Value=MCP6004) — flatten to a real MCP6004 symbol + set LCSC parts at BOM time.
- [ ] Mechanical 68×40 + castellated edge; placement; HDI route; validation; fab.

## Open items / to verify during build
- PCM3060 exact footprint + I2C address + VREF/VCOM caps (from PCM3060 datasheet).
- Op-amp choice availability at JLCPCB (TL074 / MCP6004) + LM4040-10V, LD1117-5V, TPS621x, NSR1020.
- ADC input protection / clamping detail on CV inputs vs LM4040 −10V ref network.
- Whether to keep SDMMC (SD-card) and JTAG exactly as Patch SM.
- Confirm bipolar-CV range (−5..+5 V assumed) and gate-out level (+5 V assumed) if a genuine unit is on hand.

## Sources
- Electro-Smith Daisy Patch SM: schematic (Rev3-REDUCED), datasheet v1.0.5, pinout, `DAISY_PATCH_SM.kicad_mod`.
- Pin map ground truth: [electro-smith/libDaisy](https://github.com/electro-smith/libDaisy) `src/daisy_patch_sm.h/.cpp`.
- Core reuse: sibling **Teresina** project (Daisy Seed 1.1 clone).
