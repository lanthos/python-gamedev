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


class Tank():

    def __init__(self, tank_x, tank_y, DISPLAYSURF, direction, color):
        self.tank_x = tank_x
        self.tank_y = tank_y
        self.DISPLAYSURF = DISPLAYSURF
        self.directions = 'up 22.5R 45R 67.5R right 22.5D 45D 67.5D down 22.5L 45L 67.5L left 22.5U 45U 67.5U'.split()
        self.tank_direction = direction
        if color == 'red':
            self.spritesheet = pygame.image.load('red_tanks.bmp').convert()
            self.tanks = []
            for nbr in range(8):
                self.tanks.append(self.spritesheet.subsurface((20*nbr), 0, 20, 20))
            for nbr in range(8):
                self.tanks.append(self.spritesheet.subsurface((20*nbr), 20, 20, 20))
            for nbr in range(len(self.tanks)):
                self.tanks[nbr].set_colorkey(WHITE)
                self.tanks[nbr] = self.tanks[nbr].convert_alpha()
        if color == 'blue':
            self.spritesheet = pygame.image.load('blue_tank.bmp').convert()
            self.spritesheet.set_colorkey(WHITE)
            self.spritesheet.convert_alpha()

    def draw_red(self):
        # for nbr in range(len(self.tanks)):
        #     DISPLAYSURF.blit(self.tanks[nbr], (nbr*self.tank_x, self.tank_y))
        if self.tank_direction == 'up':
            self.DISPLAYSURF.blit(self.tanks[0], (self.tank_x, self.tank_y))
        elif self.tank_direction == '22.5R':
            self.DISPLAYSURF.blit(self.tanks[1], (self.tank_x, self.tank_y))
        elif self.tank_direction == '45R':
            self.DISPLAYSURF.blit(self.tanks[2], (self.tank_x, self.tank_y))
        elif self.tank_direction == '67.5R':
            self.DISPLAYSURF.blit(self.tanks[3], (self.tank_x, self.tank_y))
        elif self.tank_direction == 'right':
            self.DISPLAYSURF.blit(self.tanks[4], (self.tank_x, self.tank_y))
        elif self.tank_direction == '22.5D':
            self.DISPLAYSURF.blit(self.tanks[5], (self.tank_x, self.tank_y))
        elif self.tank_direction == '45D':
            self.DISPLAYSURF.blit(self.tanks[6], (self.tank_x, self.tank_y))
        elif self.tank_direction == '67.5D':
            self.DISPLAYSURF.blit(self.tanks[7], (self.tank_x, self.tank_y))
        elif self.tank_direction == 'down':
            self.DISPLAYSURF.blit(self.tanks[8], (self.tank_x, self.tank_y))
        elif self.tank_direction == '22.5L':
            self.DISPLAYSURF.blit(self.tanks[9], (self.tank_x, self.tank_y))
        elif self.tank_direction == '45L':
            self.DISPLAYSURF.blit(self.tanks[10], (self.tank_x, self.tank_y))
        elif self.tank_direction == '67.5L':
            self.DISPLAYSURF.blit(self.tanks[11], (self.tank_x, self.tank_y))
        elif self.tank_direction == 'left':
            self.DISPLAYSURF.blit(self.tanks[12], (self.tank_x, self.tank_y))
        elif self.tank_direction == '22.5U':
            self.DISPLAYSURF.blit(self.tanks[13], (self.tank_x, self.tank_y))
        elif self.tank_direction == '45U':
            self.DISPLAYSURF.blit(self.tanks[14], (self.tank_x, self.tank_y))
        elif self.tank_direction == '67.5U':
            self.DISPLAYSURF.blit(self.tanks[15], (self.tank_x, self.tank_y))

    def draw_blue(self):
        if self.tank_direction == 'up':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, 0), (self.tank_x, self.tank_y))
        elif self.tank_direction == '22.5R':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, -22.5), (self.tank_x, self.tank_y))
        elif self.tank_direction == '45R':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, -45), (self.tank_x, self.tank_y))
        elif self.tank_direction == '67.5R':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, -67.5), (self.tank_x, self.tank_y))
        elif self.tank_direction == 'right':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, -90), (self.tank_x, self.tank_y))
        elif self.tank_direction == '22.5D':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, -112.5), (self.tank_x, self.tank_y))
        elif self.tank_direction == '45D':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, -135), (self.tank_x, self.tank_y))
        elif self.tank_direction == '67.5D':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, -157.5), (self.tank_x, self.tank_y))
        elif self.tank_direction == 'down':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, -180), (self.tank_x, self.tank_y))
        elif self.tank_direction == '22.5L':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, 157.5), (self.tank_x, self.tank_y))
        elif self.tank_direction == '45L':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, 135), (self.tank_x, self.tank_y))
        elif self.tank_direction == '67.5L':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, 112.5), (self.tank_x, self.tank_y))
        elif self.tank_direction == 'left':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, 90), (self.tank_x, self.tank_y))
        elif self.tank_direction == '22.5U':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, 67.5), (self.tank_x, self.tank_y))
        elif self.tank_direction == '45U':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, 45), (self.tank_x, self.tank_y))
        elif self.tank_direction == '67.5U':
            self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, 180), (self.tank_x, self.tank_y))

    def move(self, move_direction, color):
        if color == 'red':
            if move_direction == 'left':
                self.tank_direction = self.directions[self.directions.index(self.tank_direction) - 1]
                self.draw_red()
            if move_direction == 'right':
                try:
                    self.tank_direction = self.directions[self.directions.index(self.tank_direction) + 1]
                except IndexError:
                    self.tank_direction = 'up'
                self.draw_red()
        if color == 'blue':
            if move_direction == 'left':
                self.tank_direction = self.directions[self.directions.index(self.tank_direction) - 1]
                self.draw_blue()
            if move_direction == 'right':
                try:
                    self.tank_direction = self.directions[self.directions.index(self.tank_direction) + 1]
                except IndexError:
                    self.tank_direction = 'up'
                self.draw_blue()


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

    # initialize tank
    red_tank = Tank(50, 100, DISPLAYSURF, 'right', 'red')
    blue_tank = Tank(450, 100, DISPLAYSURF, 'left', 'blue')



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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_a:
                    red_tank.move('left', 'red')
                if event.key == pygame.K_d:
                    red_tank.move('right', 'red')
                if event.key == pygame.K_LEFT:
                    blue_tank.move('left', 'blue')
                if event.key == pygame.K_RIGHT:
                    blue_tank.move('right', 'blue')


        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        for row in range(MAPHEIGHT):
            for column in range(MAPWIDTH):
                pygame.draw.rect(DISPLAYSURF, colors[tilemap[row][column]],
                                 (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

        red_tank.draw_red()
        blue_tank.draw_blue()
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