import socket
import threading
import sys

MAX_CLIENTS = 10
registered_clients = {}  # Dictionary to store registered clients {client_socket: username}


def client_join(client_socket, username):
    # Handles JOIN command and checks for maximum clients
    if len(registered_clients) >= MAX_CLIENTS:
        print("Too many users")
        client_socket.sendall("Too Many Users\n Press Enter to retry command\nPress Enter to cont...".encode())
    else:
        if client_socket not in registered_clients:
            registered_clients[client_socket] = username
            print(f"{username} joined")
        else:
            client_socket.sendall("Already registered\n Press Enter to retry command\nPress Enter to cont...".encode())


def client_quit(client_socket):
    # Handles QUIT command
    if client_socket in registered_clients:
        print(f"{registered_clients[client_socket]} disconnected")
        del registered_clients[client_socket]  # Removes user from dictionary
    client_socket.close()


def client_list(client_socket):
    # Makes sure the client is registered and sends the list of clients
    if client_socket in registered_clients:
        clients_list = "\n".join([f"{i+1}. {username}" for i, username in enumerate(registered_clients.values())])
        client_socket.sendall(f"\nClient List:\n{clients_list}\nPress Enter to cont...".encode())


def client_bcst(client_socket, message):
    # Makes sure the client is registered and broadcasts the message to other clients
    if client_socket in registered_clients:
        username = registered_clients[client_socket]
        for socket, _ in registered_clients.items():
            if socket != client_socket:
                try:
                    socket.sendall(f"From {username}: {message}\nPress Enter to cont...".encode())
                except Exception as e:
                    print(f"Error sending broadcast message: {e}\nPress Enter to cont...")


def client_mesg(client_socket, receiver_username, message):
    """
    Handles the MESG command by sending a message from one client to another.
    """
    # Find the recipient's socket based on their username
    recipient_socket = None
    for socket, username in registered_clients.items():
        if username == receiver_username:
            recipient_socket = socket
            break
    
    # If recipient is found, send the message
    if recipient_socket:
        try:
            recipient_socket.sendall(f"From {registered_clients[client_socket]}: {message}\nPress Enter to cont...".encode())
            return
        except Exception as e:
            print(f"Error sending message: {e}")
    else:
        client_socket.sendall(f"User {receiver_username} not found\nPress Enter to cont...".encode())


def handle_client(client_socket):
    # Handle each client connection
    while True:
        try:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            command_parts = data.split(" ", 1)
            command = command_parts[0].upper()
            print("Command received -> " + command)  # Print received command

            if command == "JOIN":
                client_join(client_socket, command_parts[1])
                client_bcst(client_socket, (registered_clients[client_socket] + " Joined\nPress Enter to cont..."))
            elif command == "LIST":
                client_list(client_socket)
            elif command == "MESG":
                command_parts = data.split(" ", 2)
                if len(command_parts) != 3:
                    client_socket.sendall("Invalid MESG command. Usage: MESG <receiver_username> <message>\nEnter command: ".encode())
                else:
                    client_mesg(client_socket, command_parts[1], command_parts[2])
            elif command == "BCST":
                if len(command_parts) != 2:
                    client_socket.sendall("Invalid BCST command. Usage: BCST <message>\n Press Enter to cont...".encode())
                else:
                    client_bcst(client_socket, " ".join(command_parts[1:]))
            elif command == "QUIT":
                client_quit(client_socket)
                break
            else:
                client_socket.sendall("Unknown Message\n Press Enter to retry command\n Press Enter to cont...".encode())
        except Exception as e:
            print(f"Error: {e}")
            break


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <svr_port>")
        return

    # Extract port number from command-line argument
    port = int(sys.argv[1])
    # Create TCP socket and Bind the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(5)
    
    print(f"Server is listening on port {port}")

    while True:
        # Accept incoming client connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        
        # Create a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    main()  # Call the main function when the script is executed