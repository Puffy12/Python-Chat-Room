import socket
import threading
import sys

MAX_CLIENTS = 10
registered_clients = {}  # {client_socket: username}


def client_join(client_socket, username):
    #JOIN command.
    if len(registered_clients) >= MAX_CLIENTS:
        print("Too many users")
        client_socket.sendall("Too Many Users\n Press Enter to retry command\n Enter command: ".encode())
    else:
        if client_socket not in registered_clients:
            registered_clients[client_socket] = username
            print(f"{username} joined")
        else:
            client_socket.sendall("Already registered\n Press Enter to retry command\n Enter command: ".encode())


def client_quit(client_socket):
    #Handle QUIT command.
    if client_socket in registered_clients:
        
        print(f"{registered_clients[client_socket]} disconnected")
        del registered_clients[client_socket]
        
    client_socket.close()
    
def client_list(client_socket):
    if client_socket in registered_clients:
        #Joins all the registered_clients values into one string with a space
        clients_list = "\n".join(registered_clients.values()) 
        #Sends the list 
        client_socket.sendall(f"{clients_list}\n".encode())

def handle_client(client_socket):
    #Handle each client connection.
    while True:
        try:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            command_parts = data.split(" ", 1)
            command = command_parts[0].upper()
            #This is where you add commands 
            print("Command recieved -> " + command)
            if command == "JOIN":
                client_join(client_socket, command_parts[1])
            elif command == "LIST":
                #handle list EX: command client_list(client_socket)
                client_list(client_socket)
                print("LIST")
            elif command == "MESG":
                #handle message EX: client_mesg(client_socket, command_parts[1])
                print("MESG")
            elif command == "BCST":
                #handle bcst command EX: client_bcst(client_socket, command_parts[1])
                print("BCST")
            elif command == "QUIT":
                client_quit(client_socket)
                break
            else:
                client_socket.sendall("Unknown Message\n Press Enter to retry command\n Enter command: ".encode())
        except Exception as e:
            print(f"Error: {e}")
            break


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <svr_port>")
        return

    port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(5)
    print(f"Server is listening on port {port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    main()
