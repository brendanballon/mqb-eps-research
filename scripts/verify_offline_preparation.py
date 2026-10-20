#!/usr/bin/env python3
"""Verify preserved inputs and concrete outputs of the offline preparation."""
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'evidence/offline-preparation-validation-2026-10-19.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(data), 'sha256': digest(data)}


def require(value, message):
    if not value:
        raise ValueError(message)


def main():
    checks = []
    manifest = json.loads((ROOT / 'inventory/archive-manifest.json').read_text())
    for record in manifest['files']:
        data = (ROOT / record['path']).read_bytes()
        require(len(data) == record['size_bytes'] and digest(data) == record['sha256'],
                f'Original archive identity changed: {record["path"]}')
    checks.append({'name': 'original_archive', 'passed': True, 'files_checked': len(manifest['files'])})
    parsed = 0
    for path in (ROOT / 'evidence').rglob('*.json'):
        if path != DEST:
            json.loads(path.read_text())
            parsed += 1
    checks.append({'name': 'evidence_json_parse', 'passed': True, 'files_checked': parsed})
    lineage = json.loads((ROOT / 'evidence/frf-lineage-1061-2026-10-19.json').read_text())
    odx_matches = payload_matches = 0
    for component in lineage['files']:
        for member in component['members']:
            actual = (ROOT / member['derived_odx']['path']).read_bytes()
            old = (ROOT / member['archive_odx']['path']).read_bytes()
            require(actual == old and digest(actual) == member['derived_odx']['sha256'], 'ODX lineage mismatch')
            odx_matches += 1
            for payload in member['payloads']:
                actual = (ROOT / payload['derived_payload']['path']).read_bytes()
                old = (ROOT / payload['prior_odx_extraction']['path']).read_bytes()
                require(actual == old and digest(actual) == payload['derived_payload']['sha256'], 'Payload lineage mismatch')
                payload_matches += 1
    require((odx_matches, payload_matches) == (3, 6), 'Incomplete lineage set')
    checks.append({'name': 'exact_lineage_outputs', 'passed': True, 'odx_matches': odx_matches, 'payload_matches': payload_matches})
    data = (ROOT / 'analysis/1061/mapped-update.bin').read_bytes()
    require(len(data) == 516096 and digest(data) == 'a785ba137aa8b6e8a5d0d54cbb3f26108a273f23acdf6ca4f808b1e46186ff9d', 'Mapped image identity mismatch')
    for index, expected in enumerate([28183, 44595, 19249, 31407, 61010]):
        off = 0x57a20 - 0x2000 + index * 8
        value, mask = struct.unpack_from('<II', data, off)
        require(value == expected and mask == 1 << index, 'Diagnostic table mismatch')
    require(struct.unpack_from('<3I', data, 0x582fc - 0x2000) == (0x27, 0x30006, 0x2e00), 'Service descriptor mismatch')
    require(set(data[0x55606 - 0x2000:0x55800 - 0x2000]) == {255}, 'Code-tail padding changed')
    for off in range(0x78300 - 0x2000, 0x78378 - 0x2000, 4):
        value = struct.unpack_from('<I', data, off)[0]
        require(math.isqrt(value) ** 2 == value, 'Square-table corroboration changed')
    checks.append({'name': 'mapped_bytes_and_structures', 'passed': True})
    for name in ['refined-1061', 'verified-1061-reproduction']:
        require((ROOT / f'analysis/1061/ghidra/{name}.gpr').exists(), f'Missing saved project: {name}')
    original = (ROOT / 'evidence/ghidra-diagnostic-core-2026-10-19.txt').read_bytes()
    reproduced = (ROOT / 'analysis/1061/verified-1061-reproduction-diagnostics.txt').read_bytes()
    require(original == reproduced, 'Fresh diagnostic export differs')
    checks.append({'name': 'fresh_end_to_end_reproduction', 'passed': True,
                   'diagnostic_export_sha256': digest(original), 'byte_identical': True})
    mcu = json.loads((ROOT / 'evidence/mcu-identification-2026-10-19/manifest.json').read_text())
    for record in mcu['files']:
        actual = identity(ROOT / record['path'])
        require(actual['sha256'] == record['sha256'] and actual['bytes'] == record['bytes'], 'Recovered MCU source identity changed')
    checks.append({'name': 'recovered_mcu_sources', 'passed': True, 'files_checked': len(mcu['files'])})
    alc = ROOT / 'analysis/public-alc/alc.cpython-312-aarch64-linux-gnu.so'
    require(digest(alc.read_bytes()) == 'bc3bab44f449522bb5e8ff97bf2a12e02941ef14ff5af6ba10b96e6e72d56775', 'Public ALC artifact mismatch')
    require((ROOT / 'analysis/public-alc/rea-snapshot.json').exists(), 'Missing closed-session snapshot')
    checks.append({'name': 'public_alc_identity_and_snapshot', 'passed': True})
    remotes = subprocess.run(['git', 'remote'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    require(not remotes, 'Unexpected Git remote')
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    checks.append({'name': 'local_git_boundaries_and_whitespace', 'passed': True})
    paths = [ROOT / 'inventory/archive-manifest.json', ROOT / 'README.md']
    for folder in ['notes', 'scripts', 'evidence']:
        paths.extend(p for p in (ROOT / folder).rglob('*') if p.is_file()
                     and p != DEST and '__pycache__' not in p.parts and p.suffix != '.pyc')
    report = {'date': '2026-10-19', 'scope': 'Offline preparation outputs and provenance checks; no target execution',
              'checks': checks, 'all_checks_passed': True,
              'limits': ['Fresh export equality verifies reproduction, not correctness of every inferred function or runtime behavior.',
                         'Missing user-board binding and original external artifacts remain unresolved in ACTION_ITEMS.md.'],
              'files': [identity(path) for path in sorted(set(paths))]}
    DEST.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(DEST.relative_to(ROOT)), 'checks_passed': len(checks), 'archive_files': len(manifest['files']), 'bound_files': len(report['files'])}))


if __name__ == '__main__':
    main()
