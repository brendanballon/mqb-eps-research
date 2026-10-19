#!/usr/bin/env python3
"""Record local archive identity without changing input files."""

import hashlib
import json
from collections import Counter
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    archive = root / "EPS_research"
    records = []
    for path in sorted(archive.rglob("*")):
        if path.is_symlink():
            raise RuntimeError(f"Review symlink before inventory: {path}")
        if not path.is_file() or path.name == ".DS_Store":
            continue
        digest = hashlib.sha256()
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
        records.append({
            "path": path.relative_to(root).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": digest.hexdigest(),
        })
    counts = Counter(record["sha256"] for record in records)
    result = {
        "schema_version": 1,
        "scope": "All regular files under EPS_research except .DS_Store",
        "provenance": "Pre-existing local archive. Upstream completeness and authenticity unverified.",
        "file_count": len(records),
        "total_bytes": sum(record["size_bytes"] for record in records),
        "unique_sha256_count": len(counts),
        "files": records,
    }
    output = root / "inventory" / "archive-manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "files"}, indent=2))


if __name__ == "__main__":
    main()
