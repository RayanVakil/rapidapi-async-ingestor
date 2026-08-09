# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.1] - Final Polish & Corporate Styling

### Changed
- Updated the primary visualization highlight color in `src/visual.py` to match Coterie's corporate hex code (`#F05A28`).
- Updated the `YOUR_FULL_NAME` placeholder in `src/main.py` to finalize the assessment output filenames and metadata.


## [1.4.0] - RapidAPI Configuration and Schema Adjustments

### Fixed
- Updated `.env` with a valid active RapidAPI key to resolve `403 Forbidden` errors.
- Applied a surgical patch to `src/main.py` allowing proper parsing of raw JSON array responses from the `/api/years` endpoint.
- Updated `src/client.py` API parameters for the `mileages` endpoint to pass `make_model_trim_id` instead of `id` and added the `verbose=yes` flag to ensure the nested `make_model_trim` object is included in the response, fixing Pydantic validation errors.
- Cleaned up transient test scripts and generated test outputs (`test_schemas.py`, `mileage_test.csv`, `fuel_capacity_chart_test.jpeg`) from the root directory to maintain repository hygiene.

## [1.3.0] - Docker Containerization

### Added
- Implemented a lightweight, multi-stage `Dockerfile` using `python:3.10-slim` for secure, production-grade containerized execution as a non-root user.
- Added `.dockerignore` to exclude local environments, git history, and AI directives from the build context.

## [1.2.0] - Architectural Audit & Surgical Fixes

### Added
- Created `audit.md`, a comprehensive Staff-level architectural audit analyzing the pipeline's strengths, vulnerabilities, and a definitive technical teardown of the RapidAPI 403 anomaly.
- Added `audit.md` to `.gitignore` to keep it out of the public repo history if desired, though tracking it locally for documentation.

### Fixed
- Surgically patched a bug in `src/main.py` where the `YOUR_FULL_NAME` placeholder variable was not properly wired into the output filenames (`mileage_Rayan_Vakil.csv` and `fuel_capacity_chart_Rayan_Vakil.jpeg`). Outputs now dynamically reflect the placeholder.

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
