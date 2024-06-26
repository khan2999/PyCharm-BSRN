import socket

def main():
    host = input("Connect to (IP address): ")
    port = int(input("Port: "))
    protocol = input("Protocol (TCP/UDP): ").upper()
    message = input("Message: ")
    method = input("HTTP Method (GET/POST/DELETE): ").upper()

    if protocol == 'TCP':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            if method in ['POST', 'DELETE']:
                request = f"{method} / HTTP/1.1\r\nHost: {host}\r\nContent-Length: {len(message)}\r\n\r\n{message}"
            else:
                request = f"{method} / HTTP/1.1\r\nHost: {host}\r\n\r\n"
            s.sendall(request.encode('utf-8'))
            response = s.recv(1024)
            print("Received:", response.decode('utf-8'))
    elif protocol == 'UDP':
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            request = f"{method} / HTTP/1.1\r\nHost: {host}\r\nContent-Length: {len(message)}\r\n\r\n{message}"
            s.sendto(request.encode('utf-8'), (host, port))
            response, _ = s.recvfrom(1024)
            print("Received:", response.decode('utf-8'))
    else:
        print("Unsupported protocol. Please use TCP or UDP.")

if __name__ == "__main__":
    main()
