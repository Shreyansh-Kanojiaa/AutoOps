# AutoOps

AutoOps is a personal DevOps and SRE project built to explore service observability, monitoring, alerting, and incident response workflows.

The project consists of a Python HTTP service instrumented with Prometheus metrics and deployed alongside a monitoring stack using Docker Compose. It was built as a hands-on way to learn how production systems are monitored and how engineers investigate failures using metrics, dashboards, logs, and alerts.

## What It Does

The application exposes:

* Health endpoints
* Prometheus metrics
* Request counters
* Error tracking
* Request latency histograms
* Service uptime metrics

These metrics are collected by Prometheus and visualized in Grafana dashboards. Alert rules evaluate service health and generate alerts when predefined thresholds are exceeded.

The project also includes a chaos endpoint that intentionally generates failures, making it possible to test alerting and monitoring workflows under controlled conditions.

---

## Architecture

```text
Client
   │
   ▼
AutoOps Service
   │
   ├── Metrics ──► Prometheus
   │                  │
   │                  ▼
   │               Grafana
   │
   └── Alerts ──► Alertmanager
```

The stack currently consists of:

* Python service
* Docker Compose deployment
* Prometheus
* Grafana
* Alertmanager

Additional observability components are being added as the project evolves.

---

## Technologies Used

| Component     | Technology     |
| ------------- | -------------- |
| Application   | Python         |
| Containers    | Docker         |
| Orchestration | Docker Compose |
| Metrics       | Prometheus     |
| Dashboards    | Grafana        |
| Alerting      | Alertmanager   |
| CI/CD         | GitHub Actions |

---

## Metrics Exposed

Examples of metrics exposed by the service include:

```text
http_requests_total
http_request_duration_seconds
uptime_seconds
errors_total
```

These metrics are scraped by Prometheus and used for dashboarding and alert evaluation.

---

## Dashboards

The Grafana dashboards currently track:

* Request rate (RPS)
* Error rate
* Service uptime
* P95 latency
* P99 latency
* Alert status

The goal is to provide a quick overview of service health and make failures easy to identify.

---

## Alerting

Prometheus evaluates alert rules against collected metrics.

Current alert examples include:

* High error rate
* Service unavailable
* Elevated latency
* Crash-loop behaviour

Alerts are routed through Alertmanager for processing and notification delivery.

---

## Chaos Testing

A dedicated endpoint allows failures to be injected into the service:

```bash
curl http://localhost:8000/chaos
```

This makes it possible to validate dashboards, alert rules, and monitoring behaviour during failure scenarios.

---

## Load Testing

Traffic can be generated using ApacheBench:

```bash
ab -n 5000 -c 50 http://localhost:8000/test
```

Load tests are useful for observing:

* Request throughput.
* Latency behaviour.
* Error rate changes.
* Alert triggering.

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/Shreyansh-Kanojiaa/AutoOps.git
cd AutoOps
```

Start the stack:

```bash
docker compose up -d --build
```

Access the services:

| Service      | Address               |
| ------------ | --------------------- |
| Grafana      | http://localhost:3000 |
| Prometheus   | http://localhost:9090 |
| Alertmanager | http://localhost:9093 |

---

## CI Pipeline

GitHub Actions runs automatically on pushes and pull requests.

The pipeline currently performs:

* Python linting
* Prometheus configuration validation
* Alert rule validation
* Docker image build verification
* Service startup checks

---

## Why I Built This

I built AutoOps to gain practical experience with observability and SRE tooling rather than only studying the concepts theoretically.

While developing the project I encountered and resolved issues involving container networking, monitoring configuration, alert validation, SELinux permissions, Docker volumes, and service reliability. Working through those problems provided a much better understanding of how production monitoring systems behave than simply following tutorials.

---

## Future Work

Planned improvements include:

* Loki-based log aggregation
* OpenTelemetry tracing
* Kubernetes deployment
* Alert notifications through Slack or email
* Automated chaos testing workflows

---

## License

MIT License

