# Current status

## Project direction

October 20, 2026: improve openpilot steering authority, response and consistency on VW MQB vehicles, starting with the existing HCA torque-request interface. Firmware changes are a candidate solution to demonstrated restrictions; PLA angle control remains an alternative. Direct Torque and Angle Hybrid labels are not implementation requirements. Success means better path tracking and fewer steering-limit interventions while preserving driver override and bounded steering response.

Next concrete action: synthesize the retained HCA limits and compare them with driving-data evidence of saturation, tracking error, delay or rack rejection. Separate controller tuning from EPS restrictions before choosing a modification. Installed calibration and physical torque conversion remain unresolved. This documentation update does not resume firmware analysis or hardware work.

Updated: October 20, 2026, after tracing ADC phase feedback and a separate phase protection threshold.

## Target and result

User target: J500, SW/HW **5Q0 909 144 R**, **EPS_MQB_ZFLS 126 1061**, ASAM **EV_SteerAssisMQB 012140**. [TARGET.md](TARGET.md) preserves the supplied diagnostic identity.

The runnable offline preparation items are completed and reproduced. The project now has exact container lineage, a supported static hardware/memory profile, a refined annotated Ghidra database, and a traced diagnostic-table consumer. [ACTION_ITEMS.md](ACTION_ITEMS.md) distinguishes those results from missing external evidence, which remains unresolved.

## Verified results

- REA 6.7.0 sees Ghidra 12.1.4 after restart. V850 raw admission remains unsupported in REA; a documented direct Ghidra workflow works without changing the package or mislabeling the architecture.
- Independently decoded all three 1061 FRFs into ZIP/ODX: three byte-identical archived XML matches, valid ZIP CRCs and six exact payload matches. No bundled legacy utility ran.
- Historical H7 has exactly one added leading zero. Clean derived blocks preserve original bytes and hashes.
- H2 maps at `0x2000`, H7 is its exact overlapping suffix at `0x9000`, H1 maps at `0xf000`. Supplied bytes cover `[0x2000,0x80000)` only. Missing low flash is not filled.
- Recovered historical board photo shows D70F3506. Renesas identifies V850E2/PJ4, V850E2M. Applicable full hardware manual confirms code flash, data flash, RAM and peripheral windows. Its exact 40 KiB RAM address agrees with independently traced startup. The unlabeled photo does not identify the user's physical unit.
- Identified the false-code cause: numeric square-table entries mistaken for pointers. Preserved the broad database and built a separate refined project with a data partition and startup-derived application tp/gp context. RAM is modeled as uninitialized.
- Traced H1 table offset `0x48a20`, static address `0x57a20`, to diagnostic service `0x27`, its state machine, transformation helper, and access-mask consumers. The consumer loads 32-bit constants. Corrected the last two historical byte-order interpretations. No code or access level was tested on a vehicle.
- Inventoried local/public historical sources. Recovered public MQB ALC host integration and a manifest-matching native host artifact, with bounded static REA evidence. This does not recover EPS-side module firmware/hardware or prove target compatibility.
- Fresh end-to-end offline reproduction completed. Its typed diagnostic export is byte-identical to retained evidence. All 694 imported archive files still match their original manifest; no remote or publication was added.

Details: [OFFLINE_ANALYSIS.md](OFFLINE_ANALYSIS.md), [MCU_IDENTIFICATION.md](MCU_IDENTIFICATION.md), [SOURCE_RECOVERY.md](SOURCE_RECOVERY.md), and [FINDINGS.md](FINDINGS.md).

## Saved analysis and reproduction

Annotated working project: `analysis/1061/ghidra/refined-1061.gpr`.

Independent fresh validation project: `analysis/1061/ghidra/verified-1061-reproduction.gpr`.

Original broad baseline: `analysis/1061/ghidra/mapped-1061.gpr`.

Run `scripts/run_1061_analysis.sh` with a fresh project name and the recorded JAVA_HOME. Pinned public reference files are already cached; complete analysis then runs offline. Evidence and checks are indexed in `evidence/offline-preparation-validation-2026-10-19.json`.

