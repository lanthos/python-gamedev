"""
 Paraaahhh! Troopers

"""

import sys
import pygame
import turret
import trooper


# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (5, 61, 244)
GREY = (199, 199, 199)
GREEN = (63, 177, 79)
RED = (187, 8, 0)


def display_score(score_font, screen, p1_score, high_score):
    player = score_font.render('Score: %s' % p1_score, True, WHITE)
    player_rect = player.get_rect()
    player_rect.topleft = (screen.get_width() / 1.7, screen.get_height() - 50)
    high_score = score_font.render('High Score: %s' % high_score, True, WHITE)
    high_score_rect = high_score.get_rect()
    high_score_rect.topleft = (screen.get_width() / 24, screen.get_height() - 50)
    screen.blit(player, player_rect)
    screen.blit(high_score, high_score_rect)


def draw_map(screen):
    pygame.draw.line(screen, GREEN, (0, screen.get_height() / 1.1), (screen.get_width(), screen.get_height() / 1.1), 10)


def main():
    """ Main function for the game. """
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    # Initialize sounds

    # Set the width and height of the screen [width,height]
    screen_width, screen_height = [1024, 768]
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption("Paraaaahhhh! Troopers")

    # initialize fonts
    BASICFONTSIZE = 40
    score_font = pygame.font.Font('visitor1.ttf', BASICFONTSIZE)

    # initialize turret and bullets
    player = turret.Turret(screen)

    # Init troopers
    unit = trooper.Trooper(screen)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    high_score = 1234151

    # -------- Main Program Loop -----------
    while not done:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT


        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        player.draw()
        draw_map(screen)
        display_score(score_font, screen, player.score, high_score)
        unit.draw()


        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second
        clock.tick(20)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()