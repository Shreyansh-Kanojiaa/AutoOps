# AutoOps

AutoOps is a production-style Linux service designed to demonstrate
core DevOps and SRE concepts such as service management, configuration,
logging, and failure handling.

This project is intentionally built incrementally to mirror how
real services evolve in production environments.

---

## Current Features

- Python-based HTTP service
- `/health` endpoint for liveness checks
- Configurable host and port via environment variables
- Graceful shutdown using signal handling
- Managed as a systemd service
- Centralized logging via journald

---

## Project Structure

autoops/
├─ agent/
│ └─ main.py # Core service logic
├─ systemd/
│ └─ autoops.service # systemd unit file
├─ docs/
│ └─ architecture.md
└─ README.md


## How It Runs

The service runs as a systemd-managed process using a Python virtual
environment. Configuration is injected via environment variables
instead of hardcoded values.

Systemd is responsible for:
 - starting the service
 - restarting on failure
 - handling logs
 - sending termination signals


## Why This Project Exists

Most student projects focus on tools.
This project focuses on **operability**:
 - how services start
 - how they stop
 - how they fail
 - how they are debugged

## Failure Handling

AutoOps is supervised by systemd and configured to automatically
restart on failure.

The service was intentionally terminated using SIGKILL to simulate
unexpected crashes. systemd detected the failure and restarted the
service without manual intervention.

This demonstrates basic self-healing behavior expected in production
services.

The goal is to build intuition around real-world systems.
