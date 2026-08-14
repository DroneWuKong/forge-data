# Forge Data

**Sanitized public static JSON API for UAS components, platforms, schemas, and selected integration knowledge used by UAS Forge and compatible clients.**

Base URL: `https://dronewukong.github.io/forge-data`

## Source of truth

[`manifest.json`](manifest.json) is authoritative for API version, update date, category files, category counts, platform count, schema path, and total records. Clients must read the manifest instead of copying counts from this README.

At the audited 2026-06-10 manifest snapshot, the API reports **4,547 component records across 46 category files and 335 platforms**. Those values will change; the manifest wins.

## Quick start

```text
GET /manifest.json
GET /parts/flight_controllers.json
GET /parts/motors.json
GET /platforms/platforms.json
GET /schema/drone_parts_schema_v3.json
GET /circuit_forge_kb.json
```

```javascript
const base = 'https://dronewukong.github.io/forge-data';
const manifest = await fetch(`${base}/manifest.json`).then((response) => response.json());
const motors = await fetch(`${base}/${manifest.parts.motors.file}`).then((response) => response.json());
```

No API key is required. GitHub Pages serves the static files.

## Data boundary

The public export includes product specifications, public platform information, schema metadata, and selected integration knowledge. Private source records, credentials, contract-sensitive material, non-public evidence, and internal operational intelligence must not be exported.

Platform entries may include public specifications, compliance references, and manufacturer information. Their presence is not a procurement certification, endorsement, availability guarantee, or statement that every field has been independently verified.

## Repository map

| Path | Responsibility |
|---|---|
| `manifest.json` | API discovery and current record counts |
| `parts/` | Category JSON files |
| `platforms/` | Public platform data |
| `schema/` | Published data contracts |
| `circuit_forge_kb.json` | Component pin and catalog hints for Circuit Forge |
| `autonomy/`, `intel/` | Publicly releasable supporting datasets |
| `validate.py` | Dataset validation |
| `SECURITY.md` | Vulnerability reporting |

## Validation

```bash
python3 validate.py
```

Validation should run before publishing any new manifest or category file. A change that modifies a category count must update `manifest.json` in the same change.

## Updating

The dataset is exported from a private source corpus through a sanitization boundary, then validated and published through GitHub Pages. Do not hand-copy private source files into this repository.

1. Update the private source data.
2. Run the approved sanitization/export process.
3. Validate the public tree.
4. Review the diff for private fields, credentials, and restricted material.
5. Publish the public-only change.

## Data sources and reuse

Data is compiled from public manufacturer specifications, retail listings, public program material, and industry reporting. Individual records may carry their own provenance and caveats. Schema work derives in part from the public DroneClear ecosystem with portfolio-specific extensions.

No license is implied by public accessibility. Review repository and record-level notices before redistribution.

