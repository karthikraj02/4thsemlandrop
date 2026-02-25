import socket
import os
import sys
import threading
from crypto import encrypt

if len(sys.argv) < 3:
    print("Usage: python sender.py <receiver_ip> <MSG:message or filename>")
    sys.exit(1)

ip = sys.argv[1]
data_arg = sys.argv[2]
PORT = 5001
CHUNK = 1024 * 512

def recv_exact(sock, n):
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

# Single connection for handshake and MSG
if data_arg.startswith("MSG:"):
    s = socket.socket()
    s.connect((ip, PORT))
    
    # Handshake
    name = os.getlogin().encode()
    s.send(b"HELO")
    s.send(len(name).to_bytes(2, "big"))
    s.send(name)
    ack = recv_exact(s, 4)
    print(f"DEBUG: Handshake ACK: {ack}")
    
    # Send MSG on same connection
    msg = data_arg[4:].encode()
    s.send(b"MSG ")
    s.send(len(msg).to_bytes(4, "big"))
    s.send(msg)
    
    s.close()
    print("💬 Message sent")
    sys.exit()

# FILE MODE
s = socket.socket()
s.connect((ip, PORT))

# Handshake first
name = os.getlogin().encode()
s.send(b"HELO")
s.send(len(name).to_bytes(2, "big"))
s.send(name)
ack = recv_exact(s, 4)
print(f"DEBUG: Handshake ACK: {ack}")

s.close()  # Close handshake connection

def send_chunk(start, data):
    conn = socket.socket()
    try:
        conn.connect((ip, PORT))
        conn.send(b"DATA")
        conn.send(start.to_bytes(8, "big"))
        conn.send(encrypt(data))
        print(f"📦 Chunk {start} sent")
    finally:
        conn.close()

with open(data_arg, "rb") as f:
    offset = 0
    threads = []
    while True:
        chunk = f.read(CHUNK)
        if not chunk:
            break
        t = threading.Thread(target=send_chunk, args=(offset, chunk))
        t.start()
        threads.append(t)
        offset += len(chunk)

    for t in threads:
        t.join()

print("🚀 File transfer complete")
