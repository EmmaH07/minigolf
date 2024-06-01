import socket
import time
from threading import Thread
import minigolf_protocol

QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 1729
shared_data = ''
turn_index = 0
wait_index = 1
finish_round1 = False
finish_round2 = False
changed = False


def modifier(msg):
    global shared_data
    shared_data = msg
    print("i changed to: " + shared_data)


def index_modifier():
    global turn_index
    global wait_index
    if turn_index == 0:
        turn_index = 1
        wait_index = 0
    else:
        turn_index = 0
        wait_index = 1


def handle_thread(client_socket, client_address, sock_list):
    """
    handle a connection
    :param client_socket: the connection socket
    :param client_address: the remote address
    :return: None
    """
    try:
        print('New connection received from ' + client_address[0] + ':' + str(client_address[1]))
        print("client socket: " + str(client_socket))
        print("turn socket: " + str(sock_list[0]))
        # handle the communication
        while len(sock_list) < 2:
            pass
        time.sleep(1)
        while True:
            global turn_index
            global finish_round1
            global finish_round2
            global shared_data
            global wait_index
            global changed

            if str(client_socket) == str(sock_list[turn_index]) and not finish_round1:
                msg = client_socket.recv(1024).decode()
                print("i got: " + msg)
                if msg != '':
                    if '@' in msg:
                        split_msg = msg.split('@')
                        modifier(split_msg[0])
                        if split_msg[1] == 'END':
                            finish_round1 = True
                            print("round1: " + str(finish_round1))
            elif str(client_socket) == str(sock_list[wait_index]) and not finish_round2:
                if not finish_round2:
                    print("else")
                    print("the shared data is: " + shared_data)
                    if shared_data != '':
                        print(shared_data)
                        wait_msg = "wait@" + shared_data
                        wait_msg = minigolf_protocol.proto_msg(wait_msg)
                        print("I sent: " + wait_msg)
                        client_socket.send(wait_msg.encode())
                        msg = client_socket.recv(1024).decode()
                        if msg == 'END':
                            finish_round2 = True

            if finish_round1 and finish_round2:
                if str(client_socket) == str(sock_list[wait_index]):
                    index_modifier()
                    changed = True
                else:
                    while not changed:
                        pass
                changed = False
                modifier('')
                turn_msg = 'turn@'
                turn_msg = minigolf_protocol.proto_msg(turn_msg)
                sock_list[turn_index].send(turn_msg.encode())
                finish_round1 = False
                finish_round2 = False

    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)
        sock_list = []
        while len(sock_list) < 2:
            client_socket, client_address = server_socket.accept()
            sock_list.append(client_socket)
            thread = Thread(target=handle_thread,
                            args=(client_socket, client_address, sock_list))
            thread.start()
        turn_msg = 'turn@'
        turn_msg = minigolf_protocol.proto_msg(turn_msg)
        sock_list[0].send(turn_msg.encode())

    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
