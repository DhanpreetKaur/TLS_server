import socket
import ssl

HOST = '127.0.0.1'
PORT = 8443

def start_client():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as conn:
            message = input("Enter message: ")
            conn.sendall(message.encode())
            reply = conn.recv(1024).decode()
            print("Server reply:", reply)

if __name__ == "__main__":
    start_client()
