import socket
import threading
import sys

MAX_CLIENTS = 10
registered_clients = {}  # {client_socket: username} ssh mmehrdadi@ecs-coding1.csus.edu


def client_join(client_socket, username):
    #JOIN command.
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
    #Handle QUIT command.
    if client_socket in registered_clients:
        
        print(f"{registered_clients[client_socket]} disconnected")
        del registered_clients[client_socket]
        
    client_socket.close()
    
def client_list(client_socket):
    if client_socket in registered_clients:
        #Joins all the registered_clients values into one string with a space
        if client_socket in registered_clients:
            clients_list = "\n".join([f"{i+1}. {username}" for i, username in enumerate(registered_clients.values())])
            client_socket.sendall(f"\nClient List:\n{clients_list}\nPress Enter to cont...".encode())
            #Sends the list 

def client_bcst(client_socket, message):
    if client_socket in registered_clients:
        username = registered_clients[client_socket] #Gets Sender username
        for socket, _ in registered_clients.items(): #loops though all the values in the dict
            if socket != client_socket: #making sure the username isnt the sender 
                try:
                    socket.sendall(f"From {username}: {message}\nPress Enter to cont...".encode()) #broadcasts the message to them
                except Exception as e:
                    print(f"Error sending broadcast message: {e}\nPress Enter to cont...")

def client_mesg(client_socket, receiver_username , message):
    """
    Handles the MESG command by sending a message from one client to another.
    """
    # Find the recipient's IP address based on their username
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
                #print("LIST")
            elif command == "MESG":
                # handle message EX: client_mesg(client_socket, command_parts[1], command_parts[2])
                command_parts = data.split(" ", 2)
                if len(command_parts) != 3:
                    client_socket.sendall("Invalid MESG command. Usage: MESG <receiver_username> <message>\nEnter command: ".encode())
                else:
                    client_mesg(client_socket, command_parts[1], command_parts[2])
                #print("MESG")
            elif command == "BCST":
                #handle bcst command EX: client_bcst(client_socket, command_parts[1])
                if len(command_parts) != 2:
                    client_socket.sendall("Invalid BCST command. Usage: BCST <message>\n Press Enter to cont...".encode())
                else:
                    client_bcst(client_socket, " ".join(command_parts[1:]))
                #print("BCST")
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
