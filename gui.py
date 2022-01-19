import pygame
from pygame.locals import K_UP, K_LEFT, K_RIGHT, K_w, K_a, K_d, K_SPACE, K_DOWN
from classes import Speed
from game import Game


def fill_with_black(screen):
    screen.fill((0, 0, 0))


def display_entitiies(screen, list_of_entities):
    for entity in list_of_entities:
        screen.blit(entity.sprite(), (entity.position().both()))


def draw_game_rigth_side():
    pygame.draw.line(
        screen,
        (255, 255, 255,),
        (game._width + 1, 0),
        (game._width + 1, game._length)
        )


pygame.init()
pygame.font.init()
width, height = 640, 512
screen = pygame.display.set_mode((width, height))
game = Game((320, 512))
player_x = 0
player_y = height - 8
keys = [False, False, False, False]
gametick = 0
shoottick = -5


# 3 - Load images
# player = pygame.image.load("playerv2.png")

# 4 - keep looping through
while 1:
    gametick += 1
    game.update_projectile_positions()
    game.update_enemy_positions()
    # 5 - clear the screen before drawing it again
    fill_with_black(screen)
    # 6 - draw the screen elements
    display_entitiies(screen, game.entities)
    # for entity in game.entities:
    #     screen.blit(entity.sprite(), (entity.position().both()))
    pygame.draw.line(
        screen,
        (255, 255, 255,),
        (game._width + 1, 0),
        (game._width + 1, game._length)
        )

    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key in (K_UP, K_w, K_SPACE):
                keys[0] = True
            elif event.key in (K_LEFT, K_a):
                keys[1] = True
            elif event.key == K_DOWN:
                keys[2] = True
            elif event.key in (K_RIGHT, K_d):
                keys[3] = True

        if event.type == pygame.KEYUP:
            if event.key in (K_UP, K_w, K_SPACE):
                keys[0] = False
            elif event.key in (K_LEFT, K_a):
                keys[1] = False
            elif event.key == pygame.K_DOWN:
                keys[2] = False
            elif event.key in (K_RIGHT, K_d):
                keys[3] = False

    # Update the y position
    # If the up button is pressed
    if keys[0]:
        if gametick - shoottick > 50:
            player = game.player_shoot()
            shoottick = gametick
    # If the down key is pressed
    elif keys[2]:
        if player_y < height-32:
            player_y += 15

    # Update x-position
    # If the left key is pressed
    if keys[1]:
        if game.player.position().x() > 0:
            game.player.move_right()
    # If the right key is pressed
    if keys[3]:
        if game.player.position().x() < game._width - 16:
            game.player.move_left()
