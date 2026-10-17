# Independent review of analog remediation candidate

**Verdict:** The candidate matches the reviewed minimal schematic correction scope. It is suitable for applying as a schematic-only correction; it is not a synchronized PCB or production release.

Reviewed artifacts: `../candidate/analog-remediation.patch`, `../candidate/TeresinaRack.kicad_sch`, `../candidate/native-netlist.xml`, `../candidate/validation.json`, `../candidate/scope.json`, and native ERC, compared directly with the original repository schematic, baseline native XML and the independent remediation plan. No candidate, PCB or repository files were modified by this review.

## Independent verification

- The original schematic SHA256 matches `scope.json`. The candidate's full parsed S-expression tree equals a copy of the original with only the four approved label text changes and six approved resistor property changes. This checks all raw objects and preserved UUIDs/positions/library definitions, not just the patch excerpt. Scope metadata counts six edited objects; there are ten atomic changed text/property values.
- Native XML comparisons independently reproduce exactly four connection changes: U13.4, U14.4, C141.1 and C142.1 move from `/+5V` to `/+3V3A`. All850 native component-pin identities, pin-function/type attributes and all other component-pin nets are preserved. Component count remains209.
- R162/R163 each change only Value1K→100R, MPN0402WGF1001TCE→RC0402FR-07100RL and LCSCC11702→C106232. Footprint remains0402_1005Metric. Independently fetched exact product JSON and YAGEO manufacturer PDF confirm100Ω,±1%,62.5mW,0402, matching the reviewed existing R158/R159 part.
- U15.4 and C143.1 remain on `/+5V`. `scope.json` explicitly assigns C141→U13,C142→U14,C143→U15 and explicitly says no prior dedicated capacitor ownership is encoded. This is a valid stated new intent, not a claim of inferred original schematic grouping or adequate existing PCB placement.
- Every native ERC violation record is exactly unchanged from `/workspace/cloud-setup/results/erc.json`, not merely the counts. There remain3 errors and250 warnings. The candidate introduces no additional native ERC record and does not resolve the pre-existing errors.

Machine-readable independent results are in `candidate-independent-validation.json`.

## Supported improvement

With a correctly powered3.3V analog rail, U13/U14 now use the official reference's supply voltage. This removes the avoidable steady-state5V-powered output exposure at the directly connected MCU ADC pins during negative CV overrange; the nominal CV resistor/capacitor transfer remains unchanged. The correction aligns the rail topology with published Rev3. It does not establish fault immunity when rails/reference are absent, changing, noisy or outside specification.

The gate output isolation values and exact orderable parts now match the published100Ω interface. This corrects the previous1kΩ mismatch. It does not establish measured total output impedance, loaded voltage or dynamic behavior.

## Remaining caveats

1. The gate amplifiers still operate as saturated open-loop MCP6004 comparators against1.65V threshold, without hysteresis. The official circuit uses closed-loop120k/62k noninverting stages. Polarity and nominal digital low/high may agree, but loaded voltage, finite output swing, edge response, saturation recovery, capacitive-cable stability and short-circuit behavior remain unvalidated. Reducing the output resistor increases available fault/capacitive current; validate that behavior rather than infer equivalence from the new100Ω value alone.
2. The existing +3V3A feed's BOM still describes a ferrite while C175716/CR0805FR600P05Z is actually0.6Ω resistor. The planned small DC increment does not fix this sourcing/filter mismatch. The prior reviewed static proxy gives approximately2.16mA additional CV burden, about1.31mV incremental drop across0.606Ω, and an illustrative5.64mA combined MCU-analog/CV load, not a guaranteed temperature/dynamic maximum. Reference noise, ADC sampling currents, regulator headroom, power sequencing, backpowering and final ferrite DC/noise specifications remain board-level checks.
3. Dedicated bypass ownership is now documented, but the existing PCB still has inadequate/incorrect locations for that intent. Each assigned100nF needs a short supply-ground loop within the MCP datasheet2mm criterion. The PCB has not received these rail net changes or component property changes, so schematic/PCB parity is intentionally absent at this stage.
4. Negative gate input reverse B-E stress, exact Q1/Q2 sourcing, CV output fullscale headroom, -10V reference low-voltage headroom (published ±6…17V are absolute limits; typical operation is ±12V), displayed-versus-ordered C100/C103 coupling values, analog fault protection, real-device models and hardware measurements remain open from the preceding review.

No routing occurred, so no post-routing cleanliness assertion is appropriate. Applying this candidate must be followed by refreshed native netlist/ERC and independent schematic review; eventual PCB update/redesign requires full native DRC, connectivity, copper hygiene, manufacturing and firmware/hardware acceptance.
