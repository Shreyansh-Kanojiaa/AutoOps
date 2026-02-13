from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import time
import os
import signal
import sys

START_TIME = time.time()

HOST = os.getenv("AUTOOPS_HOST", "127.0.0.1")
PORT = int(os.getenv("AUTOOPS_PORT", "8000"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            uptime = int(time.time() - START_TIME)
            response = f"OK - uptime {uptime}s\n"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode())

            logging.info("Health check OK")
        else:
            self.send_response(404)
            self.end_headers()

def shutdown_handler(signum, frame):
    logging.info("Shutdown signal received, stopping service")
    sys.exit(0)

def run():
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, HealthHandler)

    logging.info(f"AutoOps service starting on {HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
