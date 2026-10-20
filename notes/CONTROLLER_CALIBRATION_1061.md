# Controller calibration origin in 1061

October 20, 2026. Offline continuation of [HCA downstream analysis](HCA_DOWNSTREAM_1061.md). This resolves the origin of candidate controller parameters and explains the blank update page. It does not identify the installed rack's active parameters or establish amperes or mechanical torque.

## Result

The `ff ff` at `0x603f8` and `0x604d8` is part of a complete blank page `[0x60000,0x61000)` supplied in H1. The boot path contains a conditional page construction/programming sequence using embedded records beginning at `0x61000`. Reading the raw update page as the final controller calibration was therefore incomplete.

Three records pass the selector's embedded identity check. They all supply `9216` (`00 24`) at the controller's command clamp `0x603f8`. They supply `11` (`0b 00`) at `0x604d8`, which is a shift count for a parallel conversion, not the command clamp. The actual command conversion uses a separate shift at `0x604da`.

| Selector | Embedded source | Command multiplier at destination `0x60112` | Command shift at `0x604da` | Multiplier / 2^shift | Command clamp at `0x603f8` |
| --- | --- | ---: | ---: | ---: | ---: |
| 0 | `0x61000` | 19733 | 12 | 4.817626953125 | 9216 |
| 1 | `0x616c0` | 19417 | 12 | 4.740478515625 | 9216 |
| 2 | `0x61d80` | 31645 | 13 | 3.8629150390625 | 9216 |

These are raw fixed-point values and conversion factors. Do not interpret `9216` as a physical steering-torque ceiling. Inputs, other limits, filtering, output state and feedback remain material.

## Address-base check

Application startup `0x100c0..0x100d6` computes `tp = 0x50000 + 0x5800 + 0x8000 = 0x5d800`. A scan of recognized instructions below `0x55606` found only two groups of `tp` writes: boot startup `0x903e/42/46` and application startup `0x100ce/d2/d6`. No recognized downstream function changes it.

At `0x4805a`, the controller computes `ep = tp + 0x2bf8`, then reads its signed clamp at `0x4805e`. This resolves to `0x603f8`. At `0x479da/de`, it reads command shift `tp+0x2cda` and parallel shift `tp+0x2cd8`. The startup arithmetic and actual operand forms support the existing base. The exported Ghidra context values were seeded in the existing project, so those values alone are not independent proof. Unrecognized code and indirect control flow prevent a whole-program invariant claim.

## Boot selection and page construction

1. `0x90e0` checks words at `0x60000` and `0x60ffc`. If both are `0xffffffff`, it returns `0xa2`. This is an endpoint test, not an exhaustive blank-page check.
2. Boot function `0x9462` calls `0x912a` on that result.
3. `0x90be` looks up record type `0xa8` through `0xbaa0`. The lookup walks variable-length records starting at `0x1000`, with a bound below `0x1ff0`. The selector is record byte `+7` when below 7; otherwise it defaults to 0. An absent record also gives 0. The entire lookup area is absent from this update.
4. `0x90fc` computes `0x61000 + selector*0x6c0`, then requires the byte at record offset `0x6b3` to equal the selector. Sources for selectors 0, 1 and 2 match. Records in slots 3 through 6 repeat identity 2 and fail that check. Do not treat all seven slots as accepted variants.
5. The full instruction range `0x912a..0x922c` prepares RAM at `0xfedf6000` and calls the H2 interface via the table at `0x2000`. It passes destination `0x60000`, page length `0x1000`, then source RAM, destination `0x60000` and body length `0x6b0`. It separately passes 16 bytes from record offset `0x6b0` to destination `0x60ff0`.
6. The interface targets are `0x7a0e`, `0x7aec`, `0x7b7c`, `0x7b34` and `0x7ac4`. Initialization resolves RAM function pointers; page wrappers convert addresses to 4 KiB indices and the data wrapper enforces 8-byte alignment. This supports an initialize/erase/program/verify/finalize interpretation. The low-level flash implementation and successful writes were not executed or fully traced here.

