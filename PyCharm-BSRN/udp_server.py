import argparse
import logging
import os
import socket

def udp_server(host='0.0.0.0', port=8082, log_file='udp_server.log'):
    # Einrichten des Loggings
    logger = setup_logger(log_file)

    # Erstellen und Binden des UDP-Sockets
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        logger.info(f"UDP-Server läuft auf {host}:{port}")
        print(f"UDP-Server läuft auf {host}:{port}")

        while True:
            # Empfang von Daten vom Client
            data, addr = s.recvfrom(1024)
            message = data.decode('utf-8')
            logger.info(f"Empfangen von {addr}: {message}")
            print(f"Empfangen von {addr}: {message}")

            # Nachricht an den Client zurücksenden
            response = f"Hello, UDP-Anfrage empfangen! Daten: {message}"
            s.sendto(response.encode('utf-8'), addr)

def setup_logger(log_file):
    # Einrichten des Loggers
    logger = logging.getLogger('udp_server')
    logger.setLevel(logging.INFO)

    # Sicherstellen, dass die Logdatei existiert
    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    # Einrichten des Handlers für die Logdatei
    handler = logging.FileHandler(log_file, mode='a')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

if __name__ == "__main__":
    # Argumentparser einrichten
    parser = argparse.ArgumentParser(description='UDP-Server mit Logging-Unterstützung')
    parser.add_argument('-host', dest='host', default='0.0.0.0', help='Host-IP-Adresse')
    parser.add_argument('-port', dest='port', type=int, default=8082, help='Portnummer')
    parser.add_argument('-logfile', dest='log_file', default='udp_server.log', help='Pfad zur Logdatei')

    # Kommandozeilenargumente parsen
    args = parser.parse_args()

    # Starten des UDP-Servers mit den angegebenen Argumenten
    udp_server(args.host, args.port, args.log_file)
