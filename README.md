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

## Covered so far

- **Research foundation:** preserved the original archive, reproduced firmware extraction, and built an annotated code-analysis project.
- **Torque control:** traced HCA request checks, speed-dependent curves, driver-input effects, and interactions with other steering modes.
- **Angle control:** identified PLA speed and driver-release conditions. Angle-controller analysis is still partial.
- **Motor output:** followed the command path into motor control. Converting software values into physical steering torque remains unresolved.
- **Prior work:** reviewed historical community research and separated reported results from verified local findings.

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
