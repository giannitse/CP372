# CP372 - Assignment 1

This project implements a TCP-based client-server application using Python's Socket API. The system allows a client to connect to a server, authenticate using a username, exchange text messages, transfer files, and disconnect gracefully.

The application uses a custom text-based application-layer protocol designed specifically for this assignment.
# Overview

The system consists of:

- A TCP server (`server.py`)
- A TCP client (`client.py`)

The client must authenticate using a valid username before performing any other operations. Once logged in, the client can:

- Send text messages
- Transfer files to the server
- Disconnect gracefully

The application uses a custom text-based application-layer protocol built on top of TCP.

# Getting Started

## Requirements

### Software

- Python 3.x
### Libraries Used

The following standard Python libraries are used:

- socket
- os

No external packages are required.
## Executing the program

### Create users.txt

Create a file named `users.txt` in the project directory.

Example:

```
Alice
Bob
Charlie
```

**Only usernames listed in this file can log in successfully**.

---
### Running the Server

Start the server:
```
python server.py
```

The server listens on:
```
Port: 3000
```

You should see:
```
Server is running and waiting for a client on port 3000...
```

When a client connects:
```
Client connected from 127.0.0.1:54321
```

---
### Running the Client

Open a second terminal and enter:
```
python client.py
```

Enter the server IP address when prompted:
```
Enter server IP address (or press Enter for localhost):
```

You should see:
```
Connected to server at 127.0.0.1:3000
```

---
## Project Structure

```
project/
│
├── client.py
├── server.py
├── users.txt
├── received_files/
│
└── README.md
```

### File Descriptions

|File|Purpose|
|---|---|
|server.py|TCP server implementation|
|client.py|TCP client implementation|
|users.txt|List of valid usernames|
|received_files/|Stores files uploaded by clients|
|README.md|Project documentation|

## Commands

### LOGIN

Authenticates a user.
#### Client

```
LOGIN <username>
```
#### Server Responses

Success:
```
OK
```

Failure:
```
ERROR: Invalid user
```
or
```
ERROR: Please login first
```

---
### MSG

Sends a text message to the server.

#### Client

```
MSG <message>
```

#### Server Response

```
OK: Message received
```

#### Server Console

```
Message received: <message>
```

---

### FILE

Transfers a file from the client to the server.

#### Command Format

```
FILE <filename> <filesize>
```

Example:
```
FILE report.pdf 12564
```

#### File Transfer Procedure

1. Client sends FILE command.
2. Server validates the command.
3. Server replies:

```
OK: Ready to receive file
```

4. Client sends raw file bytes.
5. Server saves the file.
6. Server sends confirmation.

Successful transfer:
```
OK: File 'report.pdf' received and saved (12564 bytes)
```

Files are stored in:
```
received_files/
```

---
### QUIT

Terminates the connection gracefully.

#### Client

```
QUIT
```

#### Server Response

```
OK: Goodbye
```

#### Client Output

```
Disconnected from server.
```

---
## Authors

Group Members:

- Gregory Lui - luix5601@mylaurier.ca
- Gianni Tse - gtse4760@mylaurier.ca
- Robert Glennie - glen7639@mylaurier.ca
- Mohib Abbas - abba9980@mylaurier.ca
- Philip Marian - mari8670@mylaurier.ca


## Version History

- 1.0
    - Reviewed and packaged for submission into a single ZIP archive
- 0.4
    - Found a bug where the server terminated when the client dissconected
        - Fixed the bug
- 0.3
    - File sharing functionality added
        - Added command FILE to server.py
        - Added handle_file() to server.py
        - Added send_file() to client.py
    - Found and fixed some bugs with communication
- 0.2
    - client.py created
    - In client.py:
        - Added connect_to_server()
        - Added handle_login()
        - Added send_message()
        - Added send_quit()
    - Tested connection to server.py
- 0.1
    - server.py created
    - users.txt created
    - In server.py:
        - Added load_users()
        - Added handle_login()
        - Added handle_quit()
        - Added handle_commands()
            -  Added commands: MSG, QUIT
    - Used Netcat to test command functionality

## Academic Integrity

This project was developed as part of CP372 – Computer Networks. All code was written by the group members in accordance with the course academic integrity policy.
