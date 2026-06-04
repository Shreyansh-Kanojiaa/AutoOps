import logging
import time
import signal
import sys
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)

# ---------------- Prometheus Metrics ----------------

REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

ERRORS_TOTAL = Counter(
    "http_errors_total",
    "Total HTTP errors"
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    buckets=[0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 1, 2]
)

SERVICE_UPTIME = Gauge(
    "service_uptime_seconds",
    "Service uptime in seconds"
)

# ---------------- Logging ----------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("autoops")

START_TIME = time.time()


# ---------------- HTTP Handler ----------------

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        start_time = time.time()
        endpoint = self.path
        status_code = 200

        with REQUEST_LATENCY.time():

            try:

                if self.path == "/health":

                    uptime = int(time.time() - START_TIME)
                    SERVICE_UPTIME.set(uptime)

                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()

                    self.wfile.write(
                        f"OK - uptime {uptime}s\n".encode()
                    )

                elif self.path == "/metrics":

                    self.send_response(200)
                    self.send_header("Content-Type", CONTENT_TYPE_LATEST)
                    self.end_headers()

                    self.wfile.write(generate_latest())
                    return

                elif self.path == "/chaos":

                    ERRORS_TOTAL.inc()
                    status_code = 500

                    self.send_response(500)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()

                    self.wfile.write(b"Chaos injected\n")

                elif self.path == "/test":

                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()

                    self.wfile.write(b"test ok\n")

                else:

                    ERRORS_TOTAL.inc()
                    status_code = 404

                    self.send_response(404)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()

                    self.wfile.write(b"Not Found\n")

            except Exception:

                ERRORS_TOTAL.inc()
                status_code = 500

                logger.exception("Unhandled exception")

                self.send_response(500)
                self.end_headers()

        # ---------------- Metrics Recording ----------------

        REQUESTS_TOTAL.labels(
            method="GET",
            endpoint=endpoint,
            status=str(status_code)
        ).inc()

        duration = time.time() - start_time

        logger.info(
            f"{self.client_address[0]} {endpoint} {status_code} {duration*1000:.2f}ms"
        )

    def log_message(self, format, *args):
        return


# ---------------- Graceful Shutdown ----------------

def handle_shutdown(signum, frame):
    logger.info("Shutdown signal received. Stopping AutoOps.")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


# ---------------- Server ----------------

def run_server():

    host = os.getenv("AUTOOPS_HOST", "0.0.0.0")
    port = int(os.getenv("AUTOOPS_PORT", "8000"))

    logger.info(f"AutoOps service starting on {host}:{port}")

    server = HTTPServer((host, port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    run_server()
