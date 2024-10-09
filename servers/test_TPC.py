import socket

HOST = '127.0.0.1'  # 서버 IP
PORT = 65432        # 서버 포트

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # 서버에 연결
    s.sendall(b'Hello, TCP Server')  # 데이터 전송
    data = s.recv(1024)  # 서버로부터 데이터 수신

print('서버로부터 받은 데이터:', repr(data))

