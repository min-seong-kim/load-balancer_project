import socket

# 서버 설정
HOST = '127.0.0.1'  # 서버의 로컬 IP 주소
PORT = 65432        # 사용할 포트 번호

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # 소켓 바인딩
    s.listen()            # 클라이언트의 연결 대기
    print(f"TCP 서버가 {PORT} 포트에서 기다리고 있습니다.")
    
    conn, addr = s.accept()  # 클라이언트 연결 수락
    with conn:
        print('클라이언트와 연결됨:', addr)
        while True:
            data = conn.recv(1024)  # 데이터 수신
            if not data:
                break
            conn.sendall(data)  # 받은 데이터를 그대로 클라이언트로 전송

