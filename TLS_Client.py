import socket
import ssl

HOST = '127.0.0.1'
PORT = 8443

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

try:
    print("Step 1: Creating socket...")
    sock = socket.create_connection((HOST, PORT))
    print("Step 2: TCP connected!")
    
    conn = context.wrap_socket(sock, server_hostname=HOST)
    print("Step 3: TLS handshake done!")
    
    conn.sendall(b"Hello")
    print("Step 4: Message sent!")
    
    reply = conn.recv(1024)
    print("Step 5: Server replied:", reply.decode())
    
    conn.close()

except ConnectionRefusedError:
    print("FAILED: Server is not running or wrong port")
except ssl.SSLError as e:
    print("FAILED: SSL Error:", e)
except Exception as e:
    print("FAILED:", type(e).__name__, e)