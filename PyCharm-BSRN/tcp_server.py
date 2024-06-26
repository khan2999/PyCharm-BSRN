from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse
import logging
import threading

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        content_length = int(self.headers.get('Content-Length', 0))
        message = self.rfile.read(content_length).decode('utf-8')
        self.send_response(200)
        self.end_headers()
        response = f"Hello, GET request received! Message: {message}"
        self.wfile.write(response.encode('utf-8'))
        self.log_message(f"GET request received. Message: {message}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = f"Hello, POST request received! Data: {post_data.decode('utf-8')}"
        self.wfile.write(response.encode('utf-8'))
        self.log_message(f"POST request received. Data: {post_data.decode('utf-8')}")

    def do_DELETE(self):
        content_length = int(self.headers['Content-Length'])
        delete_data = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = f"Hello, DELETE request received! Data: {delete_data.decode('utf-8')}"
        self.wfile.write(response.encode('utf-8'))
        self.log_message(f"DELETE request received. Data: {delete_data.decode('utf-8')}")

class LoggingHTTPServer(HTTPServer):
    def __init__(self, server_address, handler_class, log_file):
        super().__init__(server_address, handler_class)
        self.logger = self._setup_logger(log_file)

    def _setup_logger(self, log_file):
        logger = logging.getLogger('http_server')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def log_message(self, format, *args):
        self.logger.info(format % args)

def run_server(server_address, log_file):
    server_class = LoggingHTTPServer
    handler_class = SimpleHTTPRequestHandler
    httpd = server_class(server_address, handler_class, log_file)
    print(f"TCP Server running on {server_address[0]}:{server_address[1]}, logging to {log_file}")
    httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TCP Server with logging support')
    parser.add_argument('-host', dest='host', default='localhost', help='Host IP address')
    parser.add_argument('-port', dest='port', type=int, default=8081, help='Port number')
    parser.add_argument('-log', dest='log_file', default='tcp_server.log', help='Log file path')
    args = parser.parse_args()

    server_address = (args.host, args.port)
    run_server(server_address, args.log_file)
