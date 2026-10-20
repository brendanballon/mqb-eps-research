# Preparation checklist and evidence dependencies

October 19, 2026. The user requested completion, updates and documentation of the remaining offline action items, then authorized public internet research and confirmed there is no additional local material.

## Completed preparation work

| Item | Result | Evidence |
| --- | --- | --- |
| Read last chat and newly added notes | Reconciled the setup checklist and 67-anchor Discord review | SESSION_LOG.md, DISCORD_REVIEW.md |
| Verify restarted REA/Ghidra | Live MCP sees Ghidra 12.1.4; existing prerequisite checks pass | rea-restart-verification JSON |
| Resolve firmware-analysis route | Direct Ghidra workflow is saved and reproduced; REA's raw V850 API restriction is documented | OFFLINE_ANALYSIS.md, REA_READINESS.md |
| Recover exact FRF -> ODX -> block lineage | Three exact XML matches, ZIP CRC checks and six exact payload matches | frf-lineage-1061 JSON/MD |
| Characterize historical H7 discrepancy | Exactly one added leading zero; source preserved | odx-lineage JSON |
| Recover component map | H2 at 0x2000, overlapping H7 at 0x9000, H1 at 0xf000; no fabricated missing bytes | static-map JSON |
| Resolve CPU family/generation working profile | Photo-marked 70F3506, Renesas V850E2/PJ4/V850E2M, independent firmware corroboration | MCU_IDENTIFICATION.md |
| Recover applicable memory/peripheral documentation | Full manufacturer-authored manual and part-specific tables recovered with mirror provenance | MCU manual, manual-memory-map JSON |
| Refine false code and supply register context | Numeric table misread as pointers identified; separate data-aware database; app tp/gp recovered | code-data-refinement JSON, refined Ghidra export |
| Trace historical table consumers | Service 0x27 descriptor, five-row state-machine loop, transform helper and mask consumers identified | ghidra-diagnostic-core, annotations and mask-consumer exports |
| Recover surviving public source leads | Local/Drive metadata inventory, Ocelot investigation, MQB ALC host source and public native artifact identified | SOURCE_RECOVERY.md, source-recovery JSONs, public-alc static evidence |
| Preserve/export and reproduce | Saved projects, scripts, evidence and fresh end-to-end reproduction; original archive checked | offline-preparation-validation JSON |

The completed items establish an offline research foundation. They do not establish a complete hardware dump, a steering torque patch, or validated vehicle behavior.

## Unavailable evidence dependencies

These are **unresolved**, not completed technical claims. The accessible-source investigations are documented separately from the missing deliverables.

| Missing deliverable | Searches/results | What would actually close it |
| --- | --- | --- |
| Exact physical user's MCU identity | Historical photo lacks a module-label binding; public sources support the70F3506 family profile | A provenance-bound board/module record for the user's rack |
| Low code-flash bytes 0x0..0x1fff and data-flash contents | Absent from the supplied updates; inspected public MQB dump listing empty; vendor conversion listings are not full-dump evidence | Provenanced original bytes covering those regions |
| Original community MQB Ghidra/Binary Ninja annotations | No matching database in imported archive or inspected public Drive listings | Accessible original project export/database |
| Exact March 2025 SGO and plots | 120 local SGOs inventoried; none bound to that source event; public search did not identify it | Exact artifact/hash, axes/offsets, and plot source |
| Historical DSR-only/mixer implementation and measurements | Current public Ocelot branch/tree inspected; no identified surviving proposal implementation or logs | Original branch/commit and quantitative logs |
| EPS-side ALC firmware/hardware and tested 1061 identity | Current host integration and binary recovered; these do not supply the separate hardware firmware/schematic | Module firmware/source, hardware revision/schematic, applicable test record |
| January/August connector diagram/reply binding | Wiring link returns anonymous404; exact image attachments unavailable in reviewed register | Original diagrams/photos and message reply context |

The user has no additional local material. No credentials, server login, community contact, actuation, flashing, or bench work was authorized or performed. An absent original artifact cannot be produced by further speculative interpretation of the existing bytes. Reopen the corresponding item when a new accessible source supplies it.

## Subsequent research

The next independent firmware research task is to identify steering/HCA/DSR-related data and its code consumers in the refined project, using the now documented memory and diagnostic context. It is not evidence that a torque limit has already been located. Bench experiments, vehicle actuation and flashing still require a separately defined target and task under AGENTS.md.
