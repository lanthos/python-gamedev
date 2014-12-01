'''
Bullets class for tanks game.
'''

import pygame
import math


class Bullet(pygame.sprite.Sprite):

    def __init__(self, bullet_color, tank_color, DISPLAYSURF, game_map, enemy_tank, my_tank):
        super(Bullet, self).__init__()
        self.image = pygame.Surface([2, 2])
        self.image.fill(bullet_color)
        self.rect = self.image.get_rect()
        self.game_map = game_map
        self.rect.x = -100
        self.rect.y = -100
        self.tileX = int(self.rect.x / self.game_map.TILESIZE)
        self.tileY = int(self.rect.y / self.game_map.TILESIZE)
        self.speed = 6
        self.time_alive = 0
        self.angle = math.pi
        self.color = tank_color
        self.bullet_color = bullet_color
        self.DISPLAYSURF = DISPLAYSURF
        self.enemy_tank = enemy_tank
        self.my_tank = my_tank
        self.tank_hit = pygame.mixer.Sound("tank_hit.wav")

    def update(self):
        if self.time_alive > 0:
            if self.color == 'red':
                self.rect.x += self.speed * math.cos(self.angle_rad)
                self.rect.y += self.speed * math.sin(self.angle_rad)
                self.time_alive -= 1
                print 'bullet X and Y: %s, %s' % (self.rect.x, self.rect.y)
                if self.time_alive <= 0:
                    self.rect.x = -100
                    self.rect.y = -100
                    print 'bullets reset'
            if self.color == 'blue':
                self.rect.x += self.speed * math.cos(self.angle_rad_blue)
                self.rect.y -= self.speed * math.sin(self.angle_rad_blue)
                self.time_alive -= 1
                print 'bullet X and Y: %s, %s' % (self.rect.x, self.rect.y)
                if self.time_alive <= 0:
                    self.rect.x = -100
                    self.rect.y = -100
                    print 'bullets reset'
        self.tileX = int(self.rect.x / self.game_map.TILESIZE)
        self.tileY = int(self.rect.y / self.game_map.TILESIZE)
        if self.game_map.tilemap[self.tileY][self.tileX] == self.game_map.wall or self.enemy_tank.tileX == \
                self.tileX and self.enemy_tank.tileY == self.tileY:
            self.rect.x = -100
            self.rect.y = -100
            self.time_alive = 0
            if self.enemy_tank.tileX == self.tileX and self.enemy_tank.tileY == self.tileY:
                self.tank_hit.play()
                self.enemy_tank.hit = True
                self.my_tank.score += 1

    def draw(self):
        self.DISPLAYSURF.blit(self.image, (self.rect.x, self.rect.y))