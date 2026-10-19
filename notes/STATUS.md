# Current status

Updated: October 19, 2026.

## Objective

Resume MQB steering rack reverse engineering with a reproducible local workspace and persistent agent notes. First establish what prior work actually demonstrated and prepare REA for the selected firmware.

## Target

User diagnostic identification: J500, SW/HW **5Q0 909 144 R**, component **EPS_MQB_ZFLS 126 1061**, ASAM **EV_SteerAssisMQB 012140**. See [TARGET.md](TARGET.md). The archive contains matching part-number/software-version update files. H1/H2/H7 applicability remains unresolved.

## Completed

- Initialized local Git on `main`. No remote configured.
- Read the REA skill, version 42. Verified live REA 6.7.0 with `binary_session(expected_package_version="6.7.0")`; alignment returned `aligned`.
- Inventoried the original archive: 694 files, 356,747,307 bytes, 559 unique SHA-256 values. No archive files were changed or executed.
- Reviewed the Discord thread's accessible text from its January 12, 2023 beginning to the latest visible August 10, 2026 messages. Thread: RetroPilot, `MQB VW Rack FW Hack (5Q0, 3Q0)`.
- Established agent entry points, source boundaries, target identification, finding ledger, and session log.

## What the history establishes

The thread explored firmware modifications, HCA/DSR mixing, and later an external CAN module called ALC. These are separate approaches. Firmware reading/flashing and exact CPU identity were unresolved in the early discussion. A March 2025 report described an IAV-modified prototype rack, without the modifications or a reproducible artifact. January 2026 participants reported a working GTI ALC installation requiring no firmware flash, but did not provide a reviewed implementation or independent validation in the text examined.

## Open preparation gates

- REA connectivity is ready. Firmware decompilation is not yet ready: Ghidra is unconfigured, and no CPU-specific import profile has been verified. Hopper availability does not establish support for this rack.
- Identify the correct hardware/update variant and retain exact FRF -> ODX -> flash-block -> binary lineage.
- Confirm the CPU, endianness, base addresses, entry points, and code/data boundaries from evidence. Do not choose TriCore or V850 based on folder names or copied manuals.
- Preserve the distinction between an update payload and a full hardware flash dump.
- Images, videos, external links, attachment contents, shared Ghidra projects, and the separate Konn3kt server have not been exhaustively reviewed or synchronized. Local archive completeness relative to Google Drive is unknown.

## Next concrete work

1. Inventory the selected 1061 ODX files by flash block, explicit target metadata, declared addresses, encoding/compression, size, and checksum fields. Compare their decoded bytes with the historical H1/H7 binaries without changing originals.
2. Resolve CPU/import settings using those bytes, documentation, and any applicable hardware photographs. Record competing explanations until evidence selects one.
3. Prepare the smallest appropriate REA provider configuration after choosing the architecture. No Ghidra installation or global MCP configuration change has been made.
4. Start focused static analysis with exact artifact identity. Validate the older security-table location before relying on it, then trace relevant data and functions. Export REA evidence and update the ledger.

Current work has not flashed a rack, sent CAN messages, tested steering behavior, or demonstrated a torque modification.
