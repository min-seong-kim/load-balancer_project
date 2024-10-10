import socket
import threading
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 서버 목록 및 라운드 로빈 인덱스
tcp_servers = {}
udp_servers = {}
rest_servers = {}
tcp_index = 0
udp_index = 0
rest_index = 0

# 서버 등록 처리 (Registration)
@app.route('/register', methods=['POST'])
def register_server():
    data = request.json
    protocol = data.get("protocol")
    port = data.get("port")

    if protocol == "tcp":
        if port not in tcp_servers:
            tcp_servers[port] = []  # 해당 포트에 대한 서버 목록
        tcp_servers[port].append(('0.0.0.0', port))
        return jsonify({"ack": "successful"}), 200
    elif protocol == "udp":
        if port not in udp_servers:
            udp_servers[port] = []  # 해당 포트에 대한 서버 목록
        udp_servers[port].append(('0.0.0.0', port))
        return jsonify({"ack": "successful"}), 200
    elif protocol == "rest":
        if port not in rest_servers:
            rest_servers[port] = []  # REST 서버 등록
        rest_servers[port].append(('0.0.0.0', port))
        return jsonify({"ack": "successful"}), 200
    else:
        return jsonify({"ack": "failed", "msg": "Invalid protocol"}), 400

# 서버 해제 처리 (Unregistration)
@app.route('/unregister', methods=['POST'])
def unregister_server():
    data = request.json
    protocol = data.get("protocol")
    port = data.get("port")

    if protocol == "tcp":
        if port in tcp_servers and len(tcp_servers[port]) > 0:
            tcp_servers[port].pop()
            if len(tcp_servers[port]) == 0:
                del tcp_servers[port]
            return jsonify({"ack": "successful"}), 200
        else:
            return jsonify({"ack": "failed", "msg": "No server to unregister"}), 400
    elif protocol == "udp":
        if port in udp_servers and len(udp_servers[port]) > 0:
            udp_servers[port].pop()
            if len(udp_servers[port]) == 0:
                del udp_servers[port]
            return jsonify({"ack": "successful"}), 200
        else:
            return jsonify({"ack": "failed", "msg": "No server to unregister"}), 400
    elif protocol == "rest":
        if port in rest_servers and len(rest_servers[port]) > 0:
            rest_servers[port].pop()
            if len(rest_servers[port]) == 0:
                del rest_servers[port]
            return jsonify({"ack": "successful"}), 200
        else:
            return jsonify({"ack": "failed", "msg": "No server to unregister"}), 400
    else:
        return jsonify({"ack": "failed", "msg": "Invalid protocol"}), 400

# REST API 요청을 라운드 로빈 방식으로 분배
@app.route('/api', methods=['GET', 'POST'])
def api_request():
    global rest_index
    if not rest_servers:
        return jsonify({"error": "No REST servers available"}), 503

    # 라운드 로빈 방식으로 서버 선택
    port = list(rest_servers.keys())[rest_index]
    server = rest_servers[port][rest_index % len(rest_servers[port])]
    rest_index = (rest_index + 1) % len(rest_servers)

    # 요청을 선택된 서버로 프록시
    try:
        response = requests.request(
            method=request.method,
            url=f"http://{server[0]}:{server[1]}/api",
            json=request.get_json() if request.method == 'POST' else None
        )
        return (response.content, response.status_code, response.headers.items())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# TCP 요청을 라운드 로빈 방식으로 분배
def handle_tcp_connection(client_socket, port):
    global tcp_index
    if port not in tcp_servers or len(tcp_servers[port]) == 0:
        client_socket.send("No TCP servers available".encode())
        client_socket.close()
        return

    # 라운드 로빈 방식으로 서버 선택
    server = tcp_servers[port][tcp_index]
    tcp_index = (tcp_index + 1) % len(tcp_servers[port])

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect(server)
            data = client_socket.recv(1024)
            server_socket.send(data)
            response = server_socket.recv(1024)
            client_socket.send(response)
    except Exception as e:
        client_socket.send(f"Error: {str(e)}".encode())
    finally:
        client_socket.close()

# TCP 로드 밸런서 서버 설정
def tcp_load_balancer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lb_socket:
        lb_socket.bind(('0.0.0.0', 8080))  # 로드 밸런서가 8080에서 대기
        lb_socket.listen(5)
        print("TCP Load Balancer is listening on port 8080")

        while True:
            client_socket, _ = lb_socket.accept()
            thread = threading.Thread(target=handle_tcp_connection, args=(client_socket, 80))
            thread.start()

# UDP 요청을 라운드 로빈 방식으로 분배
# UDP 요청을 라운드 로빈 방식으로 분배
def udp_load_balancer():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as lb_socket:
        lb_socket.bind(('0.0.0.0', 8083))  # 로드 밸런서가 8083에서 대기
        print("UDP Load Balancer is listening on port 8083")

        while True:
            data, client_address = lb_socket.recvfrom(1024)
            global udp_index

            # 클라이언트가 요청한 포트를 받아옴
            client_port = client_address[1]

            if client_port not in udp_servers or len(udp_servers[client_port]) == 0:
                lb_socket.sendto("No UDP servers available".encode(), client_address)
                continue

            # 라운드 로빈 방식으로 서버 선택
            server = udp_servers[client_port][udp_index]
            udp_index = (udp_index + 1) % len(udp_servers[client_port])

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
                    server_socket.sendto(data, server)
                    response, _ = server_socket.recvfrom(1024)
                    lb_socket.sendto(response, client_address)
            except Exception as e:
                lb_socket.sendto(f"Error: {str(e)}".encode(), client_address)


if __name__ == '__main__':
    # 플라스크 서버 스레드로 실행 (서버 등록 및 해제를 처리)
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5001))
    flask_thread.start()

    # TCP 및 UDP 로드 밸런서 실행
    tcp_thread = threading.Thread(target=tcp_load_balancer)
    udp_thread = threading.Thread(target=udp_load_balancer)
    tcp_thread.start()
    udp_thread.start()

    tcp_thread.join()
    udp_thread.join()
