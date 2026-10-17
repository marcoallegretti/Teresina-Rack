# Core candidate independent acceptance

Reviewed `/workspace/cloud-setup/redesign/core-candidate` against its electrical-candidate parent and the original digital-core baseline. The parent schematic SHA256 agrees with `scope.json`.

**Accepted for schematic integration within the stated package/BOM scope.** This does not accept the PCB layout or release the board for production.

- All 13 planned Value/MPN/LCSC/Footprint/symbol fields pass the independent native-XML checker.
- C13/C14 order CL21B225KAFNNNE/C19110, retain 2.2 µF labels and now specify 0805. Both pin1 terminals and U1.F13/M10 remain on one VCAP net; both pin2 terminals connect GND. This agrees with ST AN4938 p12.
- Y1 retains 16 MHz, X322516MLB4SI/C13738, with `Device:Crystal_GND24` and the verified standard3225 footprint. Native XML shows1→OSC_IN,3→OSC_OUT,2/4→GND. The old signal-pin2 UUID is preserved on new pin3. Embedded pin names, numbers, positions and hidden pin4 agree with the installed KiCad 10 library.
- All 299 U1/U2/U3 pin functions and net assignments match the original digital-core baseline. Their identity, MPN, SKU, footprint and library IDs are unchanged.
- C37/C38 retain 18 pF, original MPN/SKU, footprint and nets; no exact-load claim or numeric retuning was introduced.
- The semantic raw-tree delta consists only of C13/C14 properties, Y1 properties/library reference/pin instances, the added Crystal_GND24 library symbol, and two GND labels at its stacked case-pin endpoint. Existing library symbols, component coordinates and property coordinates are unchanged. No wire or unrelated component changed.
- Native ERC has **zero added and zero removed records** versus the electrical parent, including record contents. The inherited 3 errors and 252 warnings remain; this is not a clean ERC result.

One minor schematic hygiene point: two identical GND labels occupy the same stacked pin2/4 endpoint. Native connectivity and ERC confirm no electrical defect. One label would be cleaner and would still ground both stacked terminals. No changes were made by this reviewer.

The physical PCB footprints and routing have not been synchronized or reviewed in this pass. Exact manufacturer load/drive limits for the retained YXC order, final oscillator loading, VCAP environmental/aging qualification, RAM refresh compatibility and remaining inherited errors remain open. The decoded ECS alternative and provisional 10 pF population were not adopted.

Evidence: `candidate-core-audit.json`, `core-raw-delta.json`, `core-candidate-erc-library-audit.json`, plus `review-core-candidate.py`. The report hashes identify the exact schematic/netlist reviewed. No CAD or firmware edits were performed.
