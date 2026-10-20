#!/usr/bin/env python3
"""Read boot-selected calibration records and model their destination offline."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = 'a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inspect():
    image = (ROOT / 'analysis/1061/mapped-update.bin').read_bytes()
    if sha(image) != EXPECTED:
        raise ValueError('Unexpected mapped input identity')

    def read(address, length):
        offset = address - 0x2000
        if offset < 0 or offset + length > len(image):
            raise ValueError('Read outside supplied update')
        return image[offset:offset + length]

    out = ROOT / 'analysis/1061/controller-calibration-model'
    out.mkdir(exist_ok=True)
    records = []
    for index in range(7):
        source = 0x61000 + index * 0x6c0
        record = read(source, 0x6c0)
        marker = record[0x6b3]
        accepted = marker == index
        entry = {'selector': index, 'source_address': hex(source),
                 'h1_offset': hex(source - 0xf000), 'bytes': len(record),
                 'sha256': sha(record), 'id_byte': marker,
                 'accepted_by_0x90fc': accepted}
        if accepted:
            page = bytearray(b'\xff' * 0x1000)
            page[:0x6b0] = record[:0x6b0]
            page[0xff0:] = record[0x6b0:]
            destination = out / f'selector-{index}-conditional-page.bin'
            destination.write_bytes(page)
            entry['conditional_page'] = {'path': str(destination.relative_to(ROOT)),
                                         'sha256': sha(page), 'bytes': len(page)}
            entry['fields'] = []
            for address, role in ((0x60112, 'signed command conversion multiplier'),
                                  (0x603f8, 'signed command magnitude clamp'),
                                  (0x604d8, 'parallel conversion right shift count'),
                                  (0x604da, 'command conversion right shift count')):
                offset = address - 0x60000
                raw = page[offset:offset + 2]
                entry['fields'].append({'destination_address': hex(address),
                                        'source_address': hex(source + offset),
                                        'source_h1_offset': hex(source + offset - 0xf000),
                                        'bytes_hex': raw.hex(' '),
                                        'unsigned_le': int.from_bytes(raw, 'little'),
                                        'signed_le': int.from_bytes(raw, 'little', signed=True),
                                        'role': role})
            values = {f['destination_address']: f['unsigned_le'] for f in entry['fields']}
            gain, shift = values['0x60112'], values['0x604da']
            entry['command_conversion'] = {
                'instruction_range': '0x48058..0x480a2',
                'formula': 'sat[-32767,32767]((clamp(x,-9216,9216) * gain) >> shift)',
                'gain': gain, 'shift': shift, 'gain_over_2_power_shift': gain / (1 << shift),
                'scope': 'One conversion stage only; later filtering and state selection still apply',
                'examples': [{'input': x, 'stage_output': max(-32767, min(32767,
                             (max(-9216, min(9216, x)) * gain) >> shift))}
                             for x in (-9216, -8192, -1024, 0, 1024, 8192, 9216)]}
        records.append(entry)
    return {'schema': 1, 'date': '2026-10-20', 'evidence_type': 'static reads and conditional copy model',
            'input_sha256': EXPECTED, 'load_base': '0x2000',
            'raw_page': {'address': '0x60000', 'length': 4096,
                         'all_ff': read(0x60000, 4096) == b'\xff' * 4096,
                         'sha256': sha(read(0x60000, 4096))},
            'boot_blank_check': {'function': '0x90e0', 'words': ['0x60000', '0x60ffc'],
                                'condition': 'Both words equal 0xffffffff', 'result': '0xa2'},
            'selection': {'function': '0x90be', 'record_lookup': '0xbaa0(0xa8)',
                          'lookup_range': '[0x1000,0x1ff0)',
                          'index': 'record byte at +7 if below 7, otherwise 0; absent record gives 0',
                          'limitation': 'Lookup bytes are absent from this update'},
            'copy': {'function': '0x912a', 'source': '0x61000 + index * 0x6c0',
                     'body': {'source_offset': '0x0', 'destination': '0x60000', 'length': '0x6b0'},
                     'metadata': {'source_offset': '0x6b0', 'destination': '0x60ff0', 'length': '0x10'},
                     'assumption': 'Successful blank-page erase/program path; not emulation or an observed ECU write'},
            'records': records,
            'limitations': ['The installed rack may already have a populated or modified page.',
                            'No current or mechanical torque units established.',
                            'No firmware execution, flashing or hardware access.',
                            'Derived pages are analysis models, never replacements for original bytes.']}


if __name__ == '__main__':
    report = inspect()
    path = ROOT / 'evidence/controller-calibration-1061-2026-10-20.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(path.relative_to(ROOT)),
                      'accepted_selectors': [r['selector'] for r in report['records'] if r['accepted_by_0x90fc']]}))