Ghidra's saved function body omits `0x915e..0x922b`: each indirect call manually loads its continuation into `lp`. Its decompilation consequently stops after the first indirect call. The new bounded instruction export recovers that continuation without modifying the database. The copy lengths and destinations above come from those instructions, not the incomplete pseudocode.

`scripts/inspect_controller_calibration_1061.py` builds conditional pages under `analysis/1061/controller-calibration-model/`. It models successful blank-page erase/programming, placing the first `0x6b0` bytes at offset zero and metadata at offset `0xff0`; the gap remains erased. These are analyst models, not ECU dumps or flashable modifications. The mapped update and original extracted blocks remain unchanged.

## Conversion consumer

Controller `0x463e2` loads `tp+0x2912 = 0x60112` at `0x4789a` and stores it to `0xfedf9f6e` at `0x478b4`. At `0x48058` it reloads that signed multiplier. Command shift `0x604da` is loaded into `r25` at `0x479da`. The bounded command is multiplied at `0x48084`, arithmetic-shifted at `0x48086`, then saturated to `[-32767,32767]` through `0x480a2`.

For this stage only:

```text
y = saturate((clamp(x, -9216, 9216) * multiplier) >> command_shift,
             -32767, 32767)
```

For example, input 1024 yields 4933, 4854 or 3955 for selectors 0, 1 or 2. These are integer stage outputs, not amperes. The following filter/state branches can change the final buffered command.

## Alternate calibration access

The earlier overlay lead is real static code, but it does not establish the runtime source. Startup `0x13cd2` copies `[0x5e000,0x60000)` to `0xfa800000` and configures `0xfa001300/304` to `0x5e000/0x5f000`. The selector tables at `0x5a87c` and `0x5a884` contain pairs `(0x5e000,0x5f000)` and `(0x5e000,0x60000)`. Function `0x16602` writes selected addresses and control value 3, polls a status register, and can schedule a two-page copy. `0x1684a` explicitly translates selected page addresses into the corresponding `0xfa800000/0xfa801000` windows when its state is enabled. Thus the second mapping can target the controller page too.

Firmware instructions corroborate a page-redirection mechanism. The exact peripheral definition, actual enabled state, later edits and runtime contents remain unverified. It would be incorrect to claim the blank controller page can never be redirected, or that a recovered template necessarily equals active calibration. Missing data flash is not needed to explain the embedded defaults; a dependency on it elsewhere is still possible.

## Evidence and next action

Mapped artifact SHA-256 `a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d`, base `0x2000`. H1 SHA-256 `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641`, base `0xf000`. For a static address A, mapped offset is A minus `0x2000`; H1 offset is A minus `0xf000`. Exact source offsets, record/page hashes and readbacks are in [structured calibration evidence](../evidence/controller-calibration-1061-2026-10-20.json).

- [Register scan and recovered boot continuation](../evidence/ghidra-calibration-context-1061-2026-10-20.txt).
- [Startup, overlay and controller-caller exports](../evidence/ghidra-calibration-origin-1061-2026-10-20.txt).
- [Selector and initialization exports](../evidence/ghidra-calibration-selection-1061-2026-10-20.txt).
- [Page-interface and missing-region lookup exports](../evidence/ghidra-calibration-writer-1061-2026-10-20.txt).
- [Existing controller instructions](../evidence/ghidra-hca-motor-chain-1061-2026-10-19.txt).
- [Validation](../evidence/controller-calibration-validation-1061-2026-10-20.json).

Direct Ghidra 12.1.4, saved refined database read-only, no reanalysis. Reused the REA skill's established V850 fallback. These exports have no REA Evidence IDs. No network retrieval, firmware execution, flashing, CAN transmission or bench work occurred.

Next offline action: follow the same selected record through feedback/current conversion into `0x1da5a`, and determine whether template constants plus the hardware ADC path establish physical current units. Active selector confirmation specifically needs provenance-bound bytes covering the `0xa8` record in `[0x1000,0x2000)` or equivalent authoritative identity evidence. A currently programmed page may also differ from the conditional defaults.
