# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - Modularization & Build Pipeline

### Added
- Created `src/processing.py` to handle pandas DataFrame construction and validation logic cleanly.
- Created `src/visual.py` to encapsulate the seaborn/matplotlib visualization logic (horizontal bar chart).
- Added `build.py`, a custom build script that intelligently concatenates the multi-file architecture into a single `script_Rayan_Vakil.txt` file, automatically stripping internal import paths.

## [1.0.0] - Initial Setup (Dual Strategy Phase 1)

### Added
- Foundational project scaffolding and environment configuration (`.env`, `.gitignore`).
- Asynchronous architectural documentation: `README.md`, `SYSTEM_DESIGN.md`, and `CHANGELOG.md`.
- `requirements.txt` locked to modern, stable asynchronous libraries (`httpx`, `pydantic`, `pandas`, `seaborn`).
- **[Validation Layer]** Pydantic data schemas (`src/models/schemas.py`) to enforce contract structures and dynamically sanitize nested JSON payloads from the RapidAPI Car API v2.

### Changed
- Configured Pydantic schemas to utilize `Optional` fields and safe defaults to prevent pipeline crashes on missing API data.
