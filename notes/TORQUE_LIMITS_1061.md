# First readable HCA torque thresholds in 1061

October 19, 2026. Static analysis of the exact 5Q0909144R / 1061 update, not a vehicle measurement. We can now read specific request-path thresholds and identify their consumers. Complete motor-output limits and a validated modification remain unresolved.

## What is visible

| Role | Location | Observed value | Interpretation and limit |
| --- | --- | --- | --- |
| Request decoder saturation | Instructions `0x2b584..0x2b596` | signed wire magnitude limited to ±500 | ±5.00 Nm using external MQB DBC units. This does not mean 5 Nm requests are eligible. |
| Request magnitude eligibility | Flash `0x5e638`, bytes `33 0c`, H1 offset `0x4f638` | 3123 | Approximately 3.0498 Nm at 1024 internal units/Nm. An absolute-magnitude comparison feeds the HCA state machine's eligibility conditions. |
| Request change comparison | Flash `0x5e630`, bytes `71 00` | 113 | Approximately 0.11035 Nm. Used with direction, previous request and active state. Not a standalone rate limit with proven time units. |
| Intermediate output saturation | Instructions `0x25528..0x25560` | ±6144 | Approximately ±6 Nm in the intermediate signal. Not measured motor torque. |
| Multiplier after curve interpolation | Flash `0x5e804`, bytes `9a 21` | 8602 / 8192 | Approximately 1.05005. Scaling occurs between two saturation checks. |
| Downstream symmetric target bound | Flash `0x5e63a`, bytes `cd 0e`; function `0x24694` | ±3789 | Approximately ±3.7002 Nm. This path also applies state and step constraints before storing `0xfedfab94`. |

The approximate Nm conversion is an inference from two sources: the external MQB DBC defines the incoming magnitude in centiNm, and firmware converts it using `(signed_value * 2621) >> 8`, nearly 1024 internal units/Nm. Raw bytes, instructions and integers are the primary observations.

## Evidence chain

The pinned external [commaai MQB DBC](https://github.com/commaai/opendbc/blob/48c7f06c6f27c41e7169242acb03ef9775658deb/opendbc/dbc/vw_mqb.dbc) defines HCA_01 as CAN `0x126`, with magnitude at bits16..24, sign at bit31, status at bits32..35 and vibration amplitude at bits36..39. Source hash and line excerpts: [protocol evidence](../evidence/hca-protocol-source-2026-10-19.json). A DBC is external protocol evidence, not a manufacturer's calibration definition.

Function `0x2b530` extracts exactly those fields from `0xfedf9b70`, saturates signed magnitude, converts it, and writes request `0xfedfab26`, status `0xfedfaf08`, and vibration amplitude `0xfedfab28`. Status values above7 produce a sentinel instead. The matching field layout strongly supports HCA association. CAN configuration and receive-buffer tables provide additional corroboration; [linkage evidence](../evidence/hca-message-linkage-1061-2026-10-19.json) states the unresolved receive-callback coverage explicitly.

Function `0x24aec` reads the signed request at `0x24bc4`. It forms its absolute magnitude at `0x24da2..0x24daa`, loads `tp+0xe38 = 0x5e638` at `0x24e06`, and compares at `0x24e0c`. This magnitude condition combines with request-change and unchanged-request state checks. Failed eligibility can clear the active flag `0xfedfaf33` through the state machine. This is a gate with state transitions, not a simple instruction that clips everything to3 Nm.

When enabled, the function uses the request in a curve-scaled output path at `0x254d6..0x25560`. The pointer group `0x5f738` includes three six-point curves at `0x5fcde`, `0x5fcfa`, `0x5fd16`. All three raw axes are `[0,1920,3200,6400,9600,12800]`. Their outputs act as Q13 multipliers in this path. Axis units and active profile selection remain unresolved; do not label these as measured torque-vs-speed maps yet. Function `0x24694` consumes the resulting `0xfedfab90` and stores a bounded, state-dependent result to `0xfedfab94`. The complete path to motor current and mechanical torque has not been traced.

## Offline boundary check

An arithmetic model of only the decoder and magnitude comparison gives:

| Signed requested magnitude | Positive internal value | Negative internal value | Magnitude condition |
| --- | ---: | ---: | --- |
| ±3.00 Nm | 3071 | -3072 | Passes |
| ±3.05 Nm | 3122 | -3123 | Passes |
| ±3.06 Nm | 3133 | -3134 | Fails |
| ±5.00 Nm | 5119 | -5120 | Fails |

These are calculated comparison outcomes, not replayed ECU responses. Other conditions can still reject a request that passes this comparison. The external controller's `STEER_MAX=300` convention is consistent with staying below this threshold but is not the firmware constant itself.

## Reproduce and inspect

Run `python3 scripts/inspect_hca_limits_1061.py` after preparing the mapped image. The reader refuses a different SHA-256 and emits the scalar bytes, mapped/H1 offsets, raw curves and boundary calculations as JSON. It writes no firmware or database changes. Retained output: [machine-readable limits](../evidence/hca-limits-1061-2026-10-19.json).

Exact artifact: mapped SHA-256 `a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d`, loaded at `0x2000`; H1 SHA-256 `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641`, loaded at `0xf000`. All addresses above use that mapping. Full extraction lineage remains in [OFFLINE_ANALYSIS.md](OFFLINE_ANALYSIS.md).

Ghidra12.1.4 exports: [decoder, state machine, downstream bound and interpolators](../evidence/ghidra-hca-limits-1061-2026-10-19.txt), [message-table consumers](../evidence/ghidra-hca-message-tables-1061-2026-10-19.txt). These are direct Ghidra observations using the documented REA-skill fallback, not REA Evidence IDs. REA6.7.0 still does not admit V850 raw images. The saved refined project was opened read-only without reanalysis.

## Remaining work

1. Complete the receive-callback linkage and independently confirm active curve/profile selection and axis units.
2. Trace `0xfedfab94` through arbitration, driver override, further limits and the motor-current controller. Keep HCA, DSR, PLA and driver torque separate.
3. Determine whether data-flash parameters or other variants alter these checks. Those physical bytes are absent from this update.
4. Establish firmware integrity checks and a separately scoped validation/recovery method before treating any edit as usable. Changing the identified bytes alone does not establish working steering behavior.

The archived CSV and four candumps contain no HCA `0x126` frames. Their Golf GTE recording context covers ignition/engine transitions. They cannot validate saturation or identify the user's physical1061 behavior.

[Validation manifest](../evidence/hca-limits-validation-1061-2026-10-19.json): all694 imported files still match original size/hash; reader output repeats byte-for-byte; selected decompilations completed.
