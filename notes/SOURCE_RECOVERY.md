# Historical source recovery

Checked October 19, 2026. This is a bounded offline/public source investigation, not a claim that missing private work has been recovered.

Evidence: [source-recovery-2026-10-19.json](../evidence/source-recovery-2026-10-19.json). It records source URLs, HTTP outcomes, folder IDs/listings, page hashes, repository commit/tree identities, selected source bytes/hashes, local inventory paths/hashes, and search limits. Historical context remains in [DISCORD_REVIEW.md](DISCORD_REVIEW.md).

## Result and disposition

| Action item | Work completed | Remaining prerequisite |
| --- | --- | --- |
| Recover MQB Ghidra/Binary Ninja annotations | Inventoried imported database extensions and public Drive MQB listings. No imported MQB analysis database found. | Original MQB project export or Binary Ninja database from its owner or an accessible source. |
| Recover exact March 2025 SGO/table plots | Inventoried all 120 local SGOs and checked public MQB metadata and bounded search. Exact historical artifact is unidentified. | Source SGO hash/name, plot/table offsets and axes, or author export. |
| Recover DSR-only and mixed Ocelot branches/logs | Read public dkiiv/ocelot branches, tags, full current tree and selected EPS source/history. Public main has no identified implementation of that proposal. | Named branch/commit or archived source and measurement logs. |
| Recover ALC implementation/hardware | Recovered current public IQ.Pilot MQB host integration and a precise public compiled-module manifest. Source/hardware remain separate. | EPS-side module firmware/source, hardware revision/schematic, and tested rack identity. Bounded host-extension static work is now retained below. |
| Resolve January/August connector diagram provenance | Checked local image/document paths and the exact linked wiring Drive. Anonymous link returns 404; no exact connector diagram recovered. | Original diagram/image attachment identity, vehicle applicability, and reply context tying August's connector to January. |

The bounded investigations above are complete. The prerequisites are still unavailable in the inspected sources. They must remain explicit dependencies, rather than being marked technically solved. None blocks independent static work on the already imported 1061 bytes.

## Local and public archive coverage

The imported manifest has 694 regular files. Its database extension inventory finds exactly two `.gzf` files, no `.gpr`, `.bndb`, `.idb` or `.i64` files:

- `EPS_research/PQ/1K0/3501_annotated_20221024.bin.gzf`, SHA-256 `8e11080d5292db86100405b31ee1645ae494afcbbde52969a7d4635b160f1d20`.
- `EPS_research/PQ/1K0/3501fw.gzf`, SHA-256 `d1c5c3c64ccad1a7df027381aef038c79a9c5100e2aa1022ea195312f924f759`.

`file` identifies Java serialization data for both. Their names and PQ paths do not establish that they contain MQB annotations. This pass did not open or reinterpret either database. The newly generated direct Ghidra project under `analysis/1061/` is independent work, not recovered community annotations. The four imported ZIP paths are legacy tool archives, not identified MQB project backups; no legacy executable was run.

