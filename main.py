# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Introduction
# In this game,you should click the red line on the top to toss the ball. The balls are either green or yellow randomly.
# Your goal is to hit the all plates below using the lest amount of time and balls.
# Whenever the green ball hits the plate, it disappears; Whenever the yellow ball hits the plate, the plate gets longer.
# The timer and the ball counter above the red line tell you how many balls/time you have used.
# The wind arrow, which changes randomly, indicate where the balls direct. It makes the game more tough.
# Good luck!


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# In this game, we have to click the red line on the top to shoot balls. When the ball hits the self.board, you win.
import pygame, time, random
from typing import *


class Board:
    """The self.board is at the bottom and can bounce back if touch the left/right side"""

    def __init__(self, x, y, width, height, color, speed=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def move(self):
        self.x += self.speed

    def bounce(self):
        self.speed = -self.speed

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class Ball:
    """The ball can be thrown by the user at the top and hit the self.board"""

    def __init__(self, radius, color, x_speed):
        self.x = 0
        self.y = 0
        self.radius = radius
        self.color = color
        self.x_speed = x_speed

    def move(self, x=0, y=0):
        self.x += x
        self.y += y

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def collision(self, board: Board) -> bool:
        return self.x >= board.x - self.radius and self.x <= board.x + board.width + self.radius and \
               self.y >= board.y - self.radius and self.y <= board.y + board.height + self.radius


class Game:

    def __init__(self):
        self.SCREEN_COLOR = (111, 111, 111)
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.BOARD_COUNT = 5

        self.BOARD_SPEED_X_MIN = 10
        self.BOARD_SPEED_X_MAX = 20
        self.BALL_RADIUS = 5
        self.BALL_SPEED_Y = 10
        self.WIND_SPEED_X = 5
        self.BALL_START_HEIGHT = 50
        self.BOARD_START_HEIGHT = 400
        self.board_list: List[Board] = []
        self.ball_list: List[Ball] = []

    def random_color(self):
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    def throw_game(self):
        # game initialization
        pygame.init()
        # background
        bg = pygame.image.load("night.jpeg")
        startTime = time.time()

        # generate multiple boards
        for i in range(self.BOARD_COUNT):
            bx = random.randint(100, self.SCREEN_WIDTH - 100)
            by = random.randint(self.BOARD_START_HEIGHT,
                                self.SCREEN_HEIGHT - 30)
            bw = random.randint(25, 60)
            bs = (1 if random.randint(0, 1) == 1 else -1) * random.randint(
                self.BOARD_SPEED_X_MIN, self.BOARD_SPEED_X_MAX)
            self.board_list.append(
                Board(bx, by, bw, 10, self.random_color(), bs))

        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Game title
        pygame.display.set_caption("Throw Game")
        # screen.fill(self.SCREEN_COLOR)
        screen.blit(bg, (0, 0))

        pygame.font.init()
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        info_font = pygame.font.SysFont("Arial", 15, "bold")
        ball_used = 0
        # if user win, stop the game.
        running = True
        isWin = False

        ball_init_x_speed = self.WIND_SPEED_X
        while running:
            # set tick time 50ms
            pygame.time.delay(50)

            used_time = int(time.time() - startTime)

            if used_time % 10 == 0:
                r = random.randint(1, 2)
                if r == 1:
                    ball_init_x_speed = self.WIND_SPEED_X
                elif r == 2:
                    ball_init_x_speed = -self.WIND_SPEED_X

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # closing the windows
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not isWin:
                    # when user clicks, add a new ball on the screen
                    if len(self.ball_list) < 10:
                        x, y = pygame.mouse.get_pos()
                        if y < self.BALL_START_HEIGHT:
                            ball = Ball(self.BALL_RADIUS, (0, 255, 0) if random.randint(1, 5) != 5 else (255, 255, 0),
                                        ball_init_x_speed)
                            ball.move(x, y)
                            self.ball_list.append(ball)
                            ball_used += 1
            if isWin:
                continue

            # screen.fill(self.SCREEN_COLOR)
            screen.blit(bg, (0, 0))

            # render timer
            timer_surface = info_font.render("Time: " + str(used_time), False, (0, 0, 255))
            screen.blit(timer_surface, (650, 15))

            # render ball used
            ball_used_surface = info_font.render("Ball used: " + str(ball_used), False, (0, 0, 255))
            screen.blit(ball_used_surface, (50, 15))

            # render wind direction
            wind_surface = info_font.render("Wind: {0}".format("<-----" if ball_init_x_speed < 0 else "----->"), False,
                                            (0, 0, 255))
            screen.blit(wind_surface, (300, 15))

            # check self.board movement, if it hits side, bounce back
            for board in self.board_list:
                if board.x > self.SCREEN_WIDTH - board.width or board.x < 0:
                    board.bounce()
                board.move()
                board.render(screen)

            pygame.draw.line(screen, (255, 0, 0), (0, self.BALL_START_HEIGHT),
                             (self.SCREEN_WIDTH, self.BALL_START_HEIGHT), 3)

            # render balls
            for index in range(len(self.ball_list) - 1, -1, -1):
                ball = self.ball_list[index]
                if ball.y > self.SCREEN_HEIGHT:
                    self.ball_list.pop(index)
                else:
                    x_speed = ball.x_speed
                    if ball.x <= ball.radius or ball.x >= self.SCREEN_WIDTH - ball.radius:
                        x_speed = -x_speed
                        ball.x_speed = x_speed
                    ball.move(x_speed, self.BALL_SPEED_Y)
                    ball.render(screen)

            # detect collision
            for index in range(len(self.ball_list) - 1, -1, -1):
                ball = self.ball_list[index]
                for b1 in filter(lambda bd: ball.collision(bd), self.board_list):
                    self.ball_list.pop(index)
                    if ball.color == (255, 255, 0):
                        # yellow ball hit, wider board
                        b1.width += b1.width + 5
                    else:
                        # green ball hit, remove board
                        self.board_list.remove(b1)

            isWin = not self.board_list
            if isWin:
                text_surface = myfont.render("Game Over", False, (0, 0, 0))
                screen.blit(text_surface, (200, 200))
            pygame.display.flip()


game = Game()
game.throw_game()