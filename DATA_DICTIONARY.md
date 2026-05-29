# Forge Data — Data Dictionary

Reference for the Forge public parts & platform dataset. Counts reflect `manifest.json` (`last_updated: 2026-05-28`): **4,459 components across 45 categories + 279 platforms.**

## How the data is organized

```
manifest.json              # API index: every file + its live count
platforms/platforms.json   # { database_meta, platforms: [ ... ] }  (279)
parts/<category>.json       # one file per component category
schema/                     # drone_parts_schema_v3.json — the master field template
intel/                      # companies, programs, articles (intelligence layer)
```

- **`manifest.json` is the source of truth for counts and file paths.** Clients should read it first, then fetch the files it lists.
- Each `parts/<category>.json` is a list of component objects following the **v3 schema** (`schema/drone_parts_schema_v3.json`).
- The schema is *additive*: an entry only includes fields applicable to it (do **not** null-fill). Fields prefixed `_` (e.g. `_vehicle_type_options`) are inline documentation/enums, not data.
- Each component carries a `compatibility` block with `_compat_hard` (ERROR if violated) and `_compat_soft` (WARNING) arrays — this is what the compatibility engine reads.

## Component categories (45)

| Category | Count | | Category | Count |
|---|--:|---|---|--:|
| frames | 632 | | esad | 12 |
| propellers | 484 | | gimbals | 12 |
| antennas | 394 | | payload_droppers | 12 |
| fpv_cameras | 379 | | airspeed_sensors | 9 |
| receivers | 359 | | telemetry_radios | 9 |
| flight_controllers | 328 | | fiber_kits | 8 |
| motors | 303 | | military_firmware | 8 |
| drone_models | 274 | | power_modules | 8 |
| batteries | 219 | | remote_id | 7 |
| escs | 165 | | integrated_stacks | 5 |
| control_link_tx | 134 | | video_scramblers | 5 |
| video_transmitters | 128 | | build_guides | 3 |
| stacks | 115 | | uas_nexus_syndicate | 1 |
| gps_modules | 78 | | platform_images | 0 |
| sensors | 44 | | ai_accelerators | 14 |
| thermal_cameras | 43 | | c2_datalinks | 14 |
| fpv_detectors | 30 | | ew_systems | 14 |
| mesh_radios | 29 | | lidar | 25 |
| counter_uas | 26 | | lidar_rangefinders | 13 |
| companion_computers | 25 | | navigation_pnt | 13 |
| simulators | 21 | | optical_flow | 16 |
| propulsion | 17 | | ground_control_stations | 14 |
| swarm_software | 10 | | | |

> `platform_images` is an index file (0 component rows). `uas_nexus_syndicate` is a single aggregate entry.

## Common fields (v3 schema)

Every component object generally includes:

| Field | Meaning |
|---|---|
| `pid` | Stable part ID (e.g. `FRM-0001`) — primary key |
| `name` | Display name |
| `manufacturer` | Maker |
| `description` | Short text |
| `link` | Public product/spec URL |
| `image_file` | Path under `component_images/` |
| `compatibility` | Block with `_compat_hard` / `_compat_soft` rules |

Category-specific fields follow (e.g. frames carry `wheelbase_mm`, `prop_size_in`, `fc_mounting_patterns_mm`; see the schema file for the full per-category field set and enum options).

## Platforms (279)

`platforms/platforms.json` → `{ database_meta, platforms: [...] }`. Public specs, compliance, and manufacturer info only. **Stripped from this public dataset:** contract details, funding data, combat theater, and operational intelligence (see `database_meta.stripped_fields`).

## Provenance

- Component data: public retail specs (GetFPV, RaceDayQuads, NewBeeDrone, manufacturer sites).
- Platform data: public DoD program announcements, manufacturer disclosures, industry reporting.
- Synced from the upstream Prismo (Ai-Project) build planner — **edit data upstream, not here.**

---
*Generated as part of the portfolio audit. Regenerate counts from `manifest.json` when the dataset changes.*
