# 1061 offline analysis

October 19, 2026. Current consolidated results. Earlier offset-only and broad-analysis exports are retained as historical evidence, superseded where stated below. No firmware or host extension was executed.

## Result

The local 5Q0909144R / 1061 preparation path is reproducible from FRF through exact ODX and payload bytes into an annotated direct Ghidra project. Independent source recovery supports a V850E2M/PJ4 working hardware profile and the flash/RAM ranges. The historical table is now traced to a diagnostic service 0x27 state machine and access-mask consumers. This is static analysis of an update, not a full physical dump or demonstrated steering modification.

## FRF, ODX, and payload lineage

`scripts/verify_1061_frf.py` adapts the inspected public VW_Flash container transform at pinned commit `293f46d782bae2ced930497889b71eb782f122cb`. It does not execute downloaded source or imported legacy utilities. All three FRFs decode into ZIPs whose sole member exactly equals the archived ODX; ZIP CRCs pass. All six ERASE/DATA payloads equal the earlier ODX extraction. [Full lineage, source hashes and offsets](../evidence/frf-lineage-1061-2026-10-19.md).

| Component | DATA bytes | DATA SHA-256 | Literal ODX source address | Matched DATA CRC32 |
| --- | ---: | --- | --- | --- |
| H1 | 462848 | `75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641` | `07` | `423BE503` |
| H2 | 53248 | `6da9a40580a2bd49b5097f6c7363a2080a76575e230b7cf8fe54a3f7a61ce5f7` | `06` | `827F508F` |
| H7 | 24576 | `10c11c159565aeff7750a8c4ebe67b2ef25e44e1ce599dbec54c42a85bbbf64a` | `02` | `2144DF1C` |

The [expanded ODX report](../evidence/odx-lineage-2026-10-19.json) preserves metadata and original IDs. All have DATAFORMAT BINARY, ENCRYPT-COMPRESS-METHOD `00`, ALFID `014101`, and shared expected hardware identifiers. Some internal IDs retain 3Q0/5061 text while outer IDs name 5Q0/1061. These small download-address fields are not CPU load addresses. No compression or authenticity conclusion is inferred solely from their labels.

Historical H1 is exact. Historical H7 SHA-256 `391f6fc7872966a3f980e21534853c0b13164d9b084d6d513fde978178e2a40d` contains one extra leading `00`; historical `[1,24577)` equals decoded `[0,24576)` exactly. The extra byte's cause remains unknown. Originals are preserved; fresh derived bytes live in `analysis/1061/blocks/`.

## CPU and hardware documentation

Competing bounded H1 decoding supports V850 over TriCore. The recovered historical board photo has base chip marking D70F3506. Renesas identifies that part as V850E2/PJ4 with V850E2M core. The applicable manufacturer-authored manual was recovered through a public mirror, with PDF identity/provenance recorded. Tables 1-3/1-4, printed page 24, explicitly give 70F3506/3507 code flash `[0,0x80000)`, data flash `[0x02000000,0x02008000)`, and RAM `[0xfedf6000,0xfee00000)`. The RAM address and size exactly agree with traced firmware startup.

[MCU identification, source hashes, page references, peripheral windows, and limits](MCU_IDENTIFICATION.md). The photo lacks a module label binding it to the user's rack. The selected static profile is strongly supported; exact silicon in the physical user rack is not independently verified. The generic Ghidra language supports E1/E2/E2M; its name alone did not identify the generation. No conclusion transfers to 2Q1, 6C1 or PQ.

## Static component map

| Component | Address range, end exclusive | Evidence |
| --- | --- | --- |
| H2 | `[0x2000,0xf000)` | Its leading code-pointer table agrees with H7's reference to address 0x2000 |
| H7 | `[0x9000,0xf000)` | Exact H2 `[0x7000,0xd000)` suffix; absolute return address 0x915e matches next-instruction offset 0x15e |
| H1 | `[0xf000,0x80000)` | Absolute table 0xfb48 corresponds to H1 offset 0xb48; vector-like sequences at H1 offset 0x1000 align to 0x10000 |

`scripts/build_1061_map.py` validates exact component hashes and overlap, then emits H2 + H1 only. H7 is not appended twice. Output: `analysis/1061/mapped-update.bin`, 516096 bytes, SHA-256 `a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d`. [Mapping lineage](../evidence/static-map-1061-2026-10-19.json).

Missing `[0,0x2000)` is not filled. RAM contents and data-flash contents are absent. Ghidra's separate Program image-base property is zero, while BinaryLoader's actual initialized block starts at 0x2000. Keep those separate. No hardware reset entry or actual execution is claimed.

## Code/data refinement and register context

The original broad database, `analysis/1061/ghidra/mapped-1061.gpr`, is preserved. Its automatic pointer discovery mistook a numeric table value at address `0x78318` for a pointer to `0x55900`, then decoded an invalid switch and branched across data. Thirty adjacent 32-bit words at `[0x78300,0x78378)` are exact integer squares; the problematic value is `592 * 592`. It is numeric data, not evidence of an executable entry.

