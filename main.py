# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

#In this game, we have to click the red line on the top to shoot balls. When the ball hits the board, you win.
import pygame

class Board:
    """The board is at the bottom and can bounce back if touch the left/right side"""
    def __init__(self,width,height,color):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.color = color

    def move(self,x=0,y=0):
        self.x+=x
        self.y+=y

    def render(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))


class Ball:
    """The ball can be thrown by the user at the top and hit the board"""
    def __init__(self,radius,color):
        self.x = 0
        self.y = 0
        self.radius = radius
        self.color = color

    def move(self,x=0,y=0):
        self.x+=x
        self.y+=y

    def render(self,screen):
        pygame.draw.circle(screen,self.color,(self.x-self.radius,self.y-self.radius),self.radius)


def throw_game():
    # game initialization
    pygame.init()
    SCREEN_COLOR=(111,111,111)
    SCREEN_WIDTH=800
    SCREEN_HEIGHT=600

    BOARD_SPEED_X=10
    BALL_RADIUS=5
    BALL_SPEED_Y=40
    BALL_START_HEIGHT = 50
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    # Game title
    pygame.display.set_caption("Throw Game")
    screen.fill(SCREEN_COLOR)
    board = Board(40,10,(255,0,0))
    board.move(0,SCREEN_HEIGHT-30)
    line = Board(800,2,(255,0,0))
    line.move(0,BALL_START_HEIGHT)
    ballList = []

    # add ball to the screen when user clicking
    def addBall():
        if len(ballList) < 10:
            x,y = pygame.mouse.get_pos()
            if y < BALL_START_HEIGHT:
                ball = Ball(BALL_RADIUS,(0,255,0))
                ball.move(x,y)
                ballList.append(ball)

    ## if user win, stop the game.
    running = True
    isWin = False
    while running:
        if isWin:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:#closing the windows
                    running = False
            continue

        # set tick time 100ms
        pygame.time.delay(100)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:#closing the windows
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # when user clicks, add a new ball on the screen
                addBall()

        # check board movement, if it hits side, bounce back
        if board.x > SCREEN_WIDTH - board.width or board.x < 0:
            BOARD_SPEED_X*=-1
        board.move(BOARD_SPEED_X)
        board.render(screen)
        line.render(screen)

        # render balls
        for index in range(len(ballList)-1,-1,-1):
            ball = ballList[index]
            if ball.y > SCREEN_HEIGHT:
                ballList.pop(index)
            else:
                ball.move(0,BALL_SPEED_Y)
                ball.render(screen)
            if ball.x >= board.x - ball.radius*2 and ball.x <= board.x + board.width and \
                    ball.y >= board.y - ball.radius*2 and ball.y <= board.y + board.height:
                isWin = True

                pygame.font.init()
                myfont = pygame.font.SysFont("Comic Sans MS", 30)
                text_surface = myfont.render("Game Over", False, (0, 0, 0))
                screen.blit(text_surface, (200, 200))
                pygame.display.flip()

        pygame.display.update()
        screen.fill(SCREEN_COLOR)

throw_game()

