import socket

def test_tcp_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    
    message = "Hello, TCP Server!"
    client_socket.send(message.encode())
    
    response = client_socket.recv(1024).decode()
    if response == f"Echo: {message}":
        print("TCP Server Test Passed:", response)
    else:
        print("TCP Server Test Failed:", response)
    
    client_socket.close()

if __name__ == "__main__":
    test_tcp_server()
