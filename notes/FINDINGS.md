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
| F011 | H1 historical binary exactly matches ODX FD_0DATA, 462848 bytes | evidence/odx-block-inventory-2026-10-19.json; SHA-256 75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641 | Subsequent map/profile/refinement results in F020/F022/F023 |
| F012 | H7 historical binary does not exactly match the ODX FD_0DATA | Same block inventory; ODX data is 24576 bytes, historical binary 24577 | Resolved as one extra leading zero in F015; original preserved |
| F013 | Project Ghidra 12.1.4 native arm64 engine passes REA prerequisite checks | evidence/rea-ghidra-doctor-2026-10-19.json; official archive SHA-256 verified | Historical setup snapshot; restart resolved in F014 and reproduced firmware route in F024 |

## Historical local clues

The imported 5Q0/3Q0 README claims a security-access table starts at `00048a20`, with two-byte code values, padding, and a one-byte flag sequence `01, 02, 04, 08, 10`. It lists three known and two untested code candidates. These are preserved in the original README; they are not independently verified here. Do not silently reinterpret this file offset as a loaded memory address.

The same README lists compatible part numbers under a 3Q0909144J H1 5063 ODX cross-flashing claim. Its text says compatibility comes from ODX declarations. That does not establish tested physical compatibility with the user's rack.

The old extraction workflow selects a long FLASHDATA hex string and manually copies it into a binary. It labels the main-code assumption unverified. Validate all relevant block metadata and extraction before relying on those binaries.

## Record format for new technical findings

For each finding, record: question; observation; inference; source path and SHA-256; file offset and/or loaded address with mapping; REA Evidence IDs and exported file; provider/import profile; coverage and limitations; verification step; next unresolved question.

Thread summaries are historical-source evidence. Session readiness is tooling evidence. Neither is executed firmware behavior.

## F014: restarted MCP sees Ghidra

Evidence type: live tooling status, not firmware execution. `binary_session` reports aligned REA 6.7.0 and available Ghidra 12.1.4, with eight passing prerequisite checks. No target open. Selected response: `evidence/rea-restart-verification-2026-10-19.json`. No firmware hash or offsets apply to this tooling-only finding. V850 raw admission remains unsupported.

## F015: ODX payload checks and H7 leading byte

Evidence type: exact local XML and byte comparison, reproduced by `scripts/inspect_1061_odx.py`. Detailed artifact paths/hashes, XML IDs, candidate FRF ancestors, sizes, CRC32, and metadata are in `evidence/odx-lineage-2026-10-19.json`.

- H1 ODX SHA-256 `a2f2620ae33701e9b5b1b2e193d6cb68a8dd2ec23cfff5870ab0069ef7923b6e`; DATA SHA-256 `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641`, CRC32 `423BE503`, 462848 bytes.
- H2 ODX SHA-256 `8c00f9bd1103deef9db0d6e07477787d35ca06c5b0d9717334b818bbb4bb2baa`; DATA SHA-256 `6da9a40580a2bd49b5097f6c7363a2080a76575e230b7cf8fe54a3f7a61ce5f7`, CRC32 `827F508F`, 53248 bytes.
- H7 ODX SHA-256 `c9265268aa6305c3a563f33e4c1af5ea664f5e04c6bef4d64d01d37f27855e60`; DATA SHA-256 `10c11c159565aeff7750a8c4ebe67b2ef25e44e1ce599dbec54c42a85bbbf64a`, CRC32 `2144DF1C`, 24576 bytes.

All three computed CRC32 values match ODX declarations. Historical H7 SHA-256 `391f6fc7872966a3f980e21534853c0b13164d9b084d6d513fde978178e2a40d`, 24577 bytes, is exactly `00` followed by decoded H7 DATA. Historical range `[1,24577)` equals decoded range `[0,24576)`. This resolves F012's size discrepancy, without establishing why it arose. Originals preserved. FRF conversion, hardware applicability, and authenticity remain unverified.

## F016: common metadata and distinct download addresses

Evidence type: declared XML metadata in the three ODX artifacts hashed in F015. All share expected hardware identifiers H12/H13/H16/H18/H19/119 and 5Q0909144/5Q0909145. Their DATA segments give literal SOURCE-START-ADDRESS values H1=`07`, H2=`06`, H7=`02`; ALFID is `014101`, DATAFORMAT is BINARY, ENCRYPT-COMPRESS-METHOD is `00`.

Inference: separate download components/selectors are a stronger working explanation than three hardware variants. Neither component role nor CPU mapping is established. These small values must not be substituted as CPU load addresses. Outer target IDs and inherited internal 3Q0 IDs are recorded separately in the lineage report.

## F017: sampled H1 code strongly favors V850

Evidence type: direct static Ghidra 12.1.4 competing disassembly, not REA Evidence or execution. Input H1 DATA SHA-256 `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641`. File-offset samples `0x82`, `0x100`, `0x200`, `0x400`, `0x1000`. BinaryLoader base zero is an offset coordinate system, not a measured runtime map. Automatic analysis disabled.

