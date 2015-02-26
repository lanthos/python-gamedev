"""
 Atari Tanks!  Weeeeeeeeeeeeeeeeeeeeeeeeeee

 Recreated here using Python and Pygame by Jeremy Kenyon as a lesson in learning programing and game design.

 Any questions please contact me at lanthos@gmail.com.

"""

import sys
from tank import *
from bullets import *
from map import *
import os
import pyglet

# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (187, 8, 0)
BLUE = (5, 61, 244)
replay = False


def display_score(score_font, level_font, DISPLAYSURF, p1_score, p2_score, game_map):
    shot_font = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 20)
    move_font = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 15)
    player1 = score_font.render('%s' % p1_score, True, WHITE)
    player1_rect = player1.get_rect()
    player1_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 4, 25)
    player2 = score_font.render('%s' % p2_score, True, WHITE)
    player2_rect = player2.get_rect()
    player2_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) * .75, 25)
    level = level_font.render('%s' % game_map.level_number, True, WHITE)
    level_rect = level.get_rect()
    level_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 2 + 40, 10)
    level_text = level_font.render('Map', True, WHITE)
    level_text_rect = level_text.get_rect()
    level_text_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 2 - 60, 10)
    display_shot = shot_font.render('Shot Type: {0}'.format(game_map.shot_types[game_map.shot_type]), True, WHITE)
    display_shot_rect = display_shot.get_rect()
    display_shot_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 2 - 100, 60)
    movement = move_font.render('Movement P1: A, W, D, Space.  P2: Left, Up, Right, Shift.  < and > to change maps', True, WHITE)
    movement_shot_rect = movement.get_rect()
    movement_shot_rect.topleft = (5, 5)
    DISPLAYSURF.blit(movement, movement_shot_rect)
    DISPLAYSURF.blit(display_shot, display_shot_rect)
    DISPLAYSURF.blit(player1, player1_rect)
    DISPLAYSURF.blit(player2, player2_rect)
    DISPLAYSURF.blit(level, level_rect)
    DISPLAYSURF.blit(level_text, level_text_rect)


def check_time(time, length, p1_score, p2_score, score_font, DISPLAYSURF, game_map, tank_idle, red_tank_move,
               blue_tank_move, credit_font):
    '''
    Checks to see if the time limit for the game has passed and if it has checks the score and asks for quit or restart.
    '''
    if time > length:
        pygame.draw.rect(DISPLAYSURF, BLACK, ((game_map.MAPWIDTH * game_map.TILESIZE) / 4.2,
                                              (game_map.MAPHEIGHT * game_map.TILESIZE) / 2, 400, 225))
        credit_text = credit_font.render('Combat clone made by Jeremy Kenyon 2014', True, WHITE)
        credit_text_rect = credit_text.get_rect()
        credit_text_rect.topleft = ((game_map.MAPWIDTH * game_map.TILESIZE) / 4,
                                    (game_map.MAPHEIGHT * game_map.TILESIZE) / 1.2)
        DISPLAYSURF.blit(credit_text, credit_text_rect)
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
        red_tank_move.stop()
        blue_tank_move.stop()
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


def score_reset(red, blue):
    red.score = 0
    blue.score = 0


