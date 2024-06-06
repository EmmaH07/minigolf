import math
import socket
import pygame
import select
import minigolf_protocol

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 800
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BROWN = (153, 76, 0)
GREEN_BLUE = (54, 126, 127)
BACKGROUND_COLOR = (0, 170, 0)
OBSTACLE_LEN = 10
START_SCREEN = 'start_background.png'
EMPTY_BACK = 'grass.png'
WIN1_BACK = 'win1.png'
LOSE1_BACK = 'lose1.png'
PLAYER1 = 'ball1.png'
PLAYER2 = 'ball2.png'
FLAG = 'flag.png'
SAND = 'sand.png'
LAKE = 'lake.png'
PINK_BUSH = 'pink_bush.png'
WHITE_BUSH = 'white_bush.png'
YELLOW_BUSH = 'yellow_bush.png'
RED_BUSH = 'red_bush.png'
ORANGE_BUSH = 'orange_bush.png'
MAP1_DICT = {
    "flag": (150, 100), "lake": (950, 100), "white_bush": (350, 50), "pink_bush": (100, 300),
    "sand": (400, 400), "yellow_bush": (690, 100), "red_bush": (950, 550), "orange_bush": (50, 600),
    "hole_center": (173, 180), "hole_radius": 30, "lake_center": (1125, 275), "lake_radius": 175,
    "sand_center": (504, 504), "sand_radius": 104, "white_bush_size": (48, 170), "pink_bush_size": (170, 40),
    "yellow_bush_size": (108, 57), "red_bush_size": (106, 59), "orange_bush_size": (105, 60)
}
MAX_SPEED = 100
MIN_SPEED = 0
START_X_POS1 = 695
START_Y_POS1 = 700
START_X_POS2 = 600
START_Y_POS2 = 700
IP = '127.0.0.1'
PORT = 1729


def distance_from_hole(x, y):
    center = MAP1_DICT["hole_center"]
    num1 = x - center[0]
    num1 = num1 ** 2
    num2 = y - center[1]
    num2 = num2 ** 2
    new_num = num1 + num2
    return math.sqrt(new_num)


def distance_from_lake(x, y):
    center = MAP1_DICT["lake_center"]
    num1 = x - center[0]
    num1 = num1 ** 2
    num2 = y - center[1]
    num2 = num2 ** 2
    new_num = num1 + num2
    return math.sqrt(new_num)


def distance_from_sand(x, y):
    center = MAP1_DICT["sand_center"]
    num1 = x - center[0]
    num1 = num1 ** 2
    num2 = y - center[1]
    num2 = num2 ** 2
    new_num = num1 + num2
    return math.sqrt(new_num)


def is_in_sand(x, y):
    if distance_from_sand(x, y) <= MAP1_DICT["sand_radius"]:
        return True
    else:
        return False


def is_in_lake(x, y):
    if distance_from_lake(x, y) <= MAP1_DICT["lake_radius"]:
        return True
    else:
        return False


def is_win(x, y):
    if distance_from_hole(x, y) <= MAP1_DICT["hole_radius"]:
        return True
    else:
        return False


def touched_white_bush(x, y):
    if (MAP1_DICT["white_bush"][0] <= x <= MAP1_DICT["white_bush"][0] + MAP1_DICT["white_bush_size"][0] and
            MAP1_DICT["white_bush"][1] <= y <= MAP1_DICT["white_bush"][1] + MAP1_DICT["white_bush_size"][1]):
        return True
    if (MAP1_DICT["white_bush"][0] <= x + 50 <= MAP1_DICT["white_bush"][0] + MAP1_DICT["white_bush_size"][0] and
            MAP1_DICT["white_bush"][1] <= y <= MAP1_DICT["white_bush"][1] + MAP1_DICT["white_bush_size"][1]):
        return True
    if (MAP1_DICT["white_bush"][0] <= x + 50 <= MAP1_DICT["white_bush"][0] + MAP1_DICT["white_bush_size"][0] and
            MAP1_DICT["white_bush"][1] <= y + 50 <= MAP1_DICT["white_bush"][1] + MAP1_DICT["white_bush_size"][1]):
        return True
    if (MAP1_DICT["white_bush"][0] <= x <= MAP1_DICT["white_bush"][0] + MAP1_DICT["white_bush_size"][0] and
            MAP1_DICT["white_bush"][1] <= y + 50 <= MAP1_DICT["white_bush"][1] + MAP1_DICT["white_bush_size"][1]):
        return True
    else:
        return False


