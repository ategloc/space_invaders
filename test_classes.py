from classes import Position, Speed, Player, Enemy, Shield


def test_position_update_position():
    position = Position(1, 0)
    speed = Speed(1, 2)
    assert position.x() == 1
    assert position.y() == 0
    position.update_position(speed)
    assert position.x() == 2
    assert position.y() == 2


def test_repr_position():
    position = Position(1, 0)
    assert position.both() == (1, 0)


def test_speed():
    speed = Speed(1, 0)
    assert speed.right() == 1
    assert speed.down() == 0


def test_player_take_hit():
    player = Player(3, Speed(0, 0), 0, 0, None, 0)
    assert player.lifes() == 3
    player.take_hit()
    assert player.lifes() == 2


def test_player_proj():
    player = Player(3, Speed(0, 0), 0, 0, None, 0)
    Player.projectile_sprite = None
    assert player.make_projectile()


def test_player_moving():
    player = Player(3, Speed(1, 0), 0, 0, None, 0)
    assert player.position().both() == (0, 0)
    player.move_right()
    assert player.position().both() == (1, 0)
    player.move_left()
    assert player.position().both() == (0, 0)


def test_enemy_take_hit():
    enemy = Enemy(Speed(1, 0), 0, 0, None, 0)
    assert enemy.take_hit()


def test_enemy_make_projectile():
    enemy = Enemy(Speed(1, 0), 0, 0, None, 0)
    Enemy.projectile_sprite = None
    assert enemy.make_projectile()


def test_shield_take_hit():
    Shield.sprite_high = 1
    Shield.sprite_mid = 2
    Shield.sprite_low = 3
    shield = Shield(1, 1, 2)
    assert shield.sprite() == 1
    shield.take_hit()
    assert shield._health == 1
    assert shield.sprite() == 2
