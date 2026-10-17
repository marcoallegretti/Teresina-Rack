# Digital-core bounded acceptance

## Decision

**U3 IS42S32160F-6BLI is not qualified for production with the pinned, unchanged official libDaisy initialization.** The blocker is a documented automatic-refresh interval exceeding the memory manufacturer's specification. This is a firmware/hardware compatibility conflict; a layout improvement or passing short prototype memory test cannot waive it. No firmware or CAD changes were made in this pass. The user requested evidence-backed progress, which authorizes continued analysis and reversible development but does not authorize changing firmware or accepting undocumented retention behavior.

U1 and U2 are qualified only for package, pin mapping and nominal firmware configuration consistency; hardware execution, timing margins, power integrity and environmental reliability are still untested. This note does not approve the board for manufacture.

## Final adversarial refresh challenge

1. **Actual selected kernel source:** libDaisy commit `08087203debc646d3710ec8caa35bac6cf20ab5e`, `src/sys/system.cpp:478–497`, actively sets PLL2 M=1, N=12, FRACN=4096, R=1 and selects `RCC_FMCCLKSOURCE_PLL2`. These assignments are outside the preceding commented-out older configuration. The library pins HAL commit `404a70d4c19c124636c78801ff7c0dbc87bc4256`. Its RCC extension selects PLL2's **R** output for FMC, enables the fractional latch and applies the divider values. RM0433 Rev9 p412 defines FMCSEL=10 as `pll2_r_ck`. The configured kernel is therefore `(16 MHz / 1) × (12 + 4096/8192) / 1 = 200 MHz`, independently of CPU 400/480 MHz and AHB division. It is not PLL2 P or Q and not an assumed 100/200 MHz AHB clock. Clock frequency is inferred from verified firmware configuration; it has not been measured on a prototype.
2. **SDCLK divider:** libDaisy's `FMC_SDRAM_CLOCK_PERIOD_2` equals `0x800` in the pinned HAL header. It encodes SDCR SDCLK bits[11:10]=10, which RM0433 p873 explicitly defines as **two FMC-kernel periods**. Thus SDCLK=100 MHz.
3. **HAL COUNT encoding:** stock `HAL_SDRAM_ProgramRefreshRate(...,0x81A-20)` supplies 2054. The pinned `FMC_SDRAM_ProgramRefreshRate` writes `RefreshRate << FMC_SDRTR_COUNT_Pos` directly, without subtracting one or inserting another divider. RM0433 pp877–878 says the decrementing counter uses **SDCLK**, and specifies COUNT+1 clocks between refresh requests. One request therefore occurs every 20.55 µs; the lower-bound full 8192-row sweep is 168.3456 ms. Queued access delays can lengthen it, not shorten it. The RM's printed multiplication by frequency has a units error; the explicit SDCLK decrementer and worked7.81 µs×60 MHz cycle example resolve the intended interpretation.
4. **No hidden four-refresh multiplier:** startup manually issues four auto-refresh commands, then programs the mode register with `AutoRefreshNumber=1`. RM0433 p876 limits NRFS to commands issued when SDCMR MODE=011; periodic automatic refresh is described separately on p869. The final mode-register command also restores NRFS=0, meaning one command. Startup's four refreshes do not multiply periodic refresh frequency.
5. **Array geometry and temperature:** ISSI RevB p1 identifies four banks,13 row bits,9 column bits and32-bit width. Page16 gives an8192-refresh/64 ms limit for commercial operation through70 °C and industrial operation through85 °C. The selected industrial6BLI order is documented on p59. There is no guaranteed relaxed168 ms normal refresh interval at room temperature in the cited datasheet. Temperature-compensated self-refresh does not govern ordinary running-mode auto-refresh. The one-command refresh requirement already covers the internal banks; the sweep calculation neither divides nor multiplies by four.
6. **Legacy/current bootloader scope:** the previously retained official v5.0.0 bootloader submodule 38d23a2... and current bootloader submodule 24be4afe... both retain COUNT 2054 at the same100 MHz SDCLK. Current PatchSM code preserves SDRAM initialized by pre-v6 bootloaders when running external-memory applications. Consequently a private change only to new applications would not resolve old binary compatibility. This pass does not claim every historical bootloader revision has been audited.

