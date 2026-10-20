# Primary target

Source: diagnostic output supplied directly by the user on October 19, 2026. No live vehicle query was performed.

| Field | Value |
| --- | --- |
| Diagnostic address | 44, Steering Assist (J500) |
| Software part number | 5Q0 909 144 R |
| Hardware part number | 5Q0 909 144 R |
| Component | EPS_MQB_ZFLS 126 1061 |
| Coding | 0102 |
| Label | 5Q0-909-144.clb |
| ASAM dataset | EV_SteerAssisMQB 012140 |
| ROD | EV_SteerAssisMQB_012_VW37.rod |

Vehicle model and year have not been supplied. Do not infer them from other participants' vehicles in Discord.

The local archive contains 5Q0909144R software version 1061 FRF and ODX variants H1, H2, and H7, plus H1 and H7 extracted binaries. The diagnostic identification matches the part number and software version, but does not establish component roles, runtime flash layout, or exact MCU. The subsequent offline pass favors V850-family code in H1 and a component/download interpretation of H1/H2/H7. See OFFLINE_ANALYSIS.md.

Initial working set: `EPS_research/MQB/5Q0, 3Q0/`. Use `inventory/archive-manifest.json` for exact local hashes. Its extracted binaries are historical derivatives of update files, not verified full dumps of this user's rack.

Current offline profile: the supplied 1061 update map and recovered manufacturer documentation support V850E2M/PJ4 analysis with code flash ending at 0x80000 and 40 KiB RAM at fedf6000..fedfffff. The historical board photo shows 70F3506 but lacks a module-label binding to this user's unit. See MCU_IDENTIFICATION.md and ACTION_ITEMS.md for the distinction between a supported static profile and physical identification.
