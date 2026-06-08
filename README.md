# Forge Data — Prismo Public Parts & Platform Database

Static JSON API serving the [Prismo](https://github.com/DroneWuKong/Ai-Project) Forge build planner.

**4,543 components** across 46 categories + **335 drone platforms**.

---

## Usage

Base URL: `https://dronewukong.github.io/forge-data`

### Discover available data
```
GET /manifest.json
```

### Fetch parts by category
```
GET /parts/flight_controllers.json
GET /parts/motors.json
GET /parts/frames.json
GET /parts/escs.json
...
```

### Fetch platforms
```
GET /platforms/platforms.json
```

### Fetch schema
```
GET /schema/drone_parts_schema_v3.json
```

### Fetch the Circuit Forge knowledge base
Component pinouts + catalog-hint map that grounds the [Circuit Forge](https://uas-forge.com/circuit-forge/)
AI hardware design tool. Keyed by component name; each entry carries `pins`, render
`shape`/`color`, and an optional `catalog` hint mapping it to a parts category here.
```
GET /circuit_forge_kb.json
```

---

## Categories

| Category | Count | Description |
|----------|-------|-------------|
| `ai_accelerators` | 14 | Edge AI / inference accelerators |
| `airspeed_sensors` | 9 | Pitot / airspeed sensors |
| `antennas` | 394 | FPV, control link, GPS antennas |
| `batteries` | 219 | LiPo, Li-Ion flight packs |
| `build_guides` | 3 | Step-by-step assembly guides |
| `c2_datalinks` | 14 | Command & control datalinks |
| `companion_computers` | 25 | Onboard companion computers |
| `control_link_tx` | 134 | Control link transmitters |
| `counter_uas` | 26 | Counter-UAS systems |
| `drone_models` | 330 | Complete drone platforms |
| `esad` | 12 | Electronic safe & arm devices |
| `escs` | 165 | Electronic speed controllers |
| `ew_systems` | 14 | Electronic warfare systems |
| `fiber_kits` | 8 | Fiber-optic control kits |
| `flight_controllers` | 328 | Flight controller boards |
| `fpv_cameras` | 387 | FPV and payload cameras |
| `fpv_detectors` | 30 | FPV signal detectors |
| `frames` | 632 | Drone frames and kits |
| `gimbals` | 12 | Camera gimbals |
| `gps_modules` | 78 | GPS/GNSS receivers |
| `ground_control_stations` | 14 | Ground control stations |
| `integrated_stacks` | 5 | Integrated FC/ESC/PDB stacks |
| `lidar` | 25 | LiDAR sensors |
| `lidar_payloads` | 17 | LiDAR survey/mapping payloads |
| `lidar_rangefinders` | 13 | LiDAR rangefinders |
| `mesh_radios` | 29 | Mesh networking radios |
| `military_firmware` | 8 | Military/defense firmware |
| `motors` | 303 | Brushless motors |
| `navigation_pnt` | 13 | Navigation / PNT systems |
| `optical_flow` | 16 | Optical flow sensors |
| `payload_droppers` | 12 | Payload release mechanisms |
| `platform_images` | 0 | Platform image lookup (asset) |
| `power_modules` | 8 | Power distribution / sensing modules |
| `propellers` | 484 | Props across all sizes |
| `propulsion` | 17 | Propulsion systems |
| `receivers` | 359 | RC receivers |
| `remote_id` | 7 | Remote ID modules |
| `sensors` | 44 | Misc sensors |
| `simulators` | 21 | Flight simulators |
| `stacks` | 115 | FC + ESC stack combos |
| `swarm_software` | 10 | Swarm coordination software |
| `telemetry_radios` | 9 | Telemetry radios |
| `thermal_cameras` | 43 | Thermal imaging cameras |
| `uas_nexus_syndicate` | 1 | UAS Nexus Syndicate reference |
| `video_scramblers` | 5 | Video scramblers |
| `video_transmitters` | 131 | Analog and digital VTx |

## Platforms

335 drone platforms with public specs, compliance data, and manufacturer info. Contract details, funding data, and operational intelligence are excluded from this public dataset.

---

## Data Sources

Component data sourced from public retail specifications (GetFPV, RaceDayQuads, NewBeeDrone, manufacturer sites). Platform data from public DoD program announcements, manufacturer disclosures, and industry reporting.

Schema based on [DroneClear](https://github.com/tedstrazimiri/droneclear) v3 with Wingman extensions.

---

## Integration

Forge reads this data at runtime via `fetch()`. No API key required. CORS enabled via GitHub Pages.

```javascript
// Fetch manifest
const manifest = await fetch('https://dronewukong.github.io/forge-data/manifest.json').then(r => r.json());

// Load a category
const motors = await fetch(`https://dronewukong.github.io/forge-data/${manifest.parts.motors.file}`).then(r => r.json());
```

---

## Updating

This dataset is synced manually from the private `DroneWuKong/Ai-Project` repository. To update:

1. Pull latest from `Ai-Project`
2. Run the sanitization + export script
3. Push to this repo
4. GitHub Pages deploys automatically

---

*Buddy up.*
