#!/usr/bin/env python3
"""Reproduce selected ODX payload lineage without executing imported tools."""
import hashlib
import json
from pathlib import Path
import struct
import zlib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'EPS_research/MQB/5Q0, 3Q0'
OUT = ROOT / 'analysis/1061/blocks'
REPORT = ROOT / 'evidence/odx-lineage-2026-10-19.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(data), 'sha256': sha(data)}


def tree(element):
    return {'tag': element.tag, 'attributes': element.attrib,
            'text': (element.text or '').strip(),
            'children': [tree(child) for child in element]}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'method': 'Python stdlib XML, hex decoding, SHA-256 and zlib CRC32',
              'limitations': [
                  'FRF files are hashed as candidate ancestors. FRF to ODX conversion was not reproduced.',
                  'Download source addresses are literal ODX fields, not established CPU mappings.',
                  'Checksum agreement establishes byte consistency, not authenticity or hardware applicability.',
                  'No original archive files are written. No firmware or legacy tool is executed.'
              ], 'files': []}
    for odx in sorted((BASE / '2_odx').glob('FL_5Q0909144R_*_1061.odx')):
        root = ET.parse(odx).getroot()
        item = {'odx': identity(odx), 'flash': root.find('FLASH').attrib,
                'candidate_frf': [identity(p) for folder in [BASE / '1_original-update-files', ROOT / 'EPS_research/clean-update-files']
                                  for p in [folder / odx.with_suffix('.frf').name] if p.exists()],
                'frf_to_odx_verified': False,
                'expected_idents': [tree(e) for e in root.iter('EXPECTED-IDENT')],
                'security_metadata': [tree(e) for e in root.iter('SECURITY')
                                      if e.findtext('SECURITY-METHOD') in ('CRC32', 'ALFID')],
                'datablocks': [tree(e) for e in root.iter('DATABLOCK')], 'payloads': []}
        for flashdata in root.iter('FLASHDATA'):
            data = bytes.fromhex(flashdata.findtext('DATA'))
            name = flashdata.findtext('SHORT-NAME')
            path = OUT / (odx.stem + '_' + name + '.bin')
            path.write_bytes(data)
            checksums = [s.findtext('FW-CHECKSUM') for s in root.iter('SECURITY')
                         if s.findtext('SECURITY-METHOD') == 'CRC32'
                         and s.findtext('VALIDITY-FOR') == name.replace('FD_', 'DB_', 1)]
            payload = {'id': flashdata.attrib['ID'], 'output': identity(path),
                       'dataformat': flashdata.find('DATAFORMAT').attrib,
                       'encrypt_compress_method': flashdata.findtext('ENCRYPT-COMPRESS-METHOD'),
                       'crc32_zlib': f'{zlib.crc32(data):08X}', 'declared_crc32': checksums,
                       'crc32_matches': bool(checksums) and all(int(c, 16) == zlib.crc32(data) for c in checksums),
                       'first_64_bytes': data[:64].hex(), 'last_32_bytes': data[-32:].hex()}
            historical = BASE / '3_bin' / odx.with_suffix('.bin').name
            if historical.exists() and name == 'FD_0DATA':
                old = historical.read_bytes()
                payload['historical'] = {'identity': identity(historical), 'exact_match': old == data,
                                         'extra_leading_byte_only': len(old) == len(data) + 1 and old[1:] == data,
                                         'leading_byte_hex': old[:1].hex()}
            if '_H1_' in odx.name and name == 'FD_0DATA':
                offset = 0x48a20
                rows = []
                for index in range(5):
                    pos = offset + index * 8
                    raw = data[pos:pos + 8]
                    value, padding, flag = struct.unpack('<HHI', raw)
                    rows.append({'file_offset': hex(pos), 'raw': raw.hex(), 'value_le16': value,
                                 'value_be16': int.from_bytes(raw[:2], 'big'), 'padding': padding, 'flag_le32': flag})
                payload['historical_table_candidate'] = {'file_offset': hex(offset), 'rows': rows,
                    'limitation': 'Observed table bytes only. No code references, security role or runtime behavior verified.'}
            item['payloads'].append(payload)
        report['files'].append(item)
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(REPORT.relative_to(ROOT)), 'files': len(report['files']),
                      'data_crc_matches': [p['crc32_matches'] for f in report['files'] for p in f['payloads'] if p['declared_crc32']]}))


if __name__ == '__main__':
    main()
