import socket
import ssl

HOST = '127.0.0.1'
PORT = 8443

def start_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile="server.crt",
        keyfile="server.key"
    )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bindsocket:
        bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        bindsocket.bind((HOST, PORT))
        bindsocket.listen(5)
        print("TLS Server listening...")

        while True:
            newsocket, addr = bindsocket.accept()
            print(f"Connection from {addr}")

            connstream = None  # <-- define before try
            try:
                connstream = context.wrap_socket(newsocket, server_side=True)
                print("TLS handshake successful")

                data = connstream.recv(1024).decode()
                print("Received:", data)

                connstream.sendall("Secure message received!".encode())

            except ssl.SSLError as e:
                print("SSL Error:", e)  # Now you'll see handshake failures
            except Exception as e:
                print("Error:", e)
            finally:
                if connstream:
                    connstream.close()
                else:
                    newsocket.close()  # close raw socket if wrap failed

if __name__ == "__main__":
    start_server()