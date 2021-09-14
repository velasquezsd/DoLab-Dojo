import http.server
import random
from prometheus_client import start_http_server
from prometheus_client import Counter

REQUESTS = Counter('kata1_server_requests_total', 'Total number of requests to this webserver')
EXCEPTIONS = Counter('kata1_server_exceptions_total', 'Total number of exception raised by this webserver')

class ServerHandler(http.server.BaseHTTPRequestHandler):
    @EXCEPTIONS.count_exceptions()
    def do_GET(self):
         REQUESTS.inc()
         if random.random() > 0.5:
             raise Exception
         self.send_response(200)
         self.end_headers()
         self.wfile.write(b"Hello World!")

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('', 8001), ServerHandler)
    print("Prometheus metrics available on port 8000 /metrics")
    print("HTTP server available on port 8001")
    server.serve_forever()
