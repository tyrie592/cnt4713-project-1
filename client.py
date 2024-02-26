import sys
import socket
# start text stuff
if len(sys.argv) != 4:
    sys.stderr.write('ERROR: command needs python3 client.py <HOSTNAME-OR-IP> <PORT> <FILENAME>\n')
    sys.exit(1)

# port and hostname define
hostnameOrIp = sys.argv[1]
port = int(sys.argv[2])
if port < 0 or port > 70000:
    sys.stderr.write("ERROR: port myst be between 0 and 70000\n")
    sys.exit(1)

binFilename = sys.argv[3]

# I give up I'm taking a different approach
#biiiiig while loop

#make socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.settimeout(10)
    try:
        #socket connect
        sock.connect((hostnameOrIp, port))
        print("connection successful\n")
        msg = b""

        #check for correct message
        while b'\r\n' not in msg
            info = sock.recv(1)
            msg += info
        print("data recieved\n")
        
        #make sure is correct
        if msg == b'accio\r\n':
            sock.send(b'confirm-accio\r\n')
            print("sent\n")
            msg =b''
            while b'\r\n' not in msg:
                info = sock.recv(1)
                msg += info
            print("recived\n")
            if msg == b'accio\r\n':
                sock.send(b'confirm-accio-again\r\n\r\n')
                print("sent\n")

                #open file and send back to server
                with open(binFilename, 'rb') as file:
                    content = file.read()
                    print("file read\n")
                    while content:
                            bytes = sock.send(content)
                            print("file sent\n")
                            content = file.read()
                file.close()
            #error handling(hopefully right)
            else:
                sys.stderr.write("ERROR: Incorrect server data\n")
                sys.exit(1)
        else:
            print("Incorrect server data\n")
            sys.exit(1)
    #more error handling
    except socket.timeout as e:
        sys.stderr.write("ERROR: Connection Timeout\n")
        sys.exit(1)
    except sock.error as e:
        sys.stderr.write("ERROR: %s\n" % str(e))
        sys.exit(1)
    pass
pass

#socket closed
sys.exit(0)
