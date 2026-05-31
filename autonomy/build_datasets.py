#!/usr/bin/env python3
"""Build the display-ready Autonomy-page dataset feed (Autonomy page Phase 0).

Reads the master registry `intel/sources/external_datasets.json` and emits
`autonomy/datasets.json` — the curated, filterable view the planned Autonomy
page (handbook Part 6 + Forge browser) fetches at runtime. Single source of
truth stays the registry; this is a generated view.

Run:  python3 autonomy/build_datasets.py
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "intel/sources/external_datasets.json"
OUT = ROOT / "autonomy/datasets.json"

# type -> user-facing task facet
TASK = {
    "vio_slam_benchmark_synthetic": "VIO/SLAM",
    "vio_benchmark_raw_sensor": "VIO/SLAM",
    "cv_drone_detection_training": "CV detection",
    "cv_cuas_discrimination": "CV detection",
    "cv_sar_person_detection": "SAR (person)",
    "rf_signature_dataset": "RF",
    "component_performance_test_data": "Propulsion",
    "structured_platform_db": "Platform specs",
    "drone_specs_aggregator": "Platform specs",
    "resource_index": "Resources",
    "discovery_portal": "Discovery",
    "tool_reference": "Tool",
}


def license_class(lic: str) -> str:
    l = (lic or "").lower()
    if "unconfirmed" in l or "unknown" in l:
        return "unconfirmed"
    if "nc" in l or "non-commercial" in l or "noncommercial" in l:
        return "noncommercial"
    if any(k in l for k in ("cc by 4", "mit", "apache")):
        return "permissive"
    if any(k in l for k in ("gpl", "agpl", "polyform", "penn", "terms of service", "tos", "proprietary")):
        return "restrictive"
    if l.startswith("n/a") or "index of" in l:
        return "n/a"
    return "other"


def usable(license_cls: str, status: str) -> str:
    """One-word verdict for the page badge."""
    if status in ("mined",):
        return "integrated"
    if status == "candidate_blocked":
        return "blocked"
    if status in ("candidate", "different_task", "tool_not_dataset", "discovery_method"):
        return "reference"
    if license_cls == "permissive":
        return "usable"
    if license_cls == "noncommercial":
        return "research-only"
    return "reference"


def main():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    items = []
    for s in reg["sources"]:
        lc = license_class(s.get("license", ""))
        items.append({
            "name": s["name"],
            "url": s["url"],
            "task": TASK.get(s.get("type", ""), s.get("type", "")),
            "license": s.get("license", ""),
            "license_class": lc,
            "status": s.get("status", ""),
            "verdict": usable(lc, s.get("status", "")),
            "ecosystem_use": s.get("ecosystem_use", []),
            "note": (s.get("notes", "")[:200]),
        })
    items.sort(key=lambda x: (x["task"], x["name"]))
    payload = {
        "generated": _dt.date.today().isoformat(),
        "source_registry": "intel/sources/external_datasets.json",
        "facets": {
            "task": sorted({i["task"] for i in items}),
            "license_class": ["permissive", "noncommercial", "restrictive", "unconfirmed", "n/a", "other"],
            "verdict": ["integrated", "usable", "research-only", "reference", "blocked"],
        },
        "count": len(items),
        "datasets": items,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = {}
    for i in items:
        counts[i["verdict"]] = counts.get(i["verdict"], 0) + 1
    print(f"wrote {OUT.relative_to(ROOT)} ({len(items)} datasets)  verdicts={counts}")


if __name__ == "__main__":
    main()
