"""
 Paratrooper class.

"""

import pygame


# Define some colors as global constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (5, 61, 244)
GREY = (199, 199, 199)
GREEN = (63, 177, 79)
RED = (187, 8, 0)


class Trooper():

    def __init__(self, screen):
        self.spritesheet = pygame.image.load('trooper.bmp').convert()
        self.spritesheet.set_colorkey(BLACK)
        self.spritesheet.convert_alpha()
        self.trooper_x = 400
        self.trooper_y = 400
        self.screen = screen

    def draw(self):
        self.screen.blit(self.spritesheet, (self.trooper_x - self.spritesheet.get_width() / 2, self.trooper_y -
                          self.spritesheet.get_height() / 2))