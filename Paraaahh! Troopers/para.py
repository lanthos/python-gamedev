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


# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (5, 61, 244)
GREY = (199, 199, 199)
GREEN = (63, 177, 79)
RED = (187, 8, 0)

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
        # self.sounds = Sounds()
        self.menu = menu.Menu()
        self.menu.mainmenu()

        self.fadecolor = (63, 177, 79)
        self.state = "mainmenu"
        self.t = 0
        self.max = 0
        self.nextstate = ""
        self.heli_timer = 30
        self.plane_timer = 120
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
            if newstate == "mainmenu":
                self.menu.mainmenu()
            elif newstate == "credits":
                self.menu.creditsmenu()
            elif newstate == "scores":
                self.menu.highscoresmenu(self.highscores)
            elif newstate == "newgame":
                self.max = 30
                self.nextstate = "reset"
                self.state = "fadeout_y"
            elif newstate == "returntogame":
                self.max = 30
                self.nextstate = "ingame"
                self.state = "fadein_y"
            else:
                self.state = newstate

    def ingamemenu(self):
        self.state = "mainmenu"
        self.menu.ingamemenu()

    def get_current_menu(self):
        return self.menu.items

    def reset(self):
        self.score = 0

    def game_over(self):
        self.state = "gameover"


def main():
    """ Main function for the game. """
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    # Initialize sounds

    # Set the width and height of the screen [width,height]
    screen_width, screen_height = [1024, 768]
    screen = pygame.display.set_mode([screen_width, screen_height])
    area = screen.get_rect()
    pygame.display.set_caption("Paraaaahhhh! Troopers")
    background = pygame.Surface((screen_width, screen_height))
    background.fill(BLACK)
    background = background.convert()

    # static load of images that are used a lot
    heli1a_image, heli_rect = player.load_image('heli1a.bmp')
    heli2a_image, heli_rect = player.load_image('heli2a.bmp')
    heli1b_image, heli_rect = player.load_image('heli1b.bmp')
    heli2b_image, heli_rect = player.load_image('heli2b.bmp')
    plane_image, plane_rect = player.load_image('plane.bmp')
    troop_image, troop_rect = player.load_image('trooper.bmp')
    falling_trooper_image, falling_trooper_rect = player.load_image('trooper_falling.bmp')
    parachute_image, parachute_rect = player.load_image('chute.bmp')
    aahh_image, aahh_rect = player.load_image('aahh.bmp')

    # initialize fonts
    menufont_h1 = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 50)
    menufont_h2 = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 40)
    menufont_h3 = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 30)
    scorefont = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 30)

    ground = pygame.Surface((screen_width, 10))
    ground.fill(GREEN)
    ground = ground.convert()
    ground_rect = ground.get_rect()
    ground_rect.x = 0
    ground_rect.y = screen.get_height() / 1.1

    # Init game
    game = Game()

    # Init sprites
    canon = player.Turret(ground_rect)
    bullet_sprites = pygame.sprite.RenderPlain()
    canon_sprite = pygame.sprite.RenderPlain(canon)
    parachute_sprites = pygame.sprite.RenderPlain()
    trooper_sprites = pygame.sprite.RenderPlain()
    plane_sprites = pygame.sprite.RenderPlain()
    heli_sprites = pygame.sprite.RenderPlain()
    dropping_sprites = pygame.sprite.RenderPlain()
    aahh_sprites = pygame.sprite.RenderPlain()

    # Initial drawing of everything

    screen.blit(background, (0, 0))
    canon_sprite.draw(screen)
    screen.blit(ground, ground_rect)
    screen.blit(canon.canonbase, canon.canonbase_rect)
    screen.blit(canon.canontop, canon.cannontop_rect)

    canon_sprite.draw(screen)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()


    shoot = False
    shoot_lock = 6
    t = 0

    # -------- Main Program Loop -----------
    while not done:

        if game.state == 'ingame':

            # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousex, mousey = event.pos
                    para = troopers.Parachute(parachute_image, parachute_rect)
                    para.rect.bottom = area.top
                    parachute_sprites.add(para)

                    trooper = troopers.Trooper(troop_image, falling_trooper_image, troop_rect, ground_rect, canon)
                    trooper.rect.x = mousex
                    trooper.rect.y = mousey
                    trooper_sprites.add(trooper)

                    trooper.para = para
                    para.trooper = trooper
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    mousex, mousey = event.pos
                    newbullet = player.Bullet()
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
                    if event.key == pygame.K_ESCAPE:
                        game.ingamemenu()
                    if event.key == pygame.K_LEFT:
                            canon.move_counter_clockwise()
                            # print canon.state
                            # print canon.angle
                            # print 'going counter clockwise'
                    elif event.key == pygame.K_RIGHT:
                        canon.move_clockwise()
                        # print canon.state
                        # print canon.angle
                        # print 'going clockwise'
                    elif event.key == pygame.K_SPACE:
                        shoot = True
                        t = 0
                    elif event.key == pygame.K_p:
                        trooper = troopers.Trooper(troop_image, troop_rect, ground_rect)
                        trooper.rect.bottom = area.bottom - 560
                        trooper.rect.x = random.randint(area.left + 5, area.right - 20)
                        trooper_sprites.add(trooper)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and canon.state == 'counterclockwise':
                        canon.halt()
                    elif event.key == pygame.K_RIGHT and canon.state == 'clockwise':
                        canon.halt()
                    elif event.key == pygame.K_SPACE:
                        t = 0
                        shoot = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                shoot = True

            # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

            # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
            if shoot and t % shoot_lock == 0:
                #shoot a bullet
                newbullet = player.Bullet()
                newbullet.direction = canon.angle
                newbullet.image = pygame.transform.rotate(newbullet.bullet, newbullet.direction)
                newbullet.rect = newbullet.bullet.get_rect()
                newbullet.rect.midbottom = canon.rect.midtop
                canon_rad = canon.angle * math.pi / 180
                newbullet.rect = newbullet.rect.move((newbullet.speed * math.cos(canon_rad),
                                                      -newbullet.speed * math.sin(canon_rad) + 20))
                bullet_sprites.add(newbullet)
                t = 0
            t += 1

            # should there be a new heli?  Setup a count down timer and if it's above zero do a count down min and max range
            if random.randrange(0, game.heli_timer) == 1:
                heli = vehicles.Helicopter(heli1a_image, heli2a_image, heli1b_image, heli2b_image, heli_rect)
                if random.randrange(0, 2) == 1:
                    heli.rect.topright = area.topright
                    heli.direction = -1
                else:
                    heli.rect.topleft = area.topleft
                    heli.rect = heli.rect.move((0, 62))
                    heli.flip_images()
                    heli.direction = 1
                heli_sprites.add(heli)
                game.heli_timer = 30

            for heli in heli_sprites.sprites():
                if heli.rect.right > canon.canonbase_rect.left and heli.rect.left < canon.canonbase_rect.right:
                    heli.dz = True
                else:
                    heli.dz = False
                if heli.rect.left > area.right and heli.direction == 1:
                    heli_sprites.remove(heli)
                elif heli.rect.right < area.left and heli.direction == -1:
                    heli_sprites.remove(heli)
                elif heli.trooper and not heli.dz:
                    if heli.trooper_chance < 1:
                        heli.trooper_chance = 1
                    if random.randrange(0, heli.trooper_chance) == 1:
                        para = troopers.Parachute(parachute_image, parachute_rect)
                        para.rect.bottom = area.top
                        parachute_sprites.add(para)

                        trooper = troopers.Trooper(troop_image, falling_trooper_image, troop_rect, ground_rect, canon)
                        trooper.rect.midtop = heli.rect.midbottom
                        trooper_sprites.add(trooper)

                        trooper.para = para
                        para.trooper = trooper
                        heli.trooper = False
                    heli.trooper_chance -= 1

            # Did a bullet hit a helicopter?
            heli_killed_dict = pygame.sprite.groupcollide(bullet_sprites, heli_sprites, 1, 1)
            for bullet in heli_killed_dict:
                screen.blit(background, bullet.rect, bullet.rect)
                for heli in heli_killed_dict:
                    screen.blit(background, heli.rect, heli.rect)
                    game.score += HELI_SHOT

            # Did a bullet hit a trooper?
            trooper_killed_dict = pygame.sprite.groupcollide(bullet_sprites, trooper_sprites, 1, 1)
            for bullet in trooper_killed_dict:
                screen.blit(background, bullet.rect, bullet.rect)
                for trooper in trooper_killed_dict[bullet]:
                    screen.blit(background, trooper.rect, trooper.rect)
                    screen.blit(background, trooper.para.rect, trooper.para.rect)
                    parachute_sprites.remove(trooper.para)
                    if trooper.chute_shot:
                        aahh_sprites.remove(trooper.aahh)
                        screen.blit(background, trooper.aahh.rect, trooper.aahh.rect)
                    game.score += TROOPER_SHOT

            # Did a bullet hit a parachute?
            para_hit_dict = pygame.sprite.groupcollide(bullet_sprites, parachute_sprites, 1, 1)
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

            # Did the falling guy die?
            for trooper in dropping_sprites.sprites():
                if trooper.falling == 0:
                    dropping_sprites.remove(trooper)
                    trooper_sprites.remove(trooper)
                    aahh_sprites.remove(trooper.aahh)
                    screen.blit(background, trooper.rect, trooper.rect)
                    screen.blit(background, trooper.aahh.rect, trooper.aahh.rect)
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
                        screen.blit(background, trooper.rect, trooper.rect)
                        screen.blit(background, hittrooper.rect, hittrooper.rect)
                        screen.blit(background, trooper.aahh.rect, trooper.aahh.rect)
                        game.score += TROOPER_DROPPED

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

            # Can a trooper move?
            game.climbers_l = []
            game.climbers_r = []

            for trooper in trooper_sprites.sprites():
                if trooper.stopped:
                    if trooper.rect.right < canon.canonbase_rect.left and trooper not in game.climbers_l:
                        game.climbers_l.append(trooper)
                        if len(game.climbers_l) > 3:
                            count = 1
                            for troop in game.climbers_l:
                                troop.number = count
                                troop.side = 'left'
                                count += count
                    elif trooper.rect.left > canon.canonbase_rect.right and trooper not in game.climbers_r:
                        game.climbers_r.append(trooper)
                        if len(game.climbers_r) > 3:
                            count = 1
                            for troop in game.climbers_r:
                                troop.number = count
                                troop.side = 'right'
                                count += count
                    if trooper.winner:
                        game.game_over()


            canon_sprite.update()
            bullet_sprites.update()
            heli_sprites.update()
            trooper_sprites.update()

            # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

            screen.blit(background, (0, 0))
            game.highscores.display_high(scorefont, screen, game.score,)
            canon_sprite.draw(screen)
            bullet_sprites.draw(screen)
            heli_sprites.draw(screen)
            parachute_sprites.draw(screen)
            trooper_sprites.draw(screen)
            aahh_sprites.draw(screen)
            screen.blit(ground, ground_rect)
            screen.blit(canon.canonbase, canon.canonbase_rect)
            screen.blit(canon.canontop, canon.cannontop_rect)


            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # Limit to 20 frames per second
            clock.tick(25)

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
                    elif event.key == pygame.K_RETURN:
                        game.menu_select()

            screen.blit(background, (0, 100))
            
            
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
                text_rect = text_rect.move((0, (300 / len(menuitems)) * i + 100))
                
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
                # explosionsprites.update()
                # explosionsprites.draw(screen)
            else:
                screen.blit(background, (0, 0))
                # game.state = game.nextstate
                game.state = 'ingame'
                game.nextstate = ""
                game.t = 0

        elif game.state == 'gameover':
            game.highscores.add(highscores.HighScoreEntry(game.player_name, str(game.score)))
            game.menu.highscoresmenu(game.highscores)
            game.highscores.save()

            print game.player_name + ' died with a score of ' + str(game.score)

            game.nextstate = 'mainmenu'
            game.state = 'fadein_y'

        elif game.state == 'reset':
            bullet_sprites.empty()
            parachute_sprites.empty()
            plane_sprites.empty()
            # bomb_sprites.empty()
            trooper_sprites.empty()
            dropping_sprites.empty()
            heli_sprites.empty()
            game.reset()
            game.nextstate = 'ingame'

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