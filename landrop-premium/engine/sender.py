import socket, os, sys, threading
from crypto import encrypt

ip = sys.argv[1]
path = sys.argv[2]

PORT = 5001
CHUNK = 1024 * 512  # 512 KB chunks

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

    while chunk := f.read(CHUNK):
        t = threading.Thread(target=send_chunk,
                             args=(offset, chunk))
        t.start()
        threads.append(t)
        offset += len(chunk)

    for t in threads:
        t.join()

print("🚀 Transfer Complete")