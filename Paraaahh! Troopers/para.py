"""
 Paraaahhh! Troopers

"""

import sys
import pygame
import player
import random
import math
import vehicles
import troopers
import menu
import highscores
import os
import particle


# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (5, 61, 244)
GREY = (199, 199, 199)
GREEN = (63, 177, 79)
RED = (187, 8, 0)
BROWN = (94, 56, 25)
YELLOW = (229, 255, 6)

# Score
HELI_SHOT = 50
PLANE_SHOT = 60
BOMB_SHOT = 90
PARA_SHOT = 75
TROOPER_SHOT = 25
TROOPER_DROPPED = 100


class Game():
    """The paratrooper Game class"""

    def __init__(self):

        self.highscores = highscores.HighScores()
        self.sounds = Sounds()
        self.menu = menu.Menu()
        self.menu.mainmenu()

        self.fadecolor = (63, 177, 79)
        self.state = "mainmenu"
        self.t = 1
        self.nextstate = ""
        self.wave = 1
        self.spawn_heli = False
        self.spawn_plane = False
        self.wave_timer = 100
        self.wave_timer_base = 50
        self.heli_count_base = 5
        self.heli_count = 5
        self.heli_timer = 30
        self.plane_timer = 1
        self.music = True
        self.timer = 50
        self.game_speed = 25
        self.game_speed_base = 25
        self.gameover = 0
        self.playing = False
        self.mine_count = 2
        self.reset()
        try:
            self.player_name = os.environ["USER"]
        except KeyError:
            try:
                self.player_name = os.environ["USERNAME"]
            except KeyError:
                self.player_name = "PlayerX"

    def start(self):
        self.state = "ingame"

    def menu_down(self):
        self.menu.move_down()

    def menu_up(self):
        self.menu.move_up()

    def menu_select(self):
        if self.menu.selected != None:
            newstate = self.menu.items[self.menu.selected].changestate
            if newstate == "mainmenu" and not self.playing:
                self.menu.mainmenu()
            elif newstate == "mainmenu" and self.playing:
                self.menu.ingamemenu()
            elif newstate == "credits":
                self.menu.creditsmenu()
            elif newstate == "scores":
                self.menu.highscoresmenu(self.highscores)
            elif newstate == "resetscores":
                self.highscores.reset()
                self.menu.highscoresmenu(self.highscores)
            elif newstate == "newgame":
                self.max = 30
                # self.nextstate = "reset"
                # self.state = "fadeout_y"
                self.state = 'reset'
            elif newstate == "returntogame":
                self.max = 30
                self.nextstate = "ingame"
                self.state = "fadeout_y"
            else:
                self.state = newstate

    def ingamemenu(self):
        self.state = "mainmenu"
        self.menu.ingamemenu()

    def get_current_menu(self):
        return self.menu.items

    def reset(self):
        self.score = 0
        self.gameover = 0
        self.t = 1
        self.heli_count = self.heli_count_base
        self.wave = 1
        self.timer = 50
        self.wave_timer = 150
        self.mine_count = 2
        self.game_speed = self.game_speed_base

    def game_over(self):
        self.state = "gameover"


class Sounds():

    def __init__(self):
        self.shot = pygame.mixer.Sound(os.path.join('data', 'shot1.wav'))
        self.splat = pygame.mixer.Sound(os.path.join('data', 'splat1.wav'))
        self.hit = pygame.mixer.Sound(os.path.join('data', 'trooper_hit1.wav'))
        self.aahhh = pygame.mixer.Sound(os.path.join('data', 'aahhh1.wav'))
        self.explosion = pygame.mixer.Sound(os.path.join('data', 'explosion1.wav'))
        self.base_explosion = pygame.mixer.Sound(os.path.join('data', 'base_explosion.wav'))
        self.bomb_falling = pygame.mixer.Sound(os.path.join('data', 'bomb_falling.wav'))
        self.music = pygame.mixer.Sound(os.path.join('data', 'who_likes_to_party.wav'))
        self.music.set_volume(0.3)


def display_wave(wave, wave_count, font, screen):
    wave = font.render('Wave {}: {} helicopters'.format(wave, wave_count), True, (255, 255, 255))
    wave_rect = wave.get_rect()
    wave_rect.topleft = (screen.get_width() / 2.7, screen.get_height() / 7)
    screen.blit(wave, wave_rect)


