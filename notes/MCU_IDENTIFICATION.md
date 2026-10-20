# MCU identification and missing memory

October 19, 2026. Public source recovery and offline static analysis. No target execution.

## Result

The recovered historical board photograph identifies its main chip's base marking as **D70F3506**. Renesas identifies UPD70F3506 as **V850E2/PJ4**, with the **V850E2M** core. This is a substantially narrower hardware hypothesis for 1061 than generic V850. Two independent capacities match the firmware: the update ends at the 512 KiB code-flash boundary, and a startup function clears exactly 40 KiB at `0xfedf6000..0xfee00000`.

This identifies the chip in the linked photograph. The photograph lacks a rack/module label, serial number, or diagnostic record tying it to the user's 5Q0909144R. Treat V850E2M/PJ4 70F3506 as strongly corroborated for the 1061 analysis, not verified silicon in the user's rack. Do not transfer this conclusion to 2Q1, 6C1, or PQ 1K0.

## Recovered photograph

The February 18, 2023 architecture lead in [the historical source anchors](../evidence/discord-history-2026-10-19/SOURCE_ANCHORS.tsv) points to [this public image page](https://ibb.co/3rDw18D). Its `og:image` resolves to [20210128-211638.jpg](https://i.ibb.co/JBfNnbf/20210128-211638.jpg). Both were retrieved without authentication and retained under [the evidence directory](../evidence/mcu-identification-2026-10-19/manifest.json).

- Image: 1908 by 4032 pixels, SHA-256 `60847d664322b9af5b10c4ca60f7878d6720d6a6398d3706e6fc6d4a6a4c929f`.
- Main chip: clearly legible `D70F3506`. The following custom/package text appears `ZGJAS`; the lot line appears `1616KP703`, followed by `JAPAN`. The suffix/lot transcription is not used as an exact Renesas ordering-code identification.
- No module label is visible. The filename is not a verified capture date, donor vehicle, or hardware revision.
- The original import contains no matching hardware JPEG. This is newly recovered external evidence, separate from the preserved archive.

## Primary manufacturer corroboration

1. [Renesas PG-FP5 supported MCU list](https://www.renesas.com/en/document/mat/list-mcus-supported-pg-fp5), R20UT0757EJ3600 Rev.36.00, April 20, 2022, page 30, maps UPD70F3506 to V850E2/PJ4. Saved PDF SHA-256 `c886f73e37dc02d2decea120224ab2e8c1595f29c0a8a5b02bdaff13e279ccd5`.
2. [Renesas UPD70F3506GJA2-GBG-AX product page](https://www.renesas.com/en/products/v850e2-px4/part-details/upd70f3506gja2-gbg-ax) lists V850E2M, 512 KB program memory, 32 KB data flash, 40 KB RAM, and 144 pins. The catalog suffix is not asserted to equal the photographed custom marking. Saved HTML SHA-256 `754db7d6c1ef7c95ff34ad0dd68cd53f78aa0622aa683e43cbbd099e553ee931`.
3. [Renesas CS+ device information](https://tool-support.renesas.com/autoupdate/support/jpn/cs_plus/DeviceInformation_V850_List.html) independently lists UPD70F3506 in the V850E2/PJ4 group. Saved HTML SHA-256 `df3eb42ab8473b7ea0baf6b7b4f0a0e3953b6620220bfb6f0387d68a58fda571`.

The manufacturer's Px4 description specifies two V850E2M CPUs operating in lockstep. That is a product feature, not an observed operating state of this rack.

The official hardware-manual URL linked by Renesas returned HTTP 403 in the initial pass. A subsequent authorized public search recovered the manufacturer-authored manual from a public Datasheet Archive mirror. The linked MHH Auto discussion still returned 403. Neither access control was bypassed.

## Recovered hardware manual and working memory profile

The [preserved manual](../evidence/mcu-identification-2026-10-19/renesas-px4-hardware-R01UH0098EJ0100.pdf) is **R01UH0098EJ0100 Rev.1.00, July 25, 2012**, SHA-256 `f2914aa669635072756bc530485d8bc690dede0e8398b51ee6adcc3b62b3bd22`. It contains 2271 PDF pages including front matter and back matter; its numbered main section contains 2239 pages. Its title, applicable-device list, and part table identify V850E2/Px4 including UPD70F3506. The mirror has rewrapped PDF metadata; an official byte-for-byte comparison is unavailable. This is manufacturer-authored documentation recovered through a public mirror, with that provenance limitation retained.

The [public listing](https://www.datasheetarchive.com/?q=V850E2) links to [the manual landing page](https://www.datasheetarchive.com/datasheet/d86e800893c8bfee?term=V850E2), whose public PDF viewer supplies [the PDF URL](https://datasheet.datasheetarchive.com/originals/library/Datasheets-ISS15/DSAIH000290215.pdf). Listing and landing HTML are preserved. No login or paywall was bypassed.

Printed page 24 (PDF page 44), Tables 1-3 and 1-4, explicitly specify these ranges for **70F3506 and 70F3507**:

| Region | Start | End, exclusive | Capacity |
| --- | --- | --- | --- |
| Code flash | `0x00000000` | `0x00080000` | 512 KiB |
| Data flash | `0x02000000` | `0x02008000` | 32 KiB |
| On-chip RAM | `0xfedf6000` | `0xfee00000` | 40 KiB |

This confirms both the RAM capacity **and its exact address** from the independently traced startup loop. The RAM range is no longer an uncorroborated firmware inference. It still does not uniquely distinguish 3506 from 3507; the photograph provides the 3506-specific observation.

Printed pages 144-147 (PDF pages 164-167), Table 3-2, provide named peripheral windows suitable for a static working profile. Selected ranges, all with exclusive ends:

| Module | Address interval |
| --- | --- |
| Port control | `[0xff400000,0xff410000)` |
| Clock/reset | `[0xff420000,0xff430000)` |
| Flash/ECC/access control | `[0xff430000,0xff440000)` |
| FCN0 / FCN1 CAN | `[0xff480000,0xff490000)` / `[0xff4a0000,0xff4b0000)` |
| FlexRay | `[0xff580000,0xff590000)` |
| OSTM0 / OSTM1 | `[0xff800000,0xff801000)` / `[0xff801000,0xff802000)` |
| TAUA0 / TAUA1 | `[0xff808000,0xff809000)` / `[0xff809000,0xff80a000)` |
| TSG20 / TSG21 | `[0xff82e000,0xff82f000)` / `[0xff82f000,0xff830000)` |
| TSU/PPU | `[0xffff5000,0xffff5400)` |
| Interrupt controller | `[0xffff6000,0xffff6460)` |
| ADCA0 short area | `[0xffffdc00,0xffffdd00)` |

These are module/protection windows, not proof that every byte is an implemented register. The manual contains additional mirrored/short peripheral windows; use its detailed register descriptions before assigning individual symbols. Printed page 1222 (PDF page 1242), Table 20-3, independently confirms FCN0 base `0xff480000` and FCN1 base `0xff4a0000`. These identify hardware controllers, not vehicle bus topology or the application's use of them.

Printed page 5 (PDF page 25) lists 8 KiB tuning RAM, and the block diagram on printed page 23 shows TRAM. A full-document text search found no address assignment for it. Do not label the observed firmware copy destination `0xfa800000` as tuning RAM from capacity alone. That region and control addresses near `0xfa0012c4` remain separate, unverified mapping leads.

The structured [manual memory map](../evidence/mcu-identification-2026-10-19/manual-memory-map.json) retains each range's exact printed/PDF page and source table. Figure 3-4 on printed page 156 (PDF page 176) was rendered and visually checked against the extracted ranges. Its caption uses 70F3507, so the part-specific Table 1-3/1-4 evidence above is the basis for applying the ranges to 70F3506.

## Firmware corroboration and limits

Input identity is H1 SHA-256 `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641`; the mapped H2+H1 image is `a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d`. Mapping provenance remains [static-map-1061](../evidence/static-map-1061-2026-10-19.json).

In [the startup export](../evidence/ghidra-tp-startup-2026-10-19.txt), function `0x13cd2` (H1 offset `0x4cd2`) loads `ep=0xfedf6000` and `r9=0xfedfffff`, stores four zero words per iteration, advances `ep` by 16, and loops at `0x13cec`. The destination interval is `[0xfedf6000,0xfee00000)`, exactly `0xa000` bytes or 40 KiB. This is static code evidence of intended initialization, not a RAM dump. `gp=0xfee01000` in application startup is a compiler addressing base; it must not be used as proof that physical RAM begins or exists there.

The supplied mapped image covers `[0x2000,0x80000)`. Its endpoint is consistent with the 512 KiB catalog program-memory size. Compatibility of these two capacities, plus the photo, strengthens the 70F3506 hypothesis but does not uniquely identify a die or prove that every 1061-compatible hardware revision uses it.

The default Ghidra language explicitly covers E1, E2, and E2M. Successful decoding of common V850 instructions alone cannot distinguish those generations. No RH850 or exact device identity is inferred merely from the decoder name. The manufacturer's identification of the photographed base part supplies the stronger generation evidence.

The [raw memory-constant scan](../evidence/mcu-identification-2026-10-19/memory-constant-candidates.txt) and `scripts/ghidra/ProbeMemoryConstants.java` retain halfword-aligned candidates in the mapped bytes. This intentionally includes data and overlapping decodes; counts and isolated constants are not a code map or a device fingerprint. The separately traced startup function provides the useful positive evidence above.

## Missing regions and closure state

| Question | Offline result | Remaining prerequisite |
| --- | --- | --- |
| CPU family and plausible generation | V850 little-endian; historical chip identified as V850E2/PJ4, V850E2M | None for this bounded hardware hypothesis |
| Exact chip in the user's rack | Not established | Existing board photograph/module-label/diagnostic binding, or applicable manufacturer hardware record |
| Low code flash `[0,0x2000)` | Absent from current update components, not synthesized | Provenanced complete readout or independently verified source covering this range |
| Runtime RAM | Exact intended 40 KiB zeroing interval confirmed by applicable manual | Runtime contents absent; a RAM capture would require a separate hardware task |
| 32 KiB data flash | Manufacturer region `0x02000000..0x02008000` established; contents not identified among these update blocks | Provenanced data-flash artifact |
| Peripheral working profile | Applicable full manual recovered; named windows recorded | Individual register annotation remains on-demand analysis, not a prerequisite |
| Tuning RAM address | 8 KiB documented; no address identified in full manual text search | Applicable debug/overlay documentation or additional provenanced static evidence |

The currently available offline evidence is enough to select a well-supported static working profile and document the missing regions. It cannot supply absent original bytes or bind an unlabeled public board photo to the user's physical rack. Those dependencies remain explicit. No acquisition from hardware, flashing, bench experiment, or actuation is part of this session.

The public follow-up search also found indexed forum prose associating 5Q0909144 with D70F3506, but the source page returned 403 and no labeled board/diagnostic binding was obtained. Vendor catalogs list 1061 FRF or converted BIN files, without a provenance-bound full flash covering the missing low 8 KiB. Those listings were not downloaded or purchased and are not evidence that the missing region is available. Exact search terms, URLs, and limitations are retained in the structured map evidence. The MCU-generation and applicable working-memory-profile research items are resolved to this documented level; exact user silicon and missing original contents remain external evidence dependencies.
