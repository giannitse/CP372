#-------------------Setup and Configuration-------------------#

import socket
import os

PORT = 3000 # port the server runs on
BUFFER_SIZE = 4096
USERS_FILE = "users.txt" # file containing valid usernames
FILES_DIR = "received_files" # folder to save files sent by client

if not os.path.exists(FILES_DIR): # check if the folder exists

    os.makedirs(FILES_DIR) # create it if it doesn't
    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create TCP socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow port reuse on restart
server_socket.bind(("", PORT)) # bind to all available network interfaces on our port  
  
# Function to return server to default waiting state (No clients)
def server_listen():
    
    server_socket.listen(1) # listen for 1 connection at a time

    print(f"Server is running and waiting for a client on port {PORT}...")

    cli_socket, cli_address = server_socket.accept() # wait until a client connects

    print(f"Client connected from {cli_address[0]}:{cli_address[1]}") #Success message 
    
    return cli_socket, cli_address


#-------------------------Login Command-------------------------#

def load_users(): 
    # read users.txt and return a list of valid usernames
    with open(USERS_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def handle_login(client_socket):
    # keep prompting until the client logs in successfully
    logged_in = False
    while not logged_in:
        data = client_socket.recv(1024).decode()

        if data.startswith("LOGIN"): #The login command should be in the format "LOGIN username"

            username = data.split(" ", 1)[1].strip() # extract username after "LOGIN "

            valid_users = load_users()

            if username in valid_users: # check if the username is valid
                client_socket.send("OK".encode())
                print(f"{username} logged in successfully")
                logged_in = True
            else:
                client_socket.send("ERROR: Invalid user".encode())
                print(f"Failed login attempt: {username}")
        else:
            # client tried to do something before logging in
            client_socket.send("ERROR: Please login first".encode())



#--------------------------File Command--------------------------#
 
def handle_file(client_socket, header):
    # header format: "FILE <filename> <filesize>"
    # parse the filename and expected byte count from the header
    try:
        parts = header.split(" ", 2)          # ["FILE", "<filename>", "<filesize>"]
        filename = parts[1].strip()
        filesize = int(parts[2].strip())
    except (IndexError, ValueError):
        client_socket.send("ERROR: Invalid FILE header. Expected: FILE <filename> <filesize>".encode())
        print("Invalid FILE header received")
        return
 
    # acknowledge the header so the client starts sending raw bytes
    client_socket.send("OK: Ready to receive file".encode())
    print(f"Receiving file '{filename}' ({filesize} bytes)...")
 
    # receive the file contents in chunks until we have all expected bytes
    save_path = os.path.join(FILES_DIR, filename)
    bytes_received = 0
    try:
        with open(save_path, "wb") as f:
            while bytes_received < filesize:
                chunk = client_socket.recv(min(BUFFER_SIZE, filesize - bytes_received))
                if not chunk:
                    break  # connection dropped mid-transfer
                f.write(chunk)
                bytes_received += len(chunk)
    except Exception as e:
        client_socket.send(f"ERROR: Could not save file: {e}".encode())
        print(f"Error saving file: {e}")
        return
 
    if bytes_received == filesize:
        client_socket.send(f"OK: File '{filename}' received and saved ({bytes_received} bytes)".encode())
        print(f"File received successfully: {save_path}")
    else:
        # transfer was cut short
        client_socket.send(f"ERROR: Incomplete transfer. Expected {filesize} bytes, got {bytes_received}".encode())
        print(f"Incomplete file transfer for '{filename}'")


#--------------------------QUIT,Error Handling & MSG Commands--------------------------#

def handle_quit(client_socket):
    # tell the client the connection is closing then close it
    client_socket.send("OK: Goodbye".encode())
    print("Client disconnected.")
    client_socket.close()

def handle_commands(client_socket):
    # main loop that keeps listening for commands after login
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                # client disconnected unexpectedly
                print("Client disconnected")
                break

            if data.startswith("MSG"):
                # extract the message text after "MSG "
                message = data.split(" ", 1)[1].strip()
                print(f"Message received: {message}")
                client_socket.send("OK: Message received".encode())

            elif data.startswith("QUIT"):
                # client wants to disconnect gracefully
                handle_quit(client_socket)
                break

            elif data.startswith("FILE"):
                # hand off to file handler — passes full header line
                handle_file(client_socket, data)

            else:
                # client sent something we don't recognize
                client_socket.send("ERROR: Unknown command".encode())
                print(f"Unknown command received: {data}")

        except Exception as e:
            # something went wrong, close the connection
            print(f"Error: {e}")
            client_socket.close()
            break
        
def main():
    
    while True:
        
        client_socket, client_address = server_listen()

        handle_login(client_socket) # run login as soon as a client connects

        handle_commands(client_socket) # start listening for commands after login

main()
        


