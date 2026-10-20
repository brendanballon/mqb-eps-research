#!/usr/bin/env python3
"""Read candidate HCA thresholds from the exact mapped 1061 image. No writes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE = ROOT / "analysis/1061/mapped-update.bin"
SHA256 = "a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d"
BASE = 0x2000


def main():
    data = IMAGE.read_bytes()
    if hashlib.sha256(data).hexdigest() != SHA256:
        raise SystemExit("Image identity differs. Refusing the 1061 address profile.")

    def u16(address):
        return int.from_bytes(data[address - BASE:address - BASE + 2], "little")

    def scalar(address, role, consumer, scale):
        return {
            "address": hex(address), "mapped_file_offset": hex(address - BASE),
            "h1_offset": hex(address - 0xf000),
            "bytes": data[address - BASE:address - BASE + 2].hex(" "),
            "uint16": u16(address), "role": role, "consumer": consumer,
            "display_value": u16(address) / scale, "display_divisor": scale,
        }

    def curve(address):
        count = u16(address)
        if not 1 <= count <= 32:
            raise SystemExit("Unexpected curve count.")
        return {
            "address": hex(address), "mapped_file_offset": hex(address - BASE),
            "h1_offset": hex(address - 0xf000), "count": count,
            "x_raw": [u16(address + 2 + i * 2) for i in range(count)],
            "y_raw": [u16(address + 2 + (count + i) * 2) for i in range(count)],
            "x_units": "unresolved", "y_scale_candidate": "Q13 multiplier",
        }

    threshold = u16(0x5e638)
    examples = []
    for magnitude in (299, 300, 304, 305, 306, 500, 511):
        row = {"wire_magnitude_cNm": magnitude}
        for sign in (1, -1):
            internal = (sign * min(magnitude, 500) * 0xa3d) >> 8
            key = "positive" if sign == 1 else "negative"
            row[key] = {"decoded": internal, "passes_magnitude_check": abs(internal) <= threshold}
        examples.append(row)
    report = {
        "artifact": {"path": str(IMAGE.relative_to(ROOT)), "sha256": SHA256,
                     "load_base": hex(BASE), "h1_sha256": "75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641"},
        "evidence_type": "direct Ghidra static observations plus analyst arithmetic model",
        "decoder": {"function": "0x2b530", "input_buffer": "0xfedf9b70",
                    "output": "0xfedfab26", "formula": "(clamp(signed_cNm, -500, 500) * 2621) >> 8",
                    "instructions": "0x2b584..0x2b5a2", "status_constraints": "status >7 produces sentinel 0x7fff"},
        "scalars": [
            scalar(0x5e638, "request magnitude eligibility threshold", "0x24e06..0x24e12", 1024),
            scalar(0x5e63a, "downstream symmetric target bound", "0x24694", 1024),
            scalar(0x5e630, "request change comparison threshold", "0x24dfc..0x24e02", 1024),
            scalar(0x5e804, "post-interpolation multiplier", "0x2553e..0x25546", 8192),
        ],
        "immediate_output_bounds": {"function": "0x24aec", "instructions": "0x25528..0x25560",
                                    "raw": [-6144, 6144], "candidate_Nm": [-6, 6]},
        "curve_pointer_table": "0x5f738", "curves": [curve(a) for a in (0x5fcde, 0x5fcfa, 0x5fd16)],
        "boundary_examples": examples,
        "limitations": [
            "No firmware execution or vehicle observation. Arithmetic examples model only decoding and one comparison.",
            "Nm interpretation combines external DBC centiNm units with observed conversion, approximately 1024 internal units per Nm.",
            "Eligibility requires additional state, validity, timing and vehicle conditions. Passing magnitude alone does not enable assistance.",
            "Output bounds are intermediate signal bounds, not measured motor torque or guaranteed steering authority.",
            "Curve axis units, active profile selection, downstream arbitration and complete override logic remain unresolved.",
            "No patch, checksum correction, flashing path or modified-firmware validation is provided.",
        ],
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
