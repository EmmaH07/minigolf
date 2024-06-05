import socket
import time
from threading import Thread
import minigolf_protocol
import logging

QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 1729
shared_data = ''
turn_index = 0
wait_index = 1
finish_round1 = False
finish_round2 = False
changed = False
sent = False

logging.basicConfig(filename='minigolf_server.log', level=logging.DEBUG)


def modifier(msg):
    global shared_data
    shared_data = msg
    print("i changed to: " + shared_data)
    logging.debug("i changed the shared data to: " + shared_data)


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
        # handle the communication
        while len(sock_list) < 2:
            pass
        time.sleep(1)
        finish = False
        while not finish:
            global turn_index
            global finish_round1
            global finish_round2
            global shared_data
            global wait_index
            global changed
            global sent

            sent = False
            changed = False

            if str(client_socket) == str(sock_list[turn_index]) and not finish_round1:
                msg = client_socket.recv(1024).decode()
                if msg == 'FINISH':
                    finish = True
                logging.debug('I recieved: ' + msg)
                if msg != '':
                    modifier(msg)
                end_msg = client_socket.recv(1024).decode()
                logging.debug('I recieved: ' + msg)
                if 'END' in end_msg:
                    finish_round1 = True
                    logging.debug('I set finish_round1 to True')
                elif 'FINISH' in end_msg:
                    finish = True

            elif str(client_socket) == str(sock_list[wait_index]) and not finish_round2:
                if shared_data != '':
                    print(shared_data)
                    wait_msg = "wait@" + shared_data
                    logging.debug('I sent: ' + wait_msg)
                    wait_msg = minigolf_protocol.proto_msg(wait_msg)
                    print("I sent: " + wait_msg)
                    client_socket.send(wait_msg.encode())
                    msg = client_socket.recv(1024).decode()
                    logging.debug('I recieved: ' + msg)
                    if 'END' in msg:
                        finish_round2 = True
                        logging.debug('I set finish_round2 to True')
                    elif 'FINISH' in msg:
                        finish = True

            if finish_round1 and finish_round2:
                if str(client_socket) == str(sock_list[wait_index]) and not changed:
                    logging.debug('prev index turn: ' + str(turn_index))
                    index_modifier()
                    logging.debug('now index turn: ' + str(turn_index))
                    changed = True
                    logging.debug('I set changed to True')
                    modifier('')
                elif str(client_socket) == str(sock_list[turn_index]):
                    while not changed:
                        pass
                finish_round1 = False
                finish_round2 = False
                logging.debug('I set finish_round1 to False')
                logging.debug('I set finish_round2 to False')
                if str(client_socket) == str(sock_list[turn_index]) and not sent:
                    turn_msg = 'turn@'
                    turn_msg = minigolf_protocol.proto_msg(turn_msg)
                    sock_list[turn_index].send(turn_msg.encode())
                    logging.debug('I sent: ' + turn_msg)
                    sent = True
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
        sock_list[0].send('pink'.encode())
        sock_list[1].send('blue'.encode())
        sock_list[0].send(turn_msg.encode())

    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
