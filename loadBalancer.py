import socket
import threading

# Zielserver-Details
TCP_SERVER_HOST = '127.0.0.1'
TCP_SERVER_PORT = 8081
UDP_SERVER_HOST = '127.0.0.1'
UDP_SERVER_PORT = 8082

def handle_tcp_client(client_socket, addr):
    # Behandeln der TCP-Client-Verbindung
    with client_socket:
        request = client_socket.recv(1024)  # Empfang der Anfrage vom Client
        print(f"Empfangen von {addr} (TCP): {request.decode('utf-8')}")

        # Weiterleiten der Anfrage an den TCP-Server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
            server_socket.sendall(request)
            response = server_socket.recv(1024)

        # Senden der Antwort zurück an den Client
        client_socket.sendall(response)

def handle_udp_client():
    # Behandeln der UDP-Client-Verbindungen
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.bind(('0.0.0.0', 8080))  # UDP-Load-Balancer auf Port 8080 binden
        print("UDP Load Balancer läuft auf Port 8080")

        while True:
            message, client_address = udp_sock.recvfrom(1024)  # Empfang der Nachricht vom Client
            print(f"Empfangen von {client_address} (UDP): {message.decode('utf-8')}")

            # Weiterleiten der Anfrage an den UDP-Server
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
                server_socket.sendto(message, (UDP_SERVER_HOST, UDP_SERVER_PORT))
                response, _ = server_socket.recvfrom(1024)

            # Senden der Antwort zurück an den Client
            udp_sock.sendto(response, client_address)

def tcp_load_balancer():
    # TCP-Load-Balancer
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 8080))  # TCP-Load-Balancer auf Port 8080 binden
        s.listen()
        print("TCP Load Balancer läuft auf Port 8080")

        while True:
            client_socket, addr = s.accept()  # Akzeptieren einer neuen Client-Verbindung
            thread = threading.Thread(target=handle_tcp_client, args=(client_socket, addr))
            thread.start()  # Starten eines neuen Threads, um die Client-Anfrage zu behandeln

if __name__ == "__main__":
    # Starten des TCP-Load-Balancers in einem separaten Thread
    tcp_thread = threading.Thread(target=tcp_load_balancer)
    tcp_thread.start()

    # Starten des UDP-Load-Balancers im Hauptthread
    handle_udp_client()
