import socket
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <server_hostname> <server_port>")
        return

    server_hostname = sys.argv[1]
    server_port = int(sys.argv[2])

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_hostname, server_port))
        print("Connected to server")

        # Ask for the username
        username = input("Enter your username: ")

        # Send JOIN request with username
        join_message = f"JOIN {username}"
        client_socket.sendall(join_message.encode())

        # Receive and handle data from the server
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(data)

            # Handle user input for commands
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