V850:LE:32:default decoded coherent compare/branch/return and call/prologue/epilogue sequences. TriCore:LE:32:default failed in all five windows. Exports: `evidence/ghidra-v850-probe-2026-10-19.txt`, `evidence/ghidra-tricore-probe-2026-10-19.txt`. Input, profile, scripts, and language hashes: `evidence/ghidra-probe-profile-2026-10-19.json`.

Inference: V850-family little-endian is now supported by artifact-specific instructions for this sampled H1 code, improving on F004's historical uncertainty. Exact MCU, V850 generation, unsampled code, component layout, and actual addresses remain unverified. Generic bundled manuals do not establish hardware identity. No claim transfers to 2Q1, 6C1, or PQ 1K0.

## F018: native decompiler works on a bounded H1 candidate

Evidence type: direct Ghidra static decompilation. Same input hash as F017, V850:LE:32:default, BinaryLoader, base zero as offset coordinates. Manually seeded candidate at file offset `0x78`, observed body `[0x78,0x99]` inclusive. `decompileCompleted=true`, no reported error. Assembly and pseudocode: `evidence/ghidra-v850-function-probe-2026-10-19.txt`; script: `scripts/ghidra/ProbeFunction.java`.

The decoded function indexes an eight-byte-stride record, reads a flag and pointer, and returns a halfword from displacement 0x10 or 0x100. Its absolute references around 0xfb48 are unresolved. No steering/security meaning assigned. This demonstrates a direct Ghidra fallback while F010 remains true for REA. It does not establish full firmware decompilation or CPU mapping. No REA native target or Evidence ID exists for these direct-engine exports.

## F019: historical table bytes confirmed, last values mix endianness

Evidence type: immutable H1 bytes, hash as F017, offset `0x48a20`. Five eight-byte rows have two-byte values, two zero bytes, flags `01,02,04,08,10`, then three zero bytes. Exact bytes and both byte orders are in the lineage report; table in OFFLINE_ANALYSIS.md.

First three little-endian values are 28183, 44595, 19249, matching the historical README. Last two raw byte pairs are `af 7a` and `52 ee`. Little-endian yields 31407 and 61010; historical 44922 and 21230 are their big-endian interpretations. Thus the old note is internally inconsistent about byte order. This verifies the pattern in F009, not working access credentials, authorization role, or execution. Loaded address, code references, and accepted values remain unresolved.

## F020: overlapping components and corroborated static map

Evidence type: exact byte overlap plus independent address relationships decoded as V850. Inputs are the three DATA hashes in F015. H7 `[0,0x6000)` equals H2 `[0x7000,0xd000)` exactly. H7 offset `0x156` loads absolute return address `0x915e` before an indirect jump at `0x15c`, supporting H7 base `0x9000`. H7 offset `0x14c` loads table address `0x2000`, whose leading H2 words resolve to plausible function starts when H2 is placed there. H1's absolute table `0xfb48` corresponds to its file offset `0xb48` at base `0xf000`.

Corroborated working map: H2 `[0x2000,0xf000)`, overlapping H7 `[0x9000,0xf000)`, H1 `[0xf000,0x80000)`. Build script checks hashes and overlap and emits H2 + H1 only, without duplicate H7 or fabricated low-flash bytes. Derived image SHA-256 `a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d`, 516096 bytes. Evidence: `evidence/static-map-1061-2026-10-19.json`, `evidence/ghidra-h7-v850-probe-2026-10-19.txt`.

Direct Ghidra V850:LE:32:default BinaryLoader at 0x2000 reports one block 0x2000..0x7ffff inclusive. Function 0xf078 decompiles, with an analyzed data reference from 0xf088 to correctly mapped records at 0xfb48. Export: `evidence/ghidra-mapped-1061-2026-10-19.txt`. Program image-base property is separately zero; do not confuse it with the observed memory block start.

The five-row historical table maps to 0x57a20 and reads identically. No direct references were recovered to any byte in 0x57a00..0x57a60 inclusive in this database. Indirect access and undiscovered code are unresolved. Default analysis completed but produced decoding warnings, including a broad candidate at 0x55900 running into likely data; its 1907-function count is provisional. Refine code/data boundaries before trusting broad graphs or negative results.

This improves the prior mapping gate with corroborated static evidence. It is not a hardware-read map or full dump, and exact MCU, V850 generation, RAM/peripherals, low flash, and runtime behavior remain unknown. No REA Evidence ID exists for the direct Ghidra run.

## Discord history findings

These findings concern what the sources establish, not verified firmware behavior. Live Discord observations have dated anchors in [SOURCE_ANCHORS.tsv](../evidence/discord-history-2026-10-19/SOURCE_ANCHORS.tsv); this is a curated paraphrase, not an original-byte transcript. No firmware address is attributed to a Discord message. Artifact and note hashes are in [SOURCES.json](../evidence/discord-history-2026-10-19/SOURCES.json).

