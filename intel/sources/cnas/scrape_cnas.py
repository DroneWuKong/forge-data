#!/usr/bin/env python3
"""Miner for the CNAS "World of Drones" database (https://drones.cnas.org/drones/).

The CNAS drone database is published as a single HTML page where every platform
is rendered as a `<div class="drone-box">` card holding a definition list (`<dl>`)
of specs plus a list of public information sources. This script downloads that
page (or reads a local copy), parses every card, normalizes the specs into the
forge-data platform schema, and writes `cnas_platforms.json`.

Usage:
    python3 scrape_cnas.py                 # fetch live page and write JSON
    python3 scrape_cnas.py --html cnas.html  # parse a local HTML copy
    python3 scrape_cnas.py --out out.json    # custom output path

The output is additive intel data: it is NOT merged into platforms/platforms.json
automatically. See MINING_REPORT.md for the integration plan.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SOURCE_URL = "https://drones.cnas.org/drones/"
SOURCE_DB = "CNAS World of Drones"

# Maps the CNAS <dt> label to (normalized_key, unit). "--" means unknown -> None.
SPEC_MAP = {
    "Endurance": ("endurance_hr", "hr"),
    "Range": ("range_km", "km"),
    "Payload cap.": ("payload_kg", "kg"),
    "Max speed": ("max_speed_kmh", "kmh"),
    "Ceiling": ("ceiling_m", "m"),
    "Max takeoff weight": ("mtow_kg", "kg"),
    "Width (wingspan or rotor)": ("width_m", "m"),
    "Length": ("length_m", "m"),
}


def _num(value: str):
    """Extract a leading number from a spec string. '6 hrs' -> 6.0, '--' -> None."""
    value = (value or "").strip()
    if not value or value.startswith("--"):
        return None
    m = re.search(r"-?\d[\d,]*\.?\d*", value.replace(",", ""))
    if not m:
        return None
    num = float(m.group())
    return int(num) if num.is_integer() else num


class DroneBoxParser(HTMLParser):
    """Streaming parser that collects one record per drone-box div."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.records: list[dict] = []
        self._cur: dict | None = None
        self._depth = 0          # div nesting depth inside the current card
        self._capture = None     # what text we are currently buffering
        self._buf: list[str] = []
        self._dt_label: str | None = None
        self._src_href: str | None = None
        self._seen_detail = False

    # -- helpers ---------------------------------------------------------
    def _flush(self) -> str:
        text = "".join(self._buf).strip()
        self._buf = []
        return text

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div" and a.get("class", "").startswith("drone-box"):
            self._cur = {
                "cnas_id": a.get("id", ""),
                "country": a.get("data-country", ""),
                "name": "",
                "detail_url": "",
                "image_url": "",
                "specs": {},
                "raw_specs": {},
                "sources": [],
            }
            self._depth = 1
            self._seen_detail = False
            return
        if self._cur is None:
            return
        if tag == "div":
            self._depth += 1
            cls = a.get("class", "")
            if "drone-name" in cls and a.get("style"):
                m = re.search(r"url\(['\"]?([^'\")]+)['\"]?\)", a["style"])
                if m:
                    self._cur["image_url"] = m.group(1)
        elif tag == "a":
            href = a.get("href", "")
            cls = a.get("class", "")
            # first content <a> is the card -> detail page link
            if href and not self._seen_detail and "button" not in cls:
                self._cur["detail_url"] = href
                self._seen_detail = True
            elif href and "button" not in cls:
                # source links live inside <ul> under information-sources
                self._src_href = href
                self._capture = "source"
                self._buf = []
        elif tag == "h2":
            self._capture = "name"
            self._buf = []
        elif tag == "dt":
            self._capture = "dt"
            self._buf = []
        elif tag == "dd":
            self._capture = "dd"
            self._buf = []

    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if self._cur is None:
            return
        if tag == "h2" and self._capture == "name":
            self._cur["name"] = self._flush()
            self._capture = None
        elif tag == "dt" and self._capture == "dt":
            self._dt_label = self._flush()
            self._capture = None
        elif tag == "dd" and self._capture == "dd":
            val = self._flush()
            label = self._dt_label or ""
            self._cur["raw_specs"][label] = val
            if label in SPEC_MAP:
                key, _unit = SPEC_MAP[label]
                self._cur["specs"][key] = _num(val)
            elif label == "Company":
                self._cur["manufacturer"] = val
            elif label == "Photo Credit":
                self._cur["photo_credit"] = val
            self._dt_label = None
            self._capture = None
        elif tag == "a" and self._capture == "source":
            text = self._flush()
            if self._src_href:
                self._cur["sources"].append({"title": text, "url": self._src_href})
            self._src_href = None
            self._capture = None
        elif tag == "div":
            self._depth -= 1
            if self._depth == 0:
                self.records.append(self._cur)
                self._cur = None


def fetch_html(url: str = SOURCE_URL) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "forge-data-miner/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310 (trusted URL)
        return resp.read().decode("utf-8", "replace")


def normalize(records: list[dict]) -> list[dict]:
    today = _dt.date.today().isoformat()
    named = sorted((r for r in records if r.get("name")), key=lambda x: x["name"].lower())
    out = []
    for i, r in enumerate(named, start=1):
        out.append({
            "pid": f"CNAS-{i:04d}",
            "name": r["name"],
            "manufacturer": r.get("manufacturer", ""),
            "country": r.get("country", ""),
            "specs": r["specs"],
            "image_url": r.get("image_url", ""),
            "photo_credit": r.get("photo_credit", ""),
            "detail_url": r.get("detail_url", ""),
            "sources": r["sources"],
            "source_db": SOURCE_DB,
            "source_url": SOURCE_URL,
            "first_seen": today,
            "last_updated": today,
        })
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Mine the CNAS World of Drones database.")
    ap.add_argument("--html", help="parse a local HTML copy instead of fetching")
    ap.add_argument("--out", default=str(Path(__file__).parent / "cnas_platforms.json"))
    args = ap.parse_args(argv)

    html = Path(args.html).read_text(encoding="utf-8") if args.html else fetch_html()
    parser = DroneBoxParser()
    parser.feed(html)
    records = normalize(parser.records)

    payload = {
        "source": SOURCE_DB,
        "source_url": SOURCE_URL,
        "license": "CNAS public research dataset — cite CNAS World of Drones",
        "generated": _dt.date.today().isoformat(),
        "count": len(records),
        "platforms": records,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                              encoding="utf-8")
    filled = sum(1 for r in records for v in r["specs"].values() if v is not None)
    print(f"Parsed {len(records)} platforms, {filled} spec values -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
