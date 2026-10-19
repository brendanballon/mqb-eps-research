# Finding ledger

Updated October 19, 2026. No firmware behavior has been reproduced yet.

| ID | Finding or question | Evidence and confidence | Remaining gap |
| --- | --- | --- | --- |
| F001 | User target is SW/HW 5Q0 909 144 R, component EPS_MQB_ZFLS 126 1061 | User-supplied diagnostic output, recorded in TARGET.md | No live vehicle check; hardware/update variant and CPU unresolved |
| F002 | Matching part-number/version firmware material exists locally | File inventory with SHA-256, inventory/archive-manifest.json; observed local bytes | Matching filenames do not establish full flash coverage or variant applicability |
| F003 | MQB 5Q0/3Q0 work used update files in early 2023 | miso, April 16 and 23, 2023, linked Discord thread | No verified full dump of this user's rack identified |
| F004 | CPU identification conflicts across historical sources | miso and ole, January/February 2023; local folder/manual names | Need artifact-specific CPU and import evidence |
| F005 | HCA/DSR mixing was proposed | dkiiv, May/June 2023 | No reproduced MQB measurements or implementation reviewed |
| F006 | A modified MQB prototype rack was reported | ole, March 14, 2025 | No firmware/map artifact, exact rack ID, or modification details |
| F007 | An external ALC module without flashing was reported on a GTI | Teal and armanthenothacker, January 2, 2026 | Source, behavior, limits, and safety claims unverified |
| F008 | REA is connected and version-aligned | evidence/rea-readiness-2026-10-19.json | Relevant firmware provider/import still unverified |
| F009 | Historical security-table candidate at offset 0x48a20 | EPS_research/MQB/5Q0, 3Q0/README.md | Note does not bind a hash or H variant; not verified in bytes or execution |
| F010 | REA 6.7.0 does not admit V850/TriCore raw-binary targets | Live open_binary schema and installed rawBinary.js; GhidraAnalysisProfile.js rejects raw language override | Requires a supported import route before rack decompilation through REA |
| F011 | H1 historical binary exactly matches ODX FD_0DATA, 462848 bytes | evidence/odx-block-inventory-2026-10-19.json; SHA-256 75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641 | CPU, executable ranges, and mapping unresolved |
| F012 | H7 historical binary does not exactly match the ODX FD_0DATA | Same block inventory; ODX data is 24576 bytes, historical binary 24577 | One-byte discrepancy must be characterized before importing; no original changed |
| F013 | Project Ghidra 12.1.4 native arm64 engine passes REA prerequisite checks | evidence/rea-ghidra-doctor-2026-10-19.json; official archive SHA-256 verified | Actual firmware import/decompilation remains unverified; existing MCP process needs reconnection |

## Historical local clues

The imported 5Q0/3Q0 README claims a security-access table starts at `00048a20`, with two-byte code values, padding, and a one-byte flag sequence `01, 02, 04, 08, 10`. It lists three known and two untested code candidates. These are preserved in the original README; they are not independently verified here. Do not silently reinterpret this file offset as a loaded memory address.

The same README lists compatible part numbers under a 3Q0909144J H1 5063 ODX cross-flashing claim. Its text says compatibility comes from ODX declarations. That does not establish tested physical compatibility with the user's rack.

The old extraction workflow selects a long FLASHDATA hex string and manually copies it into a binary. It labels the main-code assumption unverified. Validate all relevant block metadata and extraction before relying on those binaries.

## Record format for new technical findings

For each finding, record: question; observation; inference; source path and SHA-256; file offset and/or loaded address with mapping; REA Evidence IDs and exported file; provider/import profile; coverage and limitations; verification step; next unresolved question.

Thread summaries are historical-source evidence. Session readiness is tooling evidence. Neither is executed firmware behavior.
