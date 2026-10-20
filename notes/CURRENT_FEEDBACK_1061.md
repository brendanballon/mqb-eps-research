# ADC and phase feedback in 1061

October 20, 2026. Offline continuation of [controller calibration](CONTROLLER_CALIBRATION_1061.md).

## Result

The firmware reads ADCA0 channels 1 and 2, subtracts learned offsets, applies sensor gains from a missing low-flash record, and constructs three phase-feedback values. The controller normalizes and transforms those values before subtracting feedback from the buffered command. This closes the static feedback side of the earlier command-to-PWM path.

A separate protection function compares the magnitudes of the two independently measured phase values against **2880**. From reset counters, 31 consecutive calls at or above that magnitude cause a report with identifier `0x15`. All three accepted controller templates also clamp those feedback inputs at 2880. These are readable phase-signal thresholds, but their values in amperes remain unresolved. They do not establish a steering-torque ceiling or the resulting fault response.

## ADC acquisition and initialization lineage

Startup `0x13cd2` copies initialized data from `0x537e0` into RAM starting at `0xfedfa8a0`. The following source words are inside that copy:

| Flash initializer | RAM destination | Initial value | Use |
| --- | --- | --- | --- |
| `0x54f98` | `0xfedfc058` | `0x1000` | Low-flash record cursor |
| `0x54fa4` | `0xfedfc064` | `0` | Sensor calibration record pointer, later assigned |
| `0x55010` | `0xfedfc0d0` | `0xffffdc40` | First phase sample register pointer |
| `0x55014` | `0xfedfc0d4` | `0xffffdc44` | Second phase sample register pointer |

Function `0x1c47e` dereferences the last two pointers with word reads and masks with `0x3ff`. Manufacturer manual R01UH0098EJ0100 identifies the short ADC base as `0xffffdc00`, and the per-channel result address as `base+0x3c+4*m`. Thus these addresses are ADCA0 channel 1 and channel 2 conversion result registers. This identifies ADC channels, not the physical board wiring or current-sensor components.

Initialization `0x3e958` writes `0x50308001` to ADC control register `0xff81d104`. CTYP bit 15 is 1, selecting 10-bit resolution; CRAC bit 24 is 0, selecting right alignment. This independently agrees with the `0x3ff` mask. The write of zero to `0xffffdc08` configures channel group 2; it does not select resolution.

Manual anchors: printed page 1733/PDF 1753 for base addresses, printed 1780-1781/PDF 1800-1801 for CTL1 fields, printed 1795/PDF 1815 for channel-result addresses, and printed 1796/PDF 1816 for result alignment. Exact excerpts and manual hash are preserved in [manual evidence](../evidence/adc-manual-source-2026-10-20.json).

## Sensor calibration and phase construction

Record parser `0x3e34a` recognizes type 2 with length `0x20` and sets `0xfedfc064` to that record's address. Its cursor starts at `0x1000`, and parsing is bounded by `0x1ff0`. None of those bytes are supplied in this update. The initial zero pointer is not evidence of a zero gain, and cannot be substituted for the absent record.

Let R be the record base and M the mode byte at `0xfedfaecd`. The gains are unsigned little-endian words:

| Mode | First measured phase gain | Second measured phase gain | Offset RAM |
| --- | --- | --- | --- |
| M = 0 | R+`0x08` | R+`0x10` | `0xfedfae26`, `0xfedfae28` |
| M != 0 | R+`0x0a` | R+`0x12` | `0xfedfae22`, `0xfedfae24` |

For each measured phase, `0x1c47e` computes:

```text
t = (signed16(offset - (adc & 1023)) * gain + 512) >> 10
if M == 0: phase = signed16((t * 5285 + 256) >> 9)
otherwise: phase = signed16((t * 4271 + 1024) >> 11)
```

The shifts are arithmetic. The final `signed16` represents the stored halfword; it is not saturation. These equations describe the normal duplicate-consistency path. On a duplicate mismatch the firmware calls `0x3925a` and does not simply perform the usual update.

Outputs are `0xfedfaac2` and `0xfedfaac6`. The third value, `0xfedfaac4`, is the signed-halfword negative sum of the other two. These can be called logical phases A, C and B for readability; that naming does not prove physical phase order. In calibration conditions the function accumulates 16 ADC samples and updates the appropriate offset using `(sum+8)>>4`. Other state-dependent offset handling exists in `0x3ef52` and was not completely traced in this pass.

The integer slopes before final storage are approximately `10.322265625*gain/1024` or `2.08544921875*gain/1024` phase units per offset-minus-ADC count. Neither fixes amperes without the missing gain and a physical unit reference. The manual's conversion equation on printed 1756/PDF 1776 describes voltage relative to ADC references, not current through the board's sensing circuit.

## Feedback normalization and comparison with the command