| ID | Finding | Evidence type and locator | Limits |
| --- | --- | --- | --- |
| DH-01 | The initial objective was MQB rack reverse engineering and torque hacking | Live observed statement, CzokNorris, January 12, 2023 3:10 PM | Does not establish a completed patch or bounty payout |
| DH-02 | TriCore teardown context was 2Q1; ole's V850 observation concerned 5Q0 | Live statements, miso January 20 and February 18; ole February 18, 2023 | No exact target board or architecture verification in this review |
| DH-03 | Known MQB research was on update files, not a known hardware dump | Live statements, miso April 16 and 23, 2023; VCP correction by FLcruising April 23 | Cannot rule out dumps outside this thread or later private work |
| DH-04 | A historical security-table localization deserves targeted reuse | Imported MQB README, SHA-256 `3d2701a7f5fbf0b1bcc94c53dbb0395da19b0b2fa41cb3ff9855b579b01c2d63`, claimed offset `0x00048a20` | Original binary hash not specified; subsequent local byte verification and byte-order correction are in F019/F020; security purpose and accepted codes unverified |
| DH-05 | HCA/DSR mixing remained explicitly untested June 29, 2023 | Live statement, dkiiv 11:40 AM; May 22 and 24 test plans | No quantitative combined-torque result recovered |
| DH-06 | Ole corrected cancellation-vs-output confusion using reported MQB experiments | Participant result, May 22, 2023 4:02-4:05 PM and May 24 2:00-2:02 PM | About 5 Nm driver threshold and rapid motion are author reports, not validated limits for our target |
| DH-07 | June wiring work identified a candidate insertion point, with GTE access materially different | Participant results, UptownBench1187 and miso, June 29, 2023 | Photos/pins not reviewed; not a universal part or pinout |
| DH-08 | March 2025 table labels remained hypotheses and IAV modifications unavailable | Live statements and participant report, ole and dkiiv March 14, 2025 | No exact SGO, patch, rack identity, addresses, or implementation recovered |
| DH-09 | ALC developers reported a GTI module installation without firmware flashing | Participant claims, Teal and armanthenothacker January 2, 2026 | Mechanism, compatibility, demo behavior, and safety claims not independently verified |
| DH-10 | The visible ALC mechanism question was not answered technically | jp-solutionz January 2, 2026 11:10 PM; reply at 11:31 PM says unreleased | Do not convert torque-sensor-intercept question into a finding |
| DH-11 | GTE expansion stopped at access/connector work, then a revised filtering proposal | miso January 10-11, harness request January 5, Teal August 10, 2026 | No later visible install/test result; exact final connector unknown |
| DH-12 | No reason for ultimate silence can be established | Interpretation of latest visible endpoint, August 10, 2026 8:23 PM | Documented blockers do not prove abandonment, private success, or technical impossibility |

No REA evidence records were created by the Discord review because that session did not analyze firmware or binaries. Technical findings F014-F020 above are separate local evidence.

## F021: exact FRF lineage reproduced

Evidence type: independently implemented offline container transform and exact byte comparisons, using inspected primary VW_Flash source at commit `293f46d782bae2ced930497889b71eb782f122cb`. No upstream source or legacy tool executed. FRF SHA-256: H1 `6bf8e39c9ea7e0acab2251407db8e65eb8803a6e1ce606166907cbe998c92e54`, H2 `f309ecfca6b4d79d5e48dc5812c89ac587e506c15c53c80d6d27c1ce49c90fcc`, H7 `7ec18f1fbbde971f1fa0f06122342f013cf4cfe4981ee67a835cd0e5a4d25d38`.

Each decodes to a single-member ZIP whose ODX equals the F015 XML artifact exactly. ZIP CRCs pass; all six ERASE/DATA outputs equal the earlier extraction. `evidence/frf-lineage-1061-2026-10-19.json` and `.md` bind exact compressed ZIP stream ranges, XML hex-text offsets, reference hashes, and payload hashes. `scripts/verify_1061_frf.py` reproduces it. This resolves F015/F020's FRF-lineage gate. It proves local derivation, not vendor authenticity, compatibility, full flash coverage or flashing behavior.

## F022: photo and manufacturer documentation support V850E2M/PJ4

Evidence type: recovered historical board photo plus manufacturer-authored documents and independent static corroboration. Photo SHA-256 `60847d664322b9af5b10c4ca60f7878d6720d6a6398d3706e6fc6d4a6a4c929f`, visible base marking D70F3506. Renesas part page and supported-MCU list identify UPD70F3506 as V850E2/PJ4, core V850E2M. Full hardware manual R01UH0098EJ0100 Rev.1.00 was recovered through a public mirror; PDF SHA-256 `f2914aa669635072756bc530485d8bc690dede0e8398b51ee6adcc3b62b3bd22`.

