import math
import socket
import pygame


WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 800
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BROWN = (153, 76, 0)
GREEN_BLUE = (54, 126, 127)
BACKGROUND_COLOR = (0, 170, 0)
OBSTACLE_LEN = 10
START_SCREEN = 'start_background.png'
EMPTY_BACK = 'grass.png'
PLAYER2 = 'ball2.png'
PLAYER1 = 'ball1.png'
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
    "hole_center": (173, 180), "hole_radius": 20, "lake_center": (1125, 275), "lake_radius": 175,
    "sand_center": (504, 504), "sand_radius": 104, "white_bush_size": (78, 200), "pink_bush_size": (200, 70),
    "yellow_bush_size": (138, 87), "red_bush_size": (136, 89), "orange_bush_size": (135, 90)
}
MAX_SPEED = 100
MIN_SPEED = 0
START_X_POS = 600
START_Y_POS = 700
PLAYER1_START_X_POS = 695
PLAYER1_START_Y_POS = 700
IP = '127.0.0.1'
PORT = 1729


def distance_from_hole(x, y):
    center = MAP1_DICT["hole_center"]
    num1 = x - center[0]
    num1 = num1**2
    num2 = y - center[1]
    num2 = num2**2
    new_num = num1 + num2
    return math.sqrt(new_num)


def distance_from_lake(x, y):
    center = MAP1_DICT["lake_center"]
    num1 = x - center[0]
    num1 = num1**2
    num2 = y - center[1]
    num2 = num2**2
    new_num = num1 + num2
    return math.sqrt(new_num)


def distance_from_sand(x, y):
    center = MAP1_DICT["sand_center"]
    num1 = x - center[0]
    num1 = num1**2
    num2 = y - center[1]
    num2 = num2**2
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
    player_image = pygame.image.load(PLAYER2).convert()
    player_image.set_colorkey(GREEN_BLUE)
    SCREEN.blit(player_image, (x, y))


def draw_player1(x, y):
    player_image = pygame.image.load(PLAYER1).convert()
    player_image.set_colorkey(GREEN_BLUE)
    SCREEN.blit(player_image, (x, y))


def move_player(x, y, xspeed, yspeed, speed):
    won = False
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


def move_other_player(player_socket, x_player, y_player):
    data = player_socket.recv(1024).decode()
    x = x_player
    y = y_player
    while data != '':
        x, y = data.split(",")
        draw_player1(x, y)
        data = player_socket.recv(1024).decode()
    return x, y


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
        my_socket.send("waiting".encode())
        print(my_socket.recv(1024).decode())
        pygame.init()
        pygame.display.set_caption("Mini Golf Game! - Player 1")

        img = pygame.image.load(START_SCREEN)
        SCREEN.blit(img, (0, 0))
        pygame.display.flip()

        x = START_X_POS
        y = START_Y_POS
        x2 = PLAYER1_START_X_POS
        y2 = PLAYER1_START_Y_POS

        clock = pygame.time.Clock()
        fps = 150

        """starting the game"""
        start = False
        while not start:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start_game()
                        start = True

        finish = False
        while not finish:
            clock.tick(fps)
            x_speed = 0
            y_speed = 0
            turn = my_socket.recv(1024).decode()
            if turn == "turn":
                # setting direction
                cont = True
                while cont:
                    pygame.time.delay(fps)
                    redraw_screen()
                    draw_player1(x2, y2)
                    ball2 = pygame.image.load("ball2.png")
                    ball2.set_colorkey(GREEN_BLUE)
                    SCREEN.blit(ball2, (600, START_Y_POS))
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

                location = move_player(x, y, x_speed, y_speed, speed)
                x = location[0]
                y = location[1]
                my_socket.send("waiting".encode())

            else:
                my_socket.send("turn".encode())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True

        pygame.quit()

    except socket.error as err:
        print('received socket error ' + str(err))

    finally:
        my_socket.close()


if __name__ == "__main__":
    main()
