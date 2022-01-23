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


def display_score(screen: 'pygame.display', game: 'Game'):
    font = pygame.font.SysFont('timesnewroman', 32)
    text_score = font.render('Score', False, (255, 255, 255))
    text_score_number = font.render(str(game.score), False, (255, 255, 255))
    text_highscore = font.render('Highscore', False, (255, 255, 255))
    text_highscore_number = font.render(
        str(game.highscore),
        False,
        (255, 255, 255)
    )
    text_lifes = font.render('Lifes:', False, (255, 255, 255))
    text_lifes_number = font.render(
        str(game.player.lifes()),
        False,
        (255, 255, 255)
    )
    screen.blit(text_score, (325, 130))
    screen.blit(text_score_number, (325, 170))
    screen.blit(text_highscore, (325, 30))
    screen.blit(text_highscore_number, (325, 70))
    screen.blit(text_lifes, (325, 400))
    screen.blit(text_lifes_number, (325, 440))


def game_start_screen(screen, width, height):
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


def end_display(
    screen: 'pygame.display',
    width: int,
    height: int,
    result: bool,
    score: int,
    highscore: int
):
    waiting = 1
    text_to_blit = []
    font = pygame.font.SysFont('timesnewroman', 32)
    font_half = pygame.font.SysFont('timesnewroman', 16)
    if result:
        result_str = 'You won!'
    else:
        result_str = "You lost!"
    if score > highscore:
        new_highcore_str = 'New highscore!'
        old_highscore_str = 'Old highscore:'
    else:
        new_highcore_str = ''
        old_highscore_str = 'Highscore:'
    result_text = font.render(result_str, False, (255, 255, 255))
    result_text_pos = result_text.get_rect(center=(320, 60))
    text_to_blit.append((result_text, result_text_pos))

    score_text = font.render('Score:', False, (255, 255, 255))
    text_to_blit.append((score_text, (90, 100)))

    score_num_text = font.render(str(score), False, (255, 255, 255))
    text_to_blit.append((score_num_text, (90, 140)))

    highscore_text = font.render(old_highscore_str, False, (255, 255, 255))
    text_to_blit.append((highscore_text, (90, 180)))

    highscore_num_text = font.render(str(highscore), False, (255, 255, 255))
    text_to_blit.append((highscore_num_text, (90, 220)))

    start_text = 'Press ANY key to continue!'
    text_start = font_half.render(start_text, True, (255, 255, 255))
    text_start_pos = text_start.get_rect(center=(width/2, height - 50))
    text_to_blit.append((text_start, text_start_pos))

    new_highcore_text = font_half.render(
        new_highcore_str,
        False,
        (255, 255, 255)
    )
    new_highcore_text_pos = new_highcore_text.get_rect(center=(320, 20))
    blit_frames = 0

    while waiting:
        blit_frames += 1
        fill_with_black(screen)
        for text in text_to_blit:
            screen.blit(text[0], text[1])
        if blit_frames % 75 < 50:
            screen.blit(new_highcore_text, new_highcore_text_pos)
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
    while game.ongoing:
        game.gametick += 1
        game.update_enemy_positions()
        game.update_projectiles()
        game.score_calc()
        fill_with_black(screen)
        display_entitiies(screen, game.entities)
        draw_game_rigth_side(screen, game)
        display_score(screen, game)
        # 7 - update the screen
        pygame.display.flip()
        # 8 - loop through the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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

        if keys[0]:
            game.player_shoot()
        if keys[1]:
            if game.player.position().x() > 0:
                game.player.move_right()
        if keys[3]:
            if game.player.position().x() < game._width - 16:
                game.player.move_left()

        game.update_game_status()

    game.save_potential_highscore()
    return(game.result, game.score, game.highscore)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Space Invaders')
    width, height = 640, 512
    screen = pygame.display.set_mode((width, height))
    while True:
        game_start_screen(screen, width, height)
        result, score, highscore = game_display(screen)
        end_display(screen, width, height, result, score, highscore)
