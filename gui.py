import pygame
from pygame.locals import K_UP, K_LEFT, K_RIGHT, K_w, K_a, K_d, K_SPACE
from game import Game


def fill_with_black(screen):
    screen.fill((0, 0, 0))


def display_entitiies(screen, list_of_entities):
    for entity in list_of_entities:
        screen.blit(entity.sprite(), (entity.position().both()))


def draw_game_rigth_side(screen: 'pygame.display', game: 'Game'):
    pygame.draw.line(
        screen,
        (255, 255, 255,),
        (game._width + 1, 0),
        (game._width + 1, game._length)
        )


def game_start_screen():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Space Invaders')
    width, height = 640, 512
    screen = pygame.display.set_mode((width, height))
    start_text = 'Press ANY key to start!'
    font_head = pygame.font.SysFont('timesnewroman', 32)
    text_head = font_head.render('Space Invaders', False, (255, 255, 255))
    text_head_pos = text_head.get_rect(center=(width/2, 50))
    font_start = pygame.font.SysFont('timesnewroman', 16)
    text_start = font_start.render(start_text, True, (255, 255, 255))
    text_start_pos = text_start.get_rect(center=(width/2, height - 50))

    waiting = True

    while waiting:
        fill_with_black(screen)
        screen.blit(text_head, text_head_pos)
        screen.blit(text_start, text_start_pos)
        pygame.display.flip()
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
                return None
            if event.type == pygame.KEYDOWN:
                return screen


def game_display(screen: 'pygame.display'):
    game = Game((320, 512))

    keys = [False, False, False, False]

    # 3 - Load images
    # player = pygame.image.load("playerv2.png")

    # 4 - keep looping through
    while game.ongoing:
        game.gametick += 1
        game.update_enemy_positions()
        game.update_projectiles()
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
                elif event.key in (K_RIGHT, K_d):
                    keys[3] = True

            if event.type == pygame.KEYUP:
                if event.key in (K_UP, K_w, K_SPACE):
                    keys[0] = False
                elif event.key in (K_LEFT, K_a):
                    keys[1] = False
                elif event.key in (K_RIGHT, K_d):
                    keys[3] = False

        # Update the y position
        # If the up button is pressed
        if keys[0]:
            game.player_shoot()
        # Update x-position
        # If the left key is pressed
        if keys[1]:
            if game.player.position().x() > 0:
                game.player.move_right()
        # If the right key is pressed
        if keys[3]:
            if game.player.position().x() < game._width - 16:
                game.player.move_left()

        game.update_game_status()
        # game.enemies_shoot()


if __name__ == '__main__':
    screen = game_start_screen()
    game_display(screen)
