# System Design

## Architecture Overview

The `rapidapi-async-ingestor` is designed to be a highly performant, resilient, and type-safe data ingestion pipeline. It leverages an asynchronous, event-driven architecture to efficiently communicate with the RapidAPI Car API v2, overcoming common API integration bottlenecks such as network latency and rate limiting.

### 1. Networking Layer (`src/client.py`)
- **Asynchronous I/O:** Uses `httpx.AsyncClient` alongside `asyncio` to perform non-blocking HTTP requests. This is crucial for performance at scale when fetching concurrent chunks of vehicle mileage data.
- **Resilient Connectivity (Exponential Backoff):** Network volatility and strict rate limits (HTTP 429) are handled transparently via a custom asynchronous exponential backoff retry loop. This ensures that transient errors or momentary traffic spikes do not crash the pipeline.

### 2. Validation Layer (`src/models/schemas.py`)
- **Strict Type Safety:** Integrates `Pydantic` to enforce rigorous schema contracts on the incoming JSON payloads.
- **Defensive Modeling:** `Optional` bounds are placed on numerical attributes (like MSRP) that the API may omit.
- **Data Sanitization:** Implements `@field_validator` hooks to elegantly handle dirty data, such as stripping `"gal"` or `"L"` from the `fuel_tank_capacity` strings and dynamically grabbing the first payload in arrays, casting them to safe Python primitives.

### 3. Execution Engine (`src/main.py`)
- **Orchestration:** Initializes the asynchronous event loop and sequential/concurrent task execution.
- **Data Transformation:** Converts validated Pydantic models directly into `pandas.DataFrame` structures for downstream analysis and persistence (CSV generation).
- **Visualization:** Utilizes `seaborn` and `matplotlib` to generate programmatically styled, presentation-ready business intelligence charts (JPEG generation).

### 4. Containerization (`Dockerfile`)
- **Multi-Stage Build:** Employs a multi-stage Docker build to isolate dependency installation from the runtime environment, producing a lean final image.
- **Security Posture:** Configured to execute as a restricted, non-root user (`appuser`) conforming to modern production security standards.

*Note: As part of the Dual Strategy build pipeline, this `src/` codebase acts as our rich, testable core. A post-processing script will later bundle this into the single `.txt` file required for final submission.*
