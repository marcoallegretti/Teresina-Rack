# Efficient +5 V stage with static forced PWM — engineering proposal

13 October 2026. Read-only research; no CAD changes or production acceptance. This supersedes the TPS62163 preference in five-volt-architecture.md. The original LD1117 is not a safe sustained-load choice at a 17 V carrier input, and its dissipation rises to roughly 5.6 W at 12 V and 10 W at 17 V for an illustrative 838 mA total load. Genuine TI TPS62135 offers a source-backed way to reduce heat while retaining forced PWM, precise feedback and adjustable startup. The analog, input and sequencing contracts still require review.

## Candidate choice and genuine sources

| Candidate | Exact source, observed retail inventory | Behavior and suitability |
|---|---|---|
| TI TPS62135RGXR | [C167238](https://www.lcsc.com/product-detail/C167238.html), 2141 | Preferred trial: 3–17 V input, 4 A silicon, 2.5 MHz typical, forced PWM with MODE high, adjustable soft-start, hiccup overload and active output discharge. |
| TI TPS62136RGXR | [C2865220](https://www.lcsc.com/product-detail/C2865220.html), 89 | Same accuracy/control concept, 1 MHz typical. Larger ripple/negative current for the same inductor; not the first trial. |
| TI TPS621351RGXR | [C2070706](https://www.lcsc.com/product-detail/C2070706.html), 3299 | No active output discharge, but also no hiccup shutdown. Prebiased-start benefit trades against continuous fault stress; alternative requiring a deliberate sequencing/fault decision. |

TI official datasheets [TPS62135 SLVSBH3B](https://www.ti.com/lit/ds/symlink/tps62135.pdf), pp3–6,9–16,36 and appended RGX0011A drawing; [TPS62136 SLVSDV2](https://www.ti.com/lit/ds/symlink/tps62136.pdf), corresponding sections. The exact package is **11-pin VQFN-HR RGX, 3×2 mm, maximum 1 mm height**, with VIN, SW and GND as three large strips. It is not a standard QFN12 or QFN with an added exposed pad. KiCad 10 offline library contains no RGX match, so a reviewed custom footprint is necessary.

All inventories are LCSC retail observations, not JLC assembly reservations. Manufacturer names, exact order codes, product JSON, PDFs and curves are retained in this directory.

## Proposed schematic connections

Preserve the existing D1/D5 carrier/USB protected-positive OR node. U7 VIN remains on LD_IN after FB7; FB7's corrected real ferrite and all hotplug/filter stability require review. EN and MODE tie directly to **VIN at the local input capacitor**, not to the pre-diode carrier supply; their absolute limits are VIN+0.3 V. VSEL ties GND. This requires no firmware pins or changes.

| RGX pad | Name | Proposed connection |
|---|---|---|
|1|VIN|LD_IN at local input caps|
|2|SW|New SW_5V; only L2 and compact switching copper|
|3|GND|Short local input/output capacitor returns, power ground and thermal spreading|
|4|FB2|No connection, VSEL low; unused programmable-divider switch|
|5|FB|FB_5V precision-divider midpoint|
|6|VOS|Direct shortest connection to +5V local output capacitor positive|
|7|PG|No connection or optional test point, open drain|
|8|EN|VIN local tie|
|9|SS/TR|New SS_5V; C210 to GND|
|10|MODE|VIN local tie, forced PWM|
|11|VSEL|GND|

Proposed new parts/reference names are placeholders until CAD integration: L2 from SW_5V to +5V; two parallel C208A/B from +5V to GND; three parallel C209A/B/C and corrected C63 from LD_IN to GND; C210 SS_5V to GND. R210A and R210B form the top series divider from local +5V to FB_5V, R211 from FB_5V to GND. VOS must remain at the local cap, and the divider/SS return must be quiet and separate from high di/dt copper.

**Remove/bypass FB8 from the main +5 V export path**, subject to schematic review: its 100 mΩ maximum DCR adds roughly 84 mV at 838 mA. Do not compensate by moving VOS beyond the ferrite, which would place another filter inside the control loop. Preserve FB9 and codec capacitors as a separately qualified downstream analog filter; at the codec's 36 mA maximum characterization current, 0.1 Ω gives only 3.6 mV DC loss. Distributed capacitance and damping still affect loop response.

## Exact proposed parts and mechanical constraints

| Role | Exact stocked candidate | Manufacturer basis / footprint |
|---|---|---|
| Preferred L2 | Bourns SRP4020TA-1R0M, [C913245](https://www.lcsc.com/product-detail/C913245.html), 5464 | 1 µH ±20%, DCR27 mΩ maximum, Irms5 A at40°C rise, Isat8.5 A at20% inductance loss, all rated at25°C. [Official Bourns PDF](https://www.bourns.com/docs/product-datasheets/srp4020ta.pdf), p1. |
| Lower-ripple L2 alternative | Bourns SRP4020TA-2R2M, [C719179](https://www.lcsc.com/product-detail/C719179.html),1256 | 2.2 µH ±20%, DCR61 mΩ max, Irms4 A, Isat6 A. **Isat is below converter maximum6.5 A static limit**, so arbitrary-overload suitability is open. |
| C209A/B/C local input, **3 units** | Samsung CL31A106KBHNNNE, [C13585](https://www.lcsc.com/product-detail/C13585.html),620120 | 30 µF nominal total: three10 µF ±10%,50 V X5R1206; effective capacitance at17 V must remain≥3 µF with tolerances/temperature/aging. |
| C208A/B local output, **2 units** | Samsung CL21A226MOQNNNE, [C98190](https://www.lcsc.com/product-detail/C98190.html),489320 | 44 µF nominal total: two22 µF ±20%,16 V X5R0805; verify actual effective capacitance at5 V and≤200 µF total direct load. |
| C63 input HF | Samsung CL05B104KB54PNC, C307331 |100 nF50 V0402, directly between VIN/GND. |
| R210A | Yageo RT0603BRD0760KL, [C6460576](https://www.lcsc.com/product-detail/C6460576.html),4560 |60 kΩ ±0.1%,25 ppm/°C,0603. Manufacturer RT specification V16 p2 confirms B tolerance/D TCR codes. |
| R210B | UNI-ROYAL0402WGF1401TCE, [C39650](https://www.lcsc.com/product-detail/C39650.html),12100 |1.4 kΩ ±1%,100 ppm/°C,0402,62.5 mW. Exact manufacturer series PDF confirms ordering. |
| R211 | Yageo RT0603BRD0710KL, [C95204](https://www.lcsc.com/product-detail/C95204.html),445760 |10 kΩ ±0.1%,25 ppm/°C,0603. |
| C210 | FH0402B472K500NT, [C1538](https://www.lcsc.com/product-detail/C1538.html),724000 |4.7 nF ±10%,50 V X7R0402. Actual bias/aging/TCC needed for startup envelope. |

Manufacturer curve screening rejects a single input or output capacitor. Samsung official [C13585 model](https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=CL31A106KBHNNN) shows−78.34% DC capacitance at17 V. Initial−10% tolerance times independent typical worstTCC over−40..85°C gives1.730 µF; three parallel units screen5.189 µF. Samsung official [C98190 model](https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=CL21A226MOQNNN) shows−62.62% at5 V; initial−20% times typicalTCC gives5.773 µF, two units11.545 µF. This is typical screening, not a combined-bias/temperature/aging guarantee. Require actual effectiveCin≥3 µF (target4.5 µF) and localCout≥6 µF (calculation target10 µF), with correct aged capacitance. X5R componenttemperature must stay≤85°C; IC125°C junction rating does not extend capacitorrating. Keep all localcaps close and consider the larger input array in hotplug energy/damping. ManufacturerC307331100 nF model screens41.94 nF at17 V/initial−10%/typicalTCC: its50 V rating is sufficient, but nominal100 nF is not actual100 nF at17 V. Review HF impedance/decoupling acceptance separately. Curves and screening are in buck-capacitor-screen.json.

The Bourns body is4.45±0.25×4.06±0.25 mm, height1.8±0.2 mm. Manufacturer land recommendation has total width5.2 mm, inner pad gap2.2 mm and pad height2.4 mm: use two1.5×2.4 mm pads centered atx±1.85 mm. No SRP4020TA exact footprint found in the offline KiCad10 library; generic1210 is unsuitable. Minimum terminal geometry0.46×1.8 mm lies fully over the recommended pads in the centered, worst-width corner, guaranteed overlap≥0.828 mm² per terminal. Front placement must reserve≥2.0 mm plus solder/assembly margin. Final courtyard, neighbor clearance and stencil need reviewed CAD geometry.

TI RGX0011A bottom-view/top-land numbering is unusual: in the top-land drawing, top-row pads11,10,9,8 have x=−0.75,−0.25,+0.25,+0.75 mm at y=−1.4 mm; bottom-row4,5,6,7 use the same x positions at y=+1.4 mm. Power pads1,2,3 are centeredx=0 at y=−0.5,0,+0.5 mm. TI land example specifies0.25×0.6 mm for8 signal pads and2.4×0.25 mm for3 power lands, rounded corners R0.05. TI explicitly uses solder-mask-defined power pads and NSMD signal pads; follow the original drawing rather than applying a common mask expansion globally. Appended stencil drawing uses80% printed area on power pads, nine0.66×0.25 mm apertures and0.125 mm stencil. Copper/mask interpretation, thermal return and fabrication acceptance require independent footprint review before adoption. Reference images tps62135-lands.png and tps62135-land.png preserve the exact drawings.

## Accuracy and operating limits

TI specifies0.7 V feedback and±1% in forced PWM, across−40..125°C, **provided converter VIN≥VOUT+1 V**. The61.4 kΩ/10 kΩ divider yields4.998 V nominal. Exhaustively enumerating initial resistance tolerances, independent specified TCR signs at−40/25/85/125°C, reference±1% and feedback leakage±70 nA produces4.91247..5.08444 V, or−1.751/+1.689% against5 V. This fits the LD1117's±2% static target under the TI headroom condition. Resistor solder/lifetime drift, parasitic ground/trace voltage and measured noise/transients remain outside that initial calculation. No guaranteed lifetime±2% claim is made. The two series top resistors must be tightly placed; intermediate node not exposed or routed near SW.

The advertised6 V carrier boundary, after diode/bead loss, does not meetVIN≥6 V at U7 and therefore lacks TI's±1% feedback guarantee. At100% duty, full-load droop is approximately I×(high-side RDSon + inductorDCR), plus all upstream loss. At838 mA using maximum0.180+0.027 Ω, this is about174 mV, excluding diode/ferrite/trace drop. The buck gives better low-input behavior than an LDO but does not prove precise5 V at every6 V input condition. Reference-module acceptance, source impedance and complete workload must resolve this boundary explicitly.

4 A silicon capacity must not change the official external800 mA absolute limit or imply800 mA additional load independent of internal consumption. Known internal5 V quiescent maximum under48 kHz characterization is36 mA codec plus2.04 mA op-amps;838.04 mA total is only an illustrative800 mA external case. Op-amp load current, other codec sample rates, simultaneous digital draw, cable/source current and enclosure temperature require the final budget. No original absolute current is promoted to guaranteed sustained export.

## LC, startup and fault checks

TI p4 allows effective inductance0.6..2.9 µH, local effective output capacitance6..200 µF and input≥3 µF. P13 Table2 recommends1 µH/22 µF and also2.2 µH with10/22/47/100/200 µF; distributed≥400 µF needs at least10 mΩ associated ESR per application section. The previous3.3 µH±20% candidate is outside this device's effectiveL maximum and is not reused.

At1 µH nominal/44 µF nominal total, LC corner is23.994 kHz. At17 V input,5 V output, L0.8 µH,2.5 MHz typical, ideal ripple is1.765 A peak-to-peak, peak1.720 A at838 mA, and negative peak0.882 A at no load. A2 MHz sensitivity gives2.206 A ripple,1.941 A loaded peak and1.103 A no-load negative peak;2 MHz is an assumed sensitivity, not a datasheet guaranteed minimum. With a qualification target ofCeff10 µF total, capacitive ripple is8.82 mV typical/13.79 mV sensitivity, plus ESR×ripple and PCB parasitics. The TI datasheet's alternate maximum-ripple estimateVINmax×100 ns/Lmin is2.125 A, giving1.901 A peak and20% saturation margin2.281 A. Bourns normal current capacity is comfortably above this at25°C.

TPS62136 at1 MHz and2.2 µH−20% has roughly2.005 A ripple/1.003 A no-load negative peak. Its normal negative current is below the1.5 A typical limit, but that is not a guaranteed minimum limit and frequency has no guaranteed minimum. TPS62136 with1 µH is a poor equivalent: no-load negative peak≈2.206 A exceeds the listed typical negative limit. These calculations favor TPS62135 for the first trial and do not replace light-load regulation tests.

TPS62135's static positive current limit is4.8..6.5 A; dynamic peak adds(VIN−VOUT)/L×typically50 ns propagation delay (p11). For the preferred1 µH Bourns at simultaneous−20% initialL and20% saturation loss, effectiveL0.64 µH; short-circuit sensitivity at17 V gives7.828 A using6.5 A static maximum. Bourns Isat8.5 A is characterized at25°C; propagation delay is typical, and thermal saturation drift is not bounded. This is substantially more credible than the small3.5 A CJIANG part for faults, but not a guaranteed dynamic maximum. Validate hiccup/short/startup and actual component/trace/diode temperatures across accepted ambient. Do not qualify the board for4 A external load.

C2104.7 nF gives nominal ramp1.316 ms usingTI0.7×CSS/ISS; ±10% initialC and2.3..2.7 µA source gives1.097..1.573 ms, plus200 µs typical/300 µs maximum startup delay. X7R temperature±15%, actual DC bias and aging expand this envelope. An illustrative164 µF total capacitance (64 µF internal plus100 µF external) charges at748 mA at the initial fast corner; including−15% X7R TCC gives fastest ramp0.932 ms and880 mA charging; together with838 mA constant load and theTI2.125 A ripple estimate, peak≈2.781 A remains below4.8 A static minimum. This ignores extra externalcap tolerance and requires a bounded actual totalC. This closes the earlier1 A converter's poor ramp headroom only for that stated capacitance/load illustration. Bound external capacitance/inrush and test reference-compatible monotonic start, reset, codec/CV behavior and rapid cycling; slower startup cannot be silently accepted as interface-compatible.

## Noise, thermal, protection and USB contract

MODE high prevents PFM bursts without firmware control. Switching ripple/EMI remain; analog filter and ground layout, FFT/noise floor, audio scale/headroom and CV gain/clipping require hardware comparison. Do not hide these changes by using a wide codec voltage range as acceptance. Feedforward15 pF is internal; no extra external CFF proposed until loop/transient data support it. For the selected61.4 kΩ/10 kΩ divider its ideal zero is172.8 kHz and pole1.234 MHz. Large/distributed cap stability needs actual ESR and load-response measurements.

At illustrative efficiency90%,5 V×838 mA output implies0.466 W buck loss;85% gives0.739 W, versus5.6..10 W LDO heat. TI θJA38.4°C/W is a reference-board metric, giving17.9/28.4°C rise in those illustrative cases. Forced PWM efficiency at light load, actual board copper/vias/enclosure and nearby U6/diodes determine real temperature; no guaranteed efficiency or thermal export claim follows. Recommended maximum junction125°C remains the limit.

Normal U7 input must stay≤17 V and transient stress below20 V absolute. A17 V carrier at light load leaves essentially no operating margin; a generic17 V TVS often clamps above20 V and cannot be credited without itsI/V curve. Upstream ferrite+low-ESR input ceramics can resonate on hotplug, so damping, source impedance, cable energy and surge need a concrete design/test. Existing40 V1 A SMA diodes also require whole-module current/thermal/inrush qualification.

USB-only remains ordinary partial-power/DFU behavior: a buck cannot boost diode-droppedUSB to5 V, and negative analog rail is absent. EN follows protectedVIN so analog may be partly powered; completely disabling analog onUSB is a separate sequencing change. Forced PWM permits negative inductor current; full power-removal and external+5 V backdrive must be tested for energy pushed into the sharedOR node and MCU regulator. TPS62135 adds100 Ω active discharge onVOS after at least one enabled cycle, active inshutdown/UVLO/thermal withVIN typically≥2 V; this can consume50 mA from an externally driven5 V rail. Do not assume that output discharge is compatible with all carrier supply modes. TPS621351 avoids discharge but changes short-circuit behavior. Choose deliberately after interface review; no firmware workaround proposed.

## Conditions before CAD and production

Freeze accepted input/load/capacitance/temperature/noise and supply-sequencing requirements; qualify MLCC effective curves and inductor faults; create independently reviewed exactRGX/SRP footprints; allocate exact parts for assembly. Then implement an isolated CAD candidate, place the local loops, run ERC/nativeDRC/refill/connectivity/cleanliness, and measure load/hotplug/USB/backdrive/startup/FFT/CV/thermal corners. This proposal is sufficiently concrete to review and is not a production authorization.

Machine-readable evidence, exact order codes, all1024 precision corners and numeric calculations: forced-pwm-five-volt-calculations.json. Prior power baseline and manufacturing constraints remain in review.md and jlc-four-layer-constraints.json.
