import socket
import sys
import threading

def receive_data(client_socket):
    #Thread function to continuously receive data from the server.
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(data)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 client.py <server_hostname> <server_port> <username>")
        return

    server_hostname = sys.argv[1]
    server_port = int(sys.argv[2])
    username = sys.argv[3]

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_hostname, server_port))
        print("Connected to server")

        # Send JOIN request with username
        join_message = f"JOIN {username}"
        client_socket.sendall(join_message.encode())

        # Start a thread to continuously receive data from the server
        receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
        receive_thread.start()

        # Handle user input for commands
        while True:
            command = input("Enter command: ").strip()
            if command.upper() == "QUIT":
                client_socket.sendall("QUIT".encode())
                break
            else:
                client_socket.sendall(command.encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
