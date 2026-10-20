# Session log

## October 19, 2026: local project bootstrap and historical orientation

Request: resume MQB steering-rack reverse engineering, first synchronize understanding and prepare REA, review the open Discord thread, initialize local Git, and keep project-local agent notes.

Actions: read REA skill v42; queried live REA 6.7.0 and verified package alignment; inventoried 694 original files; reviewed Discord message text from January 2023 through August 2026; initialized local Git on main; wrote project entry points, current status, target, history review, finding ledger, and readiness notes.

User supplied J500 diagnostic identification for 5Q0 909 144 R, EPS_MQB_ZFLS 126 1061. Existing archive has matching part-number/version update artifacts. H1/H2/H7 applicability remains unknown.

Results: no reproducible firmware torque modification was established by this preparation pass. The history includes a separate ALC external-module claim on a GTI in 2026. Ghidra is unconfigured; Hopper is available but MCU applicability is not established. No original archive file was modified or executed. No remote configured, no messages sent, no hardware accessed, and no provider installation performed.

Validation: regenerated the manifest with identical output and matching archive hashes. Verified the SHA-256 of each staged Git blob against all 694 archive records. Added .gitattributes to preserve imported bytes and original line endings. New files passed git diff --cached --check and JSON parsing.

Next action: compare the selected 1061 ODX flash-block metadata and extracted bytes; determine CPU/import settings and provider requirements from exact artifacts. See STATUS.md for outstanding gates and the final Git history for the bootstrap snapshot.

## October 19, 2026: configure the decompiler

Request: help configure software decompilation with REA and identify what remains outstanding.

Confirmed live REA 6.7.0 provider state and inspected its installed raw-import code. V850 and TriCore are absent from raw-binary admission; the Ghidra profile also rejects language overrides on raw imports. Installing an engine does not resolve this API limitation.

Downloaded official Ghidra 12.1.4, checked its release API SHA-256, extracted under ignored `analysis/tools/`, restored archive permissions, and built its missing macOS arm64 decompiler using existing clang/make/bison. Existing OpenJDK 25.0.2 meets the installation's Java bounds. All Ghidra prerequisite checks passed through the new project CLI launcher, scripts/rea-ghidra.

Prepared the scoped Codex setup dry run with skill replacement disabled, then applied the same configuration under the user's request. Setup returned ready. Verified the pre-change backup exists and that unrelated TOML settings are unchanged. Existing live MCP process still needs reconnect/restart; CLI is usable now.

Also parsed selected 1061 ODX flash blocks without changing originals. H1 binary matches its ODX FD_0DATA exactly; H7 binary is one byte longer and has a different hash. Recorded block identities and limits in evidence/odx-block-inventory-2026-10-19.json.

Remaining: restart/reconnect MCP, resolve supported firmware raw import, establish CPU and memory mapping, characterize H7 extraction, and obtain actual target decompilation evidence. No rack firmware was executed, modified, or flashed.

## October 19, 2026: resume after restart and advance offline action items

Request: read the last project chat and work on its remaining action items. Read “Prepare REA for MQB rack” and required orientation notes. Starting Git worktree was clean. Used REA skill v42; split the independent local CPU/document evidence review into a read-only worker while examining ODX lineage.

Results:

- Live REA 6.7.0 is aligned and now sees Ghidra 12.1.4. All eight prerequisites pass. Exported selected restart verification.
- Added `scripts/inspect_1061_odx.py`: deterministic XML metadata and candidate FRF identities, exact FLASHDATA extraction into ignored analysis files, CRC32 checks, historical binary comparisons, and table-byte observations. All three DATA CRC32 declarations match. FRF conversion remains unverified.
- Resolved H7 discrepancy as exactly one extra leading zero in the historical binary. Preserved it; made clean derived copies for H1/H2/H7.
- Shared expected hardware IDs and differing small download addresses favor separate component/download roles rather than three hardware variants. Runtime mapping remains unknown.
- Local documentation and standalone image search supplied no artifact-bound silicon identity. Generic manuals and contradictory family folder labels cannot select CPU.
- Direct Ghidra competing probes favor V850-family little-endian code in H1. Sample exports contain coherent calls, returns, branches, and prologues, unlike TriCore. A bounded candidate function at file offset 0x78 successfully decompiled. This uses an explicitly provisional profile and offset coordinates, not a verified CPU load map. No original firmware or legacy utility was executed. No REA native target opened.
- Confirmed five-row byte pattern at H1 0x48a20. The first three historical values match; the last two historical values use big-endian while the first three use little-endian. Recorded raw bytes and both interpretations without asserting working security access.

