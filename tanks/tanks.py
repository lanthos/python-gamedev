"""
 Atari Tanks!  Weeeeeeeeeeeeeeeeeeeeeeeeeee

"""

import sys
from tank import *
from bullets import *
from map import *

# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (187, 8, 0)
BLUE = (5, 61, 244)
replay = False


def display_score(score_font, level_font, DISPLAYSURF, p1_score, p2_score, game_map):
    player1 = score_font.render('%s' % p1_score, True, WHITE)
    player1_rect = player1.get_rect()
    player1_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 4, 25)
    player2 = score_font.render('%s' % p2_score, True, WHITE)
    player2_rect = player2.get_rect()
    player2_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) * .75, 25)
    level = level_font.render('%s' % game_map.level_number, True, WHITE)
    level_rect = level.get_rect()
    level_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 2 + 40, 25)
    level_text = level_font.render('Map', True, WHITE)
    level_text_rect = level_text.get_rect()
    level_text_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 2 - 60, 25)
    DISPLAYSURF.blit(player1, player1_rect)
    DISPLAYSURF.blit(player2, player2_rect)
    DISPLAYSURF.blit(level, level_rect)
    DISPLAYSURF.blit(level_text, level_text_rect)


def check_time(time, length, p1_score, p2_score, score_font, DISPLAYSURF, game_map, tank_idle):
    if time > length:
        if p1_score > p2_score:
            game_over = score_font.render('Game over!  Red wins!', True,  WHITE)
            game_over_rect = game_over.get_rect()
            game_over_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 4,
                                      (game_map.MAPHEIGHT * game_map.TILESIZE) / 2)

            replay_text = score_font.render('R for Replay or Q to quit', True,  WHITE)
            replay_rect = replay_text.get_rect()
            replay_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 4,
                                   (game_map.MAPHEIGHT * game_map.TILESIZE) / 1.5)
            DISPLAYSURF.blit(replay_text, replay_rect)
            DISPLAYSURF.blit(game_over, game_over_rect)
            tank_idle.stop()
            pygame.display.flip()
            over = True
            while over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_r:
                            over = False
            return True
        elif p1_score < p2_score:
            game_over = score_font.render('Game over!  Blue wins!', True,  WHITE)
            game_over_rect = game_over.get_rect()
            game_over_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 4,
                                      (game_map.MAPHEIGHT * game_map.TILESIZE) / 2)
            replay_text = score_font.render('R for Replay or Q to quit', True,  WHITE)
            replay_rect = replay_text.get_rect()
            replay_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 4,
                                   (game_map.MAPHEIGHT * game_map.TILESIZE) / 1.5)
            DISPLAYSURF.blit(replay_text, replay_rect)
            DISPLAYSURF.blit(game_over, game_over_rect)
            tank_idle.stop()
            pygame.display.flip()
            over = True
            while over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_r:
                            over = False
            return True
        else:
            game_over = score_font.render("Game over!  It's a tie!", True,  WHITE)
            game_over_rect = game_over.get_rect()
            game_over_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 4,
                                      (game_map.MAPHEIGHT * game_map.TILESIZE) / 2)
            replay_text = score_font.render('R for Replay or Q to quit', True,  WHITE)
            replay_rect = replay_text.get_rect()
            replay_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 4,
                                   (game_map.MAPHEIGHT * game_map.TILESIZE) / 1.5)
            DISPLAYSURF.blit(replay_text, replay_rect)
            DISPLAYSURF.blit(game_over, game_over_rect)
            tank_idle.stop()
            pygame.display.flip()
            over = True
            while over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_r:
                            over = False
            return True


