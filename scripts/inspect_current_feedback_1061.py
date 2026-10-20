#!/usr/bin/env python3
"""Read ADC pointer lineage, feedback constants and a phase protection threshold."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = 'a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d'


def inspect():
    image = (ROOT / 'analysis/1061/mapped-update.bin').read_bytes()
    if hashlib.sha256(image).hexdigest() != EXPECTED:
        raise ValueError('Unexpected mapped image identity')

    def read(address, length):
        offset = address - 0x2000
        if offset < 0 or offset + length > len(image):
            raise ValueError('Address outside supplied update')
        return image[offset:offset + length]

    def field(address, length=2):
        data = read(address, length)
        return {'address': hex(address), 'mapped_offset': hex(address - 0x2000),
                'h1_offset': hex(address - 0xf000) if address >= 0xf000 else None,
                'bytes_hex': data.hex(' '), 'unsigned_le': int.from_bytes(data, 'little')}

    pointers = []
    for destination in (0xfedfc058, 0xfedfc064, 0xfedfc0d0, 0xfedfc0d4):
        source = 0x537e0 + destination - 0xfedfa8a0
        pointers.append({'ram_destination': hex(destination), 'flash_initializer': field(source, 4)})

    records = []
    for index in range(3):
        source = 0x61000 + index * 0x6c0
        if read(source + 0x6b3, 1) != bytes([index]):
            raise ValueError('Record identity mismatch')
        fields = []
        for address, role in ((0x60110, 'phase feedback normalization multiplier'),
                              (0x60500, 'phase feedback normalization shift'),
                              (0x60404, 'phase feedback signed magnitude clamp')):
            item = field(source + address - 0x60000)
            item.update({'conditional_destination': hex(address), 'role': role})
            fields.append(item)
        records.append({'selector': index, 'source': hex(source), 'fields': fields})

    return {
        'date': '2026-10-20', 'evidence_type': 'static byte/instruction analysis',
        'input_sha256': EXPECTED, 'pointer_initializers': pointers,
        'adc': {'registers': ['0xffffdc40', '0xffffdc44'],
                'channels': [1, 2], 'module': 'ADCA0', 'sample_mask': '0x3ff',
                'ctl1': {'address': '0xff81d104', 'written_value': '0x50308001',
                         'CTYP_bit15': 1, 'CRAC_bit24': 0},
                'format': '10-bit right-aligned'},
        'sensor_calibration': {
            'pointer': '0xfedfc064', 'initializer': 0,
            'parser': '0x3e34a', 'record_type': 2, 'record_length': '0x20',
            'source_records': '[0x1000,0x2000), not supplied',
            'gain_offsets': {'mode_zero_phase_A': '0x8', 'mode_nonzero_phase_A': '0xa',
                             'mode_zero_phase_C': '0x10', 'mode_nonzero_phase_C': '0x12'},
            'gain_encoding': 'uint16 little-endian',
            'mode_variable': '0xfedfaecd',
            'offsets': {'mode_zero': ['0xfedfae26', '0xfedfae28'],
                        'mode_nonzero': ['0xfedfae22', '0xfedfae24']},
            'formula_first_stage': 't = ((signed16(offset - (adc & 1023)) * gain) + 512) >> 10',
            'formula_mode_zero': 'phase = signed16((t * 5285 + 256) >> 9)',
            'formula_mode_nonzero': 'phase = signed16((t * 4271 + 1024) >> 11)',
            'third_phase': 'phase_B = signed16(-(phase_A + phase_C))',
            'offset_update': 'Under calibration conditions, average 16 ADC samples with (sum+8)>>4',
            'limitations': 'Gain values absent. Initial zero pointer is not a usable zero gain.'},
        'controller_records': records,
        'normalization_example': {'phase_input': 2880, 'multiplier': 23301, 'shift': 11,
                                  'positive_output': (2880 * 23301) >> 11,
                                  'negative_output_before_saturation': (-2880 * 23301) >> 11,
                                  'saturation': [-32767, 32767], 'unit': 'controller integers'},
        'phase_protection': {'function': '0x1cc22', 'threshold': field(0x5d08e),
                             'inputs': ['0xfedfaac2', '0xfedfaac6'],
                             'counters': ['0xfedfb6d0', '0xfedfb6d2'],
                             'condition': 'abs(phase) >= 2880 increments; below resets counter',
                             'report_on_call_count': 31, 'report_function': '0x1535e',
                             'arguments': [21, 0, 1, 1],
                             'limits': 'Call period, resulting fault action and physical units are unproven'},
        'execution_order': {'function': '0x1c43a',
                            'when': '0xfedfaed8 == 0',
                            'calls': ['0x1c47e', '0x1c3d2', '0x1cc92', '0x1da5a'],
                            'scope': 'Static order, not observed execution'},
        'limits': ['No conversion to amperes or delivered steering torque established.',
                   'No target execution or hardware measurements.',
                   'Template constants are conditional defaults, not confirmed installed calibration.',
                   'Large controller decompilation remains warning-bearing and partially hand-traced.']}


if __name__ == '__main__':
    report = inspect()
    destination = ROOT / 'evidence/current-feedback-1061-2026-10-20.json'
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(destination.relative_to(ROOT)),
                      'phase_threshold': report['phase_protection']['threshold']['unsigned_le']}))