Evidence: `evidence/odx-lineage-2026-10-19.json`, restart verification, three Ghidra text exports, tool/profile hash report, and archive-integrity report. Added OFFLINE_ANALYSIS.md with reproduction and unresolved gates. Direct Ghidra evidence has no REA Evidence ID.

Validation: extraction report reproduced byte-identically; three matching CRC32 checks; all 694 original archive identities rechecked with zero mismatches; direct function decompiler returned completed=true. Meaningful remaining gates are FRF conversion, exact V850 generation/MCU, runtime mapping/component relationships, and code references to the table. No steering modifications, hardware access, network publication, or community messages.

Next concrete action: decode bounded H7 initialization and H2 pointer targets to test cross-component address hypotheses before full analysis, as described in STATUS.md.

### Same-session continuation: map corroboration and first mapped analysis

Followed the H7 initialization/address lead before ending the session. Found H7 is exactly H2's final 0x6000 bytes. H7's absolute software return address 0x915e and next-instruction offset 0x15e support base 0x9000; shared bytes support H2 base 0x2000. H7 references a pointer table at 0x2000, matching H2's leading words and plausible function starts. H1 at 0xf000 places its absolute 0xfb48 reference on matching pointer/flag records.

Added `scripts/build_1061_map.py` with exact input-hash guards and overlap validation. It emits only H2 + H1, 516096 bytes, SHA-256 a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d, covering 0x2000..0x7ffff. Missing low flash is not invented. H7 is not appended twice.

Direct Ghidra mapped import completed default analysis in 28 seconds with bounded seeds. Memory-block bytes and a reference 0xf088 -> 0xfb48 corroborate the working map; function 0xf078 decompiled successfully. The historical table is at 0x57a20. No direct references were recovered across 0x57a00..0x57a60 inclusive. Analysis also warned about invalid flows into likely data and nonexistent memory; 1907 candidate functions are not verified real functions. Saved database remains in analysis/1061/ghidra/mapped-1061.gpr. Evidence exports include hashes and explicit limitations in F020 and OFFLINE_ANALYSIS.md.

Next action superseding the earlier entry: refine code/data boundaries, particularly broad candidate 0x55900, then trace computed/indirect table access. FRF conversion and exact MCU identification remain separate evidence gaps. No hardware actuation or firmware execution occurred.

## October 19, 2026: detailed Discord review and shared-note merge

Request: obtain an in-depth understanding of the open Discord thread's goals, accomplishments, roadblocks, and final state. Discord information gathering only. Other agents are active; keep notes separate for later merge.

Read `git status --short`, README, shared STATUS, DISCORD_REVIEW, REA_READINESS, initial Git history, and the imported MQB README. The initial history was `167f9cc` then `efe0cce`; other agents had untracked and later tracked-file changes. Did not reset, stage, stash, commit, or alter their work.

Used native Discord accessibility observations, scroll navigation, Jump To Top/Home, and Jump To Present to examine overlapping loaded message sections. Reached the thread's opening and final visible August 10, 2026 activity. Final observed state has the latest replies and no older-message banner. The screenshot returned blank, so no claim of visual media analysis is made. No messages or reactions were sent.

Results: [DISCORD_REVIEW.md](DISCORD_REVIEW.md) provides the research synthesis, participant map, distinctions between claims and results, and priorities to avoid duplication. `evidence/discord-history-2026-10-19/SOURCE_ANCHORS.tsv` records selected dated message anchors as paraphrases. `evidence/discord-history-2026-10-19/SOURCES.json` records source identities and the historical README hash. These are research notes, not firmware evidence or a lossless transcript.

Unresolved: source implementation, media contents, Ghidra/Binary Ninja state, exact 2025 SGO identity, IAV modification provenance, and final connector topology. No conclusion about why anyone stopped replying beyond the documented constraints.

The review was initially isolated per user request. The user then explicitly requested merging all of this agent's notes. Expanded DISCORD_REVIEW.md, appended DH-01 through DH-12 to FINDINGS.md, integrated status/source-recovery priorities, and relocated the 67 anchors plus source/attachment metadata to evidence/discord-history-2026-10-19/. Removed the redundant private notes after integrating them. Preserved the other agents' current offline results and reconciled the historical security-table discussion with F019/F020. No Git commit, staging, archive edit, or Discord interaction was needed for the merge.