def main():
    """ Main function for the game. """
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    # Initialize sounds
    tank_idle = pygame.mixer.Sound("tank_idle.wav")
    red_tank_move = pygame.mixer.Sound("tank_moving.wav")
    blue_tank_move = pygame.mixer.Sound("tank_moving.wav")
    tank_idle.play(-1)

    # initialize tanks
    red_tank = Tank(150, 200, 'red')
    blue_tank = Tank(550, 200, 'blue')


    # initialize the map
    game_map = Map(red_tank, blue_tank)
    map_editor = False

    # Set the width and height of the screen [width,height]
    # size = [700, 500]
    # screen = pygame.display.set_mode(size)
    DISPLAYSURF = pygame.display.set_mode((game_map.MAPWIDTH*game_map.TILESIZE, game_map.MAPHEIGHT*game_map.TILESIZE))
    pygame.display.set_caption("Tanks")

    red_tank.DISPLAYSURF = DISPLAYSURF
    red_tank.game_map = game_map
    red_tank.enemy_tank = blue_tank
    blue_tank.DISPLAYSURF = DISPLAYSURF
    blue_tank.game_map = game_map
    blue_tank.enemy_tank = red_tank
    red_tank.hack('red')
    blue_tank.hack('blue')
    blue_bullet = Bullet(BLUE, 'blue', DISPLAYSURF, game_map, red_tank, blue_tank)
    red_bullet = Bullet(RED, 'red', DISPLAYSURF, game_map, blue_tank, red_tank)

    # initialize fonts
    BASICFONTSIZE = 70
    score_font = pygame.font.Font('visitor1.ttf', BASICFONTSIZE)
    level_font = pygame.font.Font('visitor1.ttf', 50)
    game_over_font = pygame.font.Font('visitor1.ttf', 25)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    length = 60000

    # -------- Main Program Loop -----------
    while not done:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
                tileX = int(mousex / game_map.TILESIZE)
                tileY = int(mousey / game_map.TILESIZE)
                print 'Mouse X and Y: %s, %s' % event.pos
                print 'Converted tileX and tileY: %s. %s' % (tileX, tileY)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_w:
                    if not blue_tank.hit and not red_tank.hit:
                        red_tank_move.play(-1)
                    print 'W pressed down'
                if event.key == pygame.K_UP:
                    if not blue_tank.hit and not red_tank.hit:
                        blue_tank_move.play(-1)
                if event.key == pygame.K_SPACE:
                    if not blue_tank.hit and not red_tank.hit:
                        red_tank.shoot(red_bullet)
                if event.key == pygame.K_RCTRL or event.key == pygame.K_RSHIFT:
                    if not blue_tank.hit and not red_tank.hit:
                        blue_tank.shoot(blue_bullet)
                # Map editor commands here
                if event.key == pygame.K_p:
                    map_editor = True
                    print "hi I've been pressed!"
                if event.key == pygame.K_COMMA:
                    game_map.level_number -= 1
                    if game_map.level_number <= 0:
                        game_map.level_number = 1
                    game_map.load_map(game_map.level_number, red_tank, blue_tank)
                if event.key == pygame.K_PERIOD:
                    game_map.level_number += 1
                    if game_map.level_number not in game_map.map_levels.values():
                        game_map.level_number -= 1
                    game_map.load_map(game_map.level_number, red_tank, blue_tank)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    red_tank_move.stop()
                    print 'W let up'
                if event.key == pygame.K_UP:
                    blue_tank_move.stop()
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

        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        red_tank.update("red")
        red_bullet.update()
        blue_tank.update("blue")
        blue_bullet.update()
        if map_editor:
            map_editor, length = game_map.editor(map_editor, red_tank, blue_tank, length, DISPLAYSURF)

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        game_map.draw(DISPLAYSURF)

        red_bullet.draw()
        blue_bullet.draw()
        red_tank.draw_red()
        blue_tank.draw_blue()
        display_score(score_font, level_font, DISPLAYSURF, red_tank.score, blue_tank.score, game_map)
        replay = check_time(pygame.time.get_ticks(), length, red_tank.score, blue_tank.score, game_over_font,
                            DISPLAYSURF, game_map, tank_idle)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second
        clock.tick(20)
        if replay:
            length += pygame.time.get_ticks()
            tank_idle.play(-1)
            continue

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    else:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()