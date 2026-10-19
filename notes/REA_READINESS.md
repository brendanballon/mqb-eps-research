# REA preparation

Checked October 19, 2026. This is a current setup snapshot, not a completed firmware analysis.

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
