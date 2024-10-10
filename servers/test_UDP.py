import socket

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 8082)  # 로드 밸런서의 UDP 포트로 연결
    message = "Hello, UDP Load Balancer!"

    try:
        # 서버로 메시지 전송
        print(f"Sending message to {server_address}")
        client_socket.sendto(message.encode(), server_address)

        # 서버로부터 응답 받기
        response, _ = client_socket.recvfrom(1024)
        print(f"Received response from server: {response.decode()}")

    finally:
        client_socket.close()

if __name__ == '__main__':
    udp_client()
