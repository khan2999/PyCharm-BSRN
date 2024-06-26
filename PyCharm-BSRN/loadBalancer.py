import socket
import threading

# Target server details
TCP_SERVER_HOST = '127.0.0.1'
TCP_SERVER_PORT = 8081
UDP_SERVER_HOST = '127.0.0.1'
UDP_SERVER_PORT = 8082


def handle_tcp_client(client_socket, addr):
    with client_socket:
        request = client_socket.recv(1024)
        print(f"Received from {addr} (TCP): {request.decode('utf-8')}")

        # Forward the request to the TCP server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
            server_socket.sendall(request)
            response = server_socket.recv(1024)

        # Send the response back to the client
        client_socket.sendall(response)


def handle_udp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.bind(('0.0.0.0', 8080))
        print("UDP Load Balancer running on port 8080")

        while True:
            message, client_address = udp_sock.recvfrom(1024)
            print(f"Received from {client_address} (UDP): {message.decode('utf-8')}")

            # Forward the request to the UDP server
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
                server_socket.sendto(message, (UDP_SERVER_HOST, UDP_SERVER_PORT))
                response, _ = server_socket.recvfrom(1024)

            # Send the response back to the client
            udp_sock.sendto(response, client_address)


def tcp_load_balancer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 8080))
        s.listen()
        print("TCP Load Balancer running on port 8080")

        while True:
            client_socket, addr = s.accept()
            thread = threading.Thread(target=handle_tcp_client, args=(client_socket, addr))
            thread.start()


if __name__ == "__main__":
    # Start TCP load balancer in a separate thread
    tcp_thread = threading.Thread(target=tcp_load_balancer)
    tcp_thread.start()

    # Start UDP load balancer in the main thread
    handle_udp_client()
