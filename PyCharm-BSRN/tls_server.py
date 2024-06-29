import ssl
import socket

def start_tls_server():
    # Erstellen eines TLS-Kontexts für die Server-Authentifizierung
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # Laden des Zertifikats und des privaten Schlüssels
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    # Erstellen des Socket-Objekts
    bindsocket = socket.socket()
    # Binden des Sockets an die lokale Adresse und den Port 10023
    bindsocket.bind(('localhost', 10023))
    # Warten auf eingehende Verbindungen (bis zu 5 Verbindungen in der Warteschlange)
    bindsocket.listen(5)
    print("TLS-Server gestartet und hört auf Port 10023")

    while True:
        # Akzeptieren einer neuen Verbindung
        newsocket, fromaddr = bindsocket.accept()
        print("Verbindung von", fromaddr)
        # Umschalten auf TLS für die eingehende Verbindung
        connstream = context.wrap_socket(newsocket, server_side=True)

        try:
            # Empfangen der Daten von der TLS-Verbindung
            data = connstream.recv(1024)
            print("Empfangen:", data.decode())
            # Senden einer Antwort zurück an den Client
            connstream.sendall(b"Hello from TLS server!")
        finally:
            # Herunterfahren und Schließen der TLS-Verbindung
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()

if __name__ == '__main__':
    # Starten des TLS-Servers
    start_tls_server()