def touched_red_bush(x, y):
    if (MAP1_DICT["red_bush"][0] <= x <= MAP1_DICT["red_bush"][0] + MAP1_DICT["red_bush_size"][0] and
            MAP1_DICT["red_bush"][1] <= y <= MAP1_DICT["red_bush"][1] + MAP1_DICT["red_bush_size"][1]):
        return True
    if (MAP1_DICT["red_bush"][0] <= x + 50 <= MAP1_DICT["red_bush"][0] + MAP1_DICT["red_bush_size"][0] and
            MAP1_DICT["red_bush"][1] <= y <= MAP1_DICT["red_bush"][1] + MAP1_DICT["red_bush_size"][1]):
        return True
    if (MAP1_DICT["red_bush"][0] <= x + 50 <= MAP1_DICT["red_bush"][0] + MAP1_DICT["red_bush_size"][0] and
            MAP1_DICT["red_bush"][1] <= y + 50 <= MAP1_DICT["red_bush"][1] + MAP1_DICT["red_bush_size"][1]):
        return True
    if (MAP1_DICT["red_bush"][0] <= x <= MAP1_DICT["red_bush"][0] + MAP1_DICT["red_bush_size"][0] and
            MAP1_DICT["red_bush"][1] <= y + 50 <= MAP1_DICT["red_bush"][1] + MAP1_DICT["red_bush_size"][1]):
        return True
    else:
        return False


def touched_pink_bush(x, y):
    if (MAP1_DICT["pink_bush"][0] <= x <= MAP1_DICT["pink_bush"][0] + MAP1_DICT["pink_bush_size"][0] and
            MAP1_DICT["pink_bush"][1] <= y <= MAP1_DICT["pink_bush"][1] + MAP1_DICT["pink_bush_size"][1]):
        return True
    if (MAP1_DICT["pink_bush"][0] <= x + 50 <= MAP1_DICT["pink_bush"][0] + MAP1_DICT["pink_bush_size"][0] and
            MAP1_DICT["pink_bush"][1] <= y <= MAP1_DICT["pink_bush"][1] + MAP1_DICT["pink_bush_size"][1]):
        return True
    if (MAP1_DICT["pink_bush"][0] <= x + 50 <= MAP1_DICT["pink_bush"][0] + MAP1_DICT["pink_bush_size"][0] and
            MAP1_DICT["pink_bush"][1] <= y + 50 <= MAP1_DICT["pink_bush"][1] + MAP1_DICT["pink_bush_size"][1]):
        return True
    if (MAP1_DICT["pink_bush"][0] <= x <= MAP1_DICT["pink_bush"][0] + MAP1_DICT["pink_bush_size"][0] and
            MAP1_DICT["pink_bush"][1] <= y + 50 <= MAP1_DICT["pink_bush"][1] + MAP1_DICT["pink_bush_size"][1]):
        return True
    else:
        return False


def touched_yellow_bush(x, y):
    if (MAP1_DICT["yellow_bush"][0] <= x <= MAP1_DICT["yellow_bush"][0] + MAP1_DICT["yellow_bush_size"][0] and
            MAP1_DICT["yellow_bush"][1] <= y <= MAP1_DICT["yellow_bush"][1] + MAP1_DICT["yellow_bush_size"][1]):
        return True
    if (MAP1_DICT["yellow_bush"][0] <= x + 50 <= MAP1_DICT["yellow_bush"][0] + MAP1_DICT["yellow_bush_size"][0] and
            MAP1_DICT["yellow_bush"][1] <= y <= MAP1_DICT["yellow_bush"][1] + MAP1_DICT["yellow_bush_size"][1]):
        return True
    if (MAP1_DICT["yellow_bush"][0] <= x + 50 <= MAP1_DICT["yellow_bush"][0] + MAP1_DICT["yellow_bush_size"][0] and
            MAP1_DICT["yellow_bush"][1] <= y + 50 <= MAP1_DICT["yellow_bush"][1] + MAP1_DICT["yellow_bush_size"][1]):
        return True
    if (MAP1_DICT["yellow_bush"][0] <= x <= MAP1_DICT["yellow_bush"][0] + MAP1_DICT["yellow_bush_size"][0] and
            MAP1_DICT["yellow_bush"][1] <= y + 50 <= MAP1_DICT["yellow_bush"][1] + MAP1_DICT["yellow_bush_size"][1]):
        return True
    else:
        return False


