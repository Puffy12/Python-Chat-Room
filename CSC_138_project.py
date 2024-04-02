import socket
import threading
import sys

MAX_CLIENTS = 10
clients = {}  # Dictionary to store client connections and usernames


def client_commands(client_socket, address):

    # Thread function to handle each client connection.

    print(f"Connected with {address}")

    while True:
        try:
            # Receive data from client
            data = client_socket.recv(1024).decode()

            if not data:
                break  # If no data received, close connection

            command = data.split()
            #List of commands that the server accepts
            if command[0] == "JOIN":
                client_join(client_socket, command[1])
                print("JOIN")
            elif command[0] == "LIST":
                #handle list command
                print("LIST")
            elif command[0] == "MESG":
                #handle message 
                print("MESG")
            elif command[0] == "BCST":
                #handle bcst command
                print("BCST")
            elif command[0] == "QUIT":
                client_quit(client_socket)
                print("QUIT")
            else:
                Temp = "Unknown Message".encode()
                client_socket.send(Temp)
        except Exception as e:
            print(f"Error: {e}")
            break

    # Close client connection
    client_socket.close()
    print(f"Connection with {address} closed")


def client_join(client_socket, username):
    Temp = ""
    # When a user joins the server.
    if len(clients) >= MAX_CLIENTS:
        Temp = "Too Many Users".encode()
        client_socket.send(Temp)
    elif username in clients.values():
        Temp = "Username Already Exists".encode()
        client_socket.send(Temp)
    else:
        clients[client_socket] = username  #this is what saves the usernames into the dictionary with the user socket as the key and the username as the value
        Temp = "Joined Successfully".encode()
        client_socket.send(Temp)


def client_quit(client_socket):
    Temp = ""
    # This will QUIT the application.
    if client_socket in clients:
        del clients[client_socket] #Removes client from the client dictionary
    Temp = "Disconnected Successfully".encode()
    client_socket.send(Temp)


def main():
    #This handles the clients args
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <svr_port>")
        return
    port = int(sys.argv[1])

    # Set up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)

    print(f"Server listening on port {port}...")

    # Accept incoming client connections
    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=client_commands, args=(client_socket, addr))  #creates a threat for the client process
        client_thread.start()


if __name__ == "__main__":
    main()
