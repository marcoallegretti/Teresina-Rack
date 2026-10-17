# Source-backed core component selection

This note defines the smallest supported edits and separates nominal repairs from production qualification. Machine instructions are in `core-edit-plan.json`. No CAD or firmware was changed during this review.

## VCAP: replace both incorrect 22 µF orders, retain the shared net

C13 and C14 display 2.2 µF but order CL10A226MQ8NRNC/C59461, which is22 µF. Use **CL21B225KAFNNNE / C19110**,2.2 µF ±10%,25 V,X7R,0805, with `Capacitor_SMD:C_0805_2012Metric`. Keep both positive pins and U1.F13/M10 on the **same VCAP net**. Place one capacitor locally at F13 and the other locally at M10; connect both negative pins to ground with short returns. ST AN4938 Rev7 **p12 explicitly requires connecting VCAP1 to VCAP2**. Splitting the net into two isolated rails would contradict this guidance.

The exact Samsung base specification and curves are available directly at:
https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=CL21B225KAFNNN

The final packing suffix is corroborated by the exact LCSC C19110 product. Native KiCad10 confirms the0805 footprint's1.0×1.45 mm lands at x=±0.95 mm. Both existing caps require footprint changes from0603.

The previously proposed **C23630 / CL10A225KO8NNNC** is genuinely2.2 µF ±10%,16 V,X5R,0603. It is not the wrong22 µF order. However, Samsung's exact manufacturer models show approximately8.41% DC loss at1.35 V and13.76% temperature loss at85 °C separately. Multiplying these typical changes with the−10% initial tolerance as a screening estimate gives1.552 µF at the worst modeled point over1.0–1.4 V and−40..85 °C, below ST's1.76 µF lower edge. This is a **screening concern**, not a guaranteed combined characteristic or demonstrated physical failure.

The recommended C19110 has almost zero modeled DC loss at1.35–1.4 V and a worst modeled temperature change of−5.18% in that range. The analogous screen is **1.877–2.434 µF**, with modeled ESR18.6 mΩ at100 kHz and5.4 mΩ at1 MHz. Samsung expressly labels these data typical and for design reference only. They do not establish guaranteed ESR across bias/temperature, combined capacitance variation, aging or procurement extremes. Verify those limits and regulator startup/stability before release. ST specifies2.2 µF ±20% and ESR<100 mΩ (DS12556 pp96,201). The modeled voltage sweep1.0–1.4 V is an engineering screening envelope around published nominal VCAP values; it is not a measured rail range.

Reproducible source extraction and calculations: `samsung-225-0805.html`, `samsung-225-0805-curves.json`, `component-screen.json`, `check-core-components.py`. Alternative C2762602/CL21B225KBYNNNE50 V X7R also has correct nominal capacitance, but its modeled cold-temperature margin is narrower; its analogous minimum is1.803 µF. Do not choose solely by voltage rating or stock count.

## Existing YXC: package correction is supported; exact load remains unresolved

The current X322516MLB4SI/C13738 can receive the following verified package repair:

- Symbol `Device:Crystal_GND24`.
- Footprint `Crystal:Crystal_SMD_3225-4Pin_3.2x2.5 mm`.
- Pin1→OSC_IN, pin3→OSC_OUT, pins2/4→GND. The old two-pin symbol's pin2 becomes new pin3.

Native KiCad library inspection confirms signal terminals1/3 and ground terminals2/4. Pins2/4 are stacked in the symbol; pin4 is hidden, so the exported native netlist must explicitly show both grounded. Its lands1.4×1.2 mm at x=±1.1,y=±0.85 mm match the YXC manufacturer's suggested lands exactly. See `kicad-core-library.json`.

Authoritative YXC direct sheet https://www.yxc.hk/uploadfiles/2026/09/YXC-YSX321SL.pdf, p1, fixes package, pin roles, ESR≤50 Ω at16 MHz and C0≤3 pF. It lists load10 pF,20 pF or custom specification; its generic drive row permits variant-dependent maxima in the10–200 µW range. The manufacturer catalog permits7–22 pF/custom for this family. Manufacturer product page and exact-code search did not reveal a full X322516MLB4SI order-code definition. **The exact9 pF claim is still only the distributor SKU attribute; this does not close the requested manufacturer ordering proof.** Neither exact drive limit nor a final C37/C38 value is approved for the YXC variant from these generic ranges alone.

