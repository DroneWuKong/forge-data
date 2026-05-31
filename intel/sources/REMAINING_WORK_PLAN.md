# Remaining Work Plan — Data-Mining Session Backlog

**Date:** 2026-05-31. Sequences the open items surfaced across the mining effort.
Branch: `claude/drone-data-mining-JlvMB` (all repos).

## Phase A — execute now (no gate)
Run in this order; each is additive and reversible.

| # | Item | Repos | Acceptance |
|---|------|-------|-----------|
| A1 | **Verify 2 unconfirmed Kaggle licenses** (birds-vs-drone, toolazycoder) → update registry + regenerate `autonomy/datasets.json` | forge-data | licenses resolved or marked "checked, unstated"; feed regenerated |
| A2 | **Mine DTIC** (public technical-report search) for UAS program/contractor records → new `intel/sources/dtic_reports.json`; promote notable programs into intel | forge-data (+ Ai-Project intel-db mirror) | a curated, sourced set of UAS DTIC reports as structured records |
| A3 | **Autonomy page Phase 1 — handbook Part 6 chapters** (datasets, perception, detection, onboard-AI) | drone-integration-handbook | 4 chapters authored + registered in `build.py` CHAPTERS/PARTS; build green |
| A4 | **Autonomy page Phase 2 — Forge browser** (fetches `autonomy/datasets.json`, filter by task/license-class/verdict; cards link to handbook Part 6) | droneclear_Forge | page renders the feed; registered in build_static + nav |

## Phase B — decision-gated (need maintainer go; do NOT proceed without it)
| # | Item | Question for maintainer |
|---|------|------------------------|
| B1 | Visual drone-detector training scaffold | Stand up a CV-detection training effort? (Seraphim CC BY 4.0 + pathikg MIT + birds-vs-drone are permissive/ready.) Where — `apb`? |
| B2 | NeedleNThread firmware: consumer 2.4 GHz signatures | Fold the DroneRF consumer-drone signatures into `tactical_rf_detector.ino`, or keep as reference docs? |

## Phase C — blocked / external (no action possible here)
| # | Item | Blocker |
|---|------|---------|
| C1 | Tyto Robotics propulsion data (highest-value add) | ToS silent on reuse → needs **written permission** (info@tytorobotics.com) |
| C2 | DroneDB.com | closed SPA, no API/terms; low marginal value (overlaps existing) |

## Execution note
Phase A is the work. B is two yes/no calls. C is yours to unblock off-platform.
Starting now at A1 → A2 → A3 → A4.