Printed page 24, PDF page 44, Tables 1-3/1-4 specify 3506/3507 code flash `[0,0x80000)`, data flash `[0x02000000,0x02008000)`, RAM `[0xfedf6000,0xfee00000)`. These agree with mapped update end and startup zeroing at 0x13cd2 in image SHA-256 `a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d`. Peripheral windows and page/table provenance are in `evidence/mcu-identification-2026-10-19/manual-memory-map.json`; complete source identities in its manifest. See MCU_IDENTIFICATION.md.

Limits: the photo is not bound to the user's module label; applicable capacities alone do not uniquely select 3506 over 3507. Mirror PDF metadata was rewrapped and official byte equality is unknown. This resolves the static working-profile/generation question, not exact user silicon or missing physical contents. No cross-family transfer.

## F023: false code, supported data partition, and register context

Evidence type: exact image bytes plus startup/listing analysis. Image hash as F022. The candidate 0x55900 is referenced by numeric data word at 0x78318. Thirty neighboring words at `[0x78300,0x78378)` are exact squares; 0x55900 equals 592 squared. Automatic pointer discovery had treated that numeric value as an entry and expanded a false switch across data.

Observed tail function `[0x555f0,0x55606)` ends in return; `[0x55606,0x55800)` is all FF, followed by metadata/tables. Separate refined project treats `[0x55606,0x80000)` as non-executable typed data, preserving the original broad baseline. It is a supported analysis partition, not a semantic proof for every byte. Startup instructions 0x100c0..0x100d6 yield application tp=0x5d800 and gp=0xfee01000. Applying that context to application code recovers references previously missed. Boot context is separate. RAM is uninitialized, not zero-filled.

Evidence: `evidence/code-data-refinement-1061-2026-10-19.json`, startup exports, and `evidence/ghidra-refined-1061-2026-10-19.txt`. Candidate function count changes 1907 -> 1757; neither is a verified count of real functions. Missing low memory, indirect flow and uninitialized RAM warnings remain explicit.

## F024: historical table is consumed by diagnostic service 0x27

Evidence type: direct static Ghidra instructions, typed records, and dataflow. Image hash as F022; H1 hash `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641`. H1 file offset 0x48a20 maps to 0x57a20. Startup-derived tp minus0x5de0 resolves that address at instruction 0x2feea; 0x2fef0 reads a uint32 constant. Function 0x2fd96 iterates over five eight-byte rows. Service descriptor `[0x582fc,0x58308)` contains ID0x27, handler0x30006, flags0x2e00; handler calls0x2fd96 at0x3001e.

The state machine uses helper0x2fd2a to conditionally add a selected constant to challenge-derived local data before comparison. A successful branch loads the row mask at0x2ff16 and writes RAM0xfedfaf85 at0x2ff22. Mask consumers include0x3014a,0x4c65e,0x4d3d4,0x4d638,0x4fe78,0x5036e,0x50576. Several access-check paths return0x33. This corroborates diagnostic access-control use. It does not test working access values or steer anything.

Core export: `evidence/ghidra-diagnostic-core-2026-10-19.txt`. Readback, typed structure and mask references: `evidence/ghidra-diagnostic-annotations-2026-10-19.txt`. Consumer assembly/pseudocode: `evidence/ghidra-access-mask-consumers-2026-10-19.txt`. The five constants use consistent little endian; F019's last-value correction stands. This supersedes F009/F019's pattern-only uncertainty and F020's bounded negative reference result, whose missing application register context is now explained. No REA Evidence ID applies to direct Ghidra exports.

## F025: source recovery completed within documented public/local bounds

Evidence type: bounded inventory, public source/API/metadata recovery and exact selected source hashes, not absence everywhere. `evidence/source-recovery-2026-10-19.json` and `evidence/source-recovery-public-followup-2026-10-19.json` bind URLs, commits, page/source hashes, search queries and HTTP outcomes. SOURCE_RECOVERY.md records the results and remaining source prerequisites.

No original MQB analysis database, exact March2025 SGO/plots, DSR/mixer measurements, or connector diagram binding was recovered. The imported archive has120 SGOs and two PQ-named GZF files; none establishes those missing MQB sources. Eighteen public Drive folder listings were inspected, without downloading another firmware collection. Current selected Ocelot source does not identify the historical proposed VW mixer. These are bounded results, not global nonexistence claims. No credentials, outreach or server login.

## F026: public MQB ALC host integration and native artifact recovered

Evidence type: exact public source at iqinc/iqpilot release commit `1b891adc2a8fd27a5365e229d74d08ceea00b2f0`, matching primary repository release identity. MQB Python state/controller code delegates to a native host extension. Selected source bytes/hashes and immutable URLs are in F025's follow-up evidence.

