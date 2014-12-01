'''
Maps class for tanks game.
'''

import pygame
import pickle

# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (187, 8, 0)
BLUE = (5, 61, 244)


class Map():

    def __init__(self):
        # Map definitions and dimensions.
        self.wall = '1'
        self.open = '0'
        self.TILESIZE = 20
        self.MAPWIDTH = 35
        self.MAPHEIGHT = 30
        self.level_number = 1

        # Import map from file

        self.tilemap = []
        with open('tanks_map1.txt', 'rb') as f:
            self.tilemap = pickle.load(f)

        self.colors = {
            self.wall: WHITE,
            self.open: BLACK
        }

    def draw(self, DISPLAYSURF):
        for row in range(self.MAPHEIGHT):
                for column in range(self.MAPWIDTH):
                    pygame.draw.rect(DISPLAYSURF, self.colors[self.tilemap[row][column]],
                                     (column*self.TILESIZE, row*self.TILESIZE, self.TILESIZE, self.TILESIZE))

    def save_map(self, level_number):
        filename = 'tanks_map%s.txt' % level_number
        with open(filename, 'wb') as f:
            pickle.dump(self.tilemap, f)

    def load_map(self, level_number):
        filename = 'tanks_map%s.txt' % level_number
        with open(filename, 'rb') as f:
            self.tilemap = pickle.load(f)

    def add_wall(self, mousex, mousey):
        tileX = int(mousex / self.TILESIZE)
        tileY = int(mousey / self.TILESIZE)
        self.tilemap[tileY][tileX] = self.wall
        print 'added tile to X: %s and Y: %s' % (tileX, tileY)
        print 'tilemap[tileY][tileX] is now: %s' % self.tilemap[tileY][tileX]

    def remove_wall(self, mousex, mousey):
        tileX = int(mousex / self.TILESIZE)
        tileY = int(mousey / self.TILESIZE)
        self.tilemap[tileY][tileX] = self.open
        print 'added tile to X: %s and Y: %s' % (tileX, tileY)
        print 'tilemap[tileY][tileX] is now: %s' % self.tilemap[tileY][tileX]