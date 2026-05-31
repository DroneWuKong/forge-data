#!/usr/bin/env python3
"""
validate.py — integrity check for the Forge Data parts/platforms database.

This is the canonical public dataset consumed by the Forge build planner
(uas-forge.com) and Prismo. The counts are correct today only by manual
discipline — nothing stopped a hand-edit from drifting manifest.json out of sync
with the parts/*.json files (and the README). This validator closes that gap.

Checks (all must pass; exit 1 on any failure):
  1. Every JSON file in the repo is well-formed.
  2. Every category in manifest.parts points at a file that exists, and that
     file's item count matches the manifest's `count`.
  3. manifest.total_parts == sum of all category counts.
  4. The platforms file exists and its count matches manifest.platforms.count.
  5. The README headline figures (components / categories / platforms) match
     the manifest — so the front-door numbers can't silently drift.

Usage:
    python3 validate.py          # validate; exit 0 on success, 1 on failure
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest.json"
README = ROOT / "README.md"


def _count_items(path: Path) -> int:
    """Item count for a parts/platforms JSON file, tolerant of common shapes:
    a bare list, or a dict wrapping the list under a known key."""
    data = json.loads(path.read_text())
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        for key in ("components", "parts", "platforms", "items", "data"):
            if isinstance(data.get(key), list):
                return len(data[key])
        # dict-of-records (id -> record), excluding obvious metadata keys
        meta = {"database_meta", "_meta", "meta", "schema"}
        rec = {k: v for k, v in data.items() if k not in meta}
        if rec and all(isinstance(v, dict) for v in rec.values()):
            return len(rec)
    raise ValueError(f"{path.name}: unrecognized shape, cannot count items")


def _well_formed(errors: list) -> None:
    for jf in sorted(ROOT.rglob("*.json")):
        if ".git" in jf.parts:
            continue
        try:
            json.loads(jf.read_text())
        except Exception as e:  # noqa: BLE001 — report any parse failure
            errors.append(f"malformed JSON: {jf.relative_to(ROOT)} — {e}")


def main() -> int:
    errors: list[str] = []

    if not MANIFEST.exists():
        print("FAIL: manifest.json not found")
        return 1

    _well_formed(errors)

    manifest = json.loads(MANIFEST.read_text())
    parts = manifest.get("parts", {})
    if not isinstance(parts, dict) or not parts:
        errors.append("manifest.parts missing or empty")
        parts = {}

    # 2 + 3: per-category file existence + count match, and total
    running_total = 0
    for cat, entry in parts.items():
        rel = entry.get("file")
        declared = entry.get("count")
        if not rel:
            errors.append(f"manifest.parts.{cat}: no 'file'")
            continue
        fpath = ROOT / rel
        if not fpath.exists():
            errors.append(f"manifest.parts.{cat}: file missing → {rel}")
            continue
        try:
            actual = _count_items(fpath)
        except Exception as e:  # noqa: BLE001
            errors.append(str(e))
            continue
        if actual != declared:
            errors.append(f"count drift: {cat} manifest={declared} file={actual}")
        running_total += actual

    declared_total = manifest.get("total_parts")
    if declared_total != running_total:
        errors.append(
            f"total_parts drift: manifest={declared_total} sum-of-files={running_total}"
        )

    # 4: platforms file
    plat = manifest.get("platforms", {})
    plat_count = None
    pf = plat.get("file") if isinstance(plat, dict) else None
    if not pf:
        errors.append("manifest.platforms.file missing")
    else:
        ppath = ROOT / pf
        if not ppath.exists():
            errors.append(f"manifest.platforms: file missing → {pf}")
        else:
            try:
                plat_count = _count_items(ppath)
                if plat_count != plat.get("count"):
                    errors.append(
                        f"platforms count drift: manifest={plat.get('count')} file={plat_count}"
                    )
            except Exception as e:  # noqa: BLE001
                errors.append(str(e))

    # 5: README headline figures match the manifest
    if README.exists():
        txt = README.read_text()
        n_components = re.search(r"([\d,]+)\s+components", txt)
        n_categories = re.search(r"(\d+)\s+categories", txt)
        n_platforms = re.search(r"(\d+)\s+drone platforms", txt)
        if n_components:
            val = int(n_components.group(1).replace(",", ""))
            if val != declared_total:
                errors.append(
                    f"README components={val} != manifest.total_parts={declared_total}"
                )
        if n_categories:
            val = int(n_categories.group(1))
            if val != len(parts):
                errors.append(
                    f"README categories={val} != manifest category count={len(parts)}"
                )
        if n_platforms and isinstance(plat, dict):
            val = int(n_platforms.group(1))
            if val != plat.get("count"):
                errors.append(
                    f"README platforms={val} != manifest.platforms.count={plat.get('count')}"
                )

    if errors:
        print("Forge Data validation FAILED:")
        for e in errors:
            print("  -", e)
        return 1

    print(
        f"Forge Data OK: {declared_total} parts across {len(parts)} categories "
        f"+ {plat_count} platforms — manifest, files and README all consistent."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
