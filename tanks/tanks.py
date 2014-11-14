"""
 Atari Tanks!  Weeeeeeeeeeeeeeeeeeeeeeeeeee

"""

import pygame
import sys

# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Map definitions and dimensions.
WALL = 1
OPEN = 0
TILESIZE = 20
MAPWIDTH = 35
MAPHEIGHT = 30

# Generate blank map
tilemap = [[OPEN for w in range(MAPWIDTH)] for h in range(MAPHEIGHT)]

# Add borders
for i in range(MAPHEIGHT):
    tilemap[i][0] = WALL
    tilemap[i][MAPWIDTH - 1] = WALL
    if i == 0 or i == MAPHEIGHT - 1:
        for w in range(MAPWIDTH):
            tilemap[i][w] = WALL


colors = {
    WALL: WHITE,
    OPEN: BLACK
}


def main():
    """ Main function for the game. """
    pygame.init()

    # Set the width and height of the screen [width,height]
    # size = [700, 500]
    # screen = pygame.display.set_mode(size)
    DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))
    pygame.display.set_caption("Tanks")

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT


        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT



        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        for row in range(MAPHEIGHT):
            for column in range(MAPWIDTH):
                pygame.draw.rect(DISPLAYSURF, colors[tilemap[row][column]],
                                 (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
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