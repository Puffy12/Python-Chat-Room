import socket
import sys
import threading

def receive_data(client_socket):
    # Function to continuously receive data from the server in a separate thread.
    while True:
        try:
            data = client_socket.recv(1024).decode()  # Receive data from the server
            if not data:  # Check if the received data is empty
                break
            print(data)  # Print the received data
        except Exception as e:
            print(f"Error receiving data: {e}")  # Print any exceptions that occur during data reception
            break  # Break the loop if an exception was to occur

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <server_port> ")
        return

    name = input("Type your username:")  # Prompt the user to input their username
    server_hostname = "localhost"  # Set the server hostname
    server_port = int(sys.argv[1])  # Get the server port number from the command-line arguments
    username = name.strip()  # Remove any leading or trailing whitespace from the username

    try:
        # Create a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        client_socket.connect((server_hostname, server_port))
        print("Connected to server")

        # Send a JOIN request with the username to the server
        join_message = f"JOIN {username}"
        client_socket.sendall(join_message.encode())

        # Start a thread to continuously receive data from the server
        receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
        receive_thread.start()

        # Handle user input for commands
        while True:
            command = input("Enter command: ").strip()  # Prompt the user to enter a command
            if command.upper() == "QUIT":  # If the user enters 'QUIT', terminate the connection
                client_socket.sendall("QUIT".encode())
                break  # Break the loop to exit the program
            else:
                client_socket.sendall(command.encode())  # Send the user's command to the server

    except Exception as e:
        print(f"Error: {e}")  # Print any exceptions that occur during the execution process
    finally:
        client_socket.close()  # Close the client socket

if __name__ == "__main__":
    main()  # Call the main function when the script has been executed