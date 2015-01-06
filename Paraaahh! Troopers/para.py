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

    # Initial drawing of everything

    screen.blit(background, (0, 0))
    canon_sprite.draw(screen)
    screen.blit(ground, ground_rect)
    screen.blit(canon.canonbase, canon.cannonbase_rect)
    # screen.blit(canon.canontop, canon.cannontop_rect)

    canon_sprite.draw(screen)

    # Init troopers
    unit = sprites.Trooper()

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    high_score = 1234151

    shoot = False
    shoot_lock = 8
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
                        print 'going counter clockwise'
                elif event.key == pygame.K_RIGHT:
                    canon.move_clockwise()
                    print canon.state
                    print 'going clockwise'
                elif event.key == pygame.K_SPACE:
                    shoot = True
                    t = 0
                elif event.key == pygame.K_p:
                    trooper = sprites.Trooper()
                    trooper.rect.bottom = area.bottom - 560
                    trooper.rect.x = random.randint(area.left + 5, area.right - 20)
                    trooper_sprites.add(trooper)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and canon.state == "counterclockwise":
                    canon.halt()
                elif event.key == pygame.K_RIGHT and canon.state == "clockwise":
                    canon.halt()

        if shoot and t % shoot_lock == 0:
            #shoot a bullet
            newbullet = sprites.Bullet()
            newbullet.direction = canon.angle
            newbullet.image = pygame.transform.rotate(newbullet.bullet, newbullet.direction)
            newbullet.rect = newbullet.bullet.get_rect()
            newbullet.rect.midbottom = canon.cannontop_rect.midbottom
            canon_rad = math.pi / 180 * canon.angle
            newbullet.rect = newbullet.rect.move((newbullet.speed * math.sin(canon_rad), -newbullet.speed * math.cos(canon_rad))) # need to make sin and cos sine and whatnot work here
            bullet_sprites.add(newbullet)
            t = 0
            t += 1

        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        canon_sprite.update()
        bullet_sprites.update()
        # parachute_sprites.update()
        # trooper_sprites.update()


        meh = None
        meh = pygame.sprite.groupcollide(bullet_sprites, trooper_sprites, True, True)
        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

        screen.blit(background, (0, 0))
        display_score(score_font, screen, canon.score, high_score)
        canon_sprite.draw(screen)
        bullet_sprites.draw(screen)
        # parachute_sprites.draw(screen)
        trooper_sprites.draw(screen)
        screen.blit(ground, ground_rect)
        screen.blit(canon.canonbase, canon.cannonbase_rect)
        # screen.blit(canon.canontop, canon.cannontop_rect)


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