# Better openpilot steering on VW MQB

The goal is to improve **openpilot steering authority, response, and consistency on VW MQB vehicles**.

Start with the existing **HCA torque-control interface**. Investigate firmware changes where they could address a demonstrated limit. Keep PLA angle control as an alternative research path.

**Current stage: offline research. No working firmware modification or vehicle-tested improvement yet.**

## Key terms

| Term | Meaning here |
| --- | --- |
| **MQB** | VW Group vehicle platform. Research currently focuses on one rack and firmware version. |
| **EPS** | Electric power steering, including the rack's motor and controller. |
| **Firmware** | Software running inside the steering controller. |
| **HCA** | The torque-request steering interface used for lane assistance. |
| **PLA** | The angle-request steering interface used for parking assistance. |
| **DSR** | Steering requests associated with stability assistance. These can interact with other steering modes. |

## Progress beyond the reviewed thread

Building on the community's leads, this project has added:

- **Reproducible firmware extraction:** verified all three 1061 update containers against archived ODX/payload bytes and resolved overlapping flash blocks. [Extraction](notes/OFFLINE_ANALYSIS.md)
- **A usable analysis foundation:** corroborated the V850 hardware/memory profile, corrected false code identification, and built an annotated Ghidra project. [Hardware and mapping](notes/MCU_IDENTIFICATION.md)
- **Concrete torque restrictions:** located the approximately **3.05 Nm HCA request check**, three speed-dependent curves, and downstream command shaping. This explains why changing one threshold may not increase usable assistance. [Findings](notes/FINDINGS.md)
- **Request-to-motor tracing:** followed HCA contributions through shared assist calculations into current feedback and motor-output registers. Identified missing calibration needed to translate software values into physical torque. [Control path](notes/HCA_DOWNSTREAM_1061.md)
- **More precise angle-control limits:** the supplied PLA calibration indicates a low-speed entry qualifier, qualified release near **12 km/h**, and a separate driver-release threshold around **7 Nm**. This replaces the simple 15 km/h assumption for this update. [Findings](notes/FINDINGS.md)
- **Historical table verified:** traced the old security-access-table lead to diagnostic service `0x27` and corrected two earlier value interpretations. Working vehicle access remains untested. [Analysis](notes/OFFLINE_ANALYSIS.md)

These are **static findings for the supplied firmware**, not measured vehicle performance or a working torque modification. Original archive bytes remain preserved.

Initial target: **5Q0 909 144 R**, firmware **EPS_MQB_ZFLS 126 1061**. Findings do not automatically apply to other MQB racks.

## Still to do

1. Summarize known HCA limits and use driving data to distinguish insufficient authority from tuning, delay, or rack rejection.
2. Resolve firmware restrictions and missing calibration evidence that could change the answer.
3. Compare better HCA modeling/tuning with targeted firmware changes. Evaluate PLA if HCA cannot meet the goal.
4. Validate a chosen approach with matching openpilot integration and independent command limits in a separately scoped hardware phase.

Success means **better path tracking and fewer steering-limit interventions**, while preserving driver override and bounded steering response. Increased torque is a possible means; a working improvement remains unproved.

## Community credit

- **[RetroPilot MQB Discord research](https://discord.com/channels/660951518014341124/1063188305514090546):** shared firmware, hardware leads, PLA observations, and connector research helped focus this investigation and avoid duplicate work.
- **openpilot / opendbc:** vehicle interfaces and CAN definitions.
- **VW_Flash:** adapted FRF extraction logic ([license](scripts/licenses/VW_Flash-BSD-2-Clause.txt)).
- **Earlier PQ steering research:** useful methodology; findings do not automatically apply to MQB.

[Thread review and 67 dated source anchors](notes/DISCORD_REVIEW.md). Community reports are not independently verified results; no reproducible MQB firmware torque patch was established in the reviewed thread.

## AI and tooling transparency

- **OpenAI Codex desktop:** LLM agents and parallel subagents assisted research, analysis, scripts, checks, and writing. Exact historical model versions were not consistently recorded.
- **REA:** `reverse-engineer-anything` skill v42 and `rea-agents` 6.7.0 for tooling checks and separate ARM64 ALC host analysis.
- **Ghidra 12.1.4:** direct V850 firmware analysis because REA's raw-import interface did not support it. [Method and limitations](notes/REA_READINESS.md).
- **Verification:** retained hashes, instructions, source records, and reproducible checks. AI interpretations can be wrong; static checks do not prove vehicle behavior or a working modification.

## Explore the research

- [Current status and next steps](notes/STATUS.md)
- [Firmware extraction and analysis foundation](notes/OFFLINE_ANALYSIS.md)
- [Evidence-backed findings](notes/FINDINGS.md)
- [Historical community discussion](notes/DISCORD_REVIEW.md)

Original files live in `EPS_research/`, derived analysis in `analysis/`, and retained evidence in `evidence/`.
