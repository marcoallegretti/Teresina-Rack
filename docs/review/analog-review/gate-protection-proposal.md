# Bounded gate protection and fault proposal

No CAD changes were made. This proposal preserves the published gate-output100Ω value, closed-loop transfer, firmware GPIO mapping and intended positive gate-input polarity.

## Negative input clamp candidate

Add one exact **JSCJ1N4148WS, LCSC C2128, SOD323** per transistor, with diode **anode at local emitterGND and cathode at GBASE_1/2**. Suggested referencesD6/D7; Device:D pins1K/2A. Keep all original Q1/Q2 pins and100kseries/1Mpulldown/10kcollector/1kMCUseries values. Exact product JSON and corresponding manufacturer PDF p1 identify1N4148WS and specifyVF≤0.715V at1mA/25°C, IR≤25nA at20V/25°C,CT≤2pF,100V reverse and150mA average forward. This is the actual sourced JSCJ part, not a generic family model. The exact linked PDF has no dimensioned package drawing; standardD_SOD323 and stripe/pad numbering remain a package-qualification prerequisite.

At−17V external source through minimum99kΩ input resistance, forward clamp current cannot exceed171.7µA. At25°C that is below the1mA forward-voltage test: ordinary monotonic diode behavior puts reverseB-E near/below0.715V rather than the existing−10.91V demand at−12V. Exact JSCJ Q1/Q2 have6V VEBO. This protects the static negative input without relying on3.3V power, but does not certify cold/fulltemperature, transient/ESD/surge or absent-GND faults. Place clamp directly between base/emitter with a local return away from sensitive analog references. Positive logic mapping remains unchanged; qualify diode leakage/capacitance effects on threshold/edge timing instead of claiming exactly zero perturbation.

## Existing100Ω resistor limit

R162/R163 are exactYAGEO RC0402FR-07100RL/C106232,100Ω±1%,62.5mW at≤70°C. Manufacturer derating falls to zero at155°C. Using101Ω worstpower, allowed continuousRMS current is24.876mA at70°C,22.575mA at85°C,19.079mA at105°C and14.779mA at125°C. Normal5V into10kΩ dissipates only about25µW in the series resistor.

MCP6004 p3 lists±23mA short-current **typical** at5.5V, not a guaranteed maximum.23mA dissipates53.429mW in101Ω, slightly above the85°C derated51.471mW allowance. Its±30mA pin **absolute** limit would correspond to90.9mW and is not a specified current-limiter bound. “OutputShortCircuitCurrentContinuous” concerns the opamp, not an external resistor's rating. A bare ideal5V/99Ω short would be50.5mA and252.5mW, so current limiting is essential to the calculation. Do not declare continuous-short safety from typical current alone.

A source-backed higher-power option is **UNI-ROYAL0805W8F1000T5E/C17408**,100Ω±1%,125mW0805. Exact distributor metadata and manufacturer family PDF confirmW8=1/8W,0805 dimensions and70…155°C derating. At85°C it permits102.94mW or31.93mA RMS at101Ω. It preserves100Ω nominal transfer but requires a larger PCB footprint and still needs a defensible maximum-current/thermal bound. It cannot establish opamp survival against an externally forced±12V output, which is outside the published0…5V gate-output rating.

Qualification before adopting either option: loaded/unloaded andshort-toGND/opposing0/5V tests atactualsupply andtemperature extremes; maximumcurrent/time history, resistorRMS/pulse power andopampthermal; startup/poweroff andcapacitivecables; package/courtyard/CPL checks; andnative comparison retainingpre100Ω feedback andPC14/PC13 mappings. Keeping0402 remains conditional on a bounded faultduration/temperature/current envelope;0805 improves resistorpower margin but alone doesnot certify the entirefault path.

Reproducible arithmetic is in `check_gate_fault_bounds.py`; part/source/net details are in `gate-protection-proposal.json`. No production-ready claim follows from this bounded proposal.