Merge validation: checked source-register JSON, source hashes, all 67 TSV records, local links, and whitespace. Shared findings and session history that predated this merge were retained verbatim. Next action: continue the current offline work in STATUS.md while recovering the specifically identified missing historical sources.

## October 19, 2026: finish available offline action items and investigate public sources

Request: continue until remaining action items are complete, updated and documented; search newly added notes. User subsequently confirmed no additional local material and explicitly authorized public internet research. Read current Git status and required project notes, reconciled the expanded Discord review and source register. Preserved concurrent additions. Used REA skill v42 and PDF skill. Independent FRF, MCU and source-recovery work ran in parallel; integrated only supported results.

Resolved FRF -> ODX lineage using a narrow inspected implementation of VW_Flash's pinned container transform. All three derived XML members equal the archived ODX exactly, ZIP CRCs pass, and all six ERASE/DATA payloads equal prior extraction. Original archive and legacy utilities were not executed or modified. Preserved license/source provenance and exact transformation offsets.

Recovered the historical 5Q0 board photo with D70F3506 marking, primary Renesas part/device documents, and the complete manufacturer-authored V850E2/Px4 manual through a public mirror. Source hashes and mirror limitation are retained. Printed page 24/PDF 44 explicitly confirms 3506/3507 512 KiB code flash,32 KiB data flash and40 KiB RAM at fedf6000..fedfffff, agreeing with firmware startup. Parent independently extracted/rendered/read that table. Recovered named peripheral windows. Physical user-board binding and missing original contents remain absent; no neighboring rack assumptions.

Traced startup register values tp=0x5d800 / gp=0xfee01000. Found historical table consumer 0x2fd96 through tp-relative displacement -5de0, resolving address 0x57a20. Service descriptor 0x582fc binds service 0x27 to dispatcher 0x30006; state machine uses five eight-byte rows, a conditional constant transform, and access-mask writes to 0xfedfaf85. Traced mask consumers in other diagnostic handlers. Typed the constants as uint32-plus-mask records, correcting pointer-like automatic types. No code values, diagnostic behavior or steering effects were tested on hardware.

Explained false-code expansion: the word 0x55900 at 0x78318 belongs to 30 consecutive exact squares, rather than a function-pointer table. Code tail ends 0x55606, followed by FF padding to 0x55800 and metadata. Preserved broad database; created refined-1061 with candidate constant partition, typed records, startup application register context, and uninitialized manual-confirmed RAM. Candidate function count 1757 replaces broad 1907 only as an analysis count. Remaining indirect-flow/uninitialized-memory warnings documented.

Source recovery inventoried 120 local SGOs, two PQ-named databases, 18 public Drive folder listings, selected current Ocelot source/history and public ALC sources. Found current public MQB ALC host integration in iqinc/iqpilot, pinned release 1b891adc2a8fd27a5365e229d74d08ceea00b2f0. Retrieved manifest-matching public ARM64 host module, 536160 bytes, hash bc3bab44f449522bb5e8ff97bf2a12e02941ef14ff5af6ba10b96e6e72d56775. Bounded static literal/REA metadata inspection retained references and method-record read; default analysis did not recover the selected wrapper function. No algorithm/firmware-mechanism claim. Exported REA bundle, saved private snapshot, closed target. Never imported or executed extension. EPS-side firmware/hardware and original historical maps/annotations/connector images remain unavailable, explicitly not marked solved.

Added a full fresh-project runner and artifact verifier. Executed runner into verified-1061-reproduction; exit 0, saved database, typed diagnostic export byte-identical to retained core evidence. The runner refuses existing names and does not install or execute targets. Syntax/JSON/whitespace/input/source/hash checks and complete 694-file archive integrity are retained in evidence/offline-preparation-validation-2026-10-19.json. No Git remote, push, publication, login, Discord join, outreach, vehicle actuation, flashing or bench experiment.

Consolidated current STATUS, OFFLINE_ANALYSIS, readiness, target and finding ledger F021-F026. Added ACTION_ITEMS.md with completed runnable preparation and unresolved external deliverables. Those dependencies cannot be fabricated from existing updates or a public unlabeled board photo. New independent research can now focus on steering/HCA/DSR data consumers without repeating provider setup, extraction, CPU guessing or table discovery.

