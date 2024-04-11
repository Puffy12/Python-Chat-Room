# Chat Application

This is a simple chat application implemented in Python using TCP sockets. It consists of a client program (`client.py`) and a server program (`server.py`) that allow users to communicate with each other in a chat room.

## Installation

1. Clone this repository to your local machine:

```
git clone https://github.com/Puffy12/138-Socket-Project
```

2. Navigate to the cloned directory:

```
cd 138-Socket-Project
```

## Usage

### Server

To start the server, run the `project_server.py` script with the desired port number as the command-line argument:

```
python3 project_server.py <svr_port>
```

For example:

```
python3 project_server.py 1234
```

The server will then start listening for incoming client connections on the specified port.

### Client

To start the client, run the `project_client.py` script with the server hostname, server port, and your desired username as it asks you:

```
python3 project_client.py <server_hostname> <server_port> 
```

For example:

```
python3 project_client.py localhost 1234 
```

Replace `<server_hostname>` with the hostname of the server (e.g., `localhost` if running locally) and `<server_port>` with the port number on which the server is listening.

Once the client is running, you can enter commands to join the chat room, send messages, list connected users, and quit.

## Commands

The following commands are supported by the client:

- `JOIN username`: Join the chat room with the specified username.
- `LIST`: List all users currently connected to the chat room.
- `MESG username message`: Send a message to a specific user.
- `BCST message`: Broadcast a message to all users in the chat room.
- `QUIT`: Disconnect from the chat room and exit the client.

