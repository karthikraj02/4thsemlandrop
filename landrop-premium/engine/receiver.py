import socket
import os
from crypto import decrypt

PORT = 5001
CHUNK = 1024 * 512  # 512 KB

os.makedirs("transfers", exist_ok=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", PORT))
server.listen(20)

print("📡 GOD Receiver Ready on port", PORT)

while True:
    conn, addr = server.accept()

    try:
        header = conn.recv(4)

        # ===================================
        # 🔗 CONNECTION HANDSHAKE
        # ===================================
        if header == b"HELO":

            name_len = int.from_bytes(conn.recv(2), "big")
            name = conn.recv(name_len).decode()

            print(f"🔗 {name} connected from {addr[0]}")

            # Send ACK back
            conn.send(b"ACK ")

            # 🔔 LOCAL POPUP TRIGGER (terminal)
            print("✅ Connection established")

        # ===================================
        # 💬 MESSAGE
        # ===================================
        elif header == b"MSG ":

            length = int.from_bytes(conn.recv(4), "big")
            msg = conn.recv(length).decode()

            print("💬 Message:", msg)

        # ===================================
        # 📦 FILE CHUNK
        # ===================================
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

            print(f"📦 Chunk received at {start}")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        conn.close()