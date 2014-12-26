'''
Maps class for tanks game.  This is where the map editor magic works as well as saving and loading of maps and tank
positions.

Created by Jeremy Kenyon.  For questions contact lanthos@gmail.com.
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
        self.info = '2'
        self.TILESIZE = 20
        self.MAPWIDTH = 35
        self.MAPHEIGHT = 30
        self.level_number = 1
        self.map_levels = {}
        self.shot_types = [
            'Normal',
            'Guided',
            'Bounce'
        ]
        self.shot_type = 0

        # Import map from pickled file.  This includes tank states (angle, location).

        self.tilemap = []
        filename = 'tanks_map%s.txt' % self.level_number
        with open(filename, 'rb') as f:
            self.tilemap, self.shot_type = pickle.load(f)
            red_tank.tank_x, red_tank.tank_y, red_tank.angle_rad, red_tank.tank_direction = pickle.load(f)
            blue_tank.tank_x, blue_tank.tank_y, blue_tank.angle_deg, blue_tank.angle_rad_blue = pickle.load(f)
        with open('map_levels', 'rb') as ml:
            self.map_levels = pickle.load(ml)

        self.colors = {
            self.wall: WHITE,
            self.open: GREEN,
            self.info: BLACK
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
            pickle.dump((self.tilemap, self.shot_type), f)
            pickle.dump((red_tank.tank_x, red_tank.tank_y, red_tank.angle_rad, red_tank.tank_direction), f)
            pickle.dump((blue_tank.tank_x, blue_tank.tank_y, blue_tank.angle_deg, blue_tank.angle_rad_blue), f)
        with open('map_levels', 'wb') as ml:
            pickle.dump(self.map_levels, ml)

    def load_map(self, level_number, red_tank, blue_tank):
        if not level_number:
            level_number = self.level_number
        filename = 'tanks_map%s.txt' % level_number
        with open(filename, 'rb') as f:
            self.tilemap, self.shot_type = pickle.load(f)
            red_tank.tank_x, red_tank.tank_y, red_tank.angle_rad, red_tank.tank_direction = pickle.load(f)
            blue_tank.tank_x, blue_tank.tank_y, blue_tank.angle_deg, blue_tank.angle_rad_blue = pickle.load(f)
        with open('map_levels', 'rb') as ml:
            self.map_levels = pickle.load(ml)

    def add_wall(self, mousex, mousey):
        tileX = int(mousex / self.TILESIZE)
        tileY = int(mousey / self.TILESIZE)
        self.tilemap[tileY][tileX] = self.wall

    def remove_wall(self, mousex, mousey):
        tileX = int(mousex / self.TILESIZE)
        tileY = int(mousey / self.TILESIZE)
        if self.tilemap[tileY][tileX] == self.info:
            self.tilemap[tileY][tileX] = self.info
        else:
            self.tilemap[tileY][tileX] = self.open

    def add_info(self, mousex, mousey):
        tileX = int(mousex / self.TILESIZE)
        tileY = int(mousey / self.TILESIZE)
        self.tilemap[tileY][tileX] = self.info

    def editor(self, map_editor, red_tank, blue_tank, length, DISPLAYSURF):
        clock = pygame.time.Clock()
        while map_editor:
            for event in pygame.event.get():
                # Uncomment this if you need to determine where the mouse location is for troubleshooting things.
                # if event.type == pygame.MOUSEMOTION:
                #     mousex, mousey = event.pos
                #     tileX = int(mousex / self.TILESIZE)
                #     tileY = int(mousey / self.TILESIZE)
                #     print 'Mouse X and Y: %s, %s' % event.pos
                #     print 'Converted tileX and tileY: %s. %s' % (tileX, tileY)
                if event.type == pygame.KEYDOWN:
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
                    if event.key == pygame.K_h:
                        self.shot_type -= 1
                        if self.shot_type < 0:
                            self.shot_type = 0
                    if event.key == pygame.K_j:
                        self.shot_type += 1
                        if self.shot_type > 3:
                            self.shot_type = 3
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
            if mouse_keys[0] and keys[pygame.K_RSHIFT]:
                mousex, mousey = event.pos
                self.add_info(mousex, mousey)

            # This displays all of the text at the top of the screen so you know what's going on.
            level_font = pygame.font.Font('visitor1.ttf', 50)
            shot_font = pygame.font.Font('visitor1.ttf', 20)
            level = level_font.render('%s' % self.level_number, True, WHITE)
            level_rect = level.get_rect()
            level_rect.topleft = ((self.MAPWIDTH * self.TILESIZE) / 2 + 40, 25)
            level_text = level_font.render('Map', True, WHITE)
            level_text_rect = level_text.get_rect()
            level_text_rect.topleft = ((self.MAPWIDTH * self.TILESIZE) / 2 - 60, 25)
            display_shot = shot_font.render('Shot Type: {0}'.format(self.shot_types[self.shot_type]), True, WHITE)
            display_shot_rect = display_shot.get_rect()
            display_shot_rect.topleft = ((self.MAPWIDTH * self.TILESIZE) / 6, 10)

            self.draw(DISPLAYSURF)
            DISPLAYSURF.blit(level, level_rect)
            DISPLAYSURF.blit(level_text, level_text_rect)
            DISPLAYSURF.blit(display_shot, display_shot_rect)
            red_tank.draw_red()
            blue_tank.draw_blue()
            pygame.display.flip()
            clock.tick(20)
        return map_editor, (length + pygame.time.get_ticks())