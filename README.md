# Forge Data — AI Wingman Public Parts & Platform Database

Static JSON API serving the [AI Wingman](https://github.com/DroneWuKong/Ai-Project) Forge build planner.

**3,312 components** across 16 categories + **151 drone platforms**.

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

---

## Categories

| Category | Count | Description |
|----------|-------|-------------|
| `antennas` | 439 | FPV, control link, GPS antennas |
| `batteries` | 203 | LiPo, Li-Ion flight packs |
| `build_guides` | 3 | Step-by-step assembly guides |
| `drone_models` | 35 | Complete drone platforms |
| `escs` | 148 | Electronic speed controllers |
| `flight_controllers` | 420 | Flight controller boards |
| `fpv_cameras` | 199 | FPV and payload cameras |
| `frames` | 490 | Drone frames and kits |
| `gps_modules` | 74 | GPS/GNSS receivers |
| `mesh_radios` | 13 | Mesh networking radios |
| `motors` | 275 | Brushless motors |
| `propellers` | 471 | Props across all sizes |
| `receivers` | 167 | RC receivers |
| `stacks` | 102 | FC + ESC stack combos |
| `video_transmitters` | 125 | Analog and digital VTx |

## Platforms

151 drone platforms with public specs, compliance data, and manufacturer info. Contract details, funding data, and operational intelligence are excluded from this public dataset.

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
