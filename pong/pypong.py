import pygame
import sys
import random
import time
from pygame.locals import *

# Set FPS to allow for changing game speed
fps = 200

# Global Variables
WINDOWWIDTH = 700
WINDOWHEIGHT = 600
LINETHICKNESS = 10
PADDLESIZE = 35
PADDLEOFFSET = 60
XBALLSPEED = -4
YBALLSPEED = 2
NUMHITS = 0

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Draws the arena the game will be played in
def drawArena():
    DISPLAYSURF.fill((0, 0, 0))
    height = 0
    while not height >= WINDOWHEIGHT:
        pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH / 2), 0 + height), ((WINDOWWIDTH / 2), 10 + height), 4)
        height += 25


# Play the sound based upon speed
def pong_sound():
    if 3 < NUMHITS < 6:
        faster_sound.play()
    elif NUMHITS >= 6:
        fastest_sound.play()
    else:
        regular_sound.play()


# Draw the paddles
def drawPaddle(paddle):
    # Stops the paddle from moving too low
    if paddle.top > WINDOWHEIGHT:
        paddle.top = WINDOWHEIGHT
    # Stops the paddle from moving too high
    elif paddle.top < LINETHICKNESS + 15:
        paddle.top = LINETHICKNESS + 15
    # Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)


# Draw the ball
def drawBall(ball, color):
    pygame.draw.rect(DISPLAYSURF, color, ball)


# Move the ball
def moveBall(ball, XBALLSPEED, YBALLSPEED):
    ball.x += XBALLSPEED
    ball.y += YBALLSPEED
    return ball


def tension():
    global NUMHITS, YBALLSPEED, XBALLSPEED
    if NUMHITS > 6:
        if XBALLSPEED > 0:
            XBALLSPEED = 8
        else:
            XBALLSPEED = -8
    if 3 < NUMHITS < 6:
        if XBALLSPEED > 0:
            XBALLSPEED = 6
        else:
            XBALLSPEED = -6


#Checks for a collision with a wall, and 'bounces' ball off it.
#Returns new direction
def checkEdgeCollision(ball, XBALLSPEED, YBALLSPEED):
    if ball.top <= 0 or ball.bottom >= WINDOWHEIGHT:
        YBALLSPEED *= -1
        wall_sound.play()
    return XBALLSPEED, YBALLSPEED


# Paddle collision
def checkHitBall(ball, paddle1, paddle2):
    global YBALLSPEED, NUMHITS, ballDirY
    if XBALLSPEED < 0 and paddle1.colliderect(ball):
        NUMHITS += 1
        pong_sound()
        YBALLSPEED = 5 * ((ball.centery - paddle1.centery) / (PADDLESIZE / 2))
        # print("numhits = %s, xspeed = %s" % (NUMHITS, XBALLSPEED))
        pressed = pygame.key.get_pressed()
        if pressed[K_SPACE]:
            NUMHITS = 5
        return -1
    elif XBALLSPEED > 0 and paddle2.colliderect(ball):
        NUMHITS += 1
        pong_sound()
        YBALLSPEED = 5 * ((ball.centery - paddle2.centery) / (PADDLESIZE / 2))
        # print("numhits = %s, xspeed = %s" % (NUMHITS, XBALLSPEED))
        pressed = pygame.key.get_pressed()
        if pressed[K_SPACE]:
            NUMHITS = 5
        return -1
    else:
        return 1


# Check to see if a score was made
def checkPointScored(p1_score, p2_score, ballX, ballY):
    global ball, NUMHITS, XBALLSPEED, YBALLSPEED
    if ball.left <= 25:
        p2_score += 1
        miss_sound.play()
        ball = pygame.Rect(ballX, ballY, 6, 6)
        NUMHITS = 0
        XBALLSPEED = -3
        random.seed()
        YBALLSPEED = random.randint(-4, -1)
    if ball.right >= WINDOWWIDTH - 25:
        p1_score += 1
        miss_sound.play()
        ball = pygame.Rect(ballX, ballY, 6, 6)
        NUMHITS = 0
        XBALLSPEED = 3
        random.seed()
        YBALLSPEED = random.randint(1, 4)
    return p1_score, p2_score


def game_over(p1_score, p2_score):
    global paused, gameover_font
    if p1_score >= 15 or p2_score >= 15:
        gameover = gameover_font.render('Game Over', True, WHITE)
        gameover_rect = gameover.get_rect()
        gameover_rect.topleft = (WINDOWWIDTH / 3 - 15, 125)
        DISPLAYSURF.blit(gameover, gameover_rect)
        paused = True
        playagain = gameover_font.render('Press Q to quit', True, WHITE)
        playagain_rect = playagain.get_rect()
        playagain_rect.topleft = (WINDOWWIDTH / 4 - 40, 225)
        DISPLAYSURF.blit(playagain, playagain_rect)
        pygame.display.update()


