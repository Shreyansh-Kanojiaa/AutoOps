import logging
import time
import signal
import sys
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("autoops")

START_TIME = time.time()
REQUEST_COUNT = 0
ERROR_COUNT = 0
TOTAL_RESPONSE_TIME = 0.0

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global REQUEST_COUNT, ERROR_COUNT, TOTAL_RESPONSE_TIME
        REQUEST_COUNT += 1
        start_time = time.time()
        
        try:
            if self.path == "/health":
                uptime = int(time.time() - START_TIME)
                if REQUEST_COUNT > 0:
                    error_rate = ERROR_COUNT / REQUEST_COUNT
                else:
                    error_rate = 0
                
                if error_rate > 0.5:
                    self.send_response(503)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()
                    self.wfile.write(f"UNHEALTHY - error_rate {error_rate:.2f}\n".encode())
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()
                    self.wfile.write(f"OK - Uptime {uptime}s\n".encode())
                    
            elif self.path == "/metrics":
                uptime = int(time.time() - START_TIME)
                if REQUEST_COUNT > 0:
                    avg_response = TOTAL_RESPONSE_TIME / REQUEST_COUNT
                else:
                    avg_response = 0.0
                
                metrics_output = (
                    "# HELP uptime_seconds Total uptime of the service in seconds\n"
                    "# TYPE uptime_seconds gauge\n"
                    f"uptime_seconds {uptime}\n"
                    "# HELP requests_total Total number of HTTP requests received\n"
                    "# TYPE requests_total counter\n"
                    f"requests_total {REQUEST_COUNT}\n"
                    "# HELP errors_total Total number of failed HTTP requests\n"
                    "# TYPE errors_total counter\n"
                    f"errors_total {ERROR_COUNT}\n"
                    "# HELP avg_response_seconds Average response time in seconds\n"
                    "# TYPE avg_response_seconds gauge\n"
                    f"avg_response_seconds {avg_response:.6f}\n"
                )
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; version=0.0.4")
                self.end_headers()
                self.wfile.write(metrics_output.encode())
                
            else:
                ERROR_COUNT += 1
                self.send_response(404)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Not Found\n")
                
        except Exception:
            ERROR_COUNT += 1
            logger.exception("Unhandled exception during request")
            self.send_response(500)
            self.end_headers()
            
        duration = time.time() - start_time
        TOTAL_RESPONSE_TIME += duration
        logger.info(
            f"{self.client_address[0]} {self.path} {duration * 1000:.2f}ms"
        )
    
    def log_message(self, format, *args):
        return

def handle_shutdown(signum, frame):
    logger.info("Shutdown signal received. Stopping AutoOps.")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

def run_server():
    host = os.getenv("AUTOOPS_HOST", "127.0.0.1")
    port = int(os.getenv("AUTOOPS_PORT", "8000"))
    
    logger.info(f"AutoOps service starting on {host}:{port}")
    server = HTTPServer((host, port), Handler)
    server.serve_forever()

if __name__ == "__main__":
    run_server()
