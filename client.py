#-------------------Setup and Configuration-------------------#

import socket
import os
 
PORT = 3000         # needs to match server port
BUFFER_SIZE = 4096  # bytes to read at a time during file transfer

def connect_to_server(host, port):
        # create a TCP socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")
        return client_socket
    except ConnectionRefusedError:
        print(f"ERROR: Could not connect to {host}:{port}.")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None