## Unresolved external evidence

- Provenance-bound physical user-board identity, low code flash, and data-flash contents.
- Original community MQB Ghidra/Binary Ninja annotations and the exact March 2025 SGO/plots.
- Historical DSR-only/mixer implementation and measurements.
- EPS-side ALC firmware/hardware, tested 1061 identity, and the exact January/August connector diagrams/reply context.

The user confirmed there is no additional local material. Bounded public/local recovery searches and their failures are documented in ACTION_ITEMS.md and SOURCE_RECOVERY.md. These missing deliverables are not marked technically complete. General firmware collecting or speculative labels cannot substitute for original evidence.

## Subsequent research

The preparation checklist no longer requires repeating extraction, CPU-family guessing, provider setup, or rediscovering the historical table. The next independent research question is where steering/HCA/DSR-related data is consumed in the refined firmware. The subsequent HCA pass below identifies static thresholds and curve consumers. No patch, hardware experiment, CAN transmission, flashing or steering behavior has been demonstrated. Hardware work still requires a separately defined task and target.

## Shared Ghidra server reachability

On October 19, 2026 at 18:52 UTC, reread miso's January 12, 2023 pinned connection post. The pinned host `138.68.55.155` accepts TCP on all three documented default ports, 13100/13101/13102, and presents a self-signed `CN=GhidraServer` TLS certificate dated September 2026 to September 2028. The service is reachable. Login, server version, repositories and MQB annotation contents remain unverified; no credentials were sent or retained. Evidence: `evidence/shared-ghidra-reachability-2026-10-19.json`. This improves the prior source-recovery status with a live endpoint, not recovered project contents.

### Authorized login and notes-recovery attempt

The user then authorized trying the pinned login and retrieving notes. Ghidra12.1.4 rejected the server's legacy9.0 registry binding, so an official SHA-256-verified Ghidra11.4.2 client was installed under ignored analysis/tools without changing global configuration. Certificate identity was checked against the previously observed exact SHA-256 pin in an isolated JVM; certificate validity remained checked.

One pinned shared-account/default-password attempt was rejected with `FailedLoginException: User authentication failed`. Server-offered anonymous read-only access succeeded but returned an empty visible-repository list. No notes could be retrieved. This does not establish deletion of private repositories. Working authenticated access or a repository export is still needed. No shared project, permission, credential or server configuration changed; no credentials were stored in notes. Evidence: `evidence/shared-ghidra-access-2026-10-19.json`.

## Shared-server access search follow-up

Live Discord search recovered the owner's September 2023 explanation that unchanged default-password accounts expire after 30 days, later permission repairs, and miso's January 2026 failed login. No verified replacement login or endpoint found in reviewed results. See F029 and SOURCE_RECOVERY. A September 2023 PQ `.gar` backup is an uninspected alternative-source lead, not recovered MQB notes. Next concrete source-recovery action: inspect that backup without treating PQ contents as MQB.

## First HCA request thresholds now readable

[Readable report](TORQUE_LIMITS_1061.md), findings F030-F031, and `scripts/inspect_hca_limits_1061.py` now expose exact scalar bytes and consumers in the existing1061 image. Decoder0x2b530 matches HCA fields; CAN ID and buffer table entry22 corroborate0x126 ->0xfedf9b70. Full hardware receive-index and application initialization linkage remain untraced.

Verified comparison: function0x24aec loads flash0x5e638 (`33 0c`,3123) and compares absolute decoded request magnitude. Approximate interpretation is3.0498Nm. An offline arithmetic model passes±3.05Nm and fails±3.06Nm at that comparison only. The decoder separately saturates at±500cNm, output logic has curve scaling and±6144 intermediate saturation, and function0x24694 applies a downstream±3789 target bound. Passing the magnitude check alone does not establish active assistance.

