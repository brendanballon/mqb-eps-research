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

- Ghidra 12.1.4 with a native arm64 decompiler is installed and passes REA prerequisite checks. Codex's REA registration is configured; reconnect/restart is needed for its existing MCP process to inherit the settings. The CLI launcher works immediately. Firmware decompilation remains blocked on the raw import route and verified CPU/memory settings.
- Identify the correct hardware/update variant and retain exact FRF -> ODX -> flash-block -> binary lineage.
- Confirm the CPU, endianness, base addresses, entry points, and code/data boundaries from evidence. Do not choose TriCore or V850 based on folder names or copied manuals.
- Preserve the distinction between an update payload and a full hardware flash dump.
- Images, videos, external links, attachment contents, shared Ghidra projects, and the separate Konn3kt server have not been exhaustively reviewed or synchronized. Local archive completeness relative to Google Drive is unknown.

## Next concrete work

1. Extend the initial ODX block inventory in `evidence/odx-block-inventory-2026-10-19.json`. H1 historical binary matches FD_0DATA exactly; H7 historical binary has a one-byte size discrepancy and does not match. Resolve block purpose, encoding, mapping, and checksum fields before import.
2. Resolve CPU/import settings using those bytes, documentation, and any applicable hardware photographs. Record competing explanations until evidence selects one.
3. Reconnect the configured REA MCP server and resolve V850/TriCore raw import support. Do not select a false architecture or assume a language override bypasses admission.
4. Start focused static analysis with exact artifact identity. Validate the older security-table location before relying on it, then trace relevant data and functions. Export REA evidence and update the ledger.

Current work has not flashed a rack, sent CAN messages, tested steering behavior, or demonstrated a torque modification.

## Follow-up configuration findings

REA 6.7.0's raw-binary admission excludes V850 and TriCore and explicitly rejects a Ghidra language override for raw imports. This is an additional blocker beyond installing Ghidra. Ghidra 12.1.4 has been downloaded, hash-verified, installed, and built for Apple Silicon under `analysis/tools/`. REA's Ghidra checks pass and Codex registration is configured with a verified backup. Configuration details are in REA_READINESS.md. Do not treat engine setup as completed rack decompilation.
