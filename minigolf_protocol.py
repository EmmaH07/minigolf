def proto_msg(msg):
    new_msg = str(len(msg)) + "@" + msg
    return new_msg


def all_msg_recv(msg):
    new_msg = msg.split('@')
    return int(new_msg[0]) == len(new_msg[1])


def check_turn(msg):
    turn = False
    if msg.count('@') == 2:
        split_msg = msg.split('@')
        if split_msg[1] == 'turn':
            turn = True

    return turn


def check_wait(msg):
    wait = False
    if msg.count('@') == 2:
        split_msg = msg.split('@')
        if split_msg[1] == 'wait':
            wait = True

    return wait


def get_coordinates(msg):
    coordinates = '0, 0, 0'
    if msg.count('@') == 2:
        split_msg = msg.split('@')
        if split_msg[2] != '':
            coordinates = split_msg[2]

    return coordinates
