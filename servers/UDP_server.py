import socket

# 서버 설정
HOST = '127.0.0.1'  # 서버의 로컬 IP 주소
PORT = 65433        # 사용할 포트 번호

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))  # 소켓 바인딩
    print(f"UDP 서버가 {PORT} 포트에서 기다리고 있습니다.")
    
    while True:
        data, addr = s.recvfrom(1024)  # 데이터 수신
        print('클라이언트로부터 수신됨:', addr)
        print('받은 데이터:', data.decode())
        s.sendto(data, addr)  # 받은 데이터를 그대로 클라이언트로 전송

