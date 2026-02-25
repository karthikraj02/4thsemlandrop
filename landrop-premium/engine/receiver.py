import socket
import os
import threading
from crypto import decrypt

PORT = 5001
CHUNK = 1024 * 512

os.makedirs("transfers", exist_ok=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", PORT))
server.listen(20)

print(f"📡 Receiver listening on port {PORT}")
print("Test connectivity: telnet localhost 5001 or nc -v localhost 5001")

clients = []  # Track active client connections

def handle_client(conn, addr):
    print(f"🔗 New client from {addr[0]}")
    clients.append(conn)
    
    try:
        while True:
            header = recv_exact(conn, 4)
            if not header:
                break
            
            print(f"DEBUG: Received header: {header}")
            
            if header == b"HELO":
                name_len = int.from_bytes(recv_exact(conn, 2), "big")
                name = recv_exact(conn, name_len).decode()
                print(f"🔗 {name} connected from {addr[0]}")
                conn.send(b"ACK ")
            
            elif header == b"MSG ":
                length = int.from_bytes(recv_exact(conn, 4), "big")
                msg = recv_exact(conn, length).decode()
                print(f"💬 {addr[0]}: {msg}")
            
            elif header == b"DATA":
                start = int.from_bytes(recv_exact(conn, 8), "big")
                data = b""
                while True:
                    part = conn.recv(CHUNK)
                    if len(part) < CHUNK or not part:
                        break
                    data += part
                data = decrypt(data)
                file_path = "transfers/received.bin"
                mode = "r+b" if os.path.exists(file_path) else "wb"
                with open(file_path, mode) as f:
                    f.seek(start)
                    f.write(data)
                print("📦 File chunk received at offset", start)
    
    except Exception as e:
        print(f"❌ Client {addr}: Error: {e}")
    finally:
        print(f"🔌 Closing client {addr}")
        if conn in clients:
            clients.remove(conn)
        conn.close()

def recv_exact(sock, n):
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

while True:
    conn, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.daemon = True
    client_thread.start()
