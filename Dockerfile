# Stage 1: Build
FROM python:3.10-slim AS builder

WORKDIR /app

# Create a virtual environment to isolate dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim

WORKDIR /app

# Create a non-root user and group for security
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Ensure the virtual environment is active in the runtime image
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application source code
COPY src/ /app/src/

# Change ownership of the working directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Set the entry point to execute the main script
ENTRYPOINT ["python", "-m", "src.main"]
