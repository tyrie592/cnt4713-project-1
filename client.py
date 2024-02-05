import sys
import socket

if len(sys.argv) != 4:
    print('Usage: python3 client.py <HOSTNAME-OR-IP> <PORT> <FILENAME>')
    sys.exit()

hostnameOrIp = sys.argv[1]
port = int(sys.argv[2])
binFilename = sys.argv[3]


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostnameOrIp, port))
except socket.error as e:
    print('Connection failed: {}'.format(e))
    sys.exit()

data = ""
while "\r\n" not in data:
    data += s.recv(1).decode("utf-8")

if data == "accio\r\n":
    s.send("confirm-accio\r\n".encode())
    data = ""
    while "\r\n" not in data:
        data += s.recv(1).decode("utf-8")
    if data == "accio\r\n":
        s.send("confirm-accio-again\r\n".encode())

with open(binFilename, 'rb') as file:
    chunk = file.read(10000)
    while chunk:
        s.send(chunk)
        chunk = file.read(10000)

s.settimeout(10)
try:
    s.recv(1024)
except socket.timeout:
    print('Connection timed out')
    s.close()
except socket.error as e:
    print('Connection failed: {}'.format(e))
    s.close()
else:
    print('Connection established')
    s.close()
