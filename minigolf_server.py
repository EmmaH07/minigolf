import socket
import select

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 1729        # Port to listen on

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

# List of sockets for select()
inputs = [server_socket]
outputs = []

# Dictionary to store messages for each client
clients = {}

while True:
    # Wait for at least one socket to be ready for reading or writing
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # Handle new connections
    for s in readable:
        if s is server_socket:
            connection, address = server_socket.accept()
            print('Client connected:', address)
            inputs.append(connection)
            clients[connection] = ''  # Add new client with empty message
        else:
            # Handle incoming messages from clients
            try:
                data = s.recv(1024)
                if data == "turn":
                    # Add message to client dictionary
                    clients[s] += data.decode("utf-8")
                else:
                    # Client disconnected
                    print('Client disconnected:', s.getpeername())
                    inputs.remove(s)
                    del clients[s]
            except socket.error as e:
                print('Socket error:', s.getpeername(), e)
                inputs.remove(s)
                del clients[s]

    # Handle sending messages to clients
    if writable:
        for ws in writable:
            # Send message to client if available
            if ws in clients and clients[ws]:
                message = clients[ws]
                ws.sendall(message.encode("utf-8"))
                clients[ws] = ''  # Clear message after sending