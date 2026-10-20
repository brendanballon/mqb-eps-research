# MQB steering rack reverse engineering

Local research workspace to resume the MQB steering rack investigation. Initialized October 19, 2026.

## Start here

1. [Current status and next steps](notes/STATUS.md)
   [Preparation checklist and external dependencies](notes/ACTION_ITEMS.md)
2. [Discord history review and prior-work recovery](notes/DISCORD_REVIEW.md)
3. [Findings and unresolved questions](notes/FINDINGS.md)
4. [REA readiness](notes/REA_READINESS.md)
5. [Session log](notes/SESSION_LOG.md)
6. [1061 offline analysis and reproduction](notes/OFFLINE_ANALYSIS.md)
7. [MCU identification and memory documentation](notes/MCU_IDENTIFICATION.md)
8. [Historical source recovery](notes/SOURCE_RECOVERY.md)

`EPS_research/` is the imported historical archive. It includes multiple rack families, firmware containers, extracted binaries, CAN recordings, PQ reference work, and legacy tools. Original files are preserved, including outdated claims. New notes do not silently rewrite that history.

`inventory/archive-manifest.json` records every imported regular file by path, byte length, and SHA-256. Regenerate with `python3 scripts/inventory_archive.py`. A hash establishes local byte identity, not authenticity or successful extraction.

Use `analysis/` for disposable analysis databases and derived files. Export durable REA evidence to `evidence/` and link it from the finding ledger. Git is local, with no remote configured.

The expanded review includes 67 dated source anchors and covers the Discord thread's accessible message text from January 2023 through August 2026. Images, videos, external repositories, and attachment contents have not been exhaustively reviewed. Firmware changes, HCA/DSR mixing, and the later ALC CAN module are separate research paths.
