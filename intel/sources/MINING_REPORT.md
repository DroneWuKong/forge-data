# Data Mining Report — CNAS & ERAU UAS Sources

**Date:** 2026-05-30
**Branch:** `claude/drone-data-mining-JlvMB`
**Scope:** Two source URLs were evaluated for mineable drone data:

1. `https://drones.cnas.org/drones/` — CNAS *World of Drones* database
2. `https://guides.erau.edu/uas/databases` — Embry-Riddle UAS research-database guide

This pass is **additive only**. Nothing in `platforms/platforms.json`, `intel/platforms.json`,
or `parts/*` was modified. New artifacts live under `intel/sources/`.

> **Update (deeper audit):** the sources were re-audited end-to-end and mined for everything
> usable across the whole ecosystem. CNAS detail pages were confirmed to add no structured data
> beyond the cards (JS-rendered), so the card mine is canonical. Derived artifacts were added:
> DoD UAS Group classification, a 109-company manufacturer registry, a 47-country index, a
> forge-schema transform, and an open-resource library from the ERAU *Websites*/*Journals* tabs.
> See [`ECOSYSTEM_MAP.md`](ECOSYSTEM_MAP.md) for the repo-by-repo breakdown.

### Artifact index
| File | What |
|------|------|
| `cnas/scrape_cnas.py` | Re-runnable CNAS scraper (now also classifies DoD UAS Group) |
| `cnas/cnas_platforms.json` | 153 platforms — specs, UAS Group, sources |
| `cnas/derive.py` | Derives the registries + forge transform below |
| `cnas/cnas_companies.json` | 109 manufacturers (country + platform rollups) |
| `cnas/cnas_countries.json` | 47-country index |
| `cnas/cnas_platforms_forge.json` | 153 platforms mapped to `platforms/platforms.json` schema |
| `erau_databases.json` | 9 research databases (access + mineable flags) |
| `erau_resources.json` | 14 open/public resources, tagged by consuming repo |
| `ECOSYSTEM_MAP.md` | Which repo can use what |

---

## 1. CNAS "World of Drones" — MINED ✅

The CNAS database renders every platform as a `<div class="drone-box">` card containing a
`<dl>` of specs plus a list of public information sources — clean, regular, and fully parseable
with no JS rendering required.

**Tooling:** [`cnas/scrape_cnas.py`](cnas/scrape_cnas.py) — a reusable, dependency-free
(stdlib-only) scraper. Run `python3 cnas/scrape_cnas.py` to refresh from the live page,
or `--html <file>` to parse a local copy.

**Output:** [`cnas/cnas_platforms.json`](cnas/cnas_platforms.json)

### Yield
- **153 platforms** across **47 countries**
- **1,042 normalized spec values** (8 spec fields per platform)
- **151 / 153** carry at least one source link
- **150 / 153 are net-new** to the project (only `Coyote`, `Ghost`, `V Bat` already exist in `intel/platforms.json`; **zero** overlap with the build-planner `platforms/platforms.json`)

| Spec field | Coverage |
|------------|----------|
| `endurance_hr` | 145 / 153 |
| `mtow_kg` | 145 / 153 |
| `width_m` (wingspan/rotor) | 144 / 153 |
| `max_speed_kmh` | 140 / 153 |
| `ceiling_m` | 128 / 153 |
| `length_m` | 117 / 153 |
| `payload_kg` | 112 / 153 |
| `range_km` | 111 / 153 |

Top origins: USA (29), Israel (14), China (11), France (10), India (5), Argentina (5).

### Schema mapping → `platforms/platforms.json`
The mined records normalize cleanly onto the existing platform schema:

| CNAS field | forge-data field |
|------------|------------------|
| `name` | `name` |
| `manufacturer` (Company) | `industry_data` / manufacturer |
| `country` | `country` / `origin` |
| `specs.endurance_hr` × 60 | `max_endurance_min` |
| `specs.range_km` | `max_range_km` |
| `specs.max_speed_kmh` | `max_speed_kmh` |
| `specs.payload_kg` | `max_payload_kg` |
| `specs.mtow_kg` | `mtow_kg` |
| `specs.ceiling_m` | *(new field — not yet in schema)* |
| `specs.width_m`, `specs.length_m` | *(new dimension fields)* |
| `sources[]` | `intel/platforms.json` `sources[]` |

### Recommended next step (not yet done — needs your call)
These are **military/government ISR & strike platforms**, which matches the `intel/platforms.json`
domain more than the FPV-build-focused `platforms/platforms.json`. Suggested integration:
promote the net-new 150 into `intel/platforms.json` (specs + sources + `country`), assigning
real `PLT-####` IDs continuing from the current max. Hold for confirmation before merging into a
production dataset — see open question below.

---

## 2. ERAU UAS Research Guide — CATALOGED 📇 (not bulk-mineable)

The ERAU page is a **list of research databases**, not a dataset itself. Most are subscription
resources behind institutional logins and cannot be scraped. Three are publicly accessible and
are viable enrichment targets.

**Output:** [`erau_databases.json`](erau_databases.json) — registry of 9 databases with
access level and a `mineable` flag.

| Public / mineable | Subscription only |
|-------------------|-------------------|
| DTIC (technical reports) | Janes (defense specs) |
| NTRL (technical reports) | ScienceDirect, Scopus |
| HSDL (policy, partial) | Adv. Tech & Aerospace DB, Business Source Complete, ISCTRC |

**Highest-value public target:** **DTIC** (`discover.dtic.mil`) — free, with bulk search/APIs,
ideal for backfilling platform program history and contractor data that complement the CNAS specs.

---

## Open question for the maintainer
Before promoting the 150 net-new CNAS platforms into a production dataset:
- Merge into **`intel/platforms.json`** (intel/specs domain — recommended), or keep staged under
  `intel/sources/` as a reviewable feed?
- Should a `ceiling_m` + dimension (`width_m`, `length_m`) extension be added to the platform schema?

The scraper is idempotent and re-runnable, so a refresh + merge can be automated once the
destination is confirmed.
