import socket
import threading
import sys
import ssl
import logging

MAX_CLIENTS = 10
registered_clients = {}  # {client_socket: (username, password)}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def client_join(client_socket, username, password):
    # JOIN command.
    if len(registered_clients) >= MAX_CLIENTS:
        logger.warning("Too many users")
        client_socket.sendall("Too Many Users\n".encode())
    else:
        if client_socket not in registered_clients and username not in [user[0] for user in registered_clients.values()]:
            registered_clients[client_socket] = (username, password)
            logger.info(f"{username} joined")
            client_socket.sendall("Welcome to the chat!\n".encode())
        else:
            client_socket.sendall("Username already registered or already logged in\n".encode())

def client_quit(client_socket):
    # Handle QUIT command.
    if client_socket in registered_clients:
        username = registered_clients[client_socket][0]
        logger.info(f"{username} disconnected")
        del registered_clients[client_socket]
    client_socket.close()

def client_list(client_socket):
    if client_socket in registered_clients:
        clients_list = "\n".join([user[0] for user in registered_clients.values()])
        client_socket.sendall(f"Connected users:\n{clients_list}\n".encode())

def client_bcst(client_socket, message):
    if client_socket in registered_clients:
        username = registered_clients[client_socket][0]
        for socket, _ in registered_clients.items():
            if socket != client_socket:
                try:
                    socket.sendall(f"From {username}: {message}\n".encode())
                except Exception as e:
                    logger.error(f"Error sending broadcast message: {e}")

def handle_client(client_socket):
    # Handle each client connection.
    while True:
        try:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            command_parts = data.split(" ")
            command = command_parts[0].upper()

            if command == "JOIN":
                if len(command_parts) != 3:
                    client_socket.sendall("Invalid JOIN command. Usage: JOIN <username> <password>\n".encode())
                else:
                    client_join(client_socket, command_parts[1], command_parts[2])
            elif command == "LIST":
                client_list(client_socket)
            elif command == "MESG":
                # Implement message handling
                pass
            elif command == "BCST":
                if len(command_parts) < 2:
                    client_socket.sendall("Invalid BCST command. Usage: BCST <message>\n".encode())
                else:
                    client_bcst(client_socket, " ".join(command_parts[1:]))
            elif command == "QUIT":
                client_quit(client_socket)
                break
            else:
                client_socket.sendall("Unknown Command\n".encode())
        except Exception as e:
            logger.error(f"Error: {e}")
            break

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <svr_port>")
        return

    port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(5)
    logger.info(f"Server is listening on port {port}")

    # Wrap the server socket with SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    ssl_server_socket = context.wrap_socket(server_socket, server_side=True)

    while True:
        client_socket, client_address = ssl_server_socket.accept()
        logger.info(f"Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
