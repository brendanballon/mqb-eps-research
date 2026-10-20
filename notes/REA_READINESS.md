# REA preparation

Checked October 19, 2026. This is a setup record, not a completed firmware analysis. The bootstrap snapshot below precedes the follow-up configuration work recorded at the end.

## Verified

- Skill read: `/Users/brendanballon/.agents/skills/reverse-engineer-anything/SKILL.md`, metadata version 42.
- Connected MCP: `rea-agents` 6.7.0, advertising 207 tools.
- `binary_session` with expected package version 6.7.0 returned alignment `aligned`.
- No binary target is open. No firmware was executed or imported into a disassembler.
- Provider status and server identity are retained in `evidence/rea-readiness-2026-10-19.json`. This is a selected session-status snapshot, not a REA analysis Evidence record.

## Provider limits

| Capability | Observed state | Implication |
| --- | --- | --- |
| Hopper launcher | Available on macOS | Does not establish support for this MCU or raw image |
| Ghidra | Unavailable, GHIDRA_INSTALL_DIR unset | Firmware decompilation route requires a suitable installation/configuration and verified import profile |
| IDA | Unconfigured | No IDA route selected |
| Kuna | Unconfigured | No Kuna route selected |
| REA firmware region inspection/extraction | Provider missing on this host | Advertised route requires Linux with supplied Binwalk/Unblob and prlimit; not needed merely to inspect ODX XML |

A bounded filesystem search under `/Applications`, `~/Applications`, `~/Tools`, and `/opt/homebrew/opt` to depth two returned no Ghidra-named entry. This is not an exhaustive search or proof Ghidra is absent everywhere.

## Next preparation

1. Select exact bytes from the user's 5Q0909144R / 1061 working set. Compare H1/H2/H7 metadata and extraction lineage first.
2. Establish the CPU and raw import mapping. Do not use a neighboring rack's settings without evidence.
3. Select an architecture-capable provider. Installing Ghidra or changing MCP registration has not been necessary for this orientation pass and has not been done.
4. Once a provider is configured, open the selected artifact with its explicit path and import profile. Keep analysis identity, hashes, limitations, and exports in the ledger.

The installed skill and running server agree, so a setup rewrite or upgrade was not performed. REA package readiness does not mean firmware-provider readiness. Future configuration repair should follow the skill's read-only setup-plan procedure and existing user authorization.

## Follow-up: decompiler configuration

The user requested software/decompiler configuration on October 19, 2026.

An additional compatibility gate was confirmed in the actual connected tool schema and installed REA 6.7.0 code:

- `open_binary(format="raw-binary")` admits only x86, x86_64, arm, arm64, 6502, and m68k.
- Neither V850 nor TriCore is an admitted raw architecture.
- `dist/ghidra/GhidraAnalysisProfile.js` explicitly rejects `REA_GHIDRA_LANGUAGE_ID` overrides for raw-binary targets. An environment override does not solve this gate.
- Do not mislabel the rack firmware as ARM to force it through admission.

Official Ghidra release selected: 12.1.4, asset `ghidra_12.1.4_PUBLIC_20260921.zip`, release tag `Ghidra_12.1.4_build`. The downloaded ZIP matched the release API's SHA-256 `ddac49f903da9d5bac833e5cc79395098b9c33cfd3279be5f31bd00387d2d4db`.

Project-local installation: `analysis/tools/ghidra_12.1.4_PUBLIC/`. This ignored directory holds software and build products. `scripts/rea-ghidra` selects this installation for the pinned REA CLI. The existing JDK is OpenJDK 25.0.2 arm64; Ghidra declares Java minimum 21 with no maximum.

Ghidra includes V850 and TriCore language definitions. Their presence establishes Ghidra language availability, not the correct CPU for this firmware or an admitted REA raw route.

The release archive does not include a macOS decompiler. Native build command, using existing tools:

```sh
make -C analysis/tools/ghidra_12.1.4_PUBLIC/Ghidra/Features/Decompiler/src/decompile/cpp \
  -j 6 ghidra_opt 'ARCH_TYPE=-arch arm64' OSDIR=mac_arm_64
```