def main():
    """ Main function for the game. """
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    # Initialize sounds

    # Set the width and height of the screen [width,height]
    # screen_width, screen_height = [1024, 768]
    screen_width, screen_height = [800, 600]
    screen = pygame.display.set_mode([screen_width, screen_height], pygame.FULLSCREEN)
    # screen = pygame.display.set_mode([screen_width, screen_height])
    area = screen.get_rect()
    pygame.display.set_caption("Paraaaahhhh! Troopers")
    background = pygame.Surface((screen_width, screen_height))
    background.fill(BLACK)
    background = background.convert()

    # static load of images that are used a lot

    star1_image, star_rect = player.load_image('star01.bmp')
    star2_image, star_rect = player.load_image('star02.bmp')
    star3_image, star_rect = player.load_image('star03.bmp')
    star4_image, star_rect = player.load_image('star04.bmp')
    heli1a_image, heli_rect = player.load_image('heli1a.bmp')
    heli2a_image, heli_rect = player.load_image('heli2a.bmp')
    heli1b_image, heli_rect = player.load_image('heli1b.bmp')
    heli2b_image, heli_rect = player.load_image('heli2b.bmp')
    dude1a_image, dude_rect = player.load_image('dude01.bmp')
    dude2a_image, dude_rect = player.load_image('dude02.bmp')
    dude1b_image, dude_rect = player.load_image('dude03.bmp')
    dude2b_image, dude_rect = player.load_image('dude04.bmp')
    dude1c_image, dude_rect = player.load_image('dude05.bmp')
    dude2c_image, dude_rect = player.load_image('dude06.bmp')
    plane_image, plane_rect = player.load_image('plane.bmp')
    troop_image, troop_rect = player.load_image('trooper.bmp')
    bomb_image, bomb_rect = player.load_image('bomb.bmp')
    falling_trooper_image, falling_trooper_rect = player.load_image('trooper_falling.bmp')
    parachute_image, parachute_rect = player.load_image('chute.bmp')
    aahh_image, aahh_rect = player.load_image('aahh.bmp')

    # initialize fonts
    menufont_h1 = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 40)
    menufont_h2 = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 30)
    menufont_h3 = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 20)
    scorefont = pygame.font.Font(os.path.join('data', 'MonospaceTypewriter.ttf'), 18)

    ground = pygame.Surface((screen_width, 10))
    ground.fill(GREEN)
    ground = ground.convert()
    ground_rect = ground.get_rect()
    ground_rect.x = 0
    ground_rect.y = screen.get_height() / 1.1
    dirt = pygame.Surface((screen_width, 45))
    dirt.fill(BROWN)
    dirt = dirt.convert()
    dirt_rect = dirt.get_rect()
    dirt_rect.x = 0
    dirt_rect.y = screen.get_height() / 1.08

    # Init game
    game = Game()

    dude = player.Dude(dude1a_image, dude2a_image, dude1b_image, dude2b_image, dude1c_image, dude2c_image, dude_rect,
                       ground_rect, screen)
    dude.rect.bottom = ground_rect.top
    dude.rect.left = area.right
    dude.music = game.sounds.music

    # Init sprites
    canon = player.Turret(ground_rect)
    dude_sprite = pygame.sprite.RenderPlain(dude)
    star_sprites = pygame.sprite.RenderPlain()
    mine_sprites = pygame.sprite.RenderPlain()
    bullet_sprites = pygame.sprite.RenderPlain()
    bomb_sprites = pygame.sprite.RenderPlain()
    bomb_particle_sprites = pygame.sprite.RenderPlain()
    troop_particle_sprites = pygame.sprite.RenderPlain()
    canon_sprite = pygame.sprite.RenderPlain(canon)
    parachute_sprites = pygame.sprite.RenderPlain()
    trooper_sprites = pygame.sprite.RenderPlain()
    base_particle_sprites = pygame.sprite.RenderPlain()
    plane_sprites = pygame.sprite.RenderPlain()
    heli_sprites = pygame.sprite.RenderPlain()
    dropping_sprites = pygame.sprite.RenderPlain()
    aahh_sprites = pygame.sprite.RenderPlain()
    heli_particle_sprites = pygame.sprite.RenderPlain()
    plane_particle_sprites = pygame.sprite.RenderPlain()

    # Create stars!
    for i in range(60):
        star = vehicles.Star(star3_image, star4_image, star_rect)
        random.seed()
        star.rect.x = random.randrange(screen_width)
        star.rect.y = random.randrange(0, screen_height / 2)
        star_sprites.add(star)
    for i in range(15):
        star = vehicles.Star(star1_image, star2_image, star_rect)
        random.seed()
        star.rect.x = random.randrange(screen_width)
        star.rect.y = random.randrange(screen_height / 2, screen_height)
        star_sprites.add(star)

    # Initial drawing of everything
    screen.blit(background, (0, 0))
    canon_sprite.draw(screen)
    screen.blit(ground, ground_rect)
    screen.blit(dirt, dirt_rect)
    screen.blit(canon.canonbase, canon.canonbase_rect)
    screen.blit(canon.canontop, canon.cannontop_rect)

    canon_sprite.draw(screen)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    var = 0
    shoot = False
    shoot_lock = 6
    t = 0
    clear_events = True
    # -------- Main Program Loop -----------
    while not done:

        if game.state == 'ingame':
            game.playing = True

            if clear_events:
                pygame.event.clear()
                clear_events = False

            # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousex, mousey = event.pos
                    para = troopers.Parachute(parachute_image, parachute_rect)
                    para.rect.bottom = area.top
                    parachute_sprites.add(para)

                    trooper = troopers.Trooper(troop_image, falling_trooper_image, troop_rect, ground_rect, canon,
                                               screen)
                    trooper.rect.x = mousex
                    trooper.rect.y = mousey
                    trooper_sprites.add(trooper)

                    trooper.para = para
                    para.trooper = trooper
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    mousex, mousey = event.pos
                    newbullet = player.Bullet('bullet')
                    newbullet.direction = canon.angle
                    newbullet.image = pygame.transform.rotate(newbullet.bullet, newbullet.direction)
                    newbullet.rect = newbullet.bullet.get_rect()
                    newbullet.rect.x = mousex
                    newbullet.rect.y = mousey
                    canon_rad = canon.angle * math.pi / 180
                    newbullet.rect = newbullet.rect.move((newbullet.speed * math.cos(canon_rad),
                                                          -newbullet.speed * math.sin(canon_rad) + 20))
                    newbullet.test = 1
                    bullet_sprites.add(newbullet)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_m:
                        if game.music:
                            game.sounds.music.set_volume(0)
                            game.music = False
                        elif not game.music:
                            game.sounds.music.set_volume(0.3)
                            game.music = True
                    if event.key == pygame.K_l:
                        game.spawn_plane = True
                    if event.key == pygame.K_h:
                        game.spawn_heli = True
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        game.ingamemenu()
                    if event.key == pygame.K_LEFT and game.gameover == 0:
                            canon.move_counter_clockwise()
                            # print canon.state
                            # print canon.angle
                            # print 'going counter clockwise'
                    elif event.key == pygame.K_RIGHT and game.gameover == 0:
                        canon.move_clockwise()
                        # print canon.state
                        # print canon.angle
                        # print 'going clockwise'
                    elif event.key == pygame.K_SPACE and game.gameover == 0:
                        shoot = True
                        t = 0
                elif event.type == pygame.KEYUP and game.gameover == 0:
                    if event.key == pygame.K_LEFT and canon.state == 'counterclockwise':
                        canon.halt()
                    elif event.key == pygame.K_RIGHT and canon.state == 'clockwise':
                        canon.halt()
                    elif event.key == pygame.K_SPACE:
                        t = 0
                        shoot = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                random.seed()
                var = random.randint(-40, 40)
                shoot = True

            # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

            # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
            # Create and place mines

            if game.mine_count > 0:
                bl = []
                for i in canon.canonbase_rect.bottomleft:
                    bl.append(i)
                bl[0] -= 10
                left_mine = player.Bullet('mine')
                left_mine.image = pygame.transform.rotate(left_mine.bullet, 0)
                left_mine.rect.bottomright = bl
                left_mine.test = True
                bl = []
                for i in canon.canonbase_rect.bottomright:
                    bl.append(i)
                bl[0] += 10
                right_mine = player.Bullet('mine')
                right_mine.image = pygame.transform.rotate(right_mine.bullet, 0)
                right_mine.rect.bottomleft = bl

                right_mine.test = True
                mine_sprites.add(left_mine)
                mine_sprites.add(right_mine)
                game.mine_count = 0

            if shoot and t % shoot_lock == 0 and game.gameover == 0:
                #shoot a bullet
                print var
                newbullet = player.Bullet('bullet')
                newbullet.direction = canon.angle
                newbullet.image = pygame.transform.rotate(newbullet.bullet, newbullet.direction)
                newbullet.rect = newbullet.bullet.get_rect()
                newbullet.rect.midbottom = canon.rect.midtop
                canon_rad = (canon.angle + var) * math.pi / 180
                newbullet.rect = newbullet.rect.move((newbullet.speed * math.cos(canon_rad),
                                                      -newbullet.speed * math.sin(canon_rad) + 20))
                bullet_sprites.add(newbullet)
                t = 0
                game.sounds.shot.play()
            t += 1

            # Wave timer countdown
            game.wave_timer -= 1


            # should there be a new plane?
            # if game.wave_timer <= 0:
                # game.plane_timer -= 1
            if game.wave % 4 == 3 and game.wave > 2 and game.plane_timer or game.spawn_plane:
                plane = vehicles.Plane(plane_image, plane_rect)
                if random.randrange(0, 2) == 1:
                    random.seed()
                    plane.rect.topleft = area.topright
                    plane.rect = plane.rect.move((0, random.randint(3, 10)))
                    plane.direction = -1
                else:
                    random.seed()
                    plane.rect.topright = area.topleft
                    plane.rect = plane.rect.move((0, random.randrange(60, 70)))
                    plane.flip_images()
                    plane.direction = 1
                plane_sprites.add(plane)
                # game.plane_timer = random.randint(100, 120)
                game.plane_timer = 0
                game.spawn_plane = False

            for plane in plane_sprites.sprites():
                if plane.rect.left > area.right and plane.direction == 1:
                    plane_sprites.remove(plane)
                elif plane.rect.right < area.left and plane.direction == -1:
                    plane_sprites.remove(plane)

            # should the plane drop a bomb?
            for plane in plane_sprites.sprites():
                if not plane.bomb_released:
                    if (plane.direction == 1 and plane.rect.centerx > plane.random_x) or \
                            (plane.direction == -1 and plane.rect.centerx < plane.random_x + 450):
                        bomb = vehicles.Bomb(bomb_image, bomb_rect)
                        bomb.rect.midtop = plane.rect.midbottom
                        bomb.speed = plane.speed
                        bomb.rad = math.atan2(canon.cannontop_rect.centery - bomb.rect.centery,
                                              canon.cannontop_rect.centerx - bomb.rect.centerx)
                        bomb.dx, bomb.dy = bomb.speed * math.cos(bomb.rad), bomb.speed * math.sin(bomb.rad)
                        bomb_sprites.add(bomb)
                        game.sounds.bomb_falling.play()
                        plane.bomb_released = True

            # should there be a new heli?
            if game.heli_count > 0 and game.wave_timer <= 0 or game.spawn_heli:
                game.heli_timer -= 1
                if game.heli_timer <= 0:
                    heli = vehicles.Helicopter(heli1a_image, heli2a_image, heli1b_image, heli2b_image, heli_rect)
                    if random.randrange(0, 2) == 1:
                        random.seed()
                        heli.rect.topleft = area.topright
                        heli.rect = heli.rect.move((0, random.randint(3, 10)))
                        heli.direction = -1
                    else:
                        random.seed()
                        heli.rect.topright = area.topleft
                        heli.rect = heli.rect.move((0, random.randrange(60, 70)))
                        heli.flip_images()
                        heli.direction = 1
                    heli_sprites.add(heli)
                    game.heli_count -= 1
                    game.heli_timer = random.randint(20, 40)
            elif game.heli_count == 0 and len(heli_sprites) == 0:
                game.heli_count = game.heli_count_base + game.wave
                game.wave += 1
                game.heli_timer = 50
                game.wave_timer = 100
                game.plane_timer = 1
                game.spawn_heli = False
                game.game_speed += 1

            for heli in heli_sprites.sprites():
                if heli.rect.left > area.right and heli.direction == 1:
                    heli_sprites.remove(heli)
                elif heli.rect.right < area.left and heli.direction == -1:
                    heli_sprites.remove(heli)
                elif heli.trooper:
                    if (heli.direction == 1 and heli.rect.centerx > heli.random_x) \
                            or (heli.direction == -1 and heli.rect.centerx < heli.random_x):
                        para = troopers.Parachute(parachute_image, parachute_rect)
                        para.rect.bottom = area.top
                        parachute_sprites.add(para)

                        trooper = troopers.Trooper(troop_image, falling_trooper_image, troop_rect, ground_rect, canon,
                                                   screen)
                        trooper.rect.midtop = heli.rect.midbottom
                        trooper_sprites.add(trooper)
                        print 'trooper x {}'.format(trooper.rect.x)

                        trooper.para = para
                        para.trooper = trooper
                        heli.trooper = False

            # Did a bullet hit a helicopter?
            heli_killed_dict = pygame.sprite.groupcollide(bullet_sprites, heli_sprites, 1, 1)
            for bullet in heli_killed_dict:
                screen.blit(background, bullet.rect, bullet.rect)
                for heli in heli_killed_dict:
                    screen.blit(background, heli.rect, heli.rect)
                    game.score += HELI_SHOT
                    game.sounds.explosion.play()
                    for i in range(10):
                        part = particle.Particle(heli.rect.centerx, heli.rect.centery, YELLOW, 'heli')
                        part.image = pygame.transform.rotate(part.particle, part.direction)
                        heli_particle_sprites.add(part)

            # Did a bullet hit a plane?
            plane_killed_dict = pygame.sprite.groupcollide(bullet_sprites, plane_sprites, 1, 1)
            for bullet in plane_killed_dict:
                screen.blit(background, bullet.rect, bullet.rect)
                for plane in plane_killed_dict:
                    screen.blit(background, plane.rect, plane.rect)
                    game.score += PLANE_SHOT
                    game.sounds.explosion.play()
                    for i in range(10):
                        part = particle.Particle(plane.rect.centerx, plane.rect.centery, YELLOW, 'plane')
                        part.image = pygame.transform.rotate(part.particle, part.direction)
                        plane_particle_sprites.add(part)

            # Did a bullet hit a trooper?
            trooper_killed_dict = pygame.sprite.groupcollide(bullet_sprites, trooper_sprites, 1, 1)
            for bullet in trooper_killed_dict:
                screen.blit(background, bullet.rect, bullet.rect)
                for trooper in trooper_killed_dict[bullet]:
                    screen.blit(background, trooper.rect, trooper.rect)
                    screen.blit(background, trooper.para.rect, trooper.para.rect)
                    parachute_sprites.remove(trooper.para)
                    if trooper.sound:
                        trooper.sound.stop()
                    game.sounds.hit.play()
                    if trooper.chute_shot:
                        aahh_sprites.remove(trooper.aahh)
                        screen.blit(background, trooper.aahh.rect, trooper.aahh.rect)
                    game.score += TROOPER_SHOT
                    for troop in trooper_sprites.sprites():
                        if troop.in_pyramid:
                            troop.in_pyramid = False
                            troop.rect.bottom = ground_rect.top
                    for i in range(10):
                        part = particle.Particle(trooper.rect.centerx, trooper.rect.centery, RED, 'trooper')
                        part.image = pygame.transform.rotate(part.particle, part.direction)
                        troop_particle_sprites.add(part)

            # Did a mine hit a trooper?
            trooper_killed_dict = pygame.sprite.groupcollide(mine_sprites, trooper_sprites, 1, 1)
            for mine in trooper_killed_dict:
                screen.blit(background, mine.rect, mine.rect)
                for trooper in trooper_killed_dict[mine]:
                    screen.blit(background, trooper.rect, trooper.rect)
                    screen.blit(background, trooper.para.rect, trooper.para.rect)
                    parachute_sprites.remove(trooper.para)
                    game.sounds.hit.play()
                    if trooper.chute_shot:
                        aahh_sprites.remove(trooper.aahh)
                        screen.blit(background, trooper.aahh.rect, trooper.aahh.rect)
                    game.score += TROOPER_SHOT
                    for troop in trooper_sprites.sprites():
                        if troop.in_pyramid:
                            troop.in_pyramid = False
                            troop.rect.bottom = ground_rect.top
                    for i in range(10):
                        part = particle.Particle(trooper.rect.centerx, trooper.rect.centery, RED, 'trooper')
                        part.image = pygame.transform.rotate(part.particle, part.direction)
                        troop_particle_sprites.add(part)

            # Did heli shrapnel hit a trooper?
            trooper_killed_dict = pygame.sprite.groupcollide(heli_particle_sprites, trooper_sprites, 1, 1)
            for part in trooper_killed_dict:
                screen.blit(background, part.rect, part.rect)
                for trooper in trooper_killed_dict[part]:
                    screen.blit(background, trooper.rect, trooper.rect)
                    screen.blit(background, trooper.para.rect, trooper.para.rect)
                    parachute_sprites.remove(trooper.para)
                    game.sounds.hit.play()
                    if trooper.chute_shot:
                        aahh_sprites.remove(trooper.aahh)
                        screen.blit(background, trooper.aahh.rect, trooper.aahh.rect)
                    game.score += TROOPER_SHOT
                    if trooper.sound:
                        trooper.sound.stop()

            # Did a bullet hit a parachute?
            para_hit_dict = pygame.sprite.groupcollide(bullet_sprites, parachute_sprites, 0, 1)
            for bullet in para_hit_dict:
                screen.blit(background, bullet.rect, bullet.rect)
                for para in para_hit_dict[bullet]:
                    screen.blit(background, para.rect, para.rect)
                    para.trooper.speed = 4
                    para.trooper.chute_shot = True
                    para.trooper.chute_attached = False
                    dropping_sprites.add(para.trooper)
                    game.score += PARA_SHOT
                    aahh = troopers.Aahh(aahh_image, aahh_rect)
                    aahh_sprites.add(aahh)
                    para.trooper.aahh = aahh
                    para.trooper.sound = game.sounds.aahhh
                    para.trooper.sound.play()

            # Did a bullet hit a bomb?
            bomb_hit_dict = pygame.sprite.groupcollide(bullet_sprites, bomb_sprites, 1, 1)
            for bullet in bomb_hit_dict:
                screen.blit(background, bullet.rect, bullet.rect)
                for bomb in bomb_hit_dict[bullet]:
                    screen.blit(background, bomb.rect, bomb.rect)
                    game.sounds.bomb_falling.stop()
                    game.sounds.explosion.play()
                    game.score += BOMB_SHOT
                    for i in range(5):
                        part = particle.Particle(bomb.rect.centerx, bomb.rect.centery, GREY, 'bomb')
                        part.image = pygame.transform.rotate(part.particle, part.direction)
                        bomb_particle_sprites.add(part)

            # Did heli shrapnel hit a parachute?
            para_hit_dict = pygame.sprite.groupcollide(heli_particle_sprites, parachute_sprites, 0, 1)
            for part in para_hit_dict:
                screen.blit(background, part.rect, part.rect)
                for para in para_hit_dict[part]:
                    screen.blit(background, para.rect, para.rect)
                    para.trooper.speed = 4
                    para.trooper.chute_shot = True
                    para.trooper.chute_attached = False
                    dropping_sprites.add(para.trooper)
                    game.score += PARA_SHOT
                    aahh = troopers.Aahh(aahh_image, aahh_rect)
                    aahh_sprites.add(aahh)
                    para.trooper.aahh = aahh
                    game.sounds.aahhh.play()

            # Did the falling guy die?
            for trooper in dropping_sprites.sprites():
                if trooper.falling == 0:
                    dropping_sprites.remove(trooper)
                    trooper_sprites.remove(trooper)
                    aahh_sprites.remove(trooper.aahh)
                    screen.blit(background, trooper.rect, trooper.rect)
                    screen.blit(background, trooper.aahh.rect, trooper.aahh.rect)
                    game.sounds.splat.play()
                    for i in range(10):
                        part = particle.Particle(trooper.rect.centerx, trooper.rect.centery, RED, 'trooper')
                        part.image = pygame.transform.rotate(part.particle, part.direction)
                        troop_particle_sprites.add(part)
                    game.score += TROOPER_DROPPED

            # Did the falling guy fall on another guy?
            hit_trooper = pygame.sprite.groupcollide(dropping_sprites, trooper_sprites, 0, 0)
            for trooper in hit_trooper:
                for hittrooper in hit_trooper[trooper]:
                    if trooper != hittrooper:
                        dropping_sprites.remove(trooper)
                        trooper_sprites.remove(trooper)
                        trooper_sprites.remove(hittrooper)
                        aahh_sprites.remove(trooper.aahh)
                        hittrooper.para.remove_please = 1
                        screen.blit(background, trooper.rect, trooper.rect)
                        screen.blit(background, hittrooper.rect, hittrooper.rect)
                        screen.blit(background, trooper.aahh.rect, trooper.aahh.rect)
                        for i in range(10):
                            part = particle.Particle(trooper.rect.centerx, trooper.rect.centery, RED, 'trooper')
                            part.image = pygame.transform.rotate(part.particle, part.direction)
                            troop_particle_sprites.add(part)
                        game.score += TROOPER_DROPPED
                        game.sounds.splat.play()
                        game.sounds.hit.play()
                        for troop in trooper_sprites.sprites():
                            if troop.in_pyramid:
                                troop.in_pyramid = False
                                troop.rect.bottom = ground_rect.top

            # Should we remove any parachutes?
            for para in parachute_sprites.sprites():
                if para.remove_please:
                    screen.blit(background, para.rect, para.rect)
                    parachute_sprites.remove(para)

            # Should we remove any bullets?
            for bullet in bullet_sprites.sprites():
                if bullet.remove_please:
                    screen.blit(background, bullet.rect, bullet.rect)
                    bullet_sprites.remove(bullet)

            # Should we remove any particles?
            for part in troop_particle_sprites:
                if part.timer <= 0:
                    screen.blit(background, part.rect, part.rect)
                    troop_particle_sprites.remove(part)
            for part in heli_particle_sprites:
                if part.timer <= 0:
                    screen.blit(background, part.rect, part.rect)
                    heli_particle_sprites.remove(part)
            for part in plane_particle_sprites.sprites():
                if part.timer <= 0:
                    screen.blit(background, part.rect, part.rect)
                    plane_particle_sprites.remove(part)
            for part in bomb_particle_sprites.sprites():
                if part.timer <= 0:
                    screen.blit(background, part.rect, part.rect)
                    bomb_particle_sprites.remove(part)

            # Can a trooper move?
            left_nearest_dude = None
            right_nearest_dude = None
            left_side_dudes = []
            right_side_dudes = []
            left_pyramid = 0
            right_pyramid = 0

            for trooper in trooper_sprites.sprites():
                if trooper.stopped:
                    if trooper.rect.right < area.centerx:
                        left_side_dudes.append(trooper)
                    elif trooper.rect.left > area.centerx:
                        right_side_dudes.append(trooper)
            # print len(game.climbers_l)
            if len(left_side_dudes) >= 4:
                for d in left_side_dudes:
                    if not d.in_pyramid:
                        if not left_nearest_dude:
                            left_nearest_dude = d
                        else:
                            if d.rect.right > left_nearest_dude.rect.right:
                                left_nearest_dude = d
                    else:
                        left_pyramid += 1
            if left_nearest_dude:
                if left_pyramid == 0:
                    if left_nearest_dude.rect.right + left_nearest_dude.speed < left_nearest_dude.area.centerx - 50:
                        left_nearest_dude.rect = left_nearest_dude.rect.move((left_nearest_dude.speed, 0))
                        # print 'moving right'
                    else:
                        left_nearest_dude.rect.right = left_nearest_dude.area.centerx - 50
                        left_nearest_dude.in_pyramid = 1
                elif left_pyramid == 1:
                    if left_nearest_dude.rect.right + left_nearest_dude.speed < left_nearest_dude.area.centerx - 66:
                        left_nearest_dude.rect = left_nearest_dude.rect.move((left_nearest_dude.speed, 0))
                        # print 'moving right 2'
                    else:
                        left_nearest_dude.rect.right = left_nearest_dude.area.centerx - 66
                        left_nearest_dude.in_pyramid = 1
                        # print 'stopped 2'
                elif left_pyramid == 2:
                    if left_nearest_dude.rect.bottom == left_nearest_dude.ground.top:
                        if left_nearest_dude.rect.right + left_nearest_dude.speed < left_nearest_dude.area.centerx - 82:
                            left_nearest_dude.rect = left_nearest_dude.rect.move((left_nearest_dude.speed, 0))
                            # print 'moving right 3'
                        else:
                            left_nearest_dude.rect.right = left_nearest_dude.area.centerx - 82
                            left_nearest_dude.rect = left_nearest_dude.rect.move((0, -31))
                            left_nearest_dude.climbing = 1
                            # print 'moving up 3'
                    elif left_nearest_dude.rect.bottom == left_nearest_dude.ground.top - 31:
                        if left_nearest_dude.rect.right + left_nearest_dude.speed < left_nearest_dude.area.centerx - 50:
                            left_nearest_dude.rect = left_nearest_dude.rect.move((left_nearest_dude.speed, 0))
                        else:
                            left_nearest_dude.rect.right = left_nearest_dude.area.centerx - 50
                            left_nearest_dude.in_pyramid = 1
                            # print 'stopped 3'
                elif left_pyramid == 3:
                    if left_nearest_dude.rect.bottom == left_nearest_dude.ground.top:
                        if left_nearest_dude.rect.right + left_nearest_dude.speed < left_nearest_dude.area.centerx - 82:
                            left_nearest_dude.rect = left_nearest_dude.rect.move((left_nearest_dude.speed, 0))
                            # print 'moving right ground 4'
                        else:
                            left_nearest_dude.rect.right = left_nearest_dude.area.centerx - 82
                            left_nearest_dude.rect = left_nearest_dude.rect.move((0, -31))
                            left_nearest_dude.climbing = 1
                            # print 'moving up 4'
                    elif left_nearest_dude.rect.bottom == left_nearest_dude.ground.top - 31:
                        if left_nearest_dude.rect.right + left_nearest_dude.speed < left_nearest_dude.area.centerx - 66:
                            left_nearest_dude.rect = left_nearest_dude.rect.move((left_nearest_dude.speed, 0))
                            # print 'moving right guys 4'
                        else:
                            left_nearest_dude.rect.right = left_nearest_dude.area.centerx - 66
                            left_nearest_dude.rect = left_nearest_dude.rect.move((0, -31))
                            # print 'movi/ng up 4'
                    elif left_nearest_dude.rect.bottom == left_nearest_dude.ground.top - 62:
                        if left_nearest_dude.rect.right + left_nearest_dude.speed < left_nearest_dude.area.centerx - 25:
                            left_nearest_dude.rect = left_nearest_dude.rect.move((left_nearest_dude.speed, 0))
                            # print 'moving/ right almost done'
                        else:
                            left_nearest_dude.rect.right = left_nearest_dude.area.centerx - 25
                            left_nearest_dude.winner = 1

            if len(right_side_dudes) >= 4:
                for d in right_side_dudes:
                    if not d.in_pyramid:
                        if not right_nearest_dude:
                            right_nearest_dude = d
                        else:
                            if d.rect.left < right_nearest_dude.rect.left:
                                right_nearest_dude = d
                    else:
                        right_pyramid += 1
            if right_nearest_dude:
                if right_pyramid == 0:
                    if right_nearest_dude.rect.right + right_nearest_dude.speed > right_nearest_dude.area.centerx + 70:
                        right_nearest_dude.rect = right_nearest_dude.rect.move((right_nearest_dude.speed * -1, 0))
                        # print 'moving right'
                    else:
                        right_nearest_dude.rect.right = right_nearest_dude.area.centerx + 66
                        right_nearest_dude.in_pyramid = 1
                elif right_pyramid == 1:
                    if right_nearest_dude.rect.right + right_nearest_dude.speed > right_nearest_dude.area.centerx + 85:
                        right_nearest_dude.rect = right_nearest_dude.rect.move((right_nearest_dude.speed * -1, 0))
                        # print 'moving right 2'
                    else:
                        right_nearest_dude.rect.right = right_nearest_dude.area.centerx + 82
                        right_nearest_dude.in_pyramid = 1
                        # print 'stopped 2'
                elif right_pyramid == 2:
                    if right_nearest_dude.rect.bottom == right_nearest_dude.ground.top:
                        if right_nearest_dude.rect.right + right_nearest_dude.speed > right_nearest_dude.area.centerx + \
                                101:
                            right_nearest_dude.rect = right_nearest_dude.rect.move((right_nearest_dude.speed * -1, 0))
                            # print 'moving right 3'
                        else:
                            right_nearest_dude.rect.right = right_nearest_dude.area.centerx + 98
                            right_nearest_dude.rect = right_nearest_dude.rect.move((0, -31))
                            right_nearest_dude.climbing = 1
                            # print 'moving up 3'
                    elif right_nearest_dude.rect.bottom == right_nearest_dude.ground.top - 31:
                        if right_nearest_dude.rect.right + right_nearest_dude.speed > right_nearest_dude.area.centerx + \
                                70:
                            right_nearest_dude.rect = right_nearest_dude.rect.move((right_nearest_dude.speed * -1, 0))
                        else:
                            right_nearest_dude.rect.right = right_nearest_dude.area.centerx + 66
                            right_nearest_dude.in_pyramid = 1
                            # print 'stopped 3'
                elif right_pyramid == 3:
                    if right_nearest_dude.rect.bottom == right_nearest_dude.ground.top:
                        if right_nearest_dude.rect.right + right_nearest_dude.speed > right_nearest_dude.area.centerx + \
                                101:
                            right_nearest_dude.rect = right_nearest_dude.rect.move((right_nearest_dude.speed * -1, 0))
                            # print 'moving right ground 4'
                        else:
                            right_nearest_dude.rect.right = right_nearest_dude.area.centerx + 98
                            right_nearest_dude.rect = right_nearest_dude.rect.move((0, -31))
                            right_nearest_dude.climbing = 1
                            # print 'moving up 4'
                    elif right_nearest_dude.rect.bottom == right_nearest_dude.ground.top - 31:
                        if right_nearest_dude.rect.right + right_nearest_dude.speed > right_nearest_dude.area.centerx + \
                                82:
                            right_nearest_dude.rect = right_nearest_dude.rect.move((right_nearest_dude.speed * -1, 0))
                            # print 'moving right guys 4'
                        else:
                            right_nearest_dude.rect.right = right_nearest_dude.area.centerx + 82
                            right_nearest_dude.rect = right_nearest_dude.rect.move((0, -31))
                            # print 'moving up 4'
                    elif right_nearest_dude.rect.bottom == right_nearest_dude.ground.top - 62:
                        if right_nearest_dude.rect.right + right_nearest_dude.speed > right_nearest_dude.area.centerx + \
                                50:
                            right_nearest_dude.rect = right_nearest_dude.rect.move((right_nearest_dude.speed * -1, 0))
                            # print 'moving right almost done'
                        else:
                            right_nearest_dude.rect.right = right_nearest_dude.area.centerx + 45
                            right_nearest_dude.winner = 1

            # Check for winner
            for trooper in trooper_sprites.sprites():
                if trooper.winner and game.gameover == 0:
                    game.sounds.base_explosion.play()
                    screen.blit(background, canon.rect, canon.rect)
                    canon_sprite.remove(canon)
                    for i in range(100):
                        part = particle.Particle(canon.cannontop_rect.centerx - 20, canon.cannontop_rect.centery,
                                                 random.choice((RED, YELLOW)), 'base')
                        part.image = pygame.transform.rotate(part.particle, part.direction)
                        base_particle_sprites.add(part)
                    game.gameover = 1

            # did the bomb hit the base?
            for bomb in bomb_sprites.sprites():
                if bomb.rect.colliderect(canon.cannontop_rect):
                    bomb_sprites.remove(bomb)
                    screen.blit(background, bomb.rect, bomb.rect)
                    screen.blit(background, canon.rect, canon.rect)
                    canon_sprite.remove(canon)
                    game.sounds.bomb_falling.stop()
                    game.sounds.explosion.play()
                    for i in range(50):
                        part = particle.Particle(canon.cannontop_rect.centerx - 20, canon.cannontop_rect.centery,
                                                 random.choice((RED, YELLOW)), 'base')
                        part.image = pygame.transform.rotate(part.particle, part.direction)
                        base_particle_sprites.add(part)
                    game.sounds.base_explosion.play()
                    game.gameover = 1

            if game.gameover == 1:
                canon.halt()
                game.timer -= 1
                if game.timer <= 0:
                    game.game_over()

            canon_sprite.update()
            base_particle_sprites.update()
            bullet_sprites.update()
            heli_sprites.update()
            plane_sprites.update()
            trooper_sprites.update()
            bomb_sprites.update()
            heli_particle_sprites.update()
            troop_particle_sprites.update()
            plane_particle_sprites.update()
            bomb_particle_sprites.update()
            star_sprites.update()
            dude_sprite.update()

            # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

            screen.blit(background, (0, 0))
            star_sprites.draw(screen)
            canon_sprite.draw(screen)
            bullet_sprites.draw(screen)
            heli_sprites.draw(screen)
            plane_sprites.draw(screen)
            mine_sprites.draw(screen)
            bomb_particle_sprites.draw(screen)
            plane_particle_sprites.draw(screen)
            parachute_sprites.draw(screen)
            trooper_sprites.draw(screen)
            aahh_sprites.draw(screen)
            heli_particle_sprites.draw(screen)
            bomb_sprites.draw(screen)
            screen.blit(ground, ground_rect)
            screen.blit(dirt, dirt_rect)
            game.highscores.display_high(scorefont, screen, game.score)
            if game.wave_timer > 0:
                display_wave(game.wave, game.heli_count, scorefont, screen)
            screen.blit(canon.canonbase, canon.canonbase_rect)
            if game.gameover == 0:
                screen.blit(canon.canontop, canon.cannontop_rect)
            troop_particle_sprites.draw(screen)
            base_particle_sprites.draw(screen)
            if not dude.hide:
                dude_sprite.draw(screen)


            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # Limit to 25 frames per second
            clock.tick(game.game_speed)

        elif game.state == 'mainmenu':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.menu_up()
                    elif event.key == pygame.K_DOWN:
                        game.menu_down()
                    elif event.key == pygame.K_q:
                        sys.exit()
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        game.menu_select()
                    elif event.key == pygame.K_p and game.playing:
                        game.state = 'ingame'

            screen.blit(background, (0, 0))

            menuitems = game.get_current_menu()
            selected = game.menu.selected
            for i in range(0, len(menuitems)):
                cur = menuitems[i]
                if i != selected:
                    color = (63, 117, 79)
                else:
                    color = (63, 177, 79)
    
                if cur.align == 'center':
                    text = menufont_h1.render(cur.caption, 1, color)
                elif cur.align == 'left':
                    text = menufont_h2.render(cur.caption, 1, color)
                else:
                    text = menufont_h3.render(cur.caption, 1, color)
     
                text_rect = text.get_rect()
                text_rect = text_rect.move((0, (350 / len(menuitems)) * i + 100))
                
                #alignment
                if menuitems[i].align == 'center':
                    text_rect.centerx = area.centerx
                elif menuitems[i].align == 'left':
                    text_rect.left = area.left + 80
                else:
                    text_rect.right = area.right - 80
                screen.blit(text, text_rect)

        elif game.state == 'fadeout_y':

            dy = area.height / game.max + 1
            if game.t < game.max:
                surf = pygame.Surface((area.width, dy))
                surf.fill(game.fadecolor)
                screen.blit(surf, (0, dy * game.t))
                game.t += 1
            else:
                game.state = 'fadein_y'
                # game.state = 'ingame'
                game.t = 0

        elif game.state == 'fadein_y':
            dy = area.height / game.max + 1
            if game.t < game.max:
                rect = pygame.Rect((0, 0, area.width, dy))
                rect = rect.move((0, game.t*dy))
                screen.blit(background, rect, rect)
                game.t += 1
            else:
                screen.blit(background, (0, 0))
                # game.state = game.nextstate
                if game.gameover:
                    game.state = 'mainmenu'
                else:
                    game.state = 'ingame'
                game.nextstate = ""
                game.t = 0

        elif game.state == 'gameover':
            game.highscores.add(highscores.HighScoreEntry(game.player_name, str(game.score)))
            game.menu.highscoresmenu(game.highscores)
            if game.score > 9999999:
                game.score = 9999999
            game.highscores.save()
            game.gameover = 1
            game.playing = False

            print game.player_name + ' died with a score of ' + str(game.score)

            game.nextstate = 'mainmenu'
            game.state = 'fadein_y'

        elif game.state == 'reset':
            bullet_sprites.empty()
            heli_particle_sprites.empty()
            troop_particle_sprites.empty()
            parachute_sprites.empty()
            plane_sprites.empty()
            trooper_sprites.empty()
            dropping_sprites.empty()
            heli_sprites.empty()
            plane_sprites.empty()
            base_particle_sprites.empty()
            plane_particle_sprites.empty()
            bomb_sprites.empty()

            print 'resetting'
            canon_sprite = pygame.sprite.RenderPlain(canon)
            canon.angle = 90
            clear_events = True
            game.reset()
            game.state = 'ingame'

        elif game.state == 'quit':
            sys.exit(0)

        else:
            print 'Error: unknown game state: ', game.state
            sys.exit(2)

        pygame.display.flip()

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()