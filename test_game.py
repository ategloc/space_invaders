from game import Game, check_if_hit
from classes import Enemy, Projectile, Player, Position, Speed


def test_check_if_hit():
    player = Player(1, Speed(3, 0), 21, 0, None)
    projectile = Projectile(21, 0, Speed(0, 1), Player, None)
    # assert player._position == projectile._position
    assert check_if_hit(projectile, player) is True
    player._position.update_position(player._speed)
    assert check_if_hit(projectile, player) is False

def test_check_if_hit2():
    player = Player(1, Speed(1, 0), 20, 0, None)
    projectile = Projectile(21, 0, Speed(0, 1), Player, None)
    # assert player._position == projectile._position
    assert check_if_hit(projectile, player) is True
    # player._position.update_position(player._speed)
    # assert check_if_hit(projectile, player) is False

def test_game():
    game = Game((640, 512))
    assert game

def test_check_if_hit_2_projectiles():
    proj1 = Projectile(20, 20, Speed(0, -1), Player, None)
    proj2 = Projectile(21, 22, Speed(0, 1), Enemy, None)

    assert check_if_hit(proj1, proj2) is True
    proj2.position().update_position(proj2.speed())
    proj1.position().update_position(proj1.speed())
    assert check_if_hit(proj1, proj2) is False
