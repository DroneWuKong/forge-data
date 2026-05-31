#!/usr/bin/env python3
"""Promote mined CNAS data into the production intel datasets (idempotent).

- intel/platforms.json: append net-new CNAS platforms (skipping ones already
  tracked by name), extending each new entry with country + specs +
  dod_uas_group. Existing entries are untouched.
- intel/companies.json: enrich existing companies with a `countries` field
  when matched by name; append net-new CNAS manufacturers.

Re-running is safe: matches are keyed on normalized name, so already-promoted
records are skipped rather than duplicated.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[3]          # forge-data/
SRC = ROOT / "intel/sources/cnas/cnas_platforms.json"
COMP = ROOT / "intel/sources/cnas/cnas_companies.json"
PLATFORMS = ROOT / "intel/platforms.json"
COMPANIES = ROOT / "intel/companies.json"
SOURCE_DB = "CNAS World of Drones"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def next_id(records, key, prefix):
    n = 0
    for e in records:
        m = re.search(rf"{prefix}-(\d+)", e.get(key, ""))
        if m:
            n = max(n, int(m.group(1)))
    return n


def map_sources(cnas_sources):
    out = []
    for s in cnas_sources:
        url = s.get("url", "")
        out.append({
            "date": "",
            "site": urlparse(url).netloc.replace("www.", "") if url else "",
            "title": s.get("title", ""),
            "url": url,
        })
    return out


def promote_platforms():
    intel = json.loads(PLATFORMS.read_text(encoding="utf-8"))
    cnas = json.loads(SRC.read_text(encoding="utf-8"))["platforms"]
    have = {norm(e["name"]) for e in intel}
    nid = next_id(intel, "pid", "PLT")
    today = _dt.date.today().isoformat()
    added = 0
    for p in cnas:
        if norm(p["name"]) in have:
            continue
        nid += 1
        added += 1
        have.add(norm(p["name"]))
        intel.append({
            "pid": f"PLT-{nid:04d}",
            "name": p["name"],
            "manufacturer": p.get("manufacturer", ""),
            "country": p.get("country", ""),
            "dod_uas_group": p.get("dod_uas_group"),
            "specs": p.get("specs", {}),
            "programs": [],
            "tags": [],
            "sources": map_sources(p.get("sources", [])),
            "data_source": SOURCE_DB,
            "first_seen": p.get("first_seen", today),
            "last_updated": today,
        })
    PLATFORMS.write_text(json.dumps(intel, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf-8")
    print(f"intel/platforms.json: +{added} (now {len(intel)})")


def promote_companies():
    intel = json.loads(COMPANIES.read_text(encoding="utf-8"))
    cnas = json.loads(COMP.read_text(encoding="utf-8"))["companies"]
    by_name = {norm(e["name"]): e for e in intel}
    nid = next_id(intel, "cid", "CMP")
    today = _dt.date.today().isoformat()
    added = enriched = 0
    for c in cnas:
        key = norm(c["name"])
        if key in by_name:
            e = by_name[key]
            if c["countries"] and "countries" not in e:
                e["countries"] = c["countries"]
                enriched += 1
            continue
        nid += 1
        added += 1
        rec = {
            "cid": f"CMP-{nid:04d}",
            "name": c["name"],
            "countries": c["countries"],
            "platform_count": c["platform_count"],
            "programs": [],
            "tags": [],
            "sources": [],
            "data_source": SOURCE_DB,
            "last_updated": today,
        }
        by_name[key] = rec
        intel.append(rec)
    COMPANIES.write_text(json.dumps(intel, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf-8")
    print(f"intel/companies.json: +{added}, enriched {enriched} (now {len(intel)})")


if __name__ == "__main__":
    promote_platforms()
    promote_companies()
