'''
Maps class for tanks game.
'''

import pygame
import pickle
import sys
import os

# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (187, 8, 0)
BLUE = (5, 61, 244)


class Map():

    def __init__(self, red_tank, blue_tank):
        # Map definitions and dimensions.
        self.wall = '1'
        self.open = '0'
        self.TILESIZE = 20
        self.MAPWIDTH = 35
        self.MAPHEIGHT = 30
        self.level_number = 1
        self.map_levels = {}

        # Import map from file

        self.tilemap = []
        filename = 'tanks_map%s.txt' % self.level_number
        with open(filename, 'rb') as f:
            self.tilemap = pickle.load(f)
            # p_map = pickle.load(f)
            red_tank.tank_x, red_tank.tank_y, red_tank.angle_rad, red_tank.tank_direction = pickle.load(f)
            blue_tank.tank_x, blue_tank.tank_y, blue_tank.angle_deg, blue_tank.angle_rad_blue = pickle.load(f)
        # self.tilemap = p_map.tilemap
        with open('map_levels', 'rb') as ml:
            self.map_levels = pickle.load(ml)

        self.colors = {
            self.wall: WHITE,
            self.open: BLACK
        }

    def draw(self, DISPLAYSURF):
        for row in range(self.MAPHEIGHT):
                for column in range(self.MAPWIDTH):
                    pygame.draw.rect(DISPLAYSURF, self.colors[self.tilemap[row][column]],
                                     (column*self.TILESIZE, row*self.TILESIZE, self.TILESIZE, self.TILESIZE))

    def save_map(self, red_tank, blue_tank):
        filename = 'tanks_map%s.txt' % self.level_number
        self.map_levels[filename] = self.level_number
        with open(filename, 'wb') as f:
            pickle.dump(self.tilemap, f)
            pickle.dump((red_tank.tank_x, red_tank.tank_y, red_tank.angle_rad, red_tank.tank_direction), f)
            pickle.dump((blue_tank.tank_x, blue_tank.tank_y, blue_tank.angle_deg, blue_tank.angle_rad_blue), f)
        with open('map_levels', 'wb') as ml:
            pickle.dump(self.map_levels, ml)

    def load_map(self, level_number, red_tank, blue_tank):
        if not level_number:
            level_number = self.level_number
        filename = 'tanks_map%s.txt' % level_number
        with open(filename, 'rb') as f:
            self.tilemap = pickle.load(f)
            red_tank.tank_x, red_tank.tank_y, red_tank.angle_rad, red_tank.tank_direction = pickle.load(f)
            blue_tank.tank_x, blue_tank.tank_y, blue_tank.angle_deg, blue_tank.angle_rad_blue = pickle.load(f)
        with open('map_levels', 'rb') as ml:
            self.map_levels = pickle.load(ml)

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

    def editor(self, map_editor, red_tank, blue_tank, length, DISPLAYSURF):
        while map_editor:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.MOUSEMOTION:
                    mousex, mousey = event.pos
                    tileX = int(mousex / self.TILESIZE)
                    tileY = int(mousey / self.TILESIZE)
                    print 'Mouse X and Y: %s, %s' % event.pos
                    print 'Converted tileX and tileY: %s. %s' % (tileX, tileY)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    # Map editor commands here
                    if event.key == pygame.K_s:
                        self.save_map(red_tank, blue_tank)
                    if event.key == pygame.K_l:
                        self.load_map(False, red_tank, blue_tank)
                    if event.key == pygame.K_COMMA:
                        self.level_number -= 1
                        if self.level_number <= 0:
                            self.level_number = 1
                    if event.key == pygame.K_PERIOD:
                        self.level_number += 1
                    if event.key == pygame.K_p:
                        map_editor = False
            mouse_keys = pygame.mouse.get_pressed()
            if mouse_keys[0]:
                mousex, mousey = event.pos
                self.add_wall(mousex, mousey)
            if mouse_keys[2]:
                mousex, mousey = event.pos
                self.remove_wall(mousex, mousey)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                if not blue_tank.hit and not red_tank.hit:
                    red_tank.move('left', 'red')
            if keys[pygame.K_w]:
                if not blue_tank.hit and not red_tank.hit:
                    red_tank.move('forward', 'red')
            if keys[pygame.K_d]:
                if not blue_tank.hit and not red_tank.hit:
                    red_tank.move('right', 'red')
            if keys[pygame.K_LEFT]:
                if not blue_tank.hit and not red_tank.hit:
                    blue_tank.move('left', 'blue')
            if keys[pygame.K_UP]:
                if not blue_tank.hit and not red_tank.hit:
                    blue_tank.move('forward', 'blue')
            if keys[pygame.K_RIGHT]:
                if not blue_tank.hit and not red_tank.hit:
                    blue_tank.move('right', 'blue')
            level_font = pygame.font.Font('visitor1.ttf', 50)
            level = level_font.render('%s' % self.level_number, True, WHITE)
            level_rect = level.get_rect()
            level_rect.topleft = ((self.MAPWIDTH * self.TILESIZE) / 2 + 40, 25)
            level_text = level_font.render('Map', True, WHITE)
            level_text_rect = level_text.get_rect()
            level_text_rect.topleft = ((self.MAPWIDTH * self.TILESIZE) / 2 - 60, 25)

            self.draw(DISPLAYSURF)
            DISPLAYSURF.blit(level, level_rect)
            DISPLAYSURF.blit(level_text, level_text_rect)
            red_tank.draw_red()
            blue_tank.draw_blue()
            pygame.display.flip()
        return map_editor, (length + pygame.time.get_ticks())