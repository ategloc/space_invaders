import pygame


class Position():

    def __init__(self, posx: int, posy: int) -> None:
        self._positionx = posx
        self._positiony = posy

    def change_position(self, new_positionx, new_positiony):
        self._positionx = new_positionx
        self._positiony = new_positiony

    def update_position(self, speed: 'Speed'):
        self._positionx += speed.right()
        self._positiony += speed.down()

    def both(self) -> str:
        return (self._positionx, self._positiony)

    def x(self):
        return self._positionx

    def y(self):
        return self._positiony


class Speed():

    def __init__(
        self,
        xvalue: int = None,
        yvalue: int = None
            ) -> None:
        self._down = yvalue
        self._right = xvalue

    def __repr__(self) -> str:
        return (self._right, self._down)

    def down(self):
        return self._down

    def right(self):
        return self._right


class Entity():

    def __init__(
        self,
        position_x: int, position_y: int,
        sprite: "pygame.image.load()",
        width: int,
            length: int) -> None:

        self._position = Position(position_x, position_y)
        self._sprite = sprite
        self._width = width
        self._length = length

    def position(self):
        return (self._position)

    def sprite(self):
        return (self._sprite)

    def width(self):
        return (self._width)

    def length(self):
        return(self._width)


class moveable_Entity(Entity):

    def __init__(
        self,
        speed: 'Speed',
        position_x: int, position_y: int,
        sprite: "pygame.image.load()",
        width: int,
            length: int) -> None:

        super().__init__(position_x, position_y, sprite, width, length)
        self._speed = speed

    def speed(self):
        return (self._speed)


class Player(moveable_Entity):
    width = 16
    length = 8

    def __init__(
        self,
        lifes,
        speed: 'Speed',
        position_x: int, position_y: int,
            sprite: "pygame.image.load()") -> None:
        super().__init__(
            speed,
            position_x, position_y,
            sprite,
            Player.width, Player.length)
        self._lifes = lifes

    def take_hit(self):
        self._lifes -= 1
        if self._lifes < 1:
            return True

    def make_projectile(self):
        return Projectile(
            self._position.x() + Player.width/2 - 1, self._position.y(),
            Speed(0, -1),
            Player,
            pygame.image.load("bulletv2.png"))

    def lifes(self):
        return self.lifes

    def move_left(self):
        self.position().update_position(self.speed())

    def move_right(self):
        self.position().update_position(
            Speed(
                (self.speed()._right)*(-1), 0
                )
            )


class Enemy(moveable_Entity):
    width = 16
    length = 8
    speed = Speed(0, 0)

    def __init__(
        self,
        speed: 'Speed',
        position_x: int, position_y: int,
            sprite: "pygame.image.load()") -> None:
        super().__init__(
            speed,
            position_x, position_y,
            sprite,
            Enemy.width, Enemy.length)
        Enemy.speed = speed

    def take_hit(self):
        return True

    def make_projectile(self):
        return Projectile(
            self._position.x() + Enemy.width/2 - 1,
            self._position.y() + Enemy.length,
            Speed(0, 1),
            Enemy,
            pygame.image.load('bulletenemyv2.png'))


class Projectile(moveable_Entity):
    width = 2
    length = 4

    def __init__(
        self,
        position_x: int, position_y: int,
        speed: 'Speed',
        team,
            sprite: "pygame.image.load()") -> None:
        super().__init__(
            speed,
            position_x, position_y,
            sprite,
            Projectile.width, Projectile.length)
        self._team = team

    def team(self):
        return self._team


class Shield(Entity):

    sprite_high = None
    sprite_mid = None
    sprite_low = None

    def __init__(self, position_x: int, position_y: int, health: int) -> None:
        super().__init__(position_x, position_y, Shield.sprite_high)
        self._health = health
        self._hp_start = health

    def update_sprite(self):
        if self._health * 100 < Shield.hp_start * 60:
            if self._health * 100 < Shield.hp_start * 30:
                self._sprite = Shield.sprite_low
            else:
                self._sprite = Shield.sprite_mid
        else:
            self._spite = Shield.sprite_high

    def take_hit(self):
        self._health -= 1
        if not self._health:
            return True
        self.update_sprite()
        return False
