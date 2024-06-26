import socket

def udp_server(host='0.0.0.0', port=8082):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f"UDP Server running on {host}:{port}")

        while True:
            data, addr = s.recvfrom(1024)
            print(f"Received from {addr}: {data.decode('utf-8')}")
            response = f"Hello, UDP request received! Data: {data.decode('utf-8')}"
            s.sendto(response.encode('utf-8'), addr)

if __name__ == "__main__":
    udp_server()