import socket

HOST = '127.0.0.1'  # 서버 IP
PORT = 65433        # 서버 포트

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b'Hello, UDP Server', (HOST, PORT))  # 데이터 전송
    data, addr = s.recvfrom(1024)  # 서버로부터 데이터 수신

print('서버로부터 받은 데이터:', data.decode())