# artificialIntelligence for the computer
def artificialIntelligence(ball, XBALLSPEED, paddle2):
    # If ball is moving away from paddle, center it
    if XBALLSPEED < 0:
        if paddle2.centery < (WINDOWHEIGHT / 2):
            paddle2.y += 2
        elif paddle2.centery > (WINDOWHEIGHT / 2):
            paddle2.y -= 2
    # If ball is moving towards paddle, track it
    elif XBALLSPEED > 0:
        if paddle2.centery < ball.centery:
            if YBALLSPEED == 0:
                paddle2.y += 3
            else:
                paddle2.y += 3  #YBALLSPEED
        else:
            if YBALLSPEED == 0:
                paddle2.y -= 3
            else:
                paddle2.y -= 3  #YBALLSPEED
    return paddle2


def displayScore(p1_score, p2_score):
    player1 = BASICFONT.render('%s' % p1_score, True, WHITE)
    player1_rect = player1.get_rect()
    player1_rect.topleft = (WINDOWWIDTH / 4, 25)
    player2 = BASICFONT.render('%s' % p2_score, True, WHITE)
    player2_rect = player2.get_rect()
    player2_rect.topleft = (WINDOWWIDTH * .75, 25)
    DISPLAYSURF.blit(player1, player1_rect)
    DISPLAYSURF.blit(player2, player2_rect)


def spectator():
    loop = True
    while loop:
        global ball, XBALLSPEED, YBALLSPEED, p1_score, p2_score
        if ball.top <= 0 or ball.bottom >= WINDOWHEIGHT:
            YBALLSPEED *= -1
            wall_sound.play()
        if ball.left <= 0 or ball.right >= WINDOWWIDTH:
            XBALLSPEED *= -1
            wall_sound.play()
        ball = moveBall(ball, XBALLSPEED, YBALLSPEED)
        drawArena()
        drawBall(ball, WHITE)
        displayScore(p1_score, p2_score)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                loop = False
            elif event.type == MOUSEBUTTONDOWN:
                loop = False


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    global DISPLAYSURF
    global BASICFONT, BASICFONTSIZE, gameover_font
    global regular_sound, faster_sound, fastest_sound, wall_sound, miss_sound
    global ball, paused, p1_score, p2_score
    BASICFONTSIZE = 70
    BASICFONT = pygame.font.Font('visitor1.ttf', BASICFONTSIZE)
    gameover_font = pygame.font.Font('visitor1.ttf', 50)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pong')

    # Initiate sounds
    regular_sound = pygame.mixer.Sound("regular.wav")
    faster_sound = pygame.mixer.Sound("faster.wav")
    fastest_sound = pygame.mixer.Sound("fastest.wav")
    wall_sound = pygame.mixer.Sound("wallhit.wav")
    miss_sound = pygame.mixer.Sound("miss.wav")

    # Initiate variable and set starting positions
    # any future changes made within rectangles
    ballX = (WINDOWWIDTH - LINETHICKNESS) / 2
    ballY = WINDOWHEIGHT / 2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    p1_score = 0
    p2_score = 0

    # Create rects for paddles and ball
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, 6, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, 6, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, 6, 6)

    # Draws the starting position of the arena
    drawArena()
    drawBall(ball, WHITE)
    spectator()
    ball = pygame.Rect(ballX, ballY, 6, 6)
    drawPaddle(paddle1)
    drawPaddle(paddle2)

    # Paused variable
    paused = False

    pygame.mouse.set_visible(0)  # hide the cursor
    while True:
        global NUMHITS, XBALLSPEED, YBALLSPEED
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey
                # To enable AI comment out this next line and also AI function call further down.
                paddle2.y = mousey
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == K_p:
                    paused = True
                if event.key == K_y:
                    paused = False
                if event.key == K_n:
                    pygame.quit()
                    sys.exit()

        game_over(p1_score, p2_score)

        if paused:
            continue
        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball, WHITE)

        ball = moveBall(ball, XBALLSPEED, YBALLSPEED)
        XBALLSPEED, YBALLSPEED = checkEdgeCollision(ball, XBALLSPEED, YBALLSPEED)
        p1_score, p2_score = checkPointScored(p1_score, p2_score, ballX, ballY)
        XBALLSPEED *= checkHitBall(ball, paddle1, paddle2)

        # To enable AI uncomment the next line and also comment out line above for paddle2.y = mousey
        #paddle2 = artificialIntelligence(ball, XBALLSPEED, paddle2)

        displayScore(p1_score, p2_score)

        tension()

        pygame.display.update()
        FPSCLOCK.tick(fps)

if __name__ == '__main__':
    main()