def main():
    """ Main function for the game. """
    pygame.mixer.pre_init(44100, -16, 2, 8192)
    pygame.init()

    # Initialize sounds
    # tank_idle = pygame.mixer.Sound(os.path.join('data', 'tank_idle_01.ogg'))
    # red_tank_move = pygame.mixer.Sound(os.path.join('data', 'tank_moving_01.ogg'))
    # blue_tank_move = pygame.mixer.Sound(os.path.join('data', 'tank_moving_01.ogg'))
    # tank_idle.play(-1)
    tank_idle = pyglet.media.load(os.path.join('data', 'tank_idle.wav'), streaming=False)
    tank_idle_player = pyglet.media.Player()
    tank_idle_player.queue(tank_idle)
    tank_idle_player.eos_action = tank_idle_player.EOS_LOOP
    tank_idle_player.play()
    red_tank_move = pyglet.media.load(os.path.join('data', 'tank_moving.wav'), streaming=False)
    red_tank_move_player = pyglet.media.Player()
    red_tank_move_player.queue(red_tank_move)
    red_tank_move_player.eos_action = red_tank_move_player.EOS_LOOP
    red_tank_move_player.play()
    blue_tank_move = pyglet.media.load(os.path.join('data', 'tank_moving.wav'), streaming=False)
    blue_tank_move_player = pyglet.media.Player()
    blue_tank_move_player.queue(blue_tank_move)
    blue_tank_move_player.eos_action = blue_tank_move_player.EOS_LOOP
    blue_tank_move_player.play()


    # initialize tanks
    red_tank = Tank(150, 200, 'red')
    blue_tank = Tank(550, 200, 'blue')


    # initialize the map.  Need to have the tanks as part of this so that tank location can be saved in editor.
    game_map = Map(red_tank, blue_tank)
    map_editor = False

    # Set the width and height of the screen [width,height]
    icon = pygame.image.load(os.path.join('data', 'tank_icon.bmp'))
    pygame.display.set_icon(icon)
    DISPLAYSURF = pygame.display.set_mode((game_map.MAPWIDTH*game_map.TILESIZE, game_map.MAPHEIGHT*game_map.TILESIZE))
    pygame.display.set_caption("Retro Tanks")

    # More tank initialization needed to be done after initial creation of objects so that tank/map relationship works
    # ok and states can be saved and displays made.
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
    score_font = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), BASICFONTSIZE)
    level_font = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 50)
    game_over_font = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 25)
    credit_font = pygame.font.Font(os.path.join('data', 'visitor1.ttf'), 15)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Set game length here.  The length_static will be how long the game always is and length will change based upon
    # using the map editor or on switching maps.
    length = 60000
    length_static = length

    # -------- Main Program Loop -----------
    while not done:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            # Uncomment this if you need to figure out where the mouse location is for troubleshooting.
            # elif event.type == pygame.MOUSEMOTION:
            #     mousex, mousey = event.pos
            #     tileX = int(mousex / game_map.TILESIZE)
            #     tileY = int(mousey / game_map.TILESIZE)
            #     print 'Mouse X and Y: %s, %s' % event.pos
            #     print 'Converted tileX and tileY: %s. %s' % (tileX, tileY)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_w:
                    if not blue_tank.hit and not red_tank.hit:
                        red_tank_move.play()
                if event.key == pygame.K_UP:
                    if not blue_tank.hit and not red_tank.hit:
                        blue_tank_move.play()
                if event.key == pygame.K_SPACE:
                    if not blue_tank.hit and not red_tank.hit:
                        red_tank.shoot(red_bullet)
                if event.key == pygame.K_RCTRL or event.key == pygame.K_RSHIFT:
                    if not blue_tank.hit and not red_tank.hit:
                        blue_tank.shoot(blue_bullet)
                # Map editor commands here
                if event.key == pygame.K_p:
                    map_editor = True
                if event.key == pygame.K_COMMA:
                    game_map.level_number -= 1
                    length = length_static + pygame.time.get_ticks()
                    red_bullet.reset()
                    blue_bullet.reset()
                    score_reset(red_tank, blue_tank)
                    if game_map.level_number <= 0:
                        game_map.level_number = 1
                    game_map.load_map(game_map.level_number, red_tank, blue_tank)
                if event.key == pygame.K_PERIOD:
                    game_map.level_number += 1
                    length = length_static + pygame.time.get_ticks()
                    red_bullet.reset()
                    blue_bullet.reset()
                    score_reset(red_tank, blue_tank)
                    if game_map.level_number not in game_map.map_levels.values():
                        game_map.level_number -= 1
                    game_map.load_map(game_map.level_number, red_tank, blue_tank)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    red_tank_move_player.pause()
                if event.key == pygame.K_UP:
                    blue_tank_move_player.pause()
        # This allows for you to hold down the keys and have it repeat affects instead of having to continually press.
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
        red_tank.been_shot("red", red_bullet)
        red_bullet.update()
        blue_tank.been_shot("blue", blue_bullet)
        blue_bullet.update()
        if map_editor:
            map_editor, length = game_map.editor(map_editor, red_tank, blue_tank, length, DISPLAYSURF)
        replay = check_time(pygame.time.get_ticks(), length, red_tank.score, blue_tank.score, game_over_font,
                            DISPLAYSURF, game_map, tank_idle, red_tank_move, blue_tank_move, credit_font)
        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        game_map.draw(DISPLAYSURF)

        red_bullet.draw()
        blue_bullet.draw()
        red_tank.draw_red()
        blue_tank.draw_blue()
        display_score(score_font, level_font, DISPLAYSURF, red_tank.score, blue_tank.score, game_map)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second
        clock.tick(20)
        if replay:
            length += pygame.time.get_ticks() + length_static
            tank_idle.play(-1)
            red_bullet.reset()
            blue_bullet.reset()
            game_map.load_map(game_map.level_number, red_tank, blue_tank)
            continue

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    else:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()