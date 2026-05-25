#-------------------Setup and Configuration-------------------#

import socket
import os

PORT = 3000 # port the server runs on

USERS_FILE = "users.txt" # file containing valid usernames

FILES_DIR = "received_files" # folder to save files sent by client

if not os.path.exists(FILES_DIR): # check if the folder exists

    os.makedirs(FILES_DIR) # create it if it doesn't

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create TCP socket

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow port reuse on restart

server_socket.bind(("", PORT)) # bind to all available network interfaces on our port

server_socket.listen(1) # listen for 1 connection at a time

print(f"Server is running and waiting for a client on port {PORT}...")

client_socket, client_address = server_socket.accept() # wait until a client connects

print(f"Client connected from {client_address[0]}:{client_address[1]}") #Success message 


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
        
        if data.startswith("LOGIN"):
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

handle_login(client_socket) # run login as soon as a client connects