## October 19, 2026: check pinned shared Ghidra server

User asked whether the pinned Ghidra connection is still available. Read the live native Discord pinned panel and found miso's January 12, 2023 3:20 PM post. Used the pinned host only; did not save or transmit usernames/password. TCP connects succeeded on documented Ghidra ports 13100, 13101 and 13102. Minimal protocol probes received TLS alerts for plaintext JRMI; public TLS certificate retrieval succeeded on all three ports with identical SHA-256, subject/issuer CN=GhidraServer, validity September 15, 2026 through September 14, 2028. Recorded sanitized evidence. No authentication, registry enumeration, repository operation, community message or server change. Reachability verified; project availability/login remain unverified.

## October 19, 2026: authorized shared-server notes recovery

User explicitly requested trying the pinned connection and grabbing notes. Attempted a normal Ghidra client connection. Initial Java25/Ghidra12.1.4 connection rejected missing certificate SAN before credentials. Used an isolated JVM certificate-pinned trust manager which accepts only the already observed certificate SHA-256 and checks validity, without changing global trust/configuration. Reached registry compatibility check: server advertises legacy9.0 binding, incompatible with12.1.4. This binding does not identify the exact server release.

Downloaded official Ghidra11.4.2 asset from NSA GitHub, verified its published SHA-256, extracted under ignored analysis/tools, and used existing Java21. Compatibility check passed. Supplied one pinned shared-account/default-password pair through non-echoed stdin; never copied values into project notes/source or evidence. Authentication was rejected. Did not try alternative account/password combinations or change passwords.

Checked the server's offered anonymous read-only callback. That connection succeeded and listed zero visible repositories. No repository content, notes, programs or annotations could be retrieved. An empty anonymous list does not prove global repository absence. Disconnected cleanly; all local headless projects/logs remain ignored. No remote write, checkout, creation, upload, password/permission/configuration change or community message. Sanitized evidence in shared-ghidra-access-2026-10-19.json. Working credentials or an original repository export remain the concrete prerequisite.

## October 19, 2026: search Discord for Ghidra login failures

User requested searching the channel for failed login reports or alternative access. Used live read-only native Discord server search for ghidra, password, login, ghidra server and spaced log-in wording. Recovered owner's September 2, 2023 default-account 30-day expiry explanation, September 12 access request, September 19 permission repairs, and January 2, 2026 MQB login failure. Read surrounding January discussion: new combined server proposed, no address or replacement login present there. Existing PQ accounts were intended for MQB folder too, but firmware conclusions remain separate. Found September 19 PQ project-backup attachment as an uninspected lead. Saved sanitized evidence, updated F029, STATUS and SOURCE_RECOVERY. No credential retention, account retries, messages, reactions or remote changes. Current auth cause remains unknown; no alternative working login established.

## October 19, 2026: first HCA torque threshold investigation

User requested continuing the Discord firmware effort to view torque limits first. Read current status, historical review, REA readiness and matching existing evidence. Invoked REA skill; live binary_session confirms no native target open and V850 raw admission is still unsupported. Used the established direct Ghidra12.1.4 route, opening refined-1061 read-only with no reanalysis or database saves. A separate source-review agent searched archive/protocol material and used docx skill for capture context. No external messages, login attempts, target execution or hardware operations.

Exported a one-time whole-database function/reference survey under ignored analysis/1061, then exact selected instruction/pseudocode exports under evidence. Matched0x2b530 HCA layout and traced0xfedfab26 into0x24aec. Confirmed flash0x5e638 threshold3123 and exact compare instructions, decoder±500cNm saturation, output curves/gain/saturations and downstream0x24694 bound3789. Pinned public commaai MQB DBC by commit/hash and retained exact field excerpts. Independent table tracing corroborates0x126/buffer entry22, with missing receive-lookup/application initialization coverage explicit.

Added read-only hash-checked scalar/curve reader and TORQUE_LIMITS_1061.md, plus findings F030-F031. Arithmetic boundary model passes±3.05Nm and fails±3.06Nm at the magnitude comparison only; it is not ECU replay. Checked reader reproducibility and exact scalar bytes/offsets against instructions. Captures contain noHCA0x126 and cannot validate a ceiling. Firmware originals unchanged. Next concrete action: follow0xfedfab94 downstream through arbitration/override and motor-current conversion; prove curve selection/axis units and variant/data-flash influence. Changing bytes is not yet a validated modification path.

