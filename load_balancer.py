import socket
import threading

# 서버 풀 - 각 서버의 주소와 포트
servers = [
    ('127.0.0.1', 65432),  # TCP 서버 1
    ('127.0.0.1', 65433),  # UDP 서버 1
    ('127.0.0.1', 5000),   # REST API 서버
]

# 라운드 로빈을 위한 인덱스
current_server_index = 0
lock = threading.Lock()

def get_next_server():
    global current_server_index
    with lock:
        server = servers[current_server_index]
        current_server_index = (current_server_index + 1) % len(servers)
    return server

# TCP 클라이언트 요청 처리
def handle_tcp_client(client_socket):
    try:
        # 다음 서버를 선택
        server_ip, server_port = get_next_server()

        # 선택된 서버에 연결
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((server_ip, server_port))
            
            # 클라이언트로부터 데이터 수신
            client_data = client_socket.recv(1024)

            # 서버에 데이터 전송
            server_socket.sendall(client_data)
            
            # 서버로부터 응답을 받아 클라이언트에 전달
            server_data = server_socket.recv(1024)
            client_socket.sendall(server_data)
    
    finally:
        client_socket.close()

# UDP 클라이언트 요청 처리
def handle_udp_client(client_socket, client_address):
    try:
        # 다음 서버를 선택
        server_ip, server_port = get_next_server()

        # 클라이언트로부터 데이터 수신
        client_data, addr = client_socket.recvfrom(1024)

        # 선택된 서버로 데이터 전송
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.sendto(client_data, (server_ip, server_port))

            # 서버로부터 응답을 받아 클라이언트에 전달
            server_data, _ = server_socket.recvfrom(1024)
            client_socket.sendto(server_data, client_address)
    
    finally:
        client_socket.close()

def tcp_load_balancer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lb_socket:
        lb_socket.bind(('0.0.0.0', 12345))  # 로드 밸런서 TCP 포트
        lb_socket.listen()
        print("TCP Load Balancer Listening on port 12345...")

        while True:
            client_socket, addr = lb_socket.accept()
            print(f"TCP Client connected from {addr}")
            client_handler = threading.Thread(target=handle_tcp_client, args=(client_socket,))
            client_handler.start()

def udp_load_balancer():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as lb_socket:
        lb_socket.bind(('0.0.0.0', 12346))  # 로드 밸런서 UDP 포트
        print("UDP Load Balancer Listening on port 12346...")

        while True:
            client_socket, client_address = lb_socket.recvfrom(1024)
            print(f"UDP Client connected from {client_address}")
            udp_handler = threading.Thread(target=handle_udp_client, args=(lb_socket, client_address))
            udp_handler.start()

# 각각의 로드 밸런서 (TCP/UDP) 서버를 실행
if __name__ == "__main__":
    tcp_thread = threading.Thread(target=tcp_load_balancer)
    udp_thread = threading.Thread(target=udp_load_balancer)

    tcp_thread.start()
    udp_thread.start()

    tcp_thread.join()
    udp_thread.join()