Retrieved host ARM64 ELF SHA-256 `bc3bab44f449522bb5e8ff97bf2a12e02941ef14ff5af6ba10b96e6e72d56775`, 536160 bytes, matching the public manifest. Static strings include MQB-specific ALC parsing/control, frame encryption, and availability/status names at exact file offsets recorded in `evidence/public-alc-static-2026-10-19.json`. Names alone do not prove their behavior or module firmware mechanism.

REA Ghidra profile digest `4531371b0cad74a5ee44abb3b039e82bcdb881523a2c7a2a250bc3d214e1b45a` imported the ordinary ARM64 ELF. String Evidence `ev_b3bdd94da9848510dd1e2245ddf2bd25b77ecf5f2fd5065ea1ed2252435f4574` identifies `_create_mqb_alc_steering_control` at0x16c050. Read Evidence `ev_0937b05d6c2676ba27cca1b5f43e15d9d6d65903e7e33b51af4bb7a42358b99f` observes a method-record candidate at0x191c90 with name pointer0x16c050, function pointer0x14b354 and flags0x82. Default analysis did not recover a procedure at that pointer; no CAN algorithm or function behavior is claimed. Export: `evidence/public-alc-rea-bundle-2026-10-19.json`; private snapshot under analysis/public-alc. Target closed after export. Never loaded/imported as Python or executed.

This recovers host-side integration material and a reproducible static lead. It does not recover EPS-side firmware/schematic, establish 1061 compatibility, identify January2026 behavior, or validate claims about failure handling. These remain separate evidence dependencies.

## F027: pinned shared Ghidra endpoint is reachable

Evidence type: live pinned-source observation and targeted network connectivity/protocol checks, October 19, 2026 at 18:52 UTC. Pinned source: miso, January 12, 2023 3:20 PM in the reviewed MQB thread. Host138.68.55.155 accepts TCP on documented default ports13100/13101/13102; all return the same public self-signed CN=GhidraServer TLS certificate, SHA-256 `8fb96531093f38f444373d43354620c5e22e643378eed1ec268beddce48cadae`, valid September15,2026 to September14,2028. Source documentation hash and exact network observations are retained in `evidence/shared-ghidra-reachability-2026-10-19.json`. Binary offsets do not apply to a network/tooling observation.

This verifies a live responding endpoint consistent with Ghidra. It does not verify authenticated server identity, server version, account access, repository contents, or surviving MQB annotations. No credentials sent or retained, no registry/project enumeration, no remote mutation. The older January2026 participant login failure is historical context, not the result of a current login test.

## F028: pinned login rejected; anonymous connection exposes no repositories

Evidence type: user-authorized client protocol/authentication and read-only repository-list observation, October19,2026. Endpoint and certificate hash as F027. Ghidra12.1.4 encounters legacy9.0 registry binding incompatibility. Official Ghidra11.4.2 ZIP SHA-256 `795a02076af16257bd6f3f4736c4fc152ce9ff1f95df35cd47e2adc086e037a6` is compatible. Missing SAN was handled in an isolated client process using exact certificate fingerprint validation and certificate validity checks, not arbitrary trust or global changes.

One pinned shared-account/default-password login was rejected with `FailedLoginException`. The server offered anonymous read-only access, which connected and returned an empty visible-repository list. Zero notes retrieved. Source/helper hashes, timestamps, release identity and sanitized outcomes are in `evidence/shared-ghidra-access-2026-10-19.json`. Credentials are deliberately absent; no firmware offsets apply to a server-access observation.

Limits:9.0 is a registry protocol label, not exact server release. A failed credential pair does not identify the cause. Empty anonymous visibility does not establish repository deletion or authenticated visibility. No remote mutation or credential rotation. This advances the annotation-recovery investigation but does not recover MQB notes; working authenticated access or export is still needed.

## F029: shared-account expiration and recurring access failures reported

Evidence type: live Discord source observation, not a verified server configuration. Sanitized record `evidence/discord-ghidra-access-search-2026-10-19.json`, SHA-256 `43e8684f4796be80ba2e2167691ec308ac519339f830132f479c2c5bc6499028`. Exact source links and displayed dates are in the record; firmware offsets do not apply. CzokNorris reported 30-day expiry for unchanged default-password accounts on September 2, 2023, and repository permission repairs on September 19. Miso reported an alive server but failed login on January 2, 2026. Reviewed results provide no verified replacement login or endpoint. Expiry is consistent with F028, but its current cause remains unverified. A PQ project-backup attachment is a separate uninspected recovery lead and is not attributed to MQB. No credentials retained or remote mutations.

## F030: HCA-associated decoder and magnitude eligibility threshold

Evidence type: direct static Ghidra12.1.4 instructions/data plus external protocol corroboration and analyst inference. Exact mapped image SHA-256 `a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d`, base0x2000; H1 SHA-256 `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641`, base0xf000. REA V850 admission remains unsupported; documented direct fallback used, no REA analysis Evidence ID claimed.