The observed final small code function spans `[0x555f0,0x55606)`. `[0x55606,0x55800)` is entirely FF padding; metadata begins at 0x55800. The refined analysis treats `[0x55606,0x80000)` as a non-executable data candidate region and types the verified records. This removes that false-code expansion. It is an analysis partition supported by the tail/padding/tables, not proof of every byte's semantics. Lower mixed code/data and unresolved indirect branches remain subject to normal review.

Startup at `0x100c0..0x100d6` establishes application `tp=0x5d800`, `gp=0xfee01000`. The refined script supplies those defaults to application ranges only; it does not transfer them to boot code. The manual-confirmed 40 KiB RAM range is added as **uninitialized** memory, never as fabricated zero bytes. Remaining warnings about uninitialized RAM and missing low memory are preserved.

The refined database reports 1757 candidate functions, down from 1907 in the broad run. These are analysis counts, not a verified inventory of real functions. [Refinement facts](../evidence/code-data-refinement-1061-2026-10-19.json), [mapped readback](../evidence/ghidra-refined-1061-2026-10-19.txt).

## Historical table: bytes, role, and consumers

H1 offset `0x48a20` maps to static address `0x57a20`.

| Row address | Raw first two bytes | Little-endian 32-bit constant | Access-mask byte |
| --- | --- | ---: | --- |
| `0x57a20` | `17 6e` | 28183 | `01` |
| `0x57a28` | `33 ae` | 44595 | `02` |
| `0x57a30` | `31 4b` | 19249 | `04` |
| `0x57a38` | `af 7a` | 31407 | `08` |
| `0x57a40` | `52 ee` | 61010 | `10` |

Rows are eight bytes: uint32 constant, one mask byte, three zero bytes. The constants fit in uint16, but the consumer loads a **32-bit word**. The last two values in the old README used the opposite byte order, yielding 44922 and 21230. Preserve the old prose as historical evidence while using the observed byte order here.

The missing reference had a concrete explanation: `0x2feea` computes `tp - 0x5de0`, which equals `0x57a20`. Instruction `0x2fef0` loads the current row; the loop advances eight bytes and checks five rows. After supplying startup context, Ghidra resolves both the table reference and the row's mask load at `0x2ff16`.

The descriptor at `0x582fc` contains service ID `0x27`, handler address `0x30006`, and flags `0x2e00`. Handler 0x30006 calls state machine 0x2fd96. That state machine consumes the table and calls helper 0x2fd2a, which conditionally adds the selected constant to a local challenge-derived value before comparison. A successful branch writes the selected row's mask to RAM `0xfedfaf85`. Static consumers read that mask at `0x3014a`, `0x4c65e`, `0x4d3d4`, `0x4d638`, `0x4fe78`, `0x5036e`, and `0x50576`. Several paths include access checks and return 0x33 when conditions are not met.

This establishes diagnostic access-control use, improving on the previous pattern-only claim. It does not demonstrate that typing any constant into a diagnostic tool succeeds, does not validate an unknown access level in a vehicle, and says nothing about steering torque modification. State, session, timing, transformation and other conditions still matter. No diagnostic request was sent.

Core evidence: [typed state machine and dispatcher](../evidence/ghidra-diagnostic-core-2026-10-19.txt), [mask references](../evidence/ghidra-diagnostic-annotations-2026-10-19.txt), [consumer assembly/pseudocode](../evidence/ghidra-access-mask-consumers-2026-10-19.txt). Names such as `diagnostic_service_27_state_machine` describe verified static roles. These are direct Ghidra observations, not REA Evidence records.

## Reproduction and validation

Use existing Ghidra 12.1.4 and the recorded JDK. First-time public reference acquisition is explicit:

```sh
python3 scripts/inspect_1061_odx.py
python3 scripts/verify_1061_frf.py --fetch-reference
```

Once the pinned reference files exist, the complete analysis runs offline:

```sh
JAVA_HOME=/Users/brendanballon/Library/Java/JavaVirtualMachines/openjdk-25.0.2/Contents/Home \
  scripts/run_1061_analysis.sh fresh-project-name
```

The script refuses an existing project name. It verifies lineage, rebuilds the map, imports a refined project, runs bounded analysis, types/labels diagnostic records, and exports the selected functions. It does not install anything, run target code, or change originals. Reproduction outputs go under ignored `analysis/1061/`.

Current annotated database: `analysis/1061/ghidra/refined-1061.gpr`. Fresh validation database: `analysis/1061/ghidra/verified-1061-reproduction.gpr`. The fresh-run diagnostic export is byte-identical to `evidence/ghidra-diagnostic-core-2026-10-19.txt`. Completed outputs, scripts, and archive integrity are bound by [validation manifest](../evidence/offline-preparation-validation-2026-10-19.json).

REA 6.7.0 still rejects V850 raw imports. The documented direct Ghidra workflow resolves the practical firmware-analysis route without patching REA or choosing a false architecture. The separately inspected public ALC host ELF uses REA's supported ARM64 route; it is a different artifact and workstream.

## Closure and external dependencies

See [ACTION_ITEMS.md](ACTION_ITEMS.md) for completed preparation items and genuinely unavailable dependencies, and [SOURCE_RECOVERY.md](SOURCE_RECOVERY.md) for the public/local search boundary. Missing physical contents and owner-held historical artifacts are not labeled complete. Steering-limit discovery, firmware changes and hardware validation are future research tasks, not completed by this preparation pass.
