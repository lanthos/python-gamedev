"""
 Paraaahhh! Troopers

"""

import sys
import pygame
import sprites
import random
import math


# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (5, 61, 244)
GREY = (199, 199, 199)
GREEN = (63, 177, 79)
RED = (187, 8, 0)


def display_score(score_font, screen, p1_score, high_score):
    player = score_font.render('Score: %s' % p1_score, True, WHITE)
    player_rect = player.get_rect()
    player_rect.topleft = (screen.get_width() / 1.7, screen.get_height() - 50)
    high_score = score_font.render('High Score: %s' % high_score, True, WHITE)
    high_score_rect = high_score.get_rect()
    high_score_rect.topleft = (screen.get_width() / 24, screen.get_height() - 50)
    screen.blit(player, player_rect)
    screen.blit(high_score, high_score_rect)


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
    heli1_image, heli_rect = sprites.load_image('heli1.bmp')
    heli2_image, heli_rect = sprites.load_image('heli2.bmp')
    plane_image, plane_rect = sprites.load_image('plane.bmp')
    troop_image, troop_rect = sprites.load_image('trooper.bmp')
    parachute_image, parachute_rect = sprites.load_image('chute.bmp')

    # initialize fonts
    BASICFONTSIZE = 40
    score_font = pygame.font.Font('visitor1.ttf', BASICFONTSIZE)

    ground = pygame.Surface((screen_width, 10))
    ground.fill(GREEN)
    ground = ground.convert()
    ground_rect = ground.get_rect()
    ground_rect.x = 0
    ground_rect.y = screen.get_height() / 1.1

    # Init sprites
    canon = sprites.Turret(ground_rect)
    bullet_sprites = pygame.sprite.RenderPlain()
    canon_sprite = pygame.sprite.RenderPlain(canon)
    parachute_sprites = pygame.sprite.RenderPlain()
    trooper_sprites = pygame.sprite.RenderPlain()
    plane_sprites = pygame.sprite.RenderPlain()
    heli_sprites = pygame.sprite.RenderPlain()

    # Initial drawing of everything

    screen.blit(background, (0, 0))
    canon_sprite.draw(screen)
    screen.blit(ground, ground_rect)
    screen.blit(canon.canonbase, canon.cannonbase_rect)
    screen.blit(canon.canontop, canon.cannontop_rect)

    canon_sprite.draw(screen)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    high_score = 1234151
    score = 200

    shoot = False
    shoot_lock = 6
    t = 0

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
                if event.key == pygame.K_LEFT:
                        canon.move_counter_clockwise()
                        print canon.state
                        print canon.angle
                        print 'going counter clockwise'
                elif event.key == pygame.K_RIGHT:
                    canon.move_clockwise()
                    print canon.state
                    print canon.angle
                    print 'going clockwise'
                elif event.key == pygame.K_SPACE:
                    shoot = True
                    t = 0
                elif event.key == pygame.K_p:
                    trooper = sprites.Trooper(troop_image, troop_rect, ground_rect)
                    trooper.rect.bottom = area.bottom - 560
                    trooper.rect.x = random.randint(area.left + 5, area.right - 20)
                    trooper_sprites.add(trooper)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and canon.state == "counterclockwise":
                    canon.halt()
                elif event.key == pygame.K_RIGHT and canon.state == "clockwise":
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
            newbullet = sprites.Bullet()
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

        # should there be a new heli?
        if random.randrange(0, 100) == 1:
            heli = sprites.Helicopter(heli1_image, heli2_image, heli_rect)
            if random.randrange(0, 2) == 1:
                heli.rect.topright = area.topright
                heli.direction = -1
            else:
                heli.rect.topleft = area.topleft
                heli.rect = heli.rect.move((0, 62))
                heli.flip_images()
                heli.direction = 1
            heli_sprites.add(heli)

        if score < 6500:
            ch = 150 - (score / 500) * 10
        else:
            ch = 20

        para_chance = ch * len(heli_sprites.sprites())
        for heli in heli_sprites.sprites():
            if heli.rect.left > area.right and heli.direction == 1:
                heli_sprites.remove(heli)
            elif heli.rect.right < area.left and heli.direction == -1:
                heli_sprites.remove(heli)
            elif random.randrange(0, 100) == 1:
                para = sprites.Parachute(parachute_image, parachute_rect, ground_rect)
                para.rect.bottom = area.top
                parachute_sprites.add(para)

                trooper = sprites.Trooper(troop_image, troop_rect, ground_rect)
                trooper.rect.midtop = heli.rect.midbottom
                trooper_sprites.add(trooper)

                trooper.para = para
                para.trooper = trooper

        trooper_killed_dict = pygame.sprite.groupcollide(bullet_sprites, trooper_sprites, 1, 1)
        for bullet in trooper_killed_dict:
            screen.blit(background, bullet.rect, bullet.rect)
            for trooper in trooper_killed_dict[bullet]:
                screen.blit(background, trooper.rect, trooper.rect)
                screen.blit(background, trooper.para.rect, trooper.para.rect)
                parachute_sprites.remove(trooper.para)

        canon_sprite.update()
        bullet_sprites.update()
        heli_sprites.update()
        # parachute_sprites.update()
        trooper_sprites.update()


        meh = None
        meh = pygame.sprite.groupcollide(bullet_sprites, heli_sprites, True, True)
        # meh = pygame.sprite.groupcollide(bullet_sprites, trooper_sprites, True, True)
        # meh = pygame.sprite.groupcollide(bullet_sprites, parachute_sprites, True, True)
        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

        screen.blit(background, (0, 0))
        display_score(score_font, screen, canon.score, high_score)
        canon_sprite.draw(screen)
        bullet_sprites.draw(screen)
        heli_sprites.draw(screen)
        parachute_sprites.draw(screen)
        trooper_sprites.draw(screen)
        screen.blit(ground, ground_rect)
        screen.blit(canon.canonbase, canon.cannonbase_rect)
        screen.blit(canon.canontop, canon.cannontop_rect)


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