Validation retained in `evidence/hca-limits-validation-1061-2026-10-19.json`: all694 imported files match original size/SHA-256, reader output is byte-identical on rerun, selected decompilations complete, and narrow305/306 arithmetic boundary checks pass. No existing dirty work was reset or committed.

## October19,2026: HCA downstream continuation to phase PWM

User asked to continue the downstream trace. Started with Git status and current repository orientation/readiness/history, preserved existing dirty changes. Reused the exact saved refined1061 database and prior survey; read-only direct Ghidra12.1.4 export, no reanalysis. REA skill's existing V850 admission limitation/fallback unchanged. Independent read-only subtasks separated the float consistency branch from the physical-output chain.

Traced0xfedfab94 through0x244fe selected primary/secondary fields,0x36c46 shared sums, primary assist-curve path0x258b0/255dc and secondary contribution into0x2143e/fab30. Continued through0x3671a/361e4/3660a/4a494, calibration-dependent0x463e2 conversion, byte-aligned32-byte buffer,0x1da5a feedback controller and0x18e72/18ed6/3ebbc phase outputs. Manufacturer manual independently maps exact three endpoint registers toTSG20 U/V/W HT-PWM compares. Float setter37b3a is read by373d2 consistency checker; retained that distinction.

Exported selected full assembly/pseudocode and structured82-reference chain evidence. Corrected evidence transcription of manual base to0xffffcc00 and verified manual page markers907/912. Wrote HCA_DOWNSTREAM_1061.md and findingsF032-F033. No firmware/database/original edits, vehicle execution, CAN, flashing, legacy utilities, external messages or remote operations. Calibration fields603f8/604d8=ffff make physical current/torque interpretation unresolved; next action: origin/selection of that parameter set, tp context and physical scale linkage.

Validation: selected exports contain the expected input hash and all requested functions decompile; scalar readbacks and hardware-manual SHA-256 verified. All694 original archive files still match manifest. Recorded in evidence/hca-downstream-validation-1061-2026-10-19.json. No runtime or physical-output verification claimed.

## October 20, 2026: resume latest chat and resolve controller calibration origin

User requested reading the end of the latest chat, checking notes and continuing. Read the final turns of "Investigate torque limit visibility", which ended with a concrete plan to verify `tp`, inspect `ffff` controller parameters, trace initialization/selection and decode their use. Read current Git status, README, STATUS, Discord review, readiness and downstream report. Existing dirty work preserved. Applied REA skill and reused the established direct Ghidra V850 fallback and matching saved evidence. No provider setup or network recovery repeated.

Recognized-instruction register scan corroborated startup `tp=0x5d800` with no recognized downstream writes. Both suspicious fields are inside the actual all-FF update page `0x60000..0x61000`. Traced boot endpoint blank check, selector through type `0xa8` in missing low-flash records, embedded defaults at `0x61000 + index*0x6c0` and their identity checks. Recovered bounded instruction continuation omitted by Ghidra's function body after manually linked indirect calls. That continuation stages record data and invokes a page programming interface for body `0x6b0` at `0x60000` and metadata `0x10` at `0x60ff0`. Low-level flash implementation and successful writes remain inferred/unobserved, with no execution.

Added hash-checked calibration reader/model; accepted selectors 0/1/2 all provide clamp 9216. Traced command multiplier 19733/19417/31645 and shifts 12/12/13 into controller arithmetic; parallel shift is 11. Models remain under ignored analysis. Also traced the separate page-redirection table and code that can include the controller page. Current populated contents, selector, enabled redirection and amperes/torque remain unresolved. Missing data flash is no longer the necessary explanation for the embedded defaults.

Saved four focused direct Ghidra exports, structured records and validation under evidence. Added CONTROLLER_CALIBRATION_1061.md, F034-F035 and current status/downstream follow-up. Ghidra database read-only/noanalysis throughout; original archive and mapped image unchanged. Validated model repeatability, byte placements and metadata relocation, identity rejection for selectors 3..6, selected instruction witnesses and all 694 imported files against manifest. No commit, push, remote changes, messages, hardware access, CAN, flashing or target execution. Next offline action: trace selected-template feedback/current scaling into `0x1da5a` and ADC consumers; installed default identification additionally requires provenance-bound low-flash selector evidence.

