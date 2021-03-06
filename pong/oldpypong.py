import pygame
import sys
from pygame.locals import *


# Set FPS to allow for changing game speed
fps = 200

# Global Variables
WINDOWWIDTH = 700
WINDOWHEIGHT = 600
LINETHICKNESS = 10
PADDLESIZE = 35
PADDLEOFFSET = 50
XBALLSPEED = 3
YBALLSPEED = 2
NUMHITS = 0

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Draws the arena the game will be played in
def drawArena():
    DISPLAYSURF.fill((0, 0, 0))
    # Draw outline of arena
    # pygame.draw.rect(DISPLAYSURF, WHITE, ((0, 0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS * 2)
    # Draw center line
    # pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH / 2), 0), ((WINDOWWIDTH / 2), WINDOWHEIGHT), (LINETHICKNESS / 4))
    height = 0
    while not height >= WINDOWHEIGHT:
        pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH / 2), 0 + height), ((WINDOWWIDTH / 2), 10 + height), 4)
        height += 25


# Play the sound based upon speed
def pong_sound():
    if 3 < YBALLSPEED < 5:
        faster_sound.play()
        #fastest_sound.play()
    elif YBALLSPEED > 6:
        #faster_sound.play()
        fastest_sound.play()
    else:
        regular_sound.play()
        #fastest_sound.play()


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
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)


# Move the ball
def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX * XBALLSPEED  # ballspeed.speed
    ball.y += ballDirY * YBALLSPEED  # ballspeed.speed
    return ball


def tension():
    global NUMHITS, YBALLSPEED, XBALLSPEED
    if NUMHITS > 6:
        XBALLSPEED = 5
    if 3 < NUMHITS < 5:
        XBALLSPEED = 4


#Checks for a collision with a wall, and 'bounces' ball off it.
#Returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top <= 0 or ball.bottom >= WINDOWHEIGHT:
        ballDirY *= -1
        wall_sound.play()
    if ball.left <= 0 or ball.right >= WINDOWWIDTH:
        ballDirX *= -1
        wall_sound.play()
    return ballDirX, ballDirY


# Paddle collision
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    global YBALLSPEED, XBALLSPEED, NUMHITS, ballDirY
    #if ballDirX == -1 and paddle1.right == ball.left and paddle1.top <= ball.bottom and paddle1.bottom >= ball.top:
    if ballDirX == -1 and paddle1.colliderect(ball):
        NUMHITS += 1
        pong_sound()
        # Potential future collision code
        # hit_location = 5 * ((ball.centery - paddle1.centery) / (PADDLESIZE / 2))
        # if hit_location >= 0:
        #     YBALLSPEED = hit_location
        #     ballDirY = 1
        # else:
        #     YBALLSPEED = hit_location * -1
        #     ballDirY = -1
        print("general hit: paddle1.bottom = %s, ball.top = %s, ball.bottom = %s" %
              (paddle1.bottom, ball.top, ball.bottom))
        if ball.top <= paddle1.bottom - 35:
            YBALLSPEED = 5
            ballDirY = -1
        elif ball.top <= paddle1.bottom - 26:
            YBALLSPEED = 4
            ballDirY = -1
        elif ball.top <= paddle1.bottom - 21:
            YBALLSPEED = 0
            ballDirY = 0
        elif ball.top >= paddle1.bottom - 9:
            YBALLSPEED = 4
            ballDirY = 1
        elif ball.top >= paddle1.bottom - 17:
            YBALLSPEED = 5
            ballDirY = 1
        return -1
    #elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top <= ball.top and paddle2.bottom >= ball.bottom:
    elif ballDirX == 1 and paddle2.colliderect(ball):
        NUMHITS += 1
        pong_sound()
        # Potential future collision code
        # if hit_location >= 0:
        #     YBALLSPEED = hit_location
        #     ballDirY = 1
        # else:
        #     YBALLSPEED = hit_location * -1
        #     ballDirY = -1
        hit_location = 5 * ((ball.centery - paddle2.centery) / (PADDLESIZE / 2))
        print("general hit: paddle2.bottom = %s, ball.top = %s, ball.bottom = %s, HL = %s" %
              (paddle2.bottom, ball.top, ball.bottom, hit_location))
        if ball.top <= paddle2.bottom - 35:
            YBALLSPEED = 5
            ballDirY = -1
        elif ball.top <= paddle2.bottom - 26:
            YBALLSPEED = 4
            ballDirY = -1
        elif ball.top <= paddle2.bottom - 21:
            YBALLSPEED = 0
            ballDirY = 0
        elif ball.top >= paddle2.bottom - 9:
            YBALLSPEED = 4
            ballDirY = 1
        elif ball.top >= paddle2.bottom - 17:
            YBALLSPEED = 5
            ballDirY = 1
        return -1
    else:
        return 1


