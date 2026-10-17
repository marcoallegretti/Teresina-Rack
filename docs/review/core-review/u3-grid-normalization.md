# U3 graphic-only connection-grid normalization

Read-only proposal for the organized candidate. RAM remains an unqualified IS42S32160F-6BLI candidate; this change does not select memory, modify firmware or approve refresh behavior. `u3-grid-plan.json` provides all 90 exact pin moves,85 wire/global-label moves and5 NC-marker moves with UUIDs. `plan-u3-grid.py` derives the proposal from the actual files using decimal arithmetic and rejects pin collisions or intersections with unrelated wires.

## Diagnosis

Cached U3 in `memory-flash.kicad_sch` and the external `TeresinaRack.kicad_sym` have identical complete pin definitions. All 90 connection Y coordinates are off the 1.27 mm grid. X coordinates±25.4 mm and pin length 2.54 mm already follow it. The instance anchor(48.26,77.47), rotation 0°, also follows it.

The 86 ERC off-grid records are attributable to U3:85 horizontal wire stubs at its 85 connected pins, plus one additional DQ26/A1 pin record. Its five individual NC pins also have off-grid coordinates but no wire records. Although ERC lists these records under the root path, their wire UUIDs match the memory sheet; they must not be misattributed to unrelated root-sheet geometry.

## Exact coordinate change

For each pin, retain its number, name, electrical type, shape, direction, length, visibility, order and unit. Snap only its local Y to the nearest 1.27 mm multiple with decimal rounding. There are no halfway ambiguities.

| Existing group | Pins | Local Y shift | World Y shift at rotation 0° |
|---|---:|---:|---:|
| CLK/CKE/commands/address/bank/DQM |25 |+0.42 mm |−0.42 mm |
| DQ0–DQ31 |32 |+0.42 mm |−0.42 mm |
| VSS/VSSQ |14 |−0.35 mm |+0.35 mm |
| NC |5 |+0.09 mm |−0.09 mm |
| VDD/VDDQ |14 |−0.13 mm |+0.13 mm |

The resulting top Y is 58.42 mm on both sides; left bottom is−52.07 mm and right bottom−57.15 mm. All 90 endpoint positions remain distinct. Minimum same-side spacing remains 2.54 mm; group gaps become 2.54 or 3.81 mm. Preserve each of the 28 supply/ground balls individually even when their nets are shared: do not stack, hide or collapse them into one symbol pin. Preserve all five NC numbers individually with their own no-connect markers.

Optional body adjustment: rectangle start(−22.86,62) and end(22.86,−62) may become(−22.86,62.23)/(22.86,−62.23). This is purely graphic, with adequate clearance around the shifted pins. Neither the body outline nor its text needs to affect connectivity.

## Required accompanying endpoint moves

Changing the symbol alone would disconnect the schematic. For each of the85 affected horizontal stubs, translate **both wire endpoints and its global label** by the same world Y delta. Translate associated label property coordinates by that delta; preserve wire/label UUIDs, label text, shape/direction and formatting. The label is at the far end of the 3.81 mm stub, not at the pin. Move all five NC markers to their new pin endpoints and preserve their UUIDs.

At the current rotation 0°, KiCad schematic world Y is `instanceY−localY`; the sign in the table is therefore intentional. Do not apply local shifts directly to world coordinates. The JSON records explicit old/new coordinates rather than relying on this convention implicitly. Its proposed endpoints and entire horizontal segments do not collide with unrelated nodes or wire segments in the inspected sheet. Recompute if the source hash changes; do not apply UUID-bound moves to a different drawing.

## Identity correction without selecting a part

The inherited symbol identity is misleading for this use. The external `AS4C16M32MSA` definition names an Alliance 1.8 V mobile part and its manufacturer PDF; the cached definition overrides this with ISSI 3.3 V data and unsupported “drop-in” wording. The instantiated MPN is already the distinct, unqualified ISSI candidate. Shared pin-map consistency is not electrical drop-in compatibility, and graphic normalization cannot make it so.

Recommended documentary normalization:

1. Add a neutral symbol **`TeresinaRack:SDRAM_16Mx32_FBGA90`** and point U3 to it. Rename the two child graphic units consistently to `SDRAM_16Mx32_FBGA90_0_1` and `_1_1`. Synchronize its cached and external definitions exactly.
2. Use a neutral default Value and description, for example: “16M x32 SDRAM,90-ball FBGA. Pin-map reference: ISSI IS42/45S32160F. Supply,timing and compatibility require exact MPN qualification.” The ISSI PDF may remain as a clearly identified pin-map reference; it must not imply that every 90-ball device is interchangeable.
3. Keep the instantiated **U3 Value,MPN,LCSC,Datasheet and physical footprint unchanged**. Replace only unsupported compatibility prose in its Description with an accurate candidate note, for example: “IS42S32160F-6BLI candidate,512Mb(16M x32),3.3 V SDRAM,90-ball FBGA8×13 mm; clock/refresh compatibility not qualified.”
4. Retain any old Alliance-specific library definition only as an unused truthful Alliance definition, or remove it from the cache if unused. Do not silently relabel the actual Alliance 1.8 V part as a 3.3 V ISSI device. Do not replace the actual component MPN with the neutral symbol name.

This symbol alias and prose change is documentary only; physical ball IDs, names, types, nets, package and component selection remain untouched. If this metadata change is outside a deliberately narrower implementation scope, keep it separate and clearly disclose the legacy identity problem; do not retain unsupported drop-in claims in the normalized result.

## Acceptance constraints

- Check the source SHA256 before applying the plan; update all cached copies and the external symbol together.
- Preserve all 90 physical pin identities and all individual supply/NC definitions. Reject any coalescence, changed direction/type, swapped DQ bit, changed unit assignment or undocumented pin hiding.
- Export a fresh complete-project native XML. Every U3 pin number/name/net must agree with the pre-normalization source; all other component-pin connections must remain unchanged. A neutral library ID/description change is the only allowed documentary identity delta.
- Run native ERC. The 86 U3 off-grid records should disappear with no newly introduced records. Resolve the U3 cache/library mismatch through identical neutral definitions; do not disable either check. Other inherited errors are unrelated and must remain visible.
- Review the rendered memory sheet for label legibility, groups, supply/NC visibility and wire stubs. Preserve meaningful group gaps.
- Confirm no PCB footprint, copper, manufacturing rule, RAM MPN or firmware changed. This pass cannot close SDRAM timing/refresh qualification.

No CAD files were edited during this review. The JSON move table and helper are stored outside the repository for implementation and subsequent independent verification.