When `0xfedfaed8==0`, entry function `0x1c43a` calls `0x1c47e`, `0x1c3d2`, `0x1cc92` and `0x1da5a`, in that order. This demonstrates intended acquisition before control in that static branch; execution frequency and actual activation are unobserved.

Controller `0x1da5a` copies or swaps the three logical phase inputs according to `0xfedfaf4b`: byte `0xfa` keeps their order, `0x2c` swaps the latter two, and another value substitutes zeros. The record parser obtains that phase-order byte from type `0xa8`, also in the absent low flash. It must not be confused with the selector at byte +7 of that record.

The controller loads a feedback multiplier from `0x60110` at `0x1db3a`, stores it to `0xfedf9888`, and reloads it at `0x1dd3e`. It loads the two measured-input clamp from `0x60404` at `0x1ddb2` and the normalization shift from `0x60500` at `0x1dca2`. All three accepted templates give:

| Conditional field | Value | Role |
| --- | ---: | --- |
| `0x60404` | 2880 | Symmetric measured-phase input clamp |
| `0x60110` | 23301 | Feedback normalization multiplier |
| `0x60500` | 11 | Arithmetic shift |

For each independently measured input, this stage is `sat16((clamp(phase,-2880,2880)*23301)>>11)`, where saturation is `[-32767,32767]`. Positive 2880 maps to 32767. Negative -2880 yields -32768 before that saturation and therefore becomes -32767. This is evidence of numerical normalization, not a newly established ampere scale.

The controller reconstructs the third normalized contribution, applies angle-dependent transformations and optional moving averages, then subtracts the transformed feedback from its requested axis values. The command previously traced from buffer slot 2 is read at byte offset 4 at `0x1dcde`, stored to stack offset `0x1c` at `0x1dce0`, reloaded at `0x1e312`, and subtracts feedback at `0x1e31e`. Error then enters proportional/integral processing. This distinguishes the buffered command from measured feedback, while preserving their comparison in the controller domain.

The complete large controller has not been proved instruction by instruction. Saturation, angle transforms, moving averages, branch selection and feedback gains all matter. A divide by 16 in the separate floating-point path `0x1cc92` is suggestive of another numerical scale but supplies no unit label proving amperes.

## Separate phase protection threshold

Function `0x1cc22` reads unsigned threshold `0x5d08e`, bytes `40 0b`, value 2880. This address is outside the conditionally populated controller page. With `tp=0x5d800`, it is loaded through `tp-0x772` at `0x1cc26` and `0x1cc50`.

For `0xfedfaac2` and `0xfedfaac6`, independently:

```text
if abs(phase) < 2880: counter = 0
else: counter = (counter + 1) modulo 65536
if either counter >= 31: call 0x1535e(0x15, 0, 1, 1)
```

Counters are at `0xfedfb6d0/0xfedfb6d2`. The first report from zero occurs on the 31st qualifying consecutive call. These are calls to this protection routine, not proven ADC periods or milliseconds. The third reconstructed phase is not independently checked here. Other protection functions may exist.

The reporting helper enters a wider fault/state system. This pass does not establish whether report `0x15` disables PWM, latches a diagnostic, derates assistance or triggers another response. It is not a demonstrated safe operating limit or a firmware modification target.

## Evidence, limits and next action

Mapped SHA-256 `a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d`, base `0x2000`; H1 SHA-256 `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641`, base `0xf000`. At static address A, mapped offset is A minus `0x2000`; H1 offset is A minus `0xf000`. For example, threshold `0x5d08e` is H1 offset `0x4e08e` and mapped offset `0x5b08e`.

- [Structured reads and formulas](../evidence/current-feedback-1061-2026-10-20.json), reproduced by `scripts/inspect_current_feedback_1061.py`.
- [Acquisition, records, protection and ADC initialization](../evidence/ghidra-current-feedback-1061-2026-10-20.txt).
- [Controller entry and report helper](../evidence/ghidra-current-entry-protection-1061-2026-10-20.txt).
- [Existing full controller export](../evidence/ghidra-hca-motor-chain-1061-2026-10-19.txt) and [startup copy export](../evidence/ghidra-calibration-origin-1061-2026-10-20.txt).
- [Validation](../evidence/current-feedback-validation-1061-2026-10-20.json).

Used the REA skill's established direct Ghidra V850 fallback, saved database read-only and no reanalysis. Exports are direct observations, not REA Evidence IDs. Independent read-only manual review corroborated ADC register meanings. No firmware execution, board access, CAN transmission, flashing or network retrieval occurred.

Remaining unit prerequisites are now precise: the type-2 sensor gain record, a defensible phase-signal-to-ampere definition or board transfer function, the installed controller page/selector, and motor/mechanical conversion parameters for steering torque. Static files do establish integer thresholds and data flow. They do not yet establish a physical motor-current or steering-torque ceiling.

Next useful offline action: trace report `0x15` through the fault table and reaction consumers to establish its intended effect and scheduling. Do not repeat extraction or guess the missing sensor gains.