Function0x2b530 extracts a nine-bit magnitude from buffer0xfedf9b70+2/+3, bit31 sign, low-nibble byte4 status and high-nibble byte4 vibration amplitude. Its raw signed input saturates at±500 (instructions0x2b584..0x2b596), then multiplies by2621 and arithmetic-shifts8. It writes0xfedfab26. The external pinned MQB DBC identifies those HCA_01 fields in centiNm. CAN config table entry22 at0x57eb4 stores0x04980000, standard ID0x126 in the firmware's register representation; corresponding buffer entry0x57f34 is0xfedf9b70. Complete receive-index lookup/application initialization remains untraced, so HCA association is a strongly corroborated static inference, not observed execution.

Function0x24aec reads request0xfedfab26, forms absolute magnitude0x24da2..0x24daa, loads flash0x5e638 (`33 0c`,3123, mapped offset0x5c638, H1 offset0x4f638) at0x24e06, and compares at0x24e0c. This feeds eligibility/state conditions, not a standalone output clamp. Interpretation approximately3.0498Nm follows the wire conversion and approximate1024units/Nm scale. Boundary model:±3.05Nm passes this comparison,±3.06Nm fails. Other conditions still apply.

Sources: `evidence/ghidra-hca-limits-1061-2026-10-19.txt`, `evidence/hca-message-linkage-1061-2026-10-19.json`, `evidence/hca-protocol-source-2026-10-19.json`, `evidence/hca-limits-1061-2026-10-19.json`. Full readable interpretation and limitations: TORQUE_LIMITS_1061.md. Original archive unchanged; no target execution or diagnostic/CAN requests.

## F031: HCA-associated output path contains multiple scaling and bound stages

Evidence type/artifact identity/profile as F030. Function0x24aec multiplies the enabled request by interpolated curve outputs through pointer group0x5f738, shifts13, saturates at±6144, multiplies by flash0x5e804 (`9a 21`,8602, mapped offset0x5c804, H1 offset0x4f804), shifts13 and saturates again. Instructions0x254d6..0x25560. Three six-point curves at0x5fcde/0x5fcfa/0x5fd16 have shared raw axes `[0,1920,3200,6400,9600,12800]`; helper0x387e2/0x38746 establishes unsigned piecewise-linear table layout. Actual active selection and physical axis units are unresolved.

Function0x24694 consumes intermediate0xfedfab90, applies state and step constraints plus symmetric bound from0x5e63a (`cd 0e`,3789, mapped offset0x5c63a, H1 offset0x4f63a), and stores0xfedfab94. Approximate interpretations are±6Nm intermediate saturation,1.05005 multiplier,±3.7002Nm downstream target bound. They are intermediate signal interpretations, not measured motor-output limits.

The read-only reader verifies exact image SHA-256 and emits bytes, offsets, scalars, raw curves and narrowly scoped arithmetic examples. Exports as F030 plus `evidence/ghidra-hca-message-tables-1061-2026-10-19.txt`. Next: trace0xfedfab94 through arbitration/driver override/motor current; resolve curve profile selection and data-flash dependencies. No patch or usable modification is established.

## F032: HCA request reaches two selected/shared assist contributions

Evidence type: direct Ghidra12.1.4 static references/instructions, decompiler-assisted data flow and bounded analyst interpretation. Mapped SHA-256 `a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d`, base0x2000; H1 SHA-256 `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641`, base0xf000. Existing refined database opened read-only without reanalysis. Direct fallback per REA readiness; no REA Evidence IDs claimed.

Function0x244fe passes bounded0xfedfab94 as primary contribution to0x36e02(channel0), and forms a secondary correction using flash0x5e62a=2621 Q15, profile curve, sign term0x5e802=0, symmetric correction bound0x5e634=511, plus vibration0xfedfab96. Constant offsets: mapped0x5c62a/0x5c802/0x5c634, H1 0x4f62a/0x4f802/0x4f634. Selection0x36d64/36d80 and matching-channel setters gate this route.0x36c46 sums selected and other additive contributions into0xfedfaafc and0xfedfaaf8. Primary shared value read0x25994 contributes to0xfedfab48 and curve processing in0x258b0, bounded by0x5e5d8=4813 (mapped0x5c5d8/H1 0x4f5d8) into0xfedfab4a at0x25be6, then0x255dc produces0xfedfab3e.0x2143e sums that result and secondary0xfedfaaf8 with additional terms into0xfedfab30 at0x21846.

Separate float mirror setter0x37b3a feeds consistency checker0x373d2, comparing against the fixed-point sums and reporting discrepancy identifier0x3eda. This branch is not a second demonstrated motor command. Shared quantities and checks prevent treating the entire path as one scalar clamp.

Exports: `evidence/ghidra-hca-downstream-1061-2026-10-19.txt`, `evidence/ghidra-hca-motor-chain-1061-2026-10-19.txt`. Readable ledger: HCA_DOWNSTREAM_1061.md. Limits: additional channel meanings, complete priority behavior, curve axes/active profile and runtime values remain unverified. Approximate Nm interpretations are signal-scale inferences, not physical torque measurements.

