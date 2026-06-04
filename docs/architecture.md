# AutoOps Architecture

This document describes the architecture of the AutoOps observability stack. The system consists of an instrumented application and several monitoring components that collect metrics, logs, and alerts.

---

## System Overview

```
              +-------------+
              |   Clients   |
              +-------------+
                     |
                     v
              +-------------+
              |   AutoOps   |
              | HTTP Server |
              +-------------+
                     |
         +-----------+-----------+
         |                       |
         v                       v
   +-----------+           +-----------+
   | Prometheus|           | Promtail  |
   |  Metrics  |           | Log Agent |
   +-----------+           +-----------+
         |                       |
         v                       v
   +-----------+           +-----------+
   | Grafana   |           |   Loki    |
   | Dashboards|           | Log Store |
   +-----------+           +-----------+
         |
         v
   +-------------+
   | Alertmanager|
   | Alert Router|
   +-------------+
```

---

## Components

### AutoOps Service

A Python HTTP service that exposes operational metrics and structured logs.

Responsibilities:
- Serve application endpoints
- Expose Prometheus metrics
- Emit structured logs for request activity
- Provide a chaos endpoint for testing alerts

### Prometheus

Prometheus scrapes metrics from the AutoOps service on a configured interval.

Responsibilities:
- Collect and store time series metrics
- Evaluate alert rules
- Fire alerts to Alertmanager when thresholds are breached

### Grafana

Grafana provides visualization for both metrics and logs. It queries Prometheus for metrics and Loki for logs.

Dashboards display:
- Request rate
- Error rate
- Latency percentiles (p95, p99)
- Service uptime
- Live container logs

### Loki

Loki is the log aggregation backend.

Responsibilities:
- Index and store container logs forwarded by Promtail
- Serve log queries from Grafana

### Promtail

Promtail is the log collection agent. It runs as a container with access to the Docker socket, discovers other running containers, and ships their logs to Loki.

Responsibilities:
- Discover containers via Docker socket
- Attach metadata labels (container name, job, etc.)
- Forward logs to Loki

### Alertmanager

Alertmanager receives firing alerts from Prometheus and handles their delivery.

Responsibilities:
- Group related alerts
- Deduplicate repeated alerts
- Route alerts to configured notification channels

---

## Observability Pipeline

```
Application
    |
    |-- metrics --> Prometheus --> Grafana
    |                   |
    |                   v
    |             Alertmanager
    |
    |-- logs --> Promtail --> Loki --> Grafana
```

Step by step:

1. Application emits metrics and logs on every request
2. Prometheus scrapes metrics at a regular interval
3. Promtail collects logs from Docker containers
4. Loki stores and indexes the logs
5. Grafana queries both Prometheus and Loki for visualization
6. Prometheus evaluates alert rules against collected metrics
7. Alertmanager receives alerts and routes them to notification systems

---

## Design Goals

AutoOps was designed to demonstrate core observability concepts used in production systems:

- Metrics collection and storage
- Log aggregation and querying
- Alert rule evaluation and routing
- Service level monitoring
- Fully containerized, reproducible deployment
