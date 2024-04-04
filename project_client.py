import socket
import sys

def send_command(server_socket, command):
    try:
        server_socket.send(command.encode())
        response = server_socket.recv(1024).decode()
        print(response)
    except Exception as e:
        print(f"Error sending command: {e}")

def main():
        #This handles the clients args
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <svr_port>")
        return
    
    server_host = "localhost"  # Change to your server's hostname or IP address
    server_port = int(sys.argv[1])
    username = input("Enter your username: ")
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((server_host, server_port))
        print("Connected to server.")
        
        # Send JOIN command
        join_command = f"JOIN {username}"
        send_command(server_socket, join_command)

        while True:
            print("[Commands include LIST, MESG, BCST, QUIT]")
            command = input("Enter command: ")

            if command == "QUIT":
                send_command(server_socket, command)
                break

            send_command(server_socket, command)

        server_socket.close()
        print("Connection closed.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
