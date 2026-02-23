import socket, os
from crypto import decrypt

PORT = 5001
CHUNK = 1024 * 512

server = socket.socket()
server.bind(("0.0.0.0", PORT))
server.listen(50)

file_path = "transfers/received.bin"
os.makedirs("transfers", exist_ok=True)

f = open(file_path, "ab")

print("📡 GOD Receiver Ready")

while True:
    conn, addr = server.accept()
    header = conn.recv(4)

    if header == b"DATA":
        start = int.from_bytes(conn.recv(8), "big")
        data = decrypt(conn.recv(CHUNK))

        f.seek(start)
        f.write(data)

    conn.close()