## F033: static command path reaches documented U/V/W PWM registers

Evidence type/artifact identity/profile as F032. Chain0xfedfab30 ->0x3671a/fedfac04 ->0x361e4/fabfc ->0x3660a/fabfe ->0x4a494/fab2a ->0x463e2 ->32-byte double buffer ->0x1da5a ->0x18e72 ->0x18ed6 ->0x3ebbc. Buffer helpers0x4636e/46380/46390 use0xfedfc2ac and0xfedfc2cc, with producer and consumer slot2 both at byte offset4.0x1da5a subtracts transformed feedback and integrates error; phase outputs support a motor-control interpretation.

At0x3ebbc input is capped to2500; writes at0x3ebe0/0x3ebec/0x3ebf8 store2500-input to0xffffccb0/0xffffccb4/0xffffccb8. The manufacturer-authored hardware manual SHA-256 `f2914aa669635072756bc530485d8bc690dede0e8398b51ee6adcc3b62b3bd22`, table15-2 printed887/PDF907 and table15-6 printed892/PDF912, identifies TSG20 short base0xffffcc00 and HT-PWM U/V/W compare offsets0xb0/0xb4/0xb8. This independently identifies the peripheral endpoint;2500 is not a torque/current unit.

Sources: `evidence/hca-motor-chain-1061-2026-10-19.json` includes82 selected exact reference sites, source hashes, function spans and buffer alignment; full selected instructions in `evidence/ghidra-hca-motor-chain-1061-2026-10-19.txt`. Limit: large0x463e2 and0x1da5a decompilations have warnings; the whole data flow has not been independently proved instruction by instruction or run.0x603f8/0x604d8 holdffff in this map, so controller calibration origin, variant applicability and tp context must be resolved before numeric motor-current interpretation. No physical output ceiling, runtime activation, firmware change or hardware experiment demonstrated.

## F034: blank controller page has embedded boot-selected defaults

Evidence type: direct static instruction/byte observations and conditional analyst copy model, October 20, 2026. Mapped SHA-256 `a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d`, base `0x2000`; H1 SHA-256 `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641`, base `0xf000`. No database reanalysis or target execution.

`0x90e0` tests words `0x60000/0x60ffc` for all ones; `0x9462` calls `0x912a` on result `0xa2`. `0x90be` uses type `0xa8` lookup `0xbaa0`, reads byte `+7` below 7 or defaults to zero. The lookup walks low flash `[0x1000,0x1ff0)`, absent from the update. `0x90fc` selects source `0x61000 + index*0x6c0` and requires identity byte `+0x6b3` to match. Records 0/1/2 pass; slots 3..6 repeat identity 2 and fail. The full boot instructions after indirect calls at `0x915c/0x9176/0x91cc/0x9206` construct RAM data and pass body length `0x6b0` to destination `0x60000`, then 16 metadata bytes to `0x60ff0`. Interface table `0x2000` resolves to `0x7a0e/0x7aec/0x7b7c/0x7b34/0x7ac4`; wrapper behavior supports page initialization/erase/program/verify/finalize inference, not observed successful flash writes. Existing decompilation omits the manually resumed continuation `0x915e..0x922b`.

The original blank page is H1 offset `0x51000`, mapped offset `0x5e000`, length `0x1000`. Accepted source H1 offsets are `0x52000/0x526c0/0x52d80`. Exact record/page hashes and field offsets are in `evidence/controller-calibration-1061-2026-10-20.json`; read-only exports `ghidra-calibration-context/origin/selection/writer-1061-2026-10-20.txt`. Derived pages are explicitly conditional models under ignored analysis, not original or installed firmware. Current programmed contents, low-flash selector and runtime path remain unknown. This explains candidate defaults without requiring missing data-flash contents.

## F035: candidate controller clamp and conversion values become readable

Evidence type/artifact identity as F034. Startup `0x100c0..0x100d6` computes `tp=0x5d800`; recognized-instruction scan below `0x55606` finds only boot/application startup writes, not a downstream reassignment. Saved context is seeded and not independent proof; unknown control flow remains a limit. Controller `0x4805a/5e` resolves `tp+0x2bf8` to signed clamp `0x603f8`. Conditional records all supply `00 24`, 9216. Source addresses `0x613f8/0x61ab8/0x62178` correspond to H1 offsets `0x523f8/0x52ab8/0x53178`.

Multiplier `0x60112` is loaded at `0x4789a`, stored to `0xfedf9f6e` at `0x478b4`, reloaded at `0x48058`. Command shift `0x604da` goes into `r25` at `0x479da`; `0x48084..0x480a2` multiply the bounded command, arithmetic-shift and saturate to ±32767. Selectors 0/1/2 yield multipliers 19733/19417/31645, shifts 12/12/13. Parallel shift `0x604d8` is 11 in all three. Subsequent filters/state branches remain material, so this is one conversion stage, not the final controller equation or physical output limit.