Upstream references: [REA installation and Ghidra configuration](https://github.com/morluto/rea/blob/main/docs/installation.md), [official Ghidra release](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.1.4_build). Installed REA source is authoritative for its current admission limits.

Outstanding firmware route: confirm CPU and memory mapping, then establish supported V850/TriCore raw-image admission in REA or use an explicitly documented direct Ghidra workflow. Neither route has been verified for this firmware. A synthetic executable carrier, if considered later, must preserve provenance and be validated; it is not currently an established solution.

### Configuration result

- Native arm64 decompiler built and installed at `Ghidra/Features/Decompiler/os/mac_arm_64/decompile`; `file` identifies Mach-O arm64.
- `scripts/rea-ghidra doctor --provider ghidra --json` passed all eight Ghidra checks: configuration, host platform, architecture, installation, version, headless launcher, native decompiler, and Java. Report: `evidence/rea-ghidra-doctor-2026-10-19.json`. This checks prerequisites; no firmware decompilation has yet run.
- Reviewed `setup --client codex --skill=false --dry-run --json`, then applied the same scope under the user's configuration request. Setup returned `ready` and `configured_codex`.
- Updated only the REA registration in `/Users/brendanballon/.codex/config.toml` with the project Ghidra path and existing Java home. Hopper configuration retained. No skill replacement or other client configuration was requested.
- Verified all unrelated TOML configuration was identical to the pre-change backup: `/Users/brendanballon/.codex/config.toml.rea.backup.db4f3e5c9001372832581c6585947b6dd92a51137f0ffa3f871a42ab617c818d.recovery`.
- The existing MCP server retains its launch environment. Restart/reconnect Codex's REA server before expecting the in-chat MCP provider to see Ghidra. The project CLI launcher works immediately.

Use `scripts/rea-ghidra doctor --provider ghidra --json` to recheck the engine. The project-local Ghidra software is ignored by Git and must remain at the configured path. Its archive and build log are also under `analysis/tools/`.

## Restart follow-up: live provider and direct firmware probe

After the user's Codex restart, `binary_session(expected_package_version="6.7.0")` reports aligned REA and an available Ghidra 12.1.4 provider, with all eight checks passing. The restart gate is resolved. Selected live response retained in `evidence/rea-restart-verification-2026-10-19.json`.

V850/TriCore raw admission remains absent in the actual connected schema and installed 6.7.0 source. We did not change REA or pretend these bytes were ARM. A direct Ghidra BinaryLoader workflow was tested instead: bounded competing V850/TriCore decoding, followed by successful native decompilation of one manually seeded V850 candidate function. It uses base zero as offset coordinates only, with automatic analysis disabled. This resolves engine feasibility while preserving the CPU/mapping gate for substantive analysis.

See [OFFLINE_ANALYSIS.md](OFFLINE_ANALYSIS.md) for exact commands, hashes, competing results, and limits. Direct Ghidra exports are not REA Evidence records. REA has no native target open; the private direct Ghidra projects are saved under `analysis/1061/ghidra/`.

The same-session continuation established a corroborated static component map and successfully imported H2 + H1 directly with BinaryLoader at 0x2000. H7 is an exact overlapping H2 suffix. A mapped H1 function decompiles and resolves its expected data reference. The saved direct project and mapping provenance are documented in OFFLINE_ANALYSIS.md and F020. REA raw admission remains unchanged; full hardware mapping and executable/data boundaries are not established.

## Current consolidated route

The firmware preparation route is now reproduced end to end by `scripts/run_1061_analysis.sh`: exact FRF lineage, supported V850E2M/PJ4 working profile, startup register context, data partition and typed service27 analysis in a saved direct Ghidra project. REA6.7.0 V850 raw admission remains unchanged. That API restriction is handled by the documented direct route and is not a reason to relabel the image or repeat setup.

The separate public ALC host ARM64 ELF was admitted through REA's ordinary ELF route, statically inspected, exported to `evidence/public-alc-rea-bundle-2026-10-19.json`, and closed with a snapshot under analysis/public-alc. No native target remains open. Its supported ARM64 route does not imply support for the V850 update. See OFFLINE_ANALYSIS.md and ACTION_ITEMS.md for current completion/dependency status. Earlier sections above preserve historical setup states.
