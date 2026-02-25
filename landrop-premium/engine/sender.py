import socket
import os
import sys
import threading
from crypto import encrypt

ip = sys.argv[1]
path = sys.argv[2]

PORT = 5001
CHUNK = 1024 * 512  # 512 KB


# =========================
# 💬 SEND MESSAGE MODE
# =========================
if path.startswith("MSG:"):

    msg = path[4:].encode()

    s = socket.socket()
    s.connect((ip, PORT))

    s.send(b"MSG ")
    s.send(len(msg).to_bytes(4, "big"))
    s.send(msg)

    s.close()
    print("💬 Message sent")
    sys.exit()


# =========================
# 📦 SEND FILE MODE
# =========================

def send_chunk(start, data):

    s = socket.socket()
    s.connect((ip, PORT))

    s.send(b"DATA")
    s.send(start.to_bytes(8, "big"))
    s.send(encrypt(data))

    s.close()


size = os.path.getsize(path)

with open(path, "rb") as f:

    offset = 0
    threads = []

    while True:
        chunk = f.read(CHUNK)
        if not chunk:
            break

        t = threading.Thread(
            target=send_chunk,
            args=(offset, chunk)
        )

        t.start()
        threads.append(t)

        offset += len(chunk)

    for t in threads:
        t.join()

print("🚀 Transfer Complete")