Page-redirection alternative: table words `0x5a87c/0x5a880/0x5a884/0x5a888` are `0x5e000/0x5e000/0x5f000/0x60000`. `0x16602` writes selected pairs to `0xfa001300/304`, controls `0xfa0012cc`, polls `0xfa0012d0`, and schedules copies via `0x1649e/0x1679c`. `0x1684a` explicitly translates selected page addresses into `0xfa800000/0xfa801000` windows when enabled. This corroborates redirection capability but not actual enabled state or manufacturer register naming. Runtime calibration can differ from conditional defaults. Details, exact bytes and limitations: CONTROLLER_CALIBRATION_1061.md and its evidence links. Physical current/torque units remain unresolved.

## F036: phase feedback comes from ADC channels and a separate missing calibration record

Evidence type: direct static instructions, initializer bytes, manufacturer register documentation and bounded decompiler-assisted data flow. Mapped SHA-256 `a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d`, base `0x2000`; H1 SHA-256 `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641`, base `0xf000`. Saved refined database read-only, no reanalysis.

Startup copy `0x537e0 -> 0xfedfa8a0` includes source words `0x55010/14` (H1 offsets `0x46010/14`) initializing `0xfedfc0d0/d4` to `0xffffdc40/44`. Applicable manual SHA-256 `f2914aa669635072756bc530485d8bc690dede0e8398b51ee6adcc3b62b3bd22`, printed pages 1733/1795, identifies ADCA0 base `0xffffdc00`, channel result offset `0x3c+4*m`. ADC init `0x3e958` writes `0x50308001` to `0xff81d104`: CTYP=1, CRAC=0, 10-bit right-aligned per printed 1780-1781/1796. This matches `0x1c47e` word reads and mask `0x3ff`. ADC identity does not identify board sensor wiring or amperes.

Pointer `0xfedfc064` has zero initializer at `0x54fa4` (H1 `0x45fa4`). Parser `0x3e34a`, type 2, length `0x20`, sets it to a low-flash record starting from cursor `0x1000`; the region is absent. Mode-zero gain words at record offsets `0x08/0x10`, alternate mode `0x0a/0x12`, are unsigned little-endian. `0x1c47e` computes offset-minus-ADC, rounded gain/1024, then rounded `5285/512` or `4271/2048`, stores signed phase values `0xfedfaac2/c6`, and derives `0xfedfaac4` as their negative sum. Sixteen-sample offset averaging and duplicate checks are explicit. Normal formulas and limitations: CURRENT_FEEDBACK_1061.md. Initial null pointer does not supply missing gain values.

Sources: `evidence/ghidra-current-feedback-1061-2026-10-20.txt`, `evidence/current-feedback-1061-2026-10-20.json`, `evidence/adc-manual-source-2026-10-20.json`, existing calibration startup export. Missing sensor gains and physical transfer/unit definition prevent an amperage conclusion. No ADC acquisition or controller execution performed.

## F037: measured-phase protection and controller normalization both use 2880

Evidence type/artifact identity as F036. Conditional template destinations `0x60404/0x60110/0x60500` hold phase clamp 2880, feedback multiplier 23301 and shift 11 in accepted selectors 0/1/2. Source addresses, bytes, hashes and H1 offsets retained in structured evidence. Controller loads at `0x1ddb2/0x1db3a/0x1dca2`, clamps the two independently measured inputs and normalizes to signed controller units. `2880*23301 >> 11 = 32767`. Later phase/angle transformations and filtering matter. Command slot 2 is read from buffer byte offset 4 at `0x1dcde`, stored stack `+0x1c` at `0x1dce0`, reloaded `0x1e312`, then subtracts transformed feedback `0x1e31e` before error processing.

Separate `0x1cc22` loads threshold `tp-0x772 = 0x5d08e`, bytes `40 0b`, 2880, mapped offset `0x5b08e`, H1 offset `0x4e08e`. It compares absolute `0xfedfaac2/c6`; below threshold resets respective `0xfedfb6d0/d2`, otherwise increments the unsigned 16-bit counter. Either counter >=31 invokes reporting helper `0x1535e(0x15,0,1,1)` at `0x1cc8c`. From reset this is 31 consecutive routine calls, not established milliseconds or ADC periods. The third derived phase is not checked by this routine. Fault reaction remains untraced; no hard shutdown claim.

Entry `0x1c43a` calls acquisition and then `0x1da5a` in the branch where `0xfedfaed8==0`. Controller phase-order byte `0xfedfaf4b` comes from missing type-`0xa8` record byte +6. Source exports above plus `evidence/ghidra-current-entry-protection-1061-2026-10-20.txt` and retained full controller. No mechanical torque ceiling or ampere units established. This is a raw feedback/protection finding, not a demonstrated modification.