## October 20, 2026: ADC feedback, missing sensor gains and phase protection

User asked to continue. Started with Git status, README and current notes; reused the saved REA fallback, existing whole-function/reference survey, controller and startup exports. One independent read-only subagent reviewed the manufacturer's ADC documentation per the skill's parallel investigation instructions. Direct Ghidra exports remained read-only/noanalysis; no original or database edits.

Traced initializer words to ADC sample pointers `0xffffdc40/44`, exact ADCA0 channel 1/2 registers. Manual bit definitions independently confirm 10-bit right-aligned configuration via CTL1 `0x50308001`; channel-group register `0xffffdc08` does not control resolution. Traced `0x1c47e` learned offsets, separate low-flash type-2 sensor-gain record, two rounded fixed-point conversion modes, duplicate checks and reconstructed third phase. Missing gain values are now a specific unit-conversion dependency rather than an assumed data-flash problem.

Recovered feedback clamp 2880, multiplier 23301, shift 11 from all three accepted templates, and followed normalization/phase selection/transformation into command-slot-2 error subtraction at `0x1e31e`. Found independent phase protection `0x1cc22`: raw threshold 2880, resets below, increments at or above, reports identifier `0x15` after either counter reaches 31. These are routine calls, not proven time or ADC sample counts. No physical current units, mechanical torque ceiling or actual fault shutdown established.

Saved focused assembly/pseudocode, manufacturer page excerpts and source hash, structured reads and validation. Added CURRENT_FEEDBACK_1061.md and F036-F037; updated STATUS. Checked exact initializer and template readbacks, normalization rounding/saturation, threshold boundary/count arithmetic, exporter completion and original 694-file manifest. No firmware execution, network requests, vehicle/bench activity, flashing, CAN transmission, community messages, commits or pushes. Next concrete offline action: report `0x15` fault table/reaction consumers and protection scheduling. Physical units require absent sensor calibration plus authoritative unit/board transfer evidence.

## October 20, 2026: local Git research checkpoint

User requested bringing Git up to date. Reviewed pending notes, scripts and durable evidence from offline preparation through phase-feedback findings F036-F037. Parsed new JSON and Python files, checked whitespace and scanned pending text for credential-like values with no matches. Included the retained manufacturer documentation and research evidence. The analysis and private directories remain ignored. Saved the research as a local Git checkpoint; no remote is configured, and no remote, push or publication was added.

Staging exposed exporter whitespace and Git CRLF normalization in retained HTML sources. Added a scoped evidence attribute disabling text normalization and whitespace linting for captured evidence, preserving its exact hashed bytes. Source scripts and authored notes retain ordinary whitespace checks. Verified every staged evidence blob against its working-file bytes before committing.


## October 20, 2026: simplify the project introduction

User requested a short, approachable README centered on improving openpilot on VW MQB vehicles. Replaced the workspace-oriented introduction with the project goal, a small key-term table, research coverage, remaining steps and selected reading links. Used current mission and session-closeout reports as the source. Retained the specific 5Q0/1061 target and distinction between offline findings and unverified physical behavior.

Checked README local links and whitespace in the three edited documents. No firmware analysis or implementation resumed. Outstanding research and external dependencies are unchanged; the next research action remains a concise HCA-versus-PLA limits synthesis if separately requested.


## October 20, 2026: recalibrate the openpilot steering goal

User approved the researched direction and requested a local commit. Updated the README and leading status direction to focus on steering authority, response and consistency, starting with existing HCA torque control. PLA remains an alternative; Direct Torque and Angle Hybrid are no longer promised features. Identify the dominant limitation from retained firmware findings and driving data before choosing tuning or targeted firmware changes.

Sources reviewed in the preceding read-only research: commaai/opendbc Volkswagen controller/interface and safety mode, Hyundai interface, torque_data/params.toml, commaai/comma-steering-control, and sunnypilot's Hyundai angle-steering development overview. These establish existing torque requests, separate command limits and modeling options; they do not establish a working MQB modification. See https://github.com/commaai/opendbc/tree/master/opendbc/car/volkswagen and https://github.com/commaai/comma-steering-control.

Validation: checked README links against the staged Git tree and checked staged whitespace. Commit scope is the README plus this documentation session's status/log entries; earlier pending research remains outside the commit. No firmware/archive/database changes, hardware work or push. Next action is the limits-versus-driving-data comparison, if requested.