The saved refined database was read read-only without reanalysis. Exact functions and table evidence are exported under evidence; original archive bytes are preserved. Next concrete action: trace0xfedfab94 through arbitration/override into motor-current control, and resolve active curve selection and units. Missing data flash may affect variants. This is the first bounded HCA-path finding, not a complete map of motor torque limits or a validated firmware modification.

## Downstream HCA-to-output continuation

[Downstream report](HCA_DOWNSTREAM_1061.md), F032-F033: traced selected/shared primary and secondary HCA contributions into assist calculations and combined0xfedfab30, then command processing, a32-byte double buffer, feedback controller and documented TSG20 U/V/W phase-PWM compare registers0xffffccb0/b4/b8. A separate float branch checks consistency; it is not counted as another motor command. Selected full assembly/pseudocode and structured reference evidence are retained.

This improves the earlier stop at0xfedfab94. Runtime activation and physical torque/current scale are still unresolved. Some later controller parameter bytes0x603f8/0x604d8 areffff in the static map. Next concrete action is to trace controller calibration origin/selection and confirm its tp context, then connect command and feedback scales to current-sensing/motor parameters. Do not treat2500 timer counts or intermediate signal bounds as a motor-torque ceiling. No target or original archive changes.

## Controller calibration origin resolved to embedded defaults

[Controller calibration report](CONTROLLER_CALIBRATION_1061.md), F034-F035: the `ffff` values belong to the update's blank `0x60000..0x61000` page. Recovered boot continuation `0x915e..0x922b` conditionally constructs/programs that page from embedded records at `0x61000 + selector*0x6c0`. The saved decompilation missed this continuation because of manual return addresses on indirect calls. Startup arithmetic and a bounded register-write scan support `tp=0x5d800`; no recognized downstream `tp` change found.

Selectors 0/1/2 pass the record identity check. Their defaults all provide command clamp `0x603f8=9216`; command multipliers `0x60112=19733/19417/31645` and right shifts `0x604da=12/12/13`. `0x604d8=11` is a parallel conversion shift. Conditional page models and exact source hashes are retained under analysis/evidence without changing original bytes. These numbers do not establish amperes or steering torque.

Active selection remains unresolved for a specific rack: `0x90be/0xbaa0` reads type `0xa8`, byte `+7`, from records starting at `0x1000`, absent from this update. A pre-existing programmed page and the separately traced page-redirection mechanism can also affect runtime contents. Missing data flash is not necessary to explain these embedded defaults. Next concrete offline action: trace selected-template feedback/current scales into `0x1da5a` and the ADC path. Identifying the installed default additionally needs provenance-bound low-flash selector evidence. All 694 imported archive files still match their manifest; no firmware or hardware changes.

## ADC feedback and phase protection now traced

[Current feedback report](CURRENT_FEEDBACK_1061.md), F036-F037: initializer words `0x55010/14` set sample pointers to `0xffffdc40/44`, confirmed by the manufacturer manual as ADCA0 channel 1/2 result registers. ADC control value `0x50308001` selects 10-bit right-aligned results. Function `0x1c47e` subtracts learned offsets, applies four sensor-gain words from a type-2, length-`0x20` low-flash record, and derives the third phase as a negative sum. That separate gain record is absent, so embedded controller defaults alone do not establish amperes.

All three accepted templates give feedback clamp `0x60404=2880`, multiplier `0x60110=23301`, shift `0x60500=11`. Positive 2880 maps to 32767 normalized units. Buffered command slot 2 is compared against transformed feedback at `0x1e31e`, closing the static feedback chain. The actual phase order additionally depends on absent type-`0xa8` data.

Independent protection `0x1cc22` compares both measured phase magnitudes against raw threshold `0x5d08e=2880`. From zero, 31 consecutive qualifying calls invoke `0x1535e(0x15,0,1,1)`. Call period, physical units and downstream fault reaction remain unproven. These are raw measured-phase limits, not 2880 A or a proven steering-torque ceiling. Original bytes remain unchanged. Next concrete offline action: trace fault `0x15` through its table/reaction consumers and establish the protection routine's scheduling; physical units still need missing calibration and an authoritative conversion reference.
