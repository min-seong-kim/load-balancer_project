import socket

def test_udp_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    message = "Hello, UDP Server!"
    client_socket.sendto(message.encode(), ('127.0.0.1', 8081))
    
    response, _ = client_socket.recvfrom(1024)
    response = response.decode()
    if response == f"Echo: {message}":
        print("UDP Server Test Passed:", response)
    else:
        print("UDP Server Test Failed:", response)

if __name__ == "__main__":
    test_udp_server()
