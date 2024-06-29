import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Formatieren der Lognachricht
        message = "%s - - [%s] %s\n" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args
        )
        # Nachricht im Server-Logger protokollieren
        self.server.logger.info(message)
        # Nachricht im Terminal ausgeben
        print(message)

    def do_GET(self):
        # Verarbeitung der GET-Anfrage
        content_length = int(self.headers.get('Content-Length', 0))
        message = self.rfile.read(content_length).decode('utf-8')
        self.send_response(200)
        self.end_headers()
        response = f"Hello, GET request received! Message: {message}"
        self.wfile.write(response.encode('utf-8'))
        self.log_message(f"GET request received. Message: {message}")

    def do_POST(self):
        # Verarbeitung der POST-Anfrage
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = f"Hello, POST request received! Data: {post_data.decode('utf-8')}"
        self.wfile.write(response.encode('utf-8'))
        self.log_message(f"POST request received. Data: {post_data.decode('utf-8')}")

    def do_PUT(self):
        # Verarbeitung der PUT-Anfrage
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = f"Hello, PUT request received! Data: {put_data.decode('utf-8')}"
        self.wfile.write(response.encode('utf-8'))
        self.log_message(f"PUT request received. Data: {put_data.decode('utf-8')}")

    def do_DELETE(self):
        # Verarbeitung der DELETE-Anfrage
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
        self.logger = self.setup_logger(log_file)

    def setup_logger(self, log_file):
        # Einrichten des Loggers
        logger = logging.getLogger('tcp_server')
        logger.setLevel(logging.INFO)

        # File Handler
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger


def run_server(server_address, log_file):
    server_class = LoggingHTTPServer
    handler_class = SimpleHTTPRequestHandler
    httpd = server_class(server_address, handler_class, log_file)
    print(f"TCP-Server läuft auf {server_address[0]}:{server_address[1]}, loggt in {log_file}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("Server gestoppt.")

if __name__ == "__main__":
    # Argumentparser einrichten
    parser = argparse.ArgumentParser(description='TCP-Server mit Logging-Unterstützung')
    parser.add_argument('-host', dest='host', default='localhost', help='Host-IP-Adresse')
    parser.add_argument('-port', dest='port', type=int, default=8081, help='Portnummer')
    parser.add_argument('-logfile', dest='log_file', default='tcp_server.log', help='Pfad zur Logdatei')

    # Kommandozeilenargumente parsen
    args = parser.parse_args()

    server_address = (args.host, args.port)
    run_server(server_address, args.log_file)
