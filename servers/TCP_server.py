import socket

def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8081))  # 포트 8081에서 대기
    server_socket.listen(5)
    print("TCP Server is listening on port 8081")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        message = client_socket.recv(1024).decode()
        print(f"Received message: {message}")

        # 받은 메시지를 클라이언트로 다시 돌려보냄 (Echo)
        client_socket.send(f"Echo: {message}".encode())
        client_socket.close()

if __name__ == "__main__":
    tcp_server()
