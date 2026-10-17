# Unchanged-firmware RAM replacement search

Reviewed 13 October 2026. **No demonstrably compatible replacement was found.** The expanded public-source search records 14 part/family screens and 11 newly retrieved, valid manufacturer-branded PDFs, plus retained earlier datasheets. This is a bounded search, not proof that no suitable device exists. No CAD, firmware or RAM ordering selection changed.

The unresolved concrete lead is **Etron EM63B325BK**. Its manufacturer catalogue lists 512 Mb, 16M×32, 3.3 V, industrial grade and a 90-ball 8×13 mm package. Its datasheet column links to sales support rather than a downloadable specification. Catalogue dimensions cannot establish its pinout, refresh guarantee, exact ordering suffix, availability or timing. It remains unqualified; no manufacturer contact was sent.

## Acceptance criterion

The reference is pinned [libDaisy v9.0.0](https://github.com/electro-smith/libDaisy/tree/08087203debc646d3710ec8caa35bac6cf20ab5e), with the unchanged SDRAM initialization examined in the [earlier core review](review/core-review/bounded-acceptance.md). Nominal SDCLK is 100 MHz and the programmed refresh COUNT is 2054. Literal COUNT+1 accounting gives one request every **20.55 µs**, before controller scheduling delays.

For a device requiring `N` AUTO REFRESH commands within `T` milliseconds, compare the published `T/N` allowance with the stock request interval. Do not infer the command count solely from row-address bits or divide it by the number of banks. The acceptance must include oscillator and scheduling margins, the required temperature range, 64 MiB capacity, 3.3 V operation, compatible geometry and the existing 32-bit FMC protocol. Physical package/pinout, timing and sourcing review follow only if retention passes.

| Published command requirement | Maximum average interval | Stock time for that many requests, without added delays | Retention result |
|---|---:|---:|---|
| 8192 / 64 ms | 7.8125 µs | 168.3456 ms | Fails |
| 4096 / 64 ms | 15.625 µs | 84.1728 ms | Fails |

These are nominal source-derived calculations, not measured clocks. A device's higher maximum clock rating does not change the clock chosen by unchanged firmware. More frequent normal accesses cannot guarantee that all retained rows are refreshed under every workload.

## Documented candidates

| Device or family | Published normal refresh | Other relevant facts | Disposition |
|---|---|---|---|
| ISSI IS42S32160F-6BLI | 8192 / 64 ms through 85 °C | Selected 3.3 V, 16M×32, 90-ball candidate | Fails unchanged refresh |
| ISSI IS42S32160D family | 8192 / 64 ms commercial/industrial | Another 3.3 V, 16M×32, 90-ball family | Fails unchanged refresh |
| Alliance AS4C16M32SB-6BIN | 8192 / 64 ms | 3.3 V, 16M×32, 90-ball | Fails unchanged refresh |
| Alliance AS4C16M32MSA-6BIN | 8192 / 64 ms | 1.8 V part from the old SDK comment | Fails refresh and selected rail |
| Micron MT48H16M32LF/LG | 8192 / 64 ms; automotive requires 32 ms | 1.7–1.95 V; LF has 13-row/9-column geometry, LG differs | Fails refresh and selected rail |
| Micron MT48LC32M16A2 | 8192 / 64 ms | 3.3 V, x16, TSOP54 | Fails refresh; different single-device interface |
| Micron MT48LC4M32B2 | 4096 / 64 ms | 3.3 V, x32, optional 90-ball; only 16 MiB and different geometry | Fails refresh and capacity/geometry |
| Nanya NT5SV16M16CS | 8192 / 64 ms | 3.3 V, 256 Mb, x16, TSOP54 | Fails refresh; different single-device interface |
| Etron EM63A325BK industrial family | 4096 / 64 ms | 3.3 V, x32, 90-ball; only 32 MiB | Fails refresh and capacity |
| Etron EM638325BK industrial family | 4096 / 64 ms | 3.3 V, x32, 90-ball; only 8 MiB | Fails refresh and capacity |
| Etron EM63B165BM industrial family | 8192 / 64 ms | 3.3 V, 512 Mb, x16, stacked-die ordering, 54-ball | Fails refresh; different single-device interface |
| ESMT M12L5121632A-6BG2T | 8192 / 64 ms | 3.3 V, 512 Mb, x16, 54-ball | Fails refresh; different single-device interface |
| AP Memory APS512XXN-OBR-BG | Self-managed refresh | 1.8 V, octal DDR x8/x16, 24-ball | Different voltage/protocol; cannot use unchanged FMC SDRAM driver |
| Etron EM63B325BK catalogue lead | Not established | Catalogue matches capacity/width/nominal rail/package size | Unresolved; no retention or complete compatibility proof |

Pairing x16 devices does not fix their refresh requirement: each device must receive its specified command rate. Smaller x32 devices do not preserve the 64 MiB contract. Etron EM638325 is an instructive exception to simplistic row counting: its diagram has 2048-row banks, but its normal-refresh section explicitly requires **4096 commands per 64 ms**. The published command requirement governs this screening.

The Winbond DRAM selection guide retrieved in this search lists 16–256 Mb for its specialty SDRAM range and describes PSRAM/HyperRAM separately; that guide does not establish a qualifying 512 Mb SDR replacement or exclude future/custom products. Samsung mobile-SDRAM pages and ESMT/Nanya discovery leads were screened, but search snippets and incomplete documents were not used to approve devices.

Temperature-compensated self-refresh and partial-array self-refresh do not relax normal running-mode AUTO REFRESH requirements. Academic demonstrations of longer retention or schemes that discard weak rows are not manufacturer guarantees and require different control/software assumptions. The extended-retention searches did not establish a qualifying public specification.

## Sources and reproducibility

Exact URLs, SHA256 hashes, PDF page references, command-rate calculations and dispositions are in [memory-replacement-search.json](review/memory-replacement-search.json). PDFs, extracted text, catalogue captures, discovery results and scripts are retained under `/workspace/cloud-setup/redesign/memory-search`. Earlier valid retained sources are under `core-review`; the ISSI F source is `C1348852.pdf`, not the failed primary-host HTML capture named `sdram.pdf`.

Representative manufacturer-branded sources:

- [ISSI D-family datasheet, PDF pp1/19](https://media.digikey.com/pdf/Data%20Sheets/ISSI%20PDFs/IS42_45R_S_86400D_16320D_32160D.pdf).
- [Alliance 512 Mb ×32 datasheet, pp2/17](https://www.alliancememory.com/wp-content/uploads/AllianceMemory_512Mb_AS4C16M32SB-6BxN_Datasheet_16Feb2023_ver1.0.pdf).
- [Micron 512 Mb mobile SDRAM, pp1/20/21](https://media.digikey.com/PDF/Data%20Sheets/Micron%20Technology%20Inc%20PDFs/MT48H32M16LF,16M32LF,LG.pdf).
- [Micron 512 Mb SDRAM, pp1/18/27](https://www.mouser.com/datasheet/2/12/512M-SDRAM-MT48LC32M16A2P-20140714-1288428.pdf).
- [Etron industrial SDR catalogue](https://etron.com/industrial-dram-pl/sdram/) and [EM63A325 datasheet, pp1/17](https://etron.com/wp-content/uploads/2024/09/EM63A325TSBK-Industrial_Rev-2.1.pdf).
- [Etron EM638325 datasheet, pp1/16](https://etron.com/wp-content/uploads/2022/04/EM638325-Industrial_Rev-3.2.pdf).
- [ESMT 512 Mb x16 datasheet, pp1/12](<https://www.eonssi.com/upload/pdf/ESMT/datasheets/M12L5121632A(2T).pdf>).
- [AP Memory 512 Mb octal PSRAM, pp1/3/7/10](https://www.mouser.com/datasheet/2/1127/APMemoryTechnology_PSRAM_OPI_Xccela_512Mb-2949655.pdf).

TLS verification was retained. Each accepted PDF had a valid PDF header and successful text extraction. ISSI's primary-host HTML anti-bot response, unrelated Bing results and Google redirect pages were excluded as specification evidence. No physical pin audit, memory test, supplier stock confirmation or manufacturing approval is claimed by this retention screen.

## Consequence for Teresina

No RAM substitution can presently be recommended as a demonstrated fix for unchanged stock firmware. Obtain an exact Etron specification or other new manufacturer-supported evidence before accepting that path. The [Teresina firmware prototype](firmware-policy.md) remains the implemented alternative; an upstream official correction remains another possibility. This search does not freeze the memory choice or qualify either firmware path for production.
