#-------------------Setup and Configuration-------------------#

import socket
import os

PORT = 3000      # must match server port
BUFFER_SIZE = 4096


def connect_to_server(host, port):
    # create a TCP socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")
        return client_socket
    except ConnectionRefusedError:
        print(f"ERROR: Could not connect to {host}:{port}. Is the server running?")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None


#--------------------------Login Command--------------------------#

def handle_login(client_socket):
    # keep prompting until the server responds with OK
    logged_in = False
    while not logged_in:
        username = input("Enter username to login: ").strip()

        if not username:
            print("Username cannot be empty.")
            continue

        client_socket.send(f"LOGIN {username}".encode())  # format: "LOGIN <username>"

        response = client_socket.recv(1024).decode()

        if response == "OK":
            print(f"Logged in successfully as {username}.")
            logged_in = True
        else:
            print(f"Server: {response}")  # show error (e.g. "ERROR: Invalid user")


#--------------------------MSG Command--------------------------#

def send_message(client_socket, message):
    # send a text message to the server
    client_socket.send(f"MSG {message}".encode())  # format: "MSG <text>"

    response = client_socket.recv(1024).decode()
    print(f"Server: {response}")  # expect "OK: Message received"


#--------------------------FILE Command--------------------------#
 
def send_file(client_socket, filepath):
    # send a file to the server
    # protocol: "FILE <filename> <filesize>" header, wait for OK, then raw bytes
 
    if not os.path.exists(filepath):
        print(f"ERROR: File '{filepath}' not found.")
        return
 
    filename = os.path.basename(filepath)  # strip any leading directory path
    filesize = os.path.getsize(filepath)
 
    # send the FILE header so the server knows the filename and how many bytes are coming
    client_socket.send(f"FILE {filename} {filesize}".encode())
 
    # wait for server to acknowledge the header before sending raw bytes
    ack = client_socket.recv(1024).decode()
    if not ack.startswith("OK"):
        print(f"Server: {ack}")
        return
 
    # stream the file contents in chunks
    bytes_sent = 0
    with open(filepath, "rb") as f:
        while bytes_sent < filesize:
            chunk = f.read(BUFFER_SIZE)
            if not chunk:
                break
            client_socket.sendall(chunk)
            bytes_sent += len(chunk)
 
    # wait for the server to confirm the file was saved
    response = client_socket.recv(1024).decode()
    print(f"Server: {response}")
    print(f"File '{filename}' sent successfully ({bytes_sent} bytes).")


#--------------------------QUIT Command--------------------------#

def send_quit(client_socket):
    # notify the server we are disconnecting, then close the socket
    try:
        client_socket.send("QUIT".encode())
        response = client_socket.recv(1024).decode()
        print(f"Server: {response}")  # expect "OK: Goodbye"
    except Exception:
        pass  # server may have already closed; that's fine
    finally:
        client_socket.close()
        print("Disconnected from server.")


#--------------------------Main Loop--------------------------#

def main():
    # get server address from the user
    host = input("Enter server IP address (or press Enter for localhost): ").strip()
    if not host:
        host = "127.0.0.1"

    client_socket = connect_to_server(host, PORT)
    if not client_socket:
        return

    # login before anything else — server requires this
    handle_login(client_socket)

    # main command loop
    print("\nAvailable commands: MSG <text> | FILE <filepath> | QUIT\n")
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+C or end of piped input — quit gracefully
            print()
            send_quit(client_socket)
            break

        if not user_input:
            continue

        parts = user_input.split(" ", 1)
        command = parts[0].upper()

        if command == "MSG":
            if len(parts) < 2 or not parts[1].strip():
                print("Usage: MSG <your message>")
            else:
                send_message(client_socket, parts[1].strip())

        elif command == "QUIT":
            send_quit(client_socket)
            break

        elif command == "FILE":
            if len(parts) < 2 or not parts[1].strip():
                print("Usage: FILE <filepath>")
            else:
                send_file(client_socket, parts[1].strip())

        else:
            # send unknown command to server so it can respond with its error message
            client_socket.send(user_input.encode())
            response = client_socket.recv(1024).decode()
            print(f"Server: {response}")


if __name__ == "__main__":
    main()