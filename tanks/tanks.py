"""
 Atari Tanks!  Weeeeeeeeeeeeeeeeeeeeeeeeeee

"""

import pygame
import sys
import math

# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Tank():

    def __init__(self, tank_x, tank_y, DISPLAYSURF, color):
        self.tank_x = tank_x
        self.tank_y = tank_y
        self.DISPLAYSURF = DISPLAYSURF
        self.tank_direction = 4
        self.angle_deg = 180
        self.angle_rad_blue = math.pi
        self.angle_rad = math.pi/2
        self.speed = 2
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
        self.DISPLAYSURF.blit(self.tanks[self.tank_direction % 16], (self.tank_x, self.tank_y))

    def draw_blue(self):
        self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, self.angle_deg), (self.tank_x, self.tank_y))

    def check_collision(self, game_map):
        self.tileX = self.tank_x / game_map.MAPWIDTH
        self.tileY = self.tank_y / game_map.MAPHEIGHT

    def move(self, move_direction, color):
        if color == 'red':
            if move_direction == 'left':
                self.tank_direction -= 1
                self.angle_rad += math.pi/8
                self.draw_red()
            if move_direction == 'right':
                self.tank_direction += 1
                self.angle_rad -= math.pi/8
                self.draw_red()
            if move_direction == 'forward':
                self.tank_y += self.speed * math.cos(self.angle_rad)
                self.tank_x += self.speed * math.sin(self.angle_rad)
                print 'red tank_x: %s, red tank_y: %s, tilex: %s, tiley: %s' % (self.tank_x, self.tank_y, self.tileX, self.tileY)
                print 'angle_rad: %s' % self.angle_rad
        if color == 'blue':
            if move_direction == 'left':
                self.angle_deg += 22.5
                self.angle_rad_blue = degree_to_radian(self.angle_deg)
                self.draw_blue()
            if move_direction == 'right':
                self.angle_deg -= 22.5
                self.angle_rad_blue = degree_to_radian(self.angle_deg)
                self.draw_blue()
            if move_direction == 'forward':
                self.tank_y += self.speed * math.cos(self.angle_rad_blue)
                self.tank_x += self.speed * math.sin(self.angle_rad_blue)
                print 'blue tank_x: %s, blue tank_y: %s, blue angle_rad: %s' % (self.tank_x, self.tank_y, self.angle_rad_blue)


def degree_to_radian(degree):
    return degree * math.pi/180


class Map():

    def __init__(self):
        # Map definitions and dimensions.
        self.wall = 1
        self.open = 0
        self.TILESIZE = 20
        self.MAPWIDTH = 35
        self.MAPHEIGHT = 30

        # Generate blank map
        self.tilemap = [[self.open for w in range(self.MAPWIDTH)] for h in range(self.MAPHEIGHT)]

        # Add borders
        for i in range(self.MAPHEIGHT):
            self.tilemap[i][0] = self.wall
            self.tilemap[i][self.MAPWIDTH - 1] = self.wall
            if i == 0 or i == self.MAPHEIGHT - 1:
                for w in range(self.MAPWIDTH):
                    self.tilemap[i][w] = self.wall


        self.colors = {
            self.wall: WHITE,
            self.open: BLACK
        }

    def draw(self, DISPLAYSURF):
        for row in range(self.MAPHEIGHT):
                for column in range(self.MAPWIDTH):
                    pygame.draw.rect(DISPLAYSURF, self.colors[self.tilemap[row][column]],
                                     (column*self.TILESIZE, row*self.TILESIZE, self.TILESIZE, self.TILESIZE))


def main():
    """ Main function for the game. """
    pygame.init()

    # initialize the map
    game_map = Map()

    # Set the width and height of the screen [width,height]
    # size = [700, 500]
    # screen = pygame.display.set_mode(size)
    DISPLAYSURF = pygame.display.set_mode((game_map.MAPWIDTH*game_map.TILESIZE, game_map.MAPHEIGHT*game_map.TILESIZE))
    pygame.display.set_caption("Tanks")

    # initialize tank
    red_tank = Tank(50, 100, DISPLAYSURF, 'red')
    blue_tank = Tank(450, 100, DISPLAYSURF, 'blue')

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
                if event.key == pygame.K_w:
                    print 'W pressed down'
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    print 'W let up'
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            red_tank.move('left', 'red')
        if keys[pygame.K_w]:
            red_tank.move('forward', 'red')
        if keys[pygame.K_d]:
            red_tank.move('right', 'red')
        if keys[pygame.K_LEFT]:
            blue_tank.move('left', 'blue')
        if keys[pygame.K_UP]:
            blue_tank.move('forward', 'blue')
        if keys[pygame.K_RIGHT]:
            blue_tank.move('right', 'blue')


        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        red_tank.check_collision(game_map)

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        game_map.draw(DISPLAYSURF)

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