def touched_orange_bush(x, y):
    if (MAP1_DICT["orange_bush"][0] <= x <= MAP1_DICT["orange_bush"][0] + MAP1_DICT["orange_bush_size"][0] and
            MAP1_DICT["orange_bush"][1] <= y <= MAP1_DICT["orange_bush"][1] + MAP1_DICT["orange_bush_size"][1]):
        return True
    if (MAP1_DICT["orange_bush"][0] <= x + 50 <= MAP1_DICT["orange_bush"][0] + MAP1_DICT["orange_bush_size"][0] and
            MAP1_DICT["orange_bush"][1] <= y <= MAP1_DICT["orange_bush"][1] + MAP1_DICT["orange_bush_size"][1]):
        return True
    if (MAP1_DICT["orange_bush"][0] <= x + 50 <= MAP1_DICT["orange_bush"][0] + MAP1_DICT["orange_bush_size"][0] and
            MAP1_DICT["orange_bush"][1] <= y + 50 <= MAP1_DICT["orange_bush"][1] + MAP1_DICT["orange_bush_size"][1]):
        return True
    if (MAP1_DICT["orange_bush"][0] <= x <= MAP1_DICT["orange_bush"][0] + MAP1_DICT["orange_bush_size"][0] and
            MAP1_DICT["orange_bush"][1] <= y + 50 <= MAP1_DICT["orange_bush"][1] + MAP1_DICT["orange_bush_size"][1]):
        return True
    else:
        return False


def redraw_screen():
    background = pygame.image.load(EMPTY_BACK)
    SCREEN.blit(background, (0, 0))
    flag = pygame.image.load(FLAG)
    flag.set_colorkey(GREEN_BLUE)
    SCREEN.blit(flag, MAP1_DICT["flag"])
    lake = pygame.image.load(LAKE)
    lake.set_colorkey(GREEN_BLUE)
    SCREEN.blit(lake, MAP1_DICT["lake"])
    white_bush = pygame.image.load(WHITE_BUSH)
    white_bush.set_colorkey(GREEN_BLUE)
    SCREEN.blit(white_bush, MAP1_DICT["white_bush"])
    pink_bush = pygame.image.load(PINK_BUSH)
    pink_bush.set_colorkey(GREEN_BLUE)
    SCREEN.blit(pink_bush, MAP1_DICT["pink_bush"])
    sand = pygame.image.load(SAND)
    sand.set_colorkey(GREEN_BLUE)
    SCREEN.blit(sand, MAP1_DICT["sand"])
    yellow_bush = pygame.image.load(YELLOW_BUSH)
    yellow_bush.set_colorkey(GREEN_BLUE)
    SCREEN.blit(yellow_bush, MAP1_DICT["yellow_bush"])
    yellow_bush = pygame.image.load(RED_BUSH)
    yellow_bush.set_colorkey(GREEN_BLUE)
    SCREEN.blit(yellow_bush, MAP1_DICT["red_bush"])
    yellow_bush = pygame.image.load(ORANGE_BUSH)
    yellow_bush.set_colorkey(GREEN_BLUE)
    SCREEN.blit(yellow_bush, MAP1_DICT["orange_bush"])


def update_speed_bar(current_speed):
    ratio = current_speed / MAX_SPEED
    pygame.draw.rect(SCREEN, "black", (1300, 250, 40, 400 * ratio))
    pygame.display.flip()


def start_game():
    img = pygame.image.load(EMPTY_BACK)
    SCREEN.blit(img, (0, 0))
    pygame.display.flip()


