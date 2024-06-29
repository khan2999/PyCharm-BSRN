import socket
import ssl

# Fest vorgegebene Werte für Host und Port
HOST = '127.0.0.1'
PORT = 8080

def main():
    while True:
        # Benutzer nach dem gewünschten Protokoll fragen
        protocol = input("Verbinden mit (TCP/UDP/TLS): ").upper()

        # Überprüfen, ob das Protokoll unterstützt wird
        if protocol not in ['TCP', 'UDP', 'TLS']:
            print("Nicht unterstütztes Protokoll. Bitte verwenden Sie TCP, UDP oder TLS.")
            continue

        # Nachricht und HTTP-Methode vom Benutzer abfragen
        message = input("Nachricht: ")
        method = input("HTTP-Methode (GET/POST/PUT/DELETE): ").upper()

        try:
            if protocol == 'TCP':
                # TCP-Verbindung herstellen
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    # HTTP-Anfrage erstellen
                    if method in ['POST', 'PUT', 'DELETE']:
                        request = f"{method} / HTTP/1.1\r\nHost: {HOST}\r\nContent-Length: {len(message)}\r\n\r\n{message}"
                    else:
                        request = f"{method} / HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
                    # Anfrage senden und Antwort empfangen
                    s.sendall(request.encode('utf-8'))
                    response = s.recv(1024)
                    print("Antwort vom TCP-Server erhalten:", response.decode('utf-8'))
            elif protocol == 'UDP':
                # UDP-Verbindung herstellen
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    # HTTP-Anfrage erstellen
                    request = f"{method} / HTTP/1.1\r\nHost: {HOST}\r\nContent-Length: {len(message)}\r\n\r\n{message}"
                    # Anfrage senden und Antwort empfangen
                    s.sendto(request.encode('utf-8'), (HOST, PORT))
                    response, _ = s.recvfrom(1024)
                    print("Antwort vom UDP-Server erhalten:", response.decode('utf-8'))
            elif protocol == 'TLS':
                # TLS-Kontext erstellen
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                # TLS-Verbindung herstellen
                with socket.create_connection((HOST, 10023)) as sock:
                    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
                        print("TLS-Verbindung hergestellt")
                        # HTTP-Anfrage erstellen
                        if method in ['POST', 'PUT', 'DELETE']:
                            request = f"{method} / HTTP/1.1\r\nHost: {HOST}\r\nContent-Length: {len(message)}\r\n\r\n{message}"
                        else:
                            request = f"{method} / HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
                        # Anfrage senden und Antwort empfangen
                        ssock.sendall(request.encode('utf-8'))
                        response = ssock.recv(1024)
                        print("Antwort vom TLS-Server erhalten:", response.decode('utf-8'))

        except Exception as e:
            # Fehler behandeln und ausgeben
            print(f"Fehler: {e}")

        # Benutzer fragen, ob er fortfahren möchte
        choice = input("Möchten Sie mit diesem Server fortfahren? (Y/N): ").upper()
        if choice != 'Y':
            print("Vielen Dank für Ihren Besuch!")
            break

if __name__ == "__main__":
    main()