The [firmware/docs Drive root](https://drive.google.com/drive/folders/1jbYVfHPv69yVEW2BQdQ-R-QM_IWp8Gr9) is anonymously readable by ordinary HTTPS, despite the web tool returning an internal error. Eighteen folder pages were inspected, consisting of root, MQB and its rack/candump subfolders. Only embedded initial listing metadata was parsed. No firmware bytes were downloaded.

Seventy-eight nonfolder entries were listed below MQB. Seventy-five have exact local path matches. The three unmatched paths are `MQB_dbc` and `workflow.txt` Drive shortcuts, and the native Google document `candumps/readme`; a local `readme.docx` exists. These mismatches are link/document representations, not evidence of a missing firmware database. A name/path match does not verify remote byte identity. The public `5Q0, 3Q0/0_dump-files` initial listing is empty. No `.sgo`, `.gzf`, `.gpr` or `.bndb` is listed in this inspected MQB subtree. Hidden items, pagination, remote Ghidra storage and unrelated folders remain outside that conclusion.

The local 120 SGOs comprise 13 under PQ/1K0, six under PQ/5N1, seven clean-update files named 1K0/5N1, 93 under VAGHelper's Steering data, and one other VAGHelper SGO. None is under the imported MQB tree. These are filename/path classifications, not CPU or applicability determinations. No evidence binds any one of them to ole's March 14, 2025 plots. An arbitrary local SGO must not be substituted for the missing historical artifact.

## Ocelot source investigation

The public repository [dkiiv/ocelot](https://github.com/dkiiv/ocelot) exposes only `main` in the anonymous branch response, at commit `f68eef7104597d5d98a9b526a3560f948ab18d69`, and no tags. Both calls used `per_page=100`. The recursive main tree reports `truncated=false`.

The tree contains `firmware/eps_gw/` and a Volkswagen safety header. The selected `eps_gw/main.c`, SHA-256 `3ee91f2e3924165ed2e4ee4c7d8a4a5887bf7349aeacf1ab98484f11c6110b2c`, explicitly defines a Toyota-named checksum at lines 203-212 and uses it for its LKA output at lines 421-434. Its inspected text does not identify a VW HCA/DSR mixer. Its path history response contains two commits, `GPIO example` and `initial commit`. The safety header's existence is not proof that the proposed mixer survived in main.

Selected source text is preserved inside the evidence JSON with immutable raw GitHub URLs. No build, flash script, or firmware was executed. This excludes the current selected implementation as a recovered answer to the historical proposal; it does not exclude deleted branches, private commits, other forks or unpublished measurements.

## ALC lead and limits

The [historical Reddit share](https://www.reddit.com/r/Comma_ai/s/PENewTpcQX) now resolves to a post titled `[deleted by user]`, canonical post ID `1okn1bs`. No demo media was downloaded or interpreted.

Public indexed primary repository pages provide a narrower new lead:

- The [IQ.Pilot changelog at commit 38ff45dd19c631a2ddde3c7f198ce568775467e3](https://git.konn3kt.com/IQ.Lvbs/IQ.Pilot/src/commit/38ff45dd19c631a2ddde3c7f198ce568775467e3/CHANGELOG.md) mentions Volkswagen angle-based control and optional ALC torque blending.
- An [August 22, 2026 commit](https://git.konn3kt.com/IQ.Lvbs/IQ.Pilot/commit/9f9f6ba5bbc2d22c199856e01a658fbdc08cc4fb) changes `iqdbc_repo/iqdbc/car/volkswagen/carcontroller.py`. Visible source comments refer to an ALC module state machine and `alc.c` in an MLB discussion, with PQ comparisons.

These are public integration references, not a recovered MQB module algorithm. MLB/PQ comments do not prove 5Q0/1061 behavior. The anonymous Konn3kt API and exact raw-source requests returned HTTP 403. No credential, alternate authenticated route, Discord join or access workaround was used. The indexed view may be stale. Module source, hardware, compatibility and failure validation remain unresolved.

## Connector provenance

The exact [wiring Drive folder](https://drive.google.com/drive/folders/1bW8WEvV_sL4IoRP_i1ewVIfz-GTYVk5O) returned HTTP 404 anonymously. This cannot distinguish deletion, a mistyped link, or restricted access. The imported image/document path inventory contains CPU manuals, CAN-log prose and tool icons, with no identified January/August connector diagram. The historical source register does not contain the necessary image attachment IDs.

The available prose preserves T14q/T14z and candidate connector part numbers, but it cannot identify the connector intended by the final August reply. No pinout, topology or insertion-point recommendation can be verified from this recovery pass. Recovering the original images and their reply context is the concrete next prerequisite. No community member was contacted and no physical experiment was performed.

## Reproduction and limits

Use the evidence JSON's explicit public URLs and immutable GitHub commit IDs. The Drive observations are metadata snapshots from October 19, 2026; page SHA-256 values identify the returned HTML, not the listed firmware. Local paths/hashes come from the imported manifest, whose own SHA-256 is recorded. The evidence records the exact bounded search queries and HTTP failures. Absence in this search is not proof of global nonexistence.

## Additional public search: recovered MQB ALC host integration

The user explicitly authorized further internet research and confirmed there is no additional local material. Follow-up evidence: [source-recovery-public-followup-2026-10-19.json](../evidence/source-recovery-public-followup-2026-10-19.json). This contains the selected source bytes, computed SHA-256 values and immutable URLs, not just search snippets.

A public [iqinc/iqpilot GitHub repository](https://github.com/iqinc/iqpilot) exposes release commit `1b891adc2a8fd27a5365e229d74d08ceea00b2f0`. Its identifier matches the release shown on the [primary Konn3kt repository page](https://git.konn3kt.com/IQ.Lvbs/IQ.Pilot). That primary page describes a prebuilt release, rather than a complete module source tree. Anonymous GitHub access provides a concrete source route without bypassing the primary server's 403 responses.

Selected public Python files under `artifacts/package_runtime/iqdbc/car/volkswagen/` establish host-side MQB ALC integration:

- `carcontroller.py`, line 91, imports a verified module named `iqpilot_private.konn3kt.iqlvbs.alc`. Lines 241 and 348 delegate enable-state calculation and `update_vw_alc` to that module. Line 339 includes MQB/PQ/MLB in the condition controlling the ordinary steering path.
- `carstate.py`, lines 140-141, delegates MQB state parsing to `update_mqb_carstate_alc_state`; line 244 calls that path. This is direct MQB source evidence, stronger than the earlier MLB commit comments.
- `values.py`, line 331, defines the hardware-module presence/intended-path flag. This is not rack compatibility detection or proof the user's rack works.

The public tree exposes `artifacts/iqpilot_alc_private/python/iqpilot_private/konn3kt/iqlvbs/alc.cpython-312-aarch64-linux-gnu.so`. Its downloaded manifest declares 536,160 bytes and SHA-256 `bc3bab44f449522bb5e8ff97bf2a12e02941ef14ff5af6ba10b96e6e72d56775`. These are manifest-declared binary values, not an independently computed binary hash. The adjacent downloaded `.source_sha` contains `2aad9552c736a0c7f70beac4bb6c53e10315d585`. That marker does not make its private source available and is not an EPS firmware revision. No native extension was downloaded, imported, executed or decompiled in this source-recovery pass.

The recovered integration closes the question of whether current public MQB ALC host-side integration can be obtained. It does **not** recover the separate EPS-side hardware firmware, schematic, connector pinout, or prove whether the module uses PLA, sensor interception, mixing or another translation internally. Those mechanisms cannot be inferred merely from host-side names.

Two older public mirrors, `DSparks156x/iq-pilot-tt` and `FOREVERZAX1988/IQpilot`, were inventoried and their release `carcontroller.py`/`mqbcan.py` sources read at recorded immutable commits. Those selected files do not recover the current ALC calls or module implementation. `markclifton/IQishPilot` tree lookup returned HTTP 409. The current primary organization page lists eight repositories but no separately named ALC hardware/source repository. An Explore lookup redirects to sign-in; no login was attempted. The vendor's public website/terms acknowledge an Angle Lateral Control Module as hardware, but do not supply a schematic or exact 5Q0/1061 support proof.

Further narrow public searches for the March 2025 SGO, MQB Ghidra/Binary Ninja annotations, exact `alc.c`, and the known participant/project names produced no identified original map artifact or MQB project export. Generic ECU/DSG conversion material and unrelated steering-map tools were not substituted for that missing identity. The source prerequisites in the disposition table remain explicit, with the ALC host-integration recovery above now recorded as a concrete partial closure.

## Public host native artifact: static follow-up

The later follow-up retrieved the manifest-identified ARM64 host extension and independently verified its 536160-byte size and SHA-256 `bc3bab44f449522bb5e8ff97bf2a12e02941ef14ff5af6ba10b96e6e72d56775`. This supersedes the earlier source-only pass's manifest-declared identity. Binary bytes remain under ignored analysis/public-alc. It was never imported by Python, loaded as a host library, or executed.

[Static artifact evidence](../evidence/public-alc-static-2026-10-19.json) records exact literal offsets, including MQB-specific state, frame, checksum, encryption and angle-map names. [REA bundle](../evidence/public-alc-rea-bundle-2026-10-19.json) retains the supported ELF import, defined-string queries, references, and a method-record read. Default Ghidra analysis did not define the wrapper procedure addressed by that method record. Literal names and metadata are not proof of a CAN algorithm, internal EPS-side mechanism, or operational behavior. No such behavioral claim is made. The REA target was exported and closed with a private snapshot.

Host source recovery and a bounded native follow-up are complete. Full reverse engineering of the compiled host algorithm would be a separate expanded analysis, and even that cannot substitute for the missing EPS-side firmware/hardware or target-specific validation.

## Authorized attempt to recover the shared Ghidra notes

The user separately authorized server login and notes retrieval. A compatible official Ghidra11.4.2 client passed the server's legacy registry check; the12.1.4 client is incompatible with that binding. One pinned shared-account/default-password attempt was rejected. The server offered anonymous read-only access, which succeeded but exposed no repositories. No notes or annotation database could be downloaded. Exact sanitized outcomes: [shared-ghidra-access evidence](../evidence/shared-ghidra-access-2026-10-19.json).

No alternative credential combinations, password changes, server modifications, repository writes or permission changes were attempted. Credentials were not retained in tracked notes. A working authenticated account or repository export is now the specific source prerequisite. The anonymous result cannot establish that the underlying project has been deleted.

## Discord search for failed logins and replacement access

Read-only live RetroPilot search found an explicit administrator explanation: on September 2, 2023 at 5:45 PM, CzokNorris said accounts without custom passwords expire after 30 days and require renewal. [Message](https://discord.com/channels/660951518014341124/1026931406590447617/1147648620280168578). September 12 still has a participant waiting for access; September 19 has the owner reporting repository-permission repairs. This shared server was also intended to hold an MQB folder with existing PQ accounts, per January 12, 2023 discussion. This administrative relationship does not imply firmware equivalence.

On January 2, 2026 at 5:20 PM, miso independently reported the server alive but login failing. [Message](https://discord.com/channels/660951518014341124/1063188305514090546/1456774181579395103). Nearby messages proposed starting a combined EPS/ABS server, but supplied no replacement endpoint or login in the reviewed context. The old default account advice is not a verified current alternative. Expiry is a plausible explanation for our failure, not a proven diagnosis.

A separate recovery lead is dkiiv's September 19, 2023 12:16 PM PQ-thread attachment, `2023_09_19_archive.gar`, displayed as 6.18 MB and described as a full project backup. It was not downloaded in this search and is not established as MQB material. Sanitized search coverage, source dates and limits: [search evidence](../evidence/discord-ghidra-access-search-2026-10-19.json). No credentials retained, messages sent, or authentication retried.
