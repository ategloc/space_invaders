from classes import Position, Speed, Player, Projectile, Enemy, Shield


def test_position_update_position():
    position = Position(1, 0)
    speed = Speed(1, 2)
    assert position.positiony == 0
    assert position.positionx == 1
    position.update_position(speed)
    assert position.positionx == 2
    assert position.positiony == 2


def test_repr_position():
    position = Position(1, 0)
    assert position == (1, 0)