The calculation is reproduced by `check-core-calc.py` / `core-calc.txt`; native pin/geometry checks remain valid. Pinned HAL downloads are `pinned-stm32h7xx_hal_rcc_ex.c/.h` and `pinned-stm32h7xx_ll_fmc.c/.h`. URLs use the exact HAL commit, e.g. https://raw.githubusercontent.com/STMicroelectronics/stm32h7xx_hal_driver/404a70d4c19c124636c78801ff7c0dbc87bc4256/Src/stm32h7xx_hal_rcc_ex.c . All downloads retained TLS verification.

## Bounded alternative search

| Manufacturer part examined | Voltage / geometry / package | Published normal-refresh requirement | Qualification for unchanged COUNT 2054 at100 MHz |
|---|---|---|---|
| ISSI IS42S32160F-6BLI |3.3 V,13/9/32,four banks,90-ball8×13 mm |8192/64 ms through85 °C,pp1,4,16,59 |**Not qualified:**168.3456 ms exceeds64 ms |
| Alliance AS4C16M32MSA-6BIN |1.7–1.95 V,16M×32,four banks,90-ball |8192/64 ms,pp1,14–15 |**Not qualified:**wrong rail voltage and refresh interval |
| Alliance AS4C16M32SB-6BIN |3.3 V,13/9/32,four banks,90-ball,industrial−40..85 °C |8192/64 ms,Rev1.0 Feb2023 pp2,17 |**Not qualified:**same retention conflict despite matching geometry and rail |
| Alliance AS4C16M32SC-7TIN |3.3 V,16M×32,four banks,86-pinTSOP-II |8192/64 ms through85 °C,Rev1.0 Sep2018 p2 |**Not qualified:**retention conflict; additionally requires a different physical package |

Manufacturer sources downloaded from actual product-page links:

- SB: https://www.alliancememory.com/wp-content/uploads/AllianceMemory_512Mb_AS4C16M32SB-6BxN_Datasheet_16Feb2023_ver1.0.pdf
- SC: https://www.alliancememory.com/wp-content/uploads/AllianceMemory_512M-SDRAM_Cdie_AS4C16M32SC-AS4C32M16SC-AS4C64M8SC-7TIN_Sept2018_rev1.0.pdf
- MSA: https://www.alliancememory.com/wp-content/uploads/20171206_AllianceMemory_512M_LPSDRAM_AS4C16M32MSA-6BINTR_rev1.0_Dec2017.pdf
- ISSI: https://datasheet.lcsc.com/datasheet/pdf/69b92f7b55b6d6826cdb34801f64d6a4.pdf?productCode=C1348852

**No supported alternative was qualified in this bounded search.** This does not establish that no suitable memory exists. Catalog existence, compatible density and distributor stock would be insufficient: production acceptance needs an authoritative retention guarantee covering at least 168.35 ms plus scheduling margin at the required temperature, matching geometry, supply and bus behavior, followed by complete electrical/package/timing review. New sourcing evidence can reopen that qualification.

Practical next prerequisite: establish a manufacturer-supported memory/stock-firmware combination, obtain Electro-Smith/ST clarification of the published refresh settings, or use a future official stock firmware correction that satisfies the user's compatibility requirement. Until then, keep RAM choice provisional and explicitly block a 100%-ready production release. There is no authority to patch firmware privately or declare unspecified retention acceptable. Validated schematic/BOM repairs and provisional placement/fanout studies can continue while this requirement remains open.

## VCAP correction

The prior sentence claiming C13/C14 were nominally correct was wrong. Native XML gives both displayed values as 2.2 µF but orders **CL10A226MQ8NRNC / C59461**. The exact distributor product description is **22 µF ±20%,6.3 V,X5R,0603**; the Samsung catalog lists the CL10A226MQ8NRN base on **PDF page 20** as 22 µF. ST DS12556 Rev8 pp96,201 specifies 2.2 µF with±20% variation and ESR<100 mΩ. A nominal 22 µF part is a tenfold mismatch; no capacitance-bias curve or vendor stability exception has been established that makes it an acceptable substitute. Placement remains independently wrong: C13/C14 are 12–32 mm from the VCAP balls.

Both the BOM mapping and placement must be corrected. Choose an exact 2.2 µF part, verify its effective capacitance, tolerance and ESR at the actual VCAP voltage, and place one beside each ball. Do not reuse the wrong MPN by changing only its displayed value. `core-review.md` and `findings.json` have been corrected accordingly. Source: https://www.lcsc.com/product-detail/C59461.html and manufacturer catalog https://datasheet.lcsc.com/datasheet/pdf/02336ea48ea44ca18c72517dd3cb7b47.pdf?productCode=C59461 (retained by power review).
