# RapidAPI Async Ingestor

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📌 Overview

`rapidapi-async-ingestor` is a high-performance, asynchronous data ingestion pipeline designed to securely aggregate, validate, and visualize motor vehicle specifications and mileage data from a third-party REST API. 

Built with enterprise-grade reliability in mind, this project demonstrates how to handle stringent third-party rate limits, network volatility, and nested JSON payloads at scale using modern asynchronous Python paradigms.

**Key Capabilities:**
*   **Asynchronous I/O:** Utilizes `httpx` and `asyncio` for non-blocking API requests.
*   **Resilient Connectivity:** Implements robust custom retry adapters with exponential backoff to gracefully manage API rate limits (1000 requests/hour threshold) and transient connection failures.
*   **Strict Type Safety:** Leverages `Pydantic` for rigorous schema validation before data transformation.
*   **Automated Reporting:** Transforms nested JSON payloads into structured `pandas` DataFrames and generates programmatically styled, presentation-ready visualizations.

---

## 🏗️ System Architecture

This repository showcases an enterprise-grade multi-file structure within the `src/` directory.

For a deep dive into the architectural decisions and modular design, please refer to the [SYSTEM_DESIGN.md](SYSTEM_DESIGN.md).

---

## ⚙️ Tech Stack

*   **Core:** Python 3.10+
*   **Networking:** `httpx`, `asyncio`
*   **Data Validation:** `Pydantic`
*   **Data Processing:** `pandas`
*   **Visualization:** `matplotlib`, `seaborn`

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.10+ installed. You will also need a free API key from the [RapidAPI Car API v2](https://rapidapi.com/carapi/api/car-api2/).

### 2. Installation
Clone the repository and install the required dependencies:

```bash
git clone https://github.com/RayanVakil/rapidapi-async-ingestor.git
cd rapidapi-async-ingestor
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Execution (Coming Soon)
We are currently staging the `httpx` execution logic. Once finalized, a build step will be provided to compile this pipeline into the requested single script format.
