import socket
import os
from crypto import decrypt

PORT = 5001
CHUNK = 1024 * 512

os.makedirs("transfers", exist_ok=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ⭐ CRITICAL FIX
server.bind(("0.0.0.0", PORT))

server.listen(20)

print("📡 Receiver listening on port", PORT)

while True:
    conn, addr = server.accept()

    try:
        header = conn.recv(4)

        # 🔗 HANDSHAKE
        if header == b"HELO":

            name_len = int.from_bytes(conn.recv(2), "big")
            name = conn.recv(name_len).decode()

            print(f"🔗 {name} connected from {addr[0]}")
            conn.send(b"ACK ")

        # 💬 MESSAGE
        elif header == b"MSG ":

            length = int.from_bytes(conn.recv(4), "big")
            msg = conn.recv(length).decode()

            print(f"💬 {addr[0]}: {msg}")

        # 📦 FILE DATA
        elif header == b"DATA":

            start = int.from_bytes(conn.recv(8), "big")

            data = b""
            while True:
                part = conn.recv(CHUNK)
                if not part:
                    break
                data += part

            data = decrypt(data)

            file_path = "transfers/received.bin"

            with open(file_path, "r+b") if os.path.exists(file_path) else open(file_path, "wb") as f:
                f.seek(start)
                f.write(data)

            print("📦 File chunk received")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        conn.close()