# Check to see if a score was made
def checkPointScored(p1_score, p2_score, ballX, ballY, XBALLSPEED):
    global ball
    if ball.left <= 25:
        p2_score += 1
        miss_sound.play()
        ball = pygame.Rect(ballX, ballY, 6, 6)
    if ball.right >= WINDOWWIDTH - 25:
        p1_score += 1
        miss_sound.play()
        ball = pygame.Rect(ballX, ballY, 6, 6)
    return p1_score, p2_score
    # if ball.left == LINETHICKNESS:
    #     # resets the points if the ball hits the left wall
    #     return 0
    # elif ballDirX == -1 and paddle1.right == ball.left and paddle1.top <= ball.bottom and paddle1.bottom >= ball.top:
    #     score += 1
    #     return score
    # elif ball.right == WINDOWWIDTH - LINETHICKNESS:
    #     score += 5
    #     return score
    # else:
    #     return score


# artificialIntelligence for the computer
def artificialIntelligence(ball, ballDirX, paddle2):
    # If ball is moving away from paddle, center it
    if ballDirX == -1:
        if paddle2.centery < (WINDOWHEIGHT / 2):
            paddle2.y += 2
        elif paddle2.centery > (WINDOWHEIGHT / 2):
            paddle2.y -= 2
    # If ball is moving towards paddle, track it
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            if YBALLSPEED == 0:
                paddle2.y += 2
            else:
                paddle2.y += YBALLSPEED
        else:
            if YBALLSPEED == 0:
                paddle2.y -= 2
            else:
                paddle2.y -= YBALLSPEED
    return paddle2


def displayScore(p1_score, p2_score, ball):
    # resultSurf = BASICFONT.render('HITS = %s, Y/XSPEED = %s,%s, bally,x = %s,%s' %
    #                               (NUMHITS, YBALLSPEED, XBALLSPEED, ball.centery, ball.centerx), True, WHITE)
    player1 = BASICFONT.render('%s' % p1_score, True, WHITE)
    player1_rect = player1.get_rect()
    player1_rect.topleft = (WINDOWWIDTH / 4, 25)
    player2 = BASICFONT.render('%s' % p2_score, True, WHITE)
    player2_rect = player2.get_rect()
    player2_rect.topleft = (WINDOWWIDTH * .75, 25)
    # resultRect = resultSurf.get_rect()
    # resultRect.topleft = (WINDOWWIDTH / 4, 25)
    DISPLAYSURF.blit(player1, player1_rect)
    DISPLAYSURF.blit(player2, player2_rect)


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    global DISPLAYSURF
    global BASICFONT, BASICFONTSIZE
    global regular_sound, faster_sound, fastest_sound, wall_sound, miss_sound
    global ballDirY, ballDirX, ball
    BASICFONTSIZE = 70
    BASICFONT = pygame.font.Font('visitor1.ttf', BASICFONTSIZE)
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

    # Keeps track of ball direction
    ballDirX = - 1  # -1 = Left 1 = Right
    ballDirY = - 1  # -1 = Up and 1 = Down

    # Create rects for paddles and ball
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, 6, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, 6, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, 6, 6)

    # Draws the starting position of the arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    pygame.mouse.set_visible(0)  # hide the cursor
    while True:
        global NUMHITS
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    NUMHITS += 1
                if event.key == K_q:
                    pygame.quit()

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        p1_score, p2_score = checkPointScored(p1_score, p2_score, ballX, ballY, XBALLSPEED)
        ballDirX *= checkHitBall(ball, paddle1, paddle2, ballDirX)

        paddle2 = artificialIntelligence(ball, ballDirX, paddle2)

        displayScore(p1_score, p2_score, ball)

        tension()

        pygame.display.update()
        FPSCLOCK.tick(fps)

if __name__ == '__main__':
    main()