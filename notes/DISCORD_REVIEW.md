# Discord history review

Reviewed and merged October 19, 2026. This expands the initial review with dated source anchors, individual workstream stopping points, and priorities for recovering prior work.

Sources: [67 dated message anchors](../evidence/discord-history-2026-10-19/SOURCE_ANCHORS.tsv), [source and attachment register](../evidence/discord-history-2026-10-19/SOURCES.json). Findings DH-01 through DH-12 are integrated into [FINDINGS.md](FINDINGS.md#discord-history-findings).

## Main conclusion

The thread began as a firmware torque-hack effort for MQB 5Q0/3Q0 steering racks. It did not publish a reproducible firmware torque patch in the material examined. It produced a shared research collection, architecture leads, a partial extraction workflow, a historical security-access-table claim, useful reports about PLA behavior, and vehicle-specific connector research. Discussion then moved toward an external HCA/DSR mixer, and much later toward an external module called ALC. ALC developers reported one MQB GTI installation in January 2026 and explicitly said it required no firmware flashing. Those are different technical paths with different unfinished work.

The latest visible messages, August 10, 2026, revisit a connector previously dismissed during a Golf GTE investigation. Teal proposes that filtering there could work. No subsequent implementation, harness delivery, PHEV installation, or test result was visible. The thread stops at a newly proposed wiring interpretation, not at a final technical verdict that the connector cannot be used.

## Source and scope

- Live source: RetroPilot, bounties, [MQB VW Rack FW Hack (5Q0, 3Q0)](https://discord.com/channels/660951518014341124/1063188305514090546).
- Read accessible native Discord message text in overlapping loaded sections from January 12, 2023 through August 10, 2026. Returned to latest messages with no older-message banner in the final observed state.
- Source anchors below use author, displayed date, and time. They are not individual message permalinks. Discord displayed dates/times were retained without asserting a UTC conversion.
- Images, video frames, attachment bytes, external linked pages, the separate Konn3kt server, and remote Ghidra contents were not independently reviewed. The native screenshot returned a blank image, so this pass relies on accessible text rather than inventing visual interpretations.
- Read the existing orientation notes and the initial Git version of `notes/DISCORD_REVIEW.md`. This report extends that account with more precise stopping points and source anchors; it is not an independent reproduction of technical results.
- Read the imported MQB README as historical prose only. Did not decode firmware, import binaries, run tools, send CAN, flash anything, log into a shared server, join a server, message anyone, or add reactions.
- Historical credentials are omitted. No raw AX transcript containing credentials has been saved.

Evidence classes: **observed statement** means the message was read live; **participant result** means its author reports doing/seeing something; **proposal** means no completed result accompanies it; **interpretation** means this review's synthesis. A participant result is not independent verification.

## What they were trying to achieve

The opening post, CzokNorris, January 12, 2023 3:10 PM, explicitly scopes the thread to MQB rack reverse engineering and torque hacking. Later discussion makes the practical motivation clear: obtain more steering authority than the HCA/LKAS path provides for computer-controlled lateral assistance. The participants considered several ways to do that:

| Path | Intended change | What the thread actually reaches |
| --- | --- | --- |
| Firmware modification | Understand and change internal EPS limits or maps | Update-file collection and analysis leads; no reproducible patched MQB firmware or round-trip flashing demonstration |
| HCA/DSR mixing | Combine two existing steering-request paths through an inline CAN module | Proposed arithmetic and test plan; explicitly still untested June 29, 2023 |
| PLA angle control | Reuse parking assistance's stronger angle-control capability | Participant reports of actual experiments, followed by detailed objections about motor output and steering rate |
| Speed spoofing | Change speed as perceived by EPS to change assistance | Suggested in 2023 and discussed again in 2024; no measured implementation in the reviewed thread |
| ALC module | Later angle lateral control using an added EPS-side module | Claimed GTI installation, demo attachments, and an attempted PHEV harness expansion; implementation absent from the examined material |

Do not equate ALC with HCA/DSR mixing or torque-sensor interception. The thread does not establish that mechanism. The acronym and the discussion's proximity to PLA do not establish its exact CAN algorithm either.

## January to April 2023: what the firmware work established

**They organized shared material.** On January 12, miso reported 1061 on their own Mk7, which does not identify the user's vehicle. miso also linked the firmware/docs Drive folder, asked that important workflows and details be kept in per-firmware notes, then reported adding available original firmware files. CzokNorris offered the existing PQ Ghidra server and an MQB folder using existing accounts. The content may therefore be split between the local archive, Drive documents, and remote Ghidra annotations. A local firmware directory is not proof that all annotations were preserved.

**They separated some hardware families, after initial confusion.** On January 20, miso described MQB-A0 column-mounted TRW units and TriCore chips. On February 18, ole described 5Q0 rack photos and V850 decoding in Ghidra. miso then clarified that the unit they had taken apart was 2Q1 and that the rack-mounted hardware was uncertain. The useful conclusion is that the original TriCore claim was grounded in a different family. Ole's V850 observation is a stronger lead for 5Q0, but does not identify this project's exact board or prove its memory map. aw.entity's difficulty identifying part numbers did not resolve the issue.

**They did not have a known MQB hardware dump.** miso explicitly says this April 16, 8:32 and 8:51 AM, and reiterates the distinction April 23. FLcruising initially thought the earlier discussion implied a 5Q0 dump, then questioned VCP's actual capabilities. The exchange corrects a consequential ambiguity: exporting or decoding a flash update file is different from reading a module's installed flash. VCDS diagnostics/coding are also different from dumping firmware.

**The flashing pathway was a research idea, not a completed deliverable.** On April 23, dkiiv proposed reverse engineering VCP's flash procedure as a way forward, expressed uncertainty about read/edit/write, recalled an unsuccessful attempt to load what they called encrypted material into Ghidra, and then reconsidered the claim. This does not prove the payload remains encrypted today or that every current extracted file is unusable. It documents their uncertainty at that time. Buying a spare rack and adapting Willem's PQ V850 work was suggested, but no completed MQB replication follows in the reviewed thread.

### Historical local README: work worth preserving without overstating it

The imported `EPS_research/MQB/5Q0, 3Q0/README.md` contains additional historical work that is more concrete than the thread's short messages:

- An FRF-to-ODX-to-hex-to-binary-to-Ghidra workflow. Its recommendation to use the longest flash block is explicitly marked unverified. Preserve that warning. Do not repeat the legacy installation steps merely to re-establish what they did.
- A claimed security-access-code table starting at `0x00048a20` for firmware associated with `5Q0 909 144 R`. It describes two-byte codes in eight-byte entries with a flag-like field increasing through `01`, `02`, `04`, `08`, `10`.
- Known code values said to have been located: 28183, 44595, 19249. Additional values 44922 and 21230 were explicitly not tested. This is a historical localization claim, not proof the unknown values work, not seed/key bypass work, and not identification of steering torque maps.
- A compatibility list attributed to one ODX file. It is not an observed record of successfully cross-flashing all listed racks.

This pass did not inspect bytes or verify that offset. Exact README identity is recorded in the [source register](../evidence/discord-history-2026-10-19/SOURCES.json); its full prose provides context beyond this paraphrase. Do not attach the README's offset automatically to every H1/H2/H7 variant. The historical note does not name its binary hash. Concurrent offline work has since verified the H1 bytes and found mixed byte order in the last two historical values; see F019 and F020 in [FINDINGS.md](FINDINGS.md). That newer local evidence supersedes treating the table pattern as wholly unverified. Subsequent F024 establishes a static diagnostic service 0x27 consumer and access-mask references. Runtime acceptance and steering relevance remain unverified.

## May to June 2023: why they turned toward a CAN module

On May 16, dkiiv proposed a device between the EPS and the car translating HCA into a combined HCA and DSR request. They described DSR as a steering request from ABS during instability. The proposed 3 Nm plus 3 Nm equals 6 Nm arithmetic was expressly accompanied by uncertainty about MQB and possible different weighting of DSR. It was a hypothesis, not a measured combined-output curve.

On May 22, 11:30 AM, dkiiv said they had effectively given up on a firmware hack for PQ and did not see MQB getting anywhere, while expressing hope for mixing. This is direct evidence of one participant's change of priorities. It is not a formal project cancellation or proof firmware modification is impossible.

Their plan was staged: first quantify DSR alone, then test mixing, then build a custom module. On May 22, 11:33 AM, they mentioned mixed and DSR-quantification firmware branches for Ocelot v1, conditional on freeing time from a custom ACC project. On May 24, 2:44 PM, they described changing the CAN inbox for DSR to support quantification. On June 29, 11:40 AM, they explicitly said the idea was still untested and they were waiting for v1 stock to buy hardware. Paper offered Ocelot v2 hardware and access to another vehicle; UptownBench1187 offered MQB testing if PQ mixing succeeded.

**Stopping point:** a plan, hardware dependencies, and wiring preparation. No posted mixed/DSR branch, quantitative DSR result, or measured MQB combination was found. Recover any existing branch or logs before rewriting their proposed experiment. Do not interpret the later ALC module as proof this specific mixing plan eventually succeeded.

## PLA: actual participant experiments and the correction that matters

The conversation initially includes broad claims that park-assist control can overpower the driver and that cancellation seen in a clip must be external. On May 22, 4:02 PM, ole directly corrects that: in their MQB experience, the rack stops accepting PLA requests above about 5 Nm measured driver torque. They explain that motor output can still exceed that value; the threshold concerns what the driver sensor measures.

Ole then reports rate limiting requested angles because wheel acceleration can itself produce too much sensed force. At 4:05 PM they describe a closed-ground test at 15 km/h where the wheel rotated roughly 90 degrees before they stopped it, despite knowing the event would occur within the next minute.

On May 24, 2:00 PM, ole explains the causal issue more precisely: a lightly held wheel generates little measured driver torque, allowing high motor output and fast motion before the driver can react. Reducing the cancellation threshold alone does not establish acceptable motor torque or steering rate. External limits move the trust requirement into the external controller.

These are technically useful participant results and explanations, not independently measured limits for our target. The 2.85 Nm SPAS value mentioned by Paper refers to Hyundai discussion and must not be carried into MQB. The thread's ASIL arguments also contain disputed assertions; they do not certify any rack or proposed module.

**Stopping point:** no agreed reproducible PLA-based solution with demonstrated safeguards in this thread. This was a reason for skepticism and redirection, rather than a lack of evidence that the rack could move strongly.

## June 2023 wiring research: concrete reusable work

The June 29 conversation progresses from a plausible connector photograph to physical tracing. An early candidate was questioned as having too many wires. At 12:40 PM UptownBench1187 reports finding the connector; at 12:41 PM they say removing the airbox and battery tray provides access. miso agrees at 12:44 PM that it matches the diagram. This sequence matters: do not treat every earlier photograph as an identified EPS connector.

dkiiv posts harness identifiers `5Q1971111BA` and `5Q1971111AC`, then car-side connector candidates `4H0 973 713` and `3B0 973 813`. The linked listings describe six-way connectors, while an earlier general description says seven MQB wires. This discrepancy is unresolved in this text review and is another reason to recover the actual connector photos and diagram, rather than publish a pinout from prose.

The hope was to have CAN plus power and ground at one insertion point for a simpler harness. It is not a confirmed pin assignment. miso's Golf GTE has an inverter in the relevant area, unlike the ordinary ICE arrangement. UptownBench1187 also reports being able to touch a connector from underneath through the exhaust tunnel, but this is not proof of a practical installation route on the GTE.

**Reusable result:** a dated vehicle-dependent access investigation and candidate connector family. **Still missing:** exact relevant vehicle identification, confirmed wire/pin mapping, and a harness build/test artifact.

## 2024 and 2025: renewed leads, without the missing implementation

On May 12, 2024, ChosenCypher asks about presenting very low speed to EPS. dkiiv responds with 1 mph and objections. No capture, module firmware, measured output, or completed implementation accompanies it in the examined thread.

On March 14, 2025, ole identifies at least three lookup-table groups in steering-map SGO data and asks what the later groups mean. dkiiv suggests return/recentering, HCA/DSR, and TSC; ole tentatively agrees some may be HCA/DSR/TSC and notes two are identical. Both say memory references must be traced to establish meaning. Those labels remain hypotheses. The source SGO identity, exact table offsets, axes, scaling, and consumers are not specified in the read text.

Ole also reports having encountered and driven an MQB prototype rack with unusually high steering authority, reportedly after IAV flashed something. The firsthand component is experiencing the vehicle behavior. The attribution and modification details are secondhand: ole says they were only told that IAV flashed something and had no opportunity to learn more. They describe torque below PLA and some precise low-speed turns with a computer steering wheel. There is no original/modified firmware pair, exact rack identity, patch, map export, or reproducible procedure.

**Stopping point:** evidence that someone outside this thread may have achieved a stronger implementation, plus an unresolved table-identification task. It is not a community patch ready to recover from a posted download.

## January to August 2026: ALC and the exact final state

### Revival and claimed GTI result

On January 2, daniii438 asks about the old server and proposes consolidating EPS/ABS work. miso says they moved to Binary Ninja, checks the server, and reports it appears alive but login fails. Reachability is not proof the shared MQB annotations are recoverable or current.

miso then links a Reddit demo; Teal identifies themselves as its author and names the project ALC, angle lateral control. Six MOV attachments are visible. Teal and armanthenothacker say the setup needs an EPS-side module and no firmware flash. armanthenothacker reports their GTI is the only MQB car with the module at that time, and describes its insertion point as the TML coupling point under the battery.

The developers make favorable safety claims. No code, validation report, failure testing, or independent evidence in the inspected text establishes those claims. jp-solutionz asks whether it is a torque-sensor intercept module and how compatibility works. The visible answer says the project has not been released and information remains scattered, with a Konn3kt beta-testers link. It does not confirm the torque-sensor hypothesis. Broad compatibility statements are ambitions or claims, not a tested matrix.

### PHEV expansion and the roadblock

miso's stated vehicle is a 2015 Golf/Golf GTE PHEV with a C3. Their battery is in the trunk; the inverter obstructs the conventional under-battery location. The developers offer a harness after connector identification. armanthenothacker's January 5 request is specific: show both sides, every pin and wire color, and connector part number. That is the missing deliverable they needed to make the harness concrete.

On January 10, miso struggles to release T14q/T14z connectors and supplies `3C0 973 837 / 3C0 973 737` for T14q. On January 11 they report neither T14q nor T14z affected EPS when unplugged. They cannot readily access C/D/E, believed from the drawing to be near the crash beam, and cannot even see them with an endoscope. These are participant observations on that GTE, not universal MQB topology.

On January 18, Teal questions camera/park-assist faults in the posted context. miso clarifies they do not have those modules; EPS is coded to accept them, causing errors. Do not infer fitted camera/park-assist equipment from those faults.

On January 19, Teal discusses bumper access, direct CAN tapping, and a relay box. These are proposed installation directions and a claimed behavior if the panda is unavailable. The thread does not demonstrate a completed harness or fault-tolerant system. This report is not an instruction to reproduce those physical steps.

### Why the August ending is not a simple failure verdict

March 7 is a reminder, with no technical result. On August 10, Teal replies specifically to miso's January 11 statement that unplugging did not affect EPS, then says the connector works and filtering there could work, tagging armanthenothacker. The final visible message is at 8:23 PM.

The reply context is known, but the exact connector referred to by "that connector" is not established by the final prose. It may reflect a new understanding of filtering/topology rather than the original full-EPS-disconnection criterion. That explanation is an interpretation, not an established circuit fact. Do not resolve it to T14q, T14z, or a pin number without the diagram/images and implementation.

**Final stopping point:** a developer reopens a previously dismissed insertion-point idea. There is no visible follow-through. The physical access obstacle is explicitly documented; the reasons for no later response are not. Do not invent loss of interest, technical impossibility, private success, or project abandonment.

## Participants and where the missing knowledge may live

| Participant | Work visible here | Material that would reduce repeat work |
| --- | --- | --- |
| CzokNorris | Thread creation, shared Ghidra infrastructure | Existing MQB project and annotations, if preserved |
| miso | Drive archive, 2Q1 teardown context, 1061 vehicle, GTE diagrams and connector work | Per-firmware notes, extraction history, Binary Ninja work, exact PHEV diagrams |
| ole | 5Q0 V850 lead, PLA experiment report, map observations, prototype experience | Specific photos, SGO identity/table offsets, original logs and rack identities |
| dkiiv | Mixer proposal, DSR quantification plan, wiring/connector leads | Ocelot branches, any DSR measurements or later test records |
| UptownBench1187 | Physical MQB connector tracing and photos | Confirmed connector photos, vehicle details, tracing result |
| FLcruising | Corrected update-file/module-dump confusion; PQ references | Applicable prior V850 methodology, without assuming MQB equivalence |
| Teal and armanthenothacker | ALC demos, claimed GTI installation, harness offer, final filtering idea | ALC source, hardware design, known working GTI identity, compatibility and failure behavior |
| daniii438 | 2026 server revival/consolidation proposal | Whether a later consolidated project preserved old annotations |

This is a provenance map, not permission or a request to contact anyone. No outreach was performed.

## Avoiding duplicate work

1. **Preserve the local collection and its notes before collecting another firmware bundle.** The Git initial import already contains the MQB README and 1061 variants. The concurrent offline analysis covers bytes, lineage, V850 decoding, and a corroborated static map; see [OFFLINE_ANALYSIS.md](OFFLINE_ANALYSIS.md). The Discord review did not duplicate that work.
2. **Recover analysis state before recreating every annotation.** A shared Ghidra project and later Binary Ninja use are explicitly mentioned. File-only archive completeness is unknown. There is no basis here to assume the existing local PQ `.gzf` files are an MQB analysis database.
3. **Reuse the table verification already recorded in F019/F020.** The original author did not identify a binary hash, but the local H1 table pattern and static address are now documented. Trace purpose and references next, rather than repeating byte discovery. Do not carry the last two historical code interpretations forward without the byte-order correction.
4. **For map work, recover the March 2025 SGO and plotted data first.** The unanswered task is proving table consumers, not deciding a label by appearance. Many local SGO paths belong to PQ; the file extension does not make them the MQB source ole discussed.
5. **For mixing, find existing DSR-only and mixed firmware/logs before implementing them again.** The thread contains a test plan but no demonstrated outcome. Treat silence as missing evidence.
6. **For ALC, recover the actual implementation before inferring the mechanism from branding or a demo.** A successful GTI report does not prove applicability to 5Q0 909 144 R / 1061 or to the GTE. It also does not solve the firmware modification task.
7. **Recover the exact August connector context before restarting physical connector discovery.** January's no-effect result and August's filtering proposal must be reconciled, not flattened into a final negative result.
8. **Keep artifact analysis, source recovery, and vehicle work separate.** Current scope supports offline research. The historical thread does not authorize flashing, actuation, wiring changes, or bench work.

## Questions the record cannot answer yet

- Was an MQB full flash dump later obtained elsewhere? Nothing reviewed here proves it.
- What exact boards, firmware variants, and load addresses were used in the old Ghidra work?
- Did dkiiv ever finish DSR quantification or the mixing module after June 2023?
- Which SGO and offsets produced ole's March 2025 plots? Were those maps available for this target?
- What did IAV actually change, on which rack, and can any original/modified artifact be recovered?
- Does ALC use PLA frames, torque-sensor interception, another CAN translation, or a combination? The reviewed text does not establish it.
- What branch/hardware was used for the GTI, and what controls or failures were tested?
- Which connector did Teal mean in August, and why would filtering there work despite January's disconnect result?
- Did the work continue in Konn3kt or another private branch? The linked server was not inspected.

These are the remaining evidence-recovery tasks. No additional general firmware collection or speculative retelling resolves them.
