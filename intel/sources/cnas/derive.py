#!/usr/bin/env python3
"""Derive ecosystem-ready datasets from the mined CNAS platform data.

Reads `cnas_platforms.json` (produced by scrape_cnas.py) and emits three
additive artifacts that different repos in the ecosystem can consume:

  cnas_companies.json        manufacturer registry (enriches intel/companies.json)
  cnas_countries.json        country index with platform rollups
  cnas_platforms_forge.json  CNAS records mapped to the platforms/platforms.json
                             schema, ready to ingest into the build-planner DBs

Nothing here is written into a production dataset automatically.
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "cnas_platforms.json"


def load():
    return json.loads(SRC.read_text(encoding="utf-8"))["platforms"]


def companies(platforms):
    reg: dict[str, dict] = {}
    for p in platforms:
        name = (p.get("manufacturer") or "").strip()
        if not name:
            continue
        c = reg.setdefault(name, {"name": name, "countries": set(), "platforms": []})
        if p.get("country"):
            c["countries"].add(p["country"])
        c["platforms"].append({"pid": p["pid"], "name": p["name"]})
    out = []
    for i, name in enumerate(sorted(reg), start=1):
        c = reg[name]
        out.append({
            "cid": f"CNAS-CMP-{i:04d}",
            "name": c["name"],
            "countries": sorted(c["countries"]),
            "platform_count": len(c["platforms"]),
            "platforms": c["platforms"],
            "source_db": "CNAS World of Drones",
        })
    return out


def countries(platforms):
    idx: dict[str, list] = {}
    for p in platforms:
        idx.setdefault(p.get("country") or "Unknown", []).append(p["name"])
    return [
        {"country": k, "platform_count": len(v), "platforms": sorted(v)}
        for k, v in sorted(idx.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    ]


def to_forge_schema(platforms):
    """Map CNAS records onto the platforms/platforms.json platform schema."""
    out = []
    for p in platforms:
        s = p["specs"]
        endurance_min = int(s["endurance_hr"] * 60) if s.get("endurance_hr") else None
        out.append({
            "pid": p["pid"],
            "name": p["name"],
            "country": p.get("country") or "Unknown",
            "origin": p.get("country") or "Unknown",
            "group": p.get("dod_uas_group"),
            "max_endurance_min": endurance_min,
            "max_flight_time_min": endurance_min,
            "max_range_km": s.get("range_km"),
            "max_speed_kmh": s.get("max_speed_kmh"),
            "max_payload_kg": s.get("payload_kg"),
            "mtow_kg": s.get("mtow_kg"),
            "image_file": p.get("image_url", ""),
            "industry_data": {"specs": {
                "ceiling_m": s.get("ceiling_m"),
                "width_m": s.get("width_m"),
                "length_m": s.get("length_m"),
                "dod_uas_group": p.get("dod_uas_group"),
            }},
            "compliance": {"blue_uas": False, "ndaa_compliant": False,
                           "combat_proven": False, "note": ""},
            "data_source": p.get("source_db"),
            "source_url": p.get("detail_url") or p.get("source_url"),
            "sources": p.get("sources", []),
        })
    return out


def write(name, payload):
    (HERE / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")
    n = payload.get("count", "?")
    print(f"wrote {name} ({n} records)")


def main():
    platforms = load()
    today = _dt.date.today().isoformat()
    meta = {"source": "CNAS World of Drones",
            "source_url": "https://drones.cnas.org/drones/", "generated": today}

    comp = companies(platforms)
    write("cnas_companies.json", {**meta, "count": len(comp), "companies": comp})

    ctry = countries(platforms)
    write("cnas_countries.json", {**meta, "count": len(ctry), "countries": ctry})

    forge = to_forge_schema(platforms)
    write("cnas_platforms_forge.json",
          {**meta, "schema": "platforms/platforms.json", "count": len(forge),
           "platforms": forge})


if __name__ == "__main__":
    main()
