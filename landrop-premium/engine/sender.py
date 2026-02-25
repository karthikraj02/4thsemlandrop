import socket
import os
import sys
import threading
from crypto import encrypt

ip = sys.argv[1]
data_arg = sys.argv[2]

PORT = 5001
CHUNK = 1024 * 512


# 🔗 HANDSHAKE
def handshake(ip):

    name = os.getlogin().encode()

    s = socket.socket()
    s.connect((ip, PORT))

    s.send(b"HELO")
    s.send(len(name).to_bytes(2, "big"))
    s.send(name)

    s.recv(4)
    s.close()

    # ⭐ Send CONNECTED signal
    s = socket.socket()
    s.connect((ip, PORT))

    msg = b"CONNECTED"
    s.send(b"MSG ")
    s.send(len(msg).to_bytes(4, "big"))
    s.send(msg)

    s.close()


# 💬 MESSAGE MODE
if data_arg.startswith("MSG:"):

    handshake(ip)

    msg = data_arg[4:].encode()

    s = socket.socket()
    s.connect((ip, PORT))

    s.send(b"MSG ")
    s.send(len(msg).to_bytes(4, "big"))
    s.send(msg)

    s.close()

    print("💬 Message sent")
    sys.exit()


# 📦 FILE MODE

handshake(ip)


def send_chunk(start, data):

    s = socket.socket()
    s.connect((ip, PORT))

    s.send(b"DATA")
    s.send(start.to_bytes(8, "big"))
    s.send(encrypt(data))

    s.close()


with open(data_arg, "rb") as f:

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

print("🚀 Transfer complete")