# Ecosystem Mapping — What Each Repo Can Use From the CNAS + ERAU Mine

Maps the mined artifacts under `intel/sources/` to the 11 Midwest Nice UAS / DroneWuKong
repos. Honest about gaps: where a source has nothing applicable, it says so and notes what
source *would* be needed instead.

**Mined artifacts referenced below**
- `cnas/cnas_platforms.json` — 153 platforms, specs + DoD UAS Group + sources
- `cnas/cnas_platforms_forge.json` — same, mapped to the `platforms/platforms.json` schema
- `cnas/cnas_companies.json` — 109 manufacturers, country + platform rollups
- `cnas/cnas_countries.json` — 47-country index
- `erau_databases.json` / `erau_resources.json` — research DBs + open public resources

---

## Strong fits (directly ingestible)

### forge-data (this repo)
- **`intel/platforms.json`**: promote the 150 net-new CNAS platforms (specs, country, sources).
- **`intel/companies.json`**: enrich from `cnas_companies.json` — 109 manufacturers vs. the current 30 (e.g. IAI, Ghods Aviation, Blue Bear). Match on name, add `countries`.
- **`platforms/platforms.json`**: `cnas_platforms_forge.json` is pre-mapped to this schema (`max_endurance_min`, `max_range_km`, `mtow_kg`, `group`, …).

### Ai-Project (Prismo Forge — build planner, source of truth)
- Ingest `cnas_platforms_forge.json` into the platform DB: +150 military/gov platforms with a populated **DoD UAS Group** field (G1:38, G2:25, G3:59, G4:5, G5:18) for filtering/sorting.
- Manufacturer registry feeds platform → company linking.

### droneclear_Forge (uas-forge.com — public browser)
- Downstream of Ai-Project: the new platforms surface in the Platforms/Browse pages automatically once merged upstream.
- **Content feeds**: `erau_resources.json` open links (FAA, UAS Magazine) for the Guide/Academy pages.

### drone-integration-handbook (uas-handbook.com)
- **`erau_resources.json`** is the primary payload here: FAA UAS portal, FAA Policy Library, FAA ASIAS incident DB, NCSL state-law tracker, SKYbrary, Eurocontrol, UK CAA → citable references for the **regulatory / grayzone / compliance** sections.
- Federal Register + NCSL are API/scrape-friendly for a US **state-law matrix** and rule index.
- CNAS platform specs + per-platform `sources[]` = a reference corpus for platform pages.

### Command (Wingman C2 — ATAK/WinTAK)
- **Platform reference catalog**: `cnas_platforms.json` gives a known-airframe lookup (name, country, MTOW, speed, ceiling, **UAS Group**) for situational-awareness/target overlays. UAS Group + speed/ceiling map naturally to CoT threat profiles.
- FAA ASIAS incident data → optional airspace-incident layer.

### PlzHelp (ORQA doc chat — pulls from "public databases")
- Add `erau_resources.json` + `erau_databases.json` as additional curated doc sources for the RAG corpus; CNAS specs as a structured platform-fact lookup.

---

## Weak / partial fits (note the gap)

### NeedleNThread (tactical RF threat detector, learns threats over time)
- **Partial**: the manufacturer ↔ country ↔ platform-name index (`cnas_companies.json`) can back a *threat-attribution* lookup once an emitter is identified.
- **Gap**: CNAS/ERAU carry **no RF data** (bands, C2 frequencies, hopping). The signature library still needs an RF-specific source — none here.

---

## No applicable data (honest no)

| Repo | Why | What would be needed |
|------|-----|----------------------|
| **ESP32-Based-RF-Detector** | RF detection (150 MHz–5.8 GHz); these sources have no frequency data | A drone RF/C2 frequency database |
| **1G-FDMA** | Analog 5.8 GHz video mesh; no spec overlap | RF channel-plan / video-link data |
| **EternallySAD** | Pyrotechnic firing controller; unrelated domain | MIL-STD-1316 / NFPA references |
| **Hangar** | Portfolio index, no product data | n/a — links to this mine as a portfolio artifact; AUVSI association ref optional |

---

## Suggested promotion order
1. **forge-data** `intel/companies.json` enrichment (lowest risk, additive merge).
2. **forge-data** `intel/platforms.json` — promote 150 net-new platforms.
3. **Ai-Project** platform DB ingest via `cnas_platforms_forge.json` (carries UAS Group).
4. **drone-integration-handbook** regulatory resource library from `erau_resources.json`.

All transforms are produced by re-runnable scripts (`scrape_cnas.py`, `derive.py`), so each
promotion can be regenerated and diffed rather than hand-edited.
