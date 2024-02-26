import socket
import threading
import sys
import os
import signal

# whole file connection counter
connection_counter = 0
lock = threading.Lock()

# Function for client connection
def handle_client(client_socket, connection_id, save_dir):
    try:
        # thingy for storing incoming data
        data = b""
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        data = b"ERROR"

    # Save the data to a file
    file_path = os.path.join(save_dir, f"{connection_id}.file")
    with open(file_path, 'wb') as f:
        f.write(data)

    client_socket.close()

def main():
    if len(sys.argv) != 3:
        sys.stderr.write("ERROR: Invalid arguments\n")
        sys.exit(1)

    port = int(sys.argv[1])
    save_dir = sys.argv[2]

    # make socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket
    try:
        server_socket.bind(("0.0.0.0", port))
    except:
        sys.stderr.write("ERROR: Unable to bind to port\n")
        sys.exit(1)

    # socket wait for client
    server_socket.listen(10)

    # Graceful and elegant exit
    def exit_explode_violently(signum, frame):
        sys.exit(0)
    signal.signal(signal.SIGQUIT, exit_explode_violently)
    signal.signal(signal.SIGTERM, exit_explode_violently)
    signal.signal(signal.SIGINT, exit_explode_violently)
    # I'm so funny I know

    global connection_counter

    while True:
        (client_socket, address) = server_socket.accept()
        client_socket.settimeout(10)  # timeout after 10 segundo

        with lock:
            connection_counter += 1
            connection_id = connection_counter

        # make thread for all good connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, connection_id, save_dir))
        client_thread.start()