def draw_player(x, y):
    player_image = pygame.image.load(PLAYER1).convert()
    player_image.set_colorkey(GREEN_BLUE)
    SCREEN.blit(player_image, (x, y))


def draw_player2(x_player2, y_player2):
    player_image = pygame.image.load(PLAYER2).convert()
    player_image.set_colorkey(GREEN_BLUE)
    SCREEN.blit(player_image, (x_player2, y_player2))


def win(x, y):
    return distance_from_hole(x, y) <= 20


def move_player(x, y, xspeed, yspeed, speed):
    while round(xspeed) != 0 and round(yspeed) != 0:
        pygame.time.delay(20)
        redraw_screen()
        xspeed = xspeed * speed
        yspeed = yspeed * speed
        if x >= 1390:
            xspeed = xspeed * -1
            x = 1389
        if x <= 20:
            xspeed = xspeed * -1
            x = 21
        if y >= 750:
            yspeed = yspeed * -1
            y = 749
        if y <= 20:
            yspeed = yspeed * -1
            y = 21
        if is_in_lake(x + 25, y + 25):
            xspeed = xspeed * 0.5
            yspeed = yspeed * 0.5
        if is_in_sand(x + 25, y + 25):
            xspeed = xspeed * 0.3
            yspeed = yspeed * 0.3
        if touched_white_bush(x, y):
            xspeed = xspeed * -1
            yspeed = yspeed * -1
        if touched_pink_bush(x, y):
            xspeed = xspeed * -1
            yspeed = yspeed * -1
        if touched_red_bush(x, y):
            xspeed = xspeed * -1
            yspeed = yspeed * -1
        if touched_yellow_bush(x, y):
            xspeed = xspeed * -1
            yspeed = yspeed * -1
        if touched_orange_bush(x, y):
            xspeed = xspeed * -1
            yspeed = yspeed * -1
        x = int(x + xspeed)
        y = int(y + yspeed)
        draw_player(x, y)
        pygame.display.flip()
    return x, y


def move_other_player(x, y, xspeed, yspeed, speed):
    while round(xspeed) != 0 and round(yspeed) != 0:
        pygame.time.delay(20)
        redraw_screen()
        xspeed = xspeed * speed
        yspeed = yspeed * speed
        if x >= 1390:
            xspeed = xspeed * -1
            x = 1389
        if x <= 20:
            xspeed = xspeed * -1
            x = 21
        if y >= 750:
            yspeed = yspeed * -1
            y = 749
        if y <= 20:
            yspeed = yspeed * -1
            y = 21
        if is_in_lake(x + 25, y + 25):
            xspeed = xspeed * 0.5
            yspeed = yspeed * 0.5
        if is_in_sand(x + 25, y + 25):
            xspeed = xspeed * 0.3
            yspeed = yspeed * 0.3
        if touched_white_bush(x, y):
            xspeed = xspeed * -1
            yspeed = yspeed * -1
        if touched_pink_bush(x, y):
            xspeed = xspeed * -1
            yspeed = yspeed * -1
        if touched_red_bush(x, y):
            xspeed = xspeed * -1
            yspeed = yspeed * -1
        if touched_yellow_bush(x, y):
            xspeed = xspeed * -1
            yspeed = yspeed * -1
        if touched_orange_bush(x, y):
            xspeed = xspeed * -1
            yspeed = yspeed * -1
        x = int(x + xspeed)
        y = int(y + yspeed)
        draw_player2(x, y)
        pygame.display.flip()
    return x, y


def handle_socket_error(sock):
    error_message = f"Error on socket {sock}"
    # Log the error message (optional)
    print(error_message)
    sock.close()


