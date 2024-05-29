import socket

IP = '0.0.0.0'
PORT = 1729
QUEUE_SIZE = 1
MAX_PACKET = 1024
SHORT_SIZE = 2
LEN_SIGN = 'H'
ANSWER = 'have a nice day'


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        # endless loop to receive client after client
        while True:
            comm_socket, client_address = server_socket.accept()
            try:
                data = comm_socket.recv(MAX_PACKET).decode()
                print(data)
                while data != 'exit':
                    if data == 'turn':
                        comm_socket.send('turn'.encode())
                    else:
                        comm_socket.send('wait'.encode())
                    data = comm_socket.recv(MAX_PACKET).decode()
                    print(data)
            except socket.error as msg:
                print('client socket disconnected- ' + str(msg))
    except socket.error as msg:
        print('failed to open server socket - ' + str(msg))
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
