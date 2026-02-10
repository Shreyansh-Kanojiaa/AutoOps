# Architecture Overview

AutoOps is designed as a simple, single-node service that runs directly
on Linux using systemd. This design was chosen to understand service
behavior without abstractions.

---

## Key Design Decisions

### 1. No Frameworks
The service uses Python's built-in HTTP server to avoid hiding
behavior behind frameworks. This makes process lifecycle and
network binding explicit.

### 2. Environment-Based Configuration
Host and port are configured via environment variables to allow the
same code to run across different environments without modification.

### 3. systemd Integration
Instead of running as a background script, AutoOps is managed by
systemd to simulate real production services:
- supervised execution
- automatic restarts
- structured logging

### 4. Graceful Shutdown
Signal handling is implemented to ensure clean shutdowns when the
service is stopped or restarted by systemd.

---

## Current Limitations

- Single-node only
- No metrics endpoint yet
- No alerting
- No CI/CD

These are intentional and will be added incrementally.

