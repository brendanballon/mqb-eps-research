#!/usr/bin/env python3
"""Build an evidence-backed static map. No missing flash bytes are invented."""
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = ROOT / 'analysis/1061/blocks'
OUT = ROOT / 'analysis/1061/mapped-update.bin'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    payloads = {}
    for component in ['H1', 'H2', 'H7']:
        path = BLOCKS / f'FL_5Q0909144R_{component}_1061_FD_0DATA.bin'
        payloads[component] = (path, path.read_bytes())
    h1, h2, h7 = [payloads[c][1] for c in ['H1', 'H2', 'H7']]
    expected = [
        '75fd1641e3826e71bdc09a45a0e1581f0e43b01352e23c441b87f01f7d965641',
        '6da9a40580a2bd49b5097f6c7363a2080a76575e230b7cf8fe54a3f7a61ce5f7',
        '10c11c159565aeff7750a8c4ebe67b2ef25e44e1ce599dbec54c42a85bbbf64a'
    ]
    if [digest(data) for data in [h1, h2, h7]] != expected:
        raise ValueError('Payload identities differ from the examined 1061 set')
    if len(h2) != 0xd000 or len(h1) != 0x71000 or h2[0x7000:] != h7:
        raise ValueError('Unexpected component relationship')
    mapped = h2 + h1
    OUT.write_bytes(mapped)
    report = {'method': 'Contiguous static map inferred from independent V850 address relationships',
              'mapping_confidence': 'Corroborated static working map, not hardware-read verification',
              'output': {'path': str(OUT.relative_to(ROOT)), 'bytes': len(mapped), 'sha256': digest(mapped)},
              'load_base': '0x2000', 'end_exclusive': '0x80000',
              'missing_ranges': [{'start': '0x0', 'end_exclusive': '0x2000', 'status': 'not supplied, not filled'}],
              'segments': [],
              'corroboration': [
                  {'input': 'H7', 'file_offset': '0x156', 'observation': 'Decoded mov 0x915e,lp immediately precedes jmp [r27] at file offset 0x15c; next instruction is file offset 0x15e', 'inference': 'Software return address matches H7 base 0x9000'},
                  {'observation': 'H7 exactly equals H2 byte range [0x7000,0xd000)', 'inference': 'H2 base 0x2000 aligns shared bytes at 0x9000'},
                  {'input': 'H7', 'file_offset': '0x14c', 'observation': 'mov 0x2000,r29; ld.w 0x0[r29],r27; jmp [r27]', 'inference': 'H2 leading word table at address 0x2000 supplies code targets'},
                  {'input': 'H1', 'file_offset': '0x7c', 'observation': 'Function uses absolute 0xfb48 plus eight-byte index; H1 offset 0xb48 contains eight-byte pointer/flag records', 'inference': 'H1 base 0xf000 aligns these records and ends at 0x80000'}],
              'h2_leading_code_pointer_candidates': [],
              'limitations': ['No hardware dump or runtime execution. Exact MCU and RAM/peripheral map remain unverified.',
                              'H7 overlaps H2 and is not concatenated a second time.',
                              'Only the supplied update ranges are mapped. No claim of a complete flash image.',
                              'A function return-address convention supports the H7 base inference; it is not an observed execution.']}
    for c, base in [('H2', 0x2000), ('H1', 0xf000), ('H7', 0x9000)]:
        path, data = payloads[c]
        report['segments'].append({'component': c, 'path': str(path.relative_to(ROOT)), 'sha256': digest(data),
                                   'source_start': 0, 'source_end_exclusive': len(data), 'address_start': hex(base),
                                   'address_end_exclusive': hex(base + len(data)), 'output_offset': base - 0x2000,
                                   'role': 'overlapping H2 suffix' if c == 'H7' else 'contiguous source bytes'})
    for off in range(0, 0xc8, 4):
        ptr = struct.unpack_from('<I', h2, off)[0]
        source_off = ptr - 0x2000
        report['h2_leading_code_pointer_candidates'].append({'table_file_offset': hex(off), 'target_address': hex(ptr),
            'target_h2_file_offset': hex(source_off), 'target_first_8_bytes': h2[source_off:source_off+8].hex()})
    (ROOT / 'evidence/static-map-1061-2026-10-19.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['output']))


if __name__ == '__main__':
    main()
