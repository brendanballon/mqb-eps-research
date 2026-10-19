# Discord history review

Reviewed October 19, 2026 through the open native Discord UI.

Source: [RetroPilot: MQB VW Rack FW Hack (5Q0, 3Q0)](https://discord.com/channels/660951518014341124/1063188305514090546), within `bounties`.

## Coverage

Read the accessible message text in successive loaded sections, from the first post on January 12, 2023 through August 10, 2026. Reached the latest messages with no older-message indicator remaining. This is a curated history, not a lossless transcript or a complete attachment archive. Dates below are the dates displayed by Discord. Individual message permalinks were not collected; use the thread and date/author anchors to locate originals.

Images, video content, linked articles, external code, Google Drive contents, and attachment contents were not exhaustively inspected. Attachment names and message claims do not establish their contents. No messages were sent, no reactions added, no shared server login attempted, and no remote project was changed. Historical credentials are intentionally omitted.

## January to April 2023: material collection and CPU uncertainty

- January 12, CzokNorris opened the MQB-specific thread. miso linked a shared Drive folder and asked collaborators to maintain per-firmware notes. A shared Ghidra server was offered, with a suggestion to add an MQB folder to the existing PQ project.
- Shared material: [Docs and firmware Drive folder](https://drive.google.com/drive/folders/1jbYVfHPv69yVEW2BQdQ-R-QM_IWp8Gr9). This link was observed in the thread; its current contents have not been synchronized or compared with the local archive.
- miso reported version 1061 on a Mk7. That is the participant's vehicle, not identification of the user's car.
- January 20, miso discussed TRW column-mounted MQB-A0 units and claimed TriCore chips. In February, ole instead reported V850 for a 5Q0 rack, based on photos and Ghidra interpretation. miso clarified that their teardown was 2Q1 and that rack-mounted hardware might differ.
- February 19, cd_redbrick linked an MQB EPS firmware collection and a V850 reverse-engineering PDF attachment. These are leads, not checked evidence in this preparation pass.
- April 16 and 23, miso explicitly said that MQB work was on update files and that no hardware dump was known to them. Discussion corrected confusion about VCP exporting flash-file contents versus reading a module's current flash. VCDS diagnostics/coding and firmware dumping were not interchangeable.

## May to June 2023: alternatives to a firmware patch

- May 16, dkiiv proposed an inline CAN device combining HCA and DSR. They hypothesized additive assistance and explicitly said the MQB result was unknown. The proposed torque arithmetic is a hypothesis, not a measurement.
- PLA park-assist angle control was discussed separately. ole reported that MQB PLA cancelled on sufficient measured driver torque, but that unloaded wheel acceleration and motor authority remained problematic. On May 22, ole described a closed-ground experiment at 15 km/h with rapid steering movement. This corrected an earlier assertion that cancellation was entirely external to the rack.
- May 24, ole distinguished driver cancellation torque from motor output torque and steering rate. These participant reports were not reproduced here and do not establish validated control limits.
- May 24, dkiiv proposed quantifying DSR separately and mentioned a CAN inbox change as one avenue. No completed MQB HCA/DSR implementation was demonstrated in the reviewed text.
- June 29, participants traced MQB EPS wiring and discussed an inline connector. UptownBench1187 reported finding an accessible connection after removing the airbox and battery tray. miso described GTE/PHEV packaging obstructed by the inverter. Wiring access is vehicle-dependent.
- Candidate connector numbers posted by dkiiv: `4H0 973 713` and `3B0 973 813`. Other harness identifiers discussed: `5Q1971111BA` and `5Q1971111AC`. These are historical leads, not confirmed parts for the user's vehicle.
- A separate [wiring-diagram Drive folder](https://drive.google.com/drive/folders/1bW8WEvV_sL4IoRP_i1ewVIfz-GTYVk5O) was posted. Its contents were not downloaded or validated.

## 2024 and March 2025: limited renewed discussion

- May 12, 2024, speed spoofing was raised as a possibility. The response did not provide a measured implementation or validation.
- March 14, 2025, ole reported at least three lookup-table groups in steering-map SGO data. dkiiv suggested driver assistance, return/recentering, HCA/DSR, and TSC as possible meanings, while explicitly saying firmware memory tracing was needed to identify them.
- The same day, ole described driving an MQB prototype rack that reportedly had something flashed by IAV. They reported substantially increased steering authority, below PLA, but had no details of the modifications. No patch, firmware identity, map offsets, or reproducible procedure was provided in that discussion.

## January to August 2026: ALC module revival

- January 2, daniii438 asked about the old Ghidra server. miso reported that it appeared alive but that they could not log in, and said they had moved to Binary Ninja. Current shared-project availability and content remain unknown.
- Teal and armanthenothacker discussed a project they called **ALC, angle lateral control**. They reported that it required a module near the EPS and **no firmware flash**. armanthenothacker said their GTI was the only MQB car with that module installed at that time.
- Participants linked demos and claimed favorable safety properties. Neither demos nor implementations were independently evaluated in this pass. A question asking whether the device intercepted the torque sensor was not a confirmed technical description.
- Teal linked a separate Konn3kt beta-testers Discord. That server was not joined or reviewed.
- January 4 and 5, developers offered to make a harness for miso, contingent on identifying and photographing the connector. The text did not provide an openly reviewed branch or source package.
- January 10 and 11, miso investigated T14q/T14z connections on their PHEV and reported that unplugging them did not affect EPS. Record these as unsuccessful connector candidates for that vehicle, not a universal pinout.
- January 19, Teal discussed CAN wiring and a relay box. This is a design claim, not demonstrated fail-safe performance.
- March 7, a reminder was posted.
- August 10, the latest visible activity was Teal saying a previously discussed connector could work for filtering and tagging armanthenothacker. No completed PHEV test result was visible afterward.

## Implications for this project

1. Preserve the firmware investigation as its own track. A reported ALC success does not prove a firmware torque patch exists.
2. The user's 5Q0 909 144 R / 1061 target has directly relevant local update material and an older note about security-code table candidates.
3. Recover artifact lineage and CPU identity before decompilation. Avoid inheriting the thread's early cross-family assumptions.
4. Treat shared Ghidra annotations, 2025 modified-map evidence, and 2026 ALC sources as missing material. Accessing those is a future collection task, not a prerequisite for inventorying local bytes.