## Manufacturer-decoded ECS alternative

**ECS-160-8-33Q-RES-TR / C6844087** provides an unambiguous8 pF order code. Direct manufacturer PDF https://ecsxtal.com/store/pdf/ECX-33Q.pdf, Rev2023 pp1–2, defines:

- 160→16.000 MHz;8→8 pF load;33Q→ECX-33Q package.
- R→±15 ppm initial tolerance;E→±50 ppm stability;S→−40..125 °C;TR→1000-per-reel packing.
- At16 MHz: ESR≤80 Ω,C0≤7 pF,drive≤100 µW,first-year aging≤±5 ppm.
- Pins1/3 are interchangeable signal terminals;2/4 are ground. Height≤0.8 mm.

The full exact C6844087 distributor attributes independently agree. Retail stock was13 units at retrieval: this supports a few prototypes, **not production sourcing or reserved JLC assembly inventory**. Its specified accuracy is looser than the current YXC distributor claim; a published PatchSM oscillator-accuracy requirement was not established. Confirm the reference accuracy requirement before accepting this as full hardware-specification equivalence.

Use `Device:Crystal_GND24` with the same net mapping. The ECS recommended lands differ from generic KiCad3225: **1.3×1.1 mm** at x=±1.15,y=±0.90 mm (p1 Figure2). Create a manufacturer-matched project footprint, e.g. `TeresinaRack:Crystal_ECS_ECX33Q_3.2x2.5 mm`. Both share outer pad extents, but the generic footprint changes inner gaps and must not be described as an exact ECS land-pattern match. The JSON gives all four explicit numbered coordinates.

### Oscillator calculation and tuning

AN2867 Rev24 pp13–14 gives `gmcrit=4*ESR*(2*pi*F)^2*(C0+CL)^2`. For ECS16 MHz,80 Ω,7+8 pF, **gmcrit=0.727666 mA/V**, below STM32H750's maximum-critical-transconductance1.5 mA/V (DS12556 p219). This criterion already includes ST's factor-five design margin; applying another factor-five test to1.5 mA/V would incorrectly reject supported crystals. This is a source-backed oscillator selection check, not a measured startup result.

Equal load capacitors follow `C37=C38=2*(8 pF−totalCstray)`. Thus a **10 pF C0G/NP0 pair is a calculated prototype starting value only if the intended total stray is3 pF**. Stray2 pF calls for12 pF; stray1 pF calls for14 pF; stray4 pF calls for8 pF. These are conditional values, not measured capacitances of an unfinished layout. Relocate the complete oscillator loop next to U1.G1/H1, extract or measure actual load, then trim and verify HSE frequency. Keep firmware HSE16 MHz unchanged.

Conservatively using ESRmax80 Ω, a sinusoidal crystal current≤1.118 mA RMS (≤3.162 mA peak-to-peak) keeps drive≤100 µW. Measure current/drive according to AN2867 pp15–16, including startup and operating extremes. If an output-series resistor becomes necessary, its added loss must be included in the startup calculation. The theoretical total-series threshold from this simple model is164.91 Ω, leaving84.91 Ω above ESRmax before other losses; this is not a recommended resistor value or permission to add resistance without measurement.

The exact 10 pF capacitor is **Murata GRM1555C1H100JA01D / C76946**, C0G, ±5%, 50 V, 0402. The manufacturer reference sheet p1 explicitly gives the full part-number system including D packing and these electrical specifications; its LCSC attributes independently agree (retail 296,600 at retrieval, not reserved). Source: https://datasheet.lcsc.com/datasheet/pdf/1c6af07abaa9451a8a7a76981760389d.pdf?productCode=C76946 . C1560 was considered and rejected: its actual SKU is 2.5 pF, not 10 pF. Do not substitute a guessed distributor code. Manufacturer startup, drive, final frequency accuracy and procurement closure remain production gates even with the fully decoded ECS part.

## Independent review after implementation

The staged candidate currently has no core edits. After implementation applies the selected JSON strategy, independently export native XML and compare every explicit Value/MPN/LCSC/Footprint field; verify all four crystal nets and the shared VCAP topology; compare all U1/U2/U3 assignments with baseline; validate exact chosen lands after orientation/backside normalization; inspect native ERC and later PCB synchronization/DRC. Keep the source alternative mutually exclusive with the YXC package-only strategy. None of these repairs resolves the separate RAM-refresh blocker.
