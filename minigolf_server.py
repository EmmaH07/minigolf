import socket
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

logging.basicConfig(filename='mini-golf_server.log', level=logging.DEBUG)


def modifier(msg):
    global SHARED_DATA
    SHARED_DATA = msg
    print("i changed to: " + SHARED_DATA)
    logging.debug("i changed the shared data to: " + SHARED_DATA)


def index_modifier():
    global TURN_INDEX
    global WAIT_INDEX
    if TURN_INDEX == 0:
        TURN_INDEX = 1
        WAIT_INDEX = 0
    else:
        TURN_INDEX = 0
        WAIT_INDEX = 1


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
            global FINISH_ROUND1
            global FINISH_ROUND2
            global SHARED_DATA
            global WAIT_INDEX
            global CHANGED
            global SENT

            SENT = False
            CHANGED = False

            if client_socket is sock_list[TURN_INDEX] and not FINISH_ROUND1:
                msg = client_socket.recv(1024).decode()
                if msg == 'FINISH':
                    finish = True
                logging.debug('I recieved: ' + msg)
                if msg != '':
                    modifier(msg)
                end_msg = client_socket.recv(1024).decode()
                logging.debug('I recieved: ' + msg)
                if 'END' in end_msg:
                    FINISH_ROUND1 = True
                    logging.debug('I set finish_round1 to True')
                elif 'FINISH' in end_msg:
                    finish = True

            elif client_socket is sock_list[WAIT_INDEX] and not FINISH_ROUND2:
                if SHARED_DATA != '':
                    print(SHARED_DATA)
                    wait_msg = "wait@" + SHARED_DATA
                    logging.debug('I sent: ' + wait_msg)
                    wait_msg = minigolf_protocol.proto_msg(wait_msg)
                    print("I sent: " + wait_msg)
                    client_socket.send(wait_msg.encode())
                    msg = client_socket.recv(1024).decode()
                    logging.debug('I recieved: ' + msg)
                    if 'END' in msg:
                        FINISH_ROUND2 = True
                        logging.debug('I set finish_round2 to True')
                    elif 'FINISH' in msg:
                        finish = True

            if FINISH_ROUND1 and FINISH_ROUND2:
                if client_socket is sock_list[WAIT_INDEX] and not CHANGED:
                    logging.debug('prev index turn: ' + str(TURN_INDEX))
                    index_modifier()
                    logging.debug('now index turn: ' + str(TURN_INDEX))
                    CHANGED = True
                    logging.debug('I set changed to True')
                    modifier('')
                elif client_socket is sock_list[TURN_INDEX]:
                    while not CHANGED:
                        pass
                FINISH_ROUND1 = False
                FINISH_ROUND2 = False
                logging.debug('I set finish_round1 to False')
                logging.debug('I set finish_round2 to False')
                if client_socket is sock_list[TURN_INDEX] and not SENT:
                    turn_msg = 'turn@'
                    turn_msg = minigolf_protocol.proto_msg(turn_msg)
                    sock_list[TURN_INDEX].send(turn_msg.encode())
                    logging.debug('I sent: ' + turn_msg)
                    SENT = True
                    logging.debug('I set sent to True')
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
