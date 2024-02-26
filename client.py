import sys
import socket

# start text stuff
if len(sys.argv) != 4:
    sys.stderr.write('ERROR: command needs python3 client.py <HOSTNAME-OR-IP> <PORT> <FILENAME>\n')
    sys.exit(1)

# port and hostname define
hostnameOrIp = sys.argv[1]
port = int(sys.argv[2])
if not (0 <= port <= 70000):
    sys.stderr.write("ERROR: port must be between 0 and 70000\n")
    sys.exit(1)

binFilename = sys.argv[3]

# socket stuff and connect
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostnameOrIp, port))
except socket.error as e:
    sys.stderr.write(f'ERROR: Connection failed: {e}\n')
    sys.exit(1)

# data handling
data = ""
while "\r\n" not in data:
    data += s.recv(1024).decode("utf-8")

if data == "accio\r\n":
    s.send("confirm-accio\r\n".encode())
    data = ""
    while "\r\n" not in data:
        data += s.recv(1024).decode("utf-8")
    if data == "accio\r\n":
        s.send("confirm-accio-again\r\n".encode())

# file stuff
with open(binFilename, 'rb') as file:
    chunk = file.read(10000)
    while chunk:
        s.send(chunk)
        chunk = file.read(10000)

# error handling
s.settimeout(10)
try:
    s.recv(1024)
except socket.timeout:
    sys.stderr.write('ERROR: Connection timed out\n')
    sys.exit(1)
except socket.error as e:
    sys.stderr.write(f'ERROR: Connection failed: {e}\n')
    sys.exit(1)
else:
    sys.stderr.write('Connection established\n')
    sys.exit(0)
