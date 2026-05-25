import socket
import os

PORT = 5000 # port the server runs on

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

