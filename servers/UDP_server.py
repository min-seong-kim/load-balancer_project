import socket

def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 8082))  # 포트 8082에서 대기
    print("UDP Server is listening on port 8082")

    while True:
        message, addr = server_socket.recvfrom(1024)
        print(f"Received message from {addr}: {message.decode()}")

        # 받은 메시지를 클라이언트로 다시 돌려보냄 (Echo)
        server_socket.sendto(f"Echo: {message.decode()}".encode(), addr)

if __name__ == "__main__":
    udp_server()