def main():
    global PLAYER1
    global PLAYER2
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
        pygame.init()
        pygame.display.set_caption("Mini-Golf Game!")

        img = pygame.image.load(START_SCREEN)
        SCREEN.blit(img, (0, 0))
        pygame.display.flip()

        color = my_socket.recv(1024).decode()
        if color == 'pink':
            x = START_X_POS1
            y = START_Y_POS1
            x2 = START_X_POS2
            y2 = START_Y_POS2
        elif color == 'blue':
            PLAYER1 = 'ball2.png'
            PLAYER2 = 'ball1.png'
            x = START_X_POS2
            y = START_Y_POS2
            x2 = START_X_POS1
            y2 = START_Y_POS1
        else:
            x = 0
            y = 0
            x2 = 0
            y2 = 0

        clock = pygame.time.Clock()
        fps = 150

        """starting the game
        start = False
        while not start:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start_game()
                        start = True
        """

        finish = False
        while not finish:
            clock.tick(fps)
            rlist, wlist, xlist = select.select([my_socket], [my_socket], [my_socket])

            if xlist:
                # Handle errors on the sockets in xlist
                for sock in xlist:
                    handle_socket_error(sock)

            msg = '~'
            if rlist:
                msg = my_socket.recv(1024).decode()
                print(msg)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True

            x_speed = 0
            y_speed = 0

            redraw_screen()
            draw_player2(x2, y2)
            draw_player(x, y)
            pygame.display.flip()

            if minigolf_protocol.check_turn(msg):
                # setting direction
                cont = True
                while cont:
                    pygame.time.delay(fps)
                    redraw_screen()
                    draw_player2(x2, y2)
                    pygame.display.flip()
                    draw_player(x, y)
                    pos = pygame.mouse.get_pos()
                    pygame.draw.line(SCREEN, (255, 255, 255), (x + 25, y + 25), pos, width=5)
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()

                        if event.type == pygame.MOUSEBUTTONUP:
                            x_speed = int((pos[0] - x) / 20)
                            y_speed = int((pos[1] - y) / 20)
                            cont = False

                # setting the speed
                pygame.draw.rect(SCREEN, "white", (1300, 250, 40, 400))
                pygame.display.flip()
                speed = MIN_SPEED
                press_space = False
                while not press_space:
                    if math.floor(speed) == 100:
                        speed = MIN_SPEED
                        update_speed_bar(speed)
                        pygame.draw.rect(SCREEN, "white", (1300, 250, 40, 400))

                    speed = speed + 0.1
                    update_speed_bar(speed)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                speed = 1 - (speed / 700)
                                press_space = True

                redraw_screen()
                pygame.display.flip()

                send_str = str(x_speed) + "," + str(y_speed) + "," + str(speed)
                send_str = minigolf_protocol.proto_msg(send_str)
                print("I sent: " + send_str)
                my_socket.send(send_str.encode())

                x, y = move_player(x, y, x_speed, y_speed, speed)

                if is_win(x + 25, y + 25):
                    print("I sent: FINISH")
                    my_socket.send(minigolf_protocol.proto_msg('FINISH').encode())
                    finish = True
                else:
                    print("I sent: END")
                    my_socket.send(minigolf_protocol.proto_msg('END').encode())

            elif minigolf_protocol.check_wait(msg):
                redraw_screen()
                draw_player2(x2, y2)
                draw_player(x, y)
                pygame.display.flip()

                coordinates = minigolf_protocol.get_coordinates_client(msg)
                print(coordinates)
                x2_speed, y2_speed, speed2 = coordinates.split(',')
                x2_speed = float(x2_speed)
                y2_speed = float(y2_speed)
                speed2 = float(speed2)
                x2, y2 = move_other_player(x2, y2, x2_speed, y2_speed, speed2)

                if is_win(x2 + 25, y2 + 25):
                    print("I sent: FINISH")
                    my_socket.send(minigolf_protocol.proto_msg('FINISH').encode())
                    finish = True
                else:
                    print("I sent: END")
                    my_socket.send(minigolf_protocol.proto_msg('END').encode())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

        start = False
        while not start:
            if is_win(x + 25, y + 25):
                img = pygame.image.load(WIN1_BACK)
                SCREEN.blit(img, (0, 0))
                pygame.display.flip()
            elif is_win(x2 + 25, y2 + 25):
                img = pygame.image.load(LOSE1_BACK)
                SCREEN.blit(img, (0, 0))
                pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = True
                if event.type == pygame.QUIT:
                    quit()

        pygame.quit()

    except socket.error as err:
        print('received socket error ' + str(err))

    finally:
        my_socket.close()


if __name__ == "__main__":
    main()
