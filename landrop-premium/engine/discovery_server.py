import socket, getpass

PORT = 5002
name = getpass.getuser()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

while True:
    data, addr = sock.recvfrom(1024)

    if data == b"GOD_DISCOVER":
        sock.sendto(name.encode(), addr)