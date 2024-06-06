import socket
import threading
import time
from threading import Thread
import minigolf_protocol
import logging

QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 1729
SHARED_DATA = ''
TURN_INDEX = 0
WAIT_INDEX = 1
FINISH_ROUND1 = False
FINISH_ROUND2 = False
CHANGED = False
SENT = False
COUNTER = 0

logging.basicConfig(filename='mini-golf_server.log', level=logging.DEBUG)


def count_modifier(sock_list):
    global COUNTER
    global TURN_INDEX
    lock = threading.Lock()
    lock.acquire()
    COUNTER += 1
    if COUNTER == 2:
        index_modifier()
        sock_list[TURN_INDEX].send(minigolf_protocol.proto_msg('turn@').encode())
        COUNTER = 0
    lock.release()


def index_modifier():
    global TURN_INDEX
    global WAIT_INDEX
    if TURN_INDEX == 0:
        TURN_INDEX = 1
        WAIT_INDEX = 0
    else:
        TURN_INDEX = 0
        WAIT_INDEX = 1


def is_directions(msg):
    directions = False
    if msg.count(',') == 2:
        directions = True
    return directions


def handle_thread(client_socket, client_address, sock_list):
    """
    handle a connection
    :param client_socket: the connection socket
    :param client_address: the remote address
    :return: None
    """
    try:
        # handle the communication
        while len(sock_list) < 2:
            pass
        time.sleep(1)
        finish = False
        while not finish:
            global TURN_INDEX
            global WAIT_INDEX

            if client_socket is sock_list[TURN_INDEX]:
                msg = client_socket.recv(1024).decode()
                logging.debug('I recieved: ' + msg)
                if is_directions(msg):
                    directions = minigolf_protocol.get_coordinates_server(msg)
                    print('the directions are: ' + directions)
                    wait_msg = 'wait@' + directions
                    wait_msg = minigolf_protocol.proto_msg(wait_msg)
                    sock_list[WAIT_INDEX].send(wait_msg.encode())
                elif 'FINISH' in msg:
                    finish = True
                elif 'END' in msg:
                    count_modifier(sock_list)

            elif client_socket is sock_list[WAIT_INDEX]:
                msg = client_socket.recv(1024).decode()
                if 'END' in msg:
                    count_modifier(sock_list)

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
        sock_list[TURN_INDEX].send('pink'.encode())
        sock_list[WAIT_INDEX].send('blue'.encode())
        sock_list[TURN_INDEX].send(turn_msg.encode())

    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
