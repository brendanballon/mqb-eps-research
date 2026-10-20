#!/usr/bin/env python3
"""Verify 1061 FRF container lineage without running imported utilities.

The container transform follows bri3d/VW_Flash, pinned below. The downloaded
source is retained for inspection, never imported or executed by this script.
Transform copyright (c) 2022-2024, Brian Ledbetter and contributors.
See scripts/licenses/VW_Flash-BSD-2-Clause.txt for its license and disclaimer.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'EPS_research/MQB/5Q0, 3Q0'
OUT = ROOT / 'analysis/1061/frf-derived'
REFERENCE = ROOT / 'analysis/1061/frf-source'
COMMIT = '293f46d782bae2ced930497889b71eb782f122cb'
UPSTREAM = 'https://github.com/bri3d/VW_Flash'
FILES = {
    'frf/decryptfrf.py': '52bd9e72d214aebd8713dc413e5b96bfb5d481378cdedc7221c57faba06d57c5',
    'data/frf.key': '08909854ee0856571035b53bb0b260d13a01fb66a0357f84540a5892376a1ee3',
    'LICENSE': 'd08b7d9656eb0c078ebc71926be5a6c3fecb36f695e4d01105ba9f3b917d6ccc',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(data), 'sha256': sha(data)}


def decode_container(encrypted, key):
    output = bytearray()
    first_seed, second_seed = 0, 1
    for index, value in enumerate(encrypted):
        key_byte = key[index % len(key)]
        first_seed = ((first_seed + key_byte) * 3) & 255
        output.append(value ^ first_seed ^ 255 ^ second_seed ^ key_byte)
        second_seed = ((second_seed + 1) * first_seed) & 255
    return bytes(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch-reference', action='store_true',
                        help='Fetch only the three pinned public reference files')
    args = parser.parse_args()
    REFERENCE.mkdir(parents=True, exist_ok=True)
    refs = []
    for relative, expected in FILES.items():
        path = REFERENCE / Path(relative).name
        url = f'https://raw.githubusercontent.com/bri3d/VW_Flash/{COMMIT}/{relative}'
        if args.fetch_reference and not path.exists():
            data = urllib.request.urlopen(url, timeout=30).read()
            if sha(data) != expected:
                raise ValueError(f'Reference digest mismatch: {relative}')
            path.write_bytes(data)
        if sha(path.read_bytes()) != expected:
            raise ValueError(f'Reference digest mismatch: {relative}')
        refs.append({'url': url, **identity(path)})
    key = (REFERENCE / 'frf.key').read_bytes()
    OUT.mkdir(parents=True, exist_ok=True)
    report = {
        'method': 'Inspected recursive XOR FRF container transform, Python ZIP CRC verification, exact XML and payload comparisons',
        'upstream': {'repository': UPSTREAM, 'commit': COMMIT, 'reference_files': refs},
        'script': identity(Path(__file__)),
        'limitations': [
            'Local byte lineage only. No authenticity, hardware compatibility or installation claim.',
            'Container transform is distinct from ECU security access. No seed/key script is interpreted.',
            'Only the three 5Q0909144R 1061 containers and their duplicate copies are covered.',
            'Original files are read only. Only derived ZIP, XML and payload bytes are written.',
        ],
        'files': [],
    }
    for tag in ('H1', 'H2', 'H7'):
        stem = f'FL_5Q0909144R_{tag}_1061'
        original = BASE / '1_original-update-files' / f'{stem}.frf'
        duplicate = ROOT / 'EPS_research/clean-update-files' / original.name
        container = decode_container(original.read_bytes(), key)
        zip_path = OUT / f'{stem}.zip'
        zip_path.write_bytes(container)
        item = {'frf': identity(original), 'duplicate_frf': identity(duplicate),
                'duplicate_exact_match': original.read_bytes() == duplicate.read_bytes(),
                'derived_zip': identity(zip_path), 'members': []}
        with zipfile.ZipFile(io.BytesIO(container)) as archive:
            if archive.testzip() is not None:
                raise ValueError('ZIP CRC failure')
            members = archive.infolist()
            if len(members) != 1 or members[0].filename != f'{stem}.odx':
                raise ValueError('Unexpected ZIP member inventory')
            for member in members:
                xml = archive.read(member)
                old = BASE / '2_odx' / member.filename
                xml_path = OUT / member.filename
                xml_path.write_bytes(xml)
                header = member.header_offset
                name_len, extra_len = struct.unpack_from('<HH', container, header + 26)
                compressed_start = header + 30 + name_len + extra_len
                detail = {'member_name': member.filename,
                          'zip_local_header_offset': header,
                          'zip_compressed_data_offset': compressed_start,
                          'zip_compressed_data_end_exclusive': compressed_start + member.compress_size,
                          'compression_type': member.compress_type,
                          'compressed_bytes': member.compress_size,
                          'zip_crc32': f'{member.CRC:08X}',
                          'crc32_matches': zlib.crc32(xml) == member.CRC,
                          'derived_odx': identity(xml_path), 'archive_odx': identity(old),
                          'odx_exact_match': xml == old.read_bytes(), 'payloads': []}
                if not detail['odx_exact_match']:
                    raise ValueError('ODX differs from historical archive')
                root = ET.fromstring(xml)
                for flash in root.iter('FLASHDATA'):
                    name = flash.findtext('SHORT-NAME')
                    payload = bytes.fromhex(flash.findtext('DATA'))
                    path = OUT / f'{stem}_{name}.bin'
                    path.write_bytes(payload)
                    previous = ROOT / 'analysis/1061/blocks' / path.name
                    comparison = previous.read_bytes()
                    data_text = flash.findtext('DATA').encode('ascii')
                    flash_id = re.escape(flash.attrib['ID'].encode('ascii'))
                    span = re.search(rb'<FLASHDATA\b[^>]*\bID="' + flash_id
                                     + rb'"[^>]*>.*?<DATA>([0-9A-Fa-f\s]+)</DATA>',
                                     xml, re.DOTALL)
                    if span is None or span.group(1) != data_text:
                        raise ValueError('XML DATA source span mismatch')
                    xml_start = span.start(1)
                    detail['payloads'].append({
                        'id': flash.attrib['ID'], 'derived_payload': identity(path),
                        'prior_odx_extraction': identity(previous),
                        'payload_exact_match': payload == comparison,
                        'xml_hex_text_offset': xml_start,
                        'xml_hex_text_end_exclusive': xml_start + len(data_text),
                        'crc32': f'{zlib.crc32(payload):08X}',
                    })
                    if payload != comparison:
                        raise ValueError('Payload differs from prior ODX extraction')
                item['members'].append(detail)
        report['files'].append(item)
    dest = ROOT / 'evidence/frf-lineage-1061-2026-10-19.json'
    dest.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(dest.relative_to(ROOT)),
                      'odx_exact_matches': [m['odx_exact_match'] for f in report['files'] for m in f['members']],
                      'payload_exact_matches': [p['payload_exact_match'] for f in report['files'] for m in f['members'] for p in m['payloads']]}))


if __name__ == '__main__':
    main()
