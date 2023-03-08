import pygame


class Position:
    """
    Class Position. Contains attributes:
    :attrib name: _positionx
    :attrib type: int

    :attrib name: _positiony
    :attrib type: int

    Contains entity's position
    """

    def __init__(self, posx: int, posy: int) -> None:
        """
        inits position
        """

        self._positionx = posx
        self._positiony = posy

    def update_position(self, speed: 'Speed'):
        """
        updates position by moving it by distance given in speed
        """

        self._positionx += speed.right()
        self._positiony += speed.down()

    def both(self) -> tuple[int, int]:
        """
        returns both coords of position
        """

        return self._positionx, self._positiony

    def x(self):
        """
        returns x value of position
        """

        return self._positionx

    def y(self):
        """
        returns negative y value of position
        """

        return self._positiony


class Speed:
    """
    Class Position. Contains attributes:
    :attrib name: right
    :attrib type: int

    :attrib name: down
    :attrib type: int

    Contains entity's speed
    """

    def __init__(
        self,
        xvalue: int = None,
        yvalue: int = None
            ) -> None:
        """
        inits speed
        """

        self._down = yvalue
        self._right = xvalue

    def down(self):
        """
        returns negative y value of speed
        """

        return self._down

    def right(self):
        """
        returns positive x value of speed
        """
        return self._right


class Entity:
    """
    Class Entity. Contains attributes:
    :attrib name: _position
    :attrib type: Position

    :attrib name: _sprite
    :attrib type: pygame.image.load()

    :attrib name: _width
    :attrib type: int

    :attrib name: _length
    :attrib type: int

    Contains entities attributes
    """

    def __init__(
        self,
        position_x: int, position_y: int,
        sprite: "pygame.image.load()",
        width: int,
        length: int
    ) -> None:
        """
        Parameters:
        :param name: position_x
        :param type: int

        :param name: position_y
        :param type: int

        :param name: sprite
        :param type: pygame.image.load()

        :param name: width
        :param type: int

        :param name: length
        :param type: int

        inits an entity
        """

        self._position = Position(position_x, position_y)
        self._sprite = sprite
        self._width = width
        self._length = length

    def position(self):
        """
        returns an instance of position of the entity
        """

        return self._position

    def sprite(self):
        """
        returns sprite of the entity
        """

        return self._sprite

    def width(self):
        """
        returns width of the entity
        """

        return self._width

    def length(self):
        """
        returns length of entity
        """

        return self._width


class moveable_Entity(Entity):
    """
    Class moveable_Entity. Contains attributes:
    :attrib name: _position
    :attrib type: Position

    :attrib name: _sprite
    :attrib type: pygame.image.load()

    :attrib name: _width
    :attrib type: int

    :attrib name: _length
    :attrib type: int

    :attrib name: speed
    :attrib type: Speed

    Contains attributes of entity that moves
    """

    def __init__(
        self,
        speed: 'Speed',
        position_x: int, position_y: int,
        sprite: "pygame.image.load()",
        width: int,
        length: int
    ) -> None:
        """
        Parameters:
        :param name: speed
        :param type: Speed

        :param name: position_x
        :param type: int

        :param name: position_y
        :param type: int

        :param name: sprite
        :param type: pygame.image.load()

        :param name: width
        :param type: int

        :param name: length
        :param type: int

        inits a moving entity
        """

        super().__init__(position_x, position_y, sprite, width, length)
        self._speed = speed

    def speed(self):
        """
        returns speed of the entity
        """

        return self._speed


class shooting_Entity(moveable_Entity):
    """
    Class shooting_Entity. Contains attributes:
    :attrib name: _position
    :attrib type: Position

    :attrib name: _sprite
    :attrib type: pygame.image.load()

    :attrib name: _width
    :attrib type: int

    :attrib name: _length
    :attrib type: int

    :attrib name: speed
    :attrib type: Speed

    :attrib name: shoot_cooldown
    :attrib type: int

    :attrib name: _last_shot_tick
    :attrib type: int

    Contains attributes of entity that moves and shoots
    """

    def __init__(
        self,
        speed: 'Speed',
        position_x: int, position_y: int,
        sprite: "pygame.image.load()",
        width: int,
        length: int,
        shoot_cooldown: int
    ) -> None:
        """
        Parameters:
        :param name: speed
        :param type: Speed

        :param name: position_x
        :param type: int

        :param name: position_y
        :param type: int

        :param name: sprite
        :param type: pygame.image.load()

        :param name: width
        :param type: int

        :param name: length
        :param type: int

        :param name: shoot_cooldown
        :param type: int

        inits a shooting and moving entity
        """

        super().__init__(speed, position_x, position_y, sprite, width, length)
        self._shoot_cooldown = shoot_cooldown
        self._last_shot_tick = (-1) * shoot_cooldown

    def shoot_cooldown(self):
        """
        returns shoot cooldown of the entity
        """

        return self._shoot_cooldown

    def can_shoot(self, game_tick):
        """
        checks wheter entity can shoot or not
        """

        if game_tick - self.shoot_cooldown() > self._last_shot_tick:
            self._last_shot_tick = int(game_tick)
            return True
        return False


class Player(shooting_Entity):
    """
    Class Player. Contains attributes:
    :attrib name: _position
    :attrib type: Position

    :attrib name: _sprite
    :attrib type: pygame.image.load()

    :attrib name: _width
    :attrib type: int

    :attrib name: _length
    :attrib type: int

    :attrib name: speed
    :attrib type: Speed

    :attrib name: shoot_cooldown
    :attrib type: int

    :attrib name: _last_shot_tick
    :attrib type: int

    :attrib name: lifes
    :attrib type: int


    Contains attributes of player
    """

    width = 16
    length = 8

    def __init__(
        self,
        lifes,
        speed: 'Speed',
        position_x: int, position_y: int,
        sprite: "pygame.image.load()",
        shoot_cooldown: int
    ) -> None:
        """
        Parameters:
        :param type: lifes
        :param name: int

        :param name: speed
        :param type: Speed

        :param name: position_x
        :param type: int

        :param name: position_y
        :param type: int

        :param name: sprite
        :param type: pygame.image.load()

        :param name: shoot_cooldown
        :param type: int

        inits a player
        """

        super().__init__(
            speed,
            position_x, position_y,
            sprite,
            Player.width, Player.length,
            shoot_cooldown)
        self._lifes = lifes

    def take_hit(self):
        """
        reduces players life by one, returns True if player is dead
        """

        self._lifes -= 1
        if self._lifes < 1:
            return True

    def make_projectile(self):
        """
        makes projectile that is in Player's team
        """

        return Projectile(
            self._position.x() + Player.width/2 - 1, self._position.y(),
            Speed(0, -1),
            Player,
            Player.projectile_sprite)

    def lifes(self):
        """
        return amopunt of player's life
        """

        return self._lifes

    def move_right(self):
        """
        move player right by his speed value
        """

        self.position().update_position(self.speed())

    def move_left(self):
        """
        moves player left by his speed value
        """
        self.position().update_position(
            Speed(
                self.speed()._right * (-1), 0
                )
            )


# noinspection GrazieInspection
class Enemy(shooting_Entity):
    """
    Class Enemy. Contains attributes:
    :attrib name: _position
    :attrib type: Position

    :attrib name: _sprite
    :attrib type: pygame.image.load()

    :attrib name: speed
    :attrib type: Speed

    :attrib name: shoot_cooldown
    :attrib type: int

    :attrib name: _last_shot_tick
    :attrib type: int

    Contains attributes of enemy
    """

    width = 16
    length = 8
    speed = Speed(0, 0)

    def __init__(
        self,
        speed: 'Speed',
        position_x: int, position_y: int,
        sprite: "pygame.image.load()",
        shoot_cooldown: int
    ) -> None:
        """
        Parameters:
        :param name: speed
        :param type: Speed

        :param name: position_x
        :param type: int

        :param name: position_y
        :param type: int

        :param name: sprite
        :param type: pygame.image.load()

        :param name: shoot_cooldown
        :param type: int

        inits an enemy
        """

        super().__init__(
            speed,
            position_x, position_y,
            sprite,
            Enemy.width, Enemy.length,
            shoot_cooldown)
        Enemy.speed = speed

    @staticmethod
    def take_hit():
        """
        returns True as enemy has 1 health
        """

        return True

    def make_projectile(self):
        """
        makes projectile that is in Enenmy's team
        """

        return Projectile(
            self._position.x() + Enemy.width/2 - 1,
            self._position.y() + Enemy.length,
            Speed(0, 1),
            Enemy,
            Enemy.projectile_sprite)


class Projectile(moveable_Entity):
    """
    Class Projectile. Contains attributes:
    :attrib name: _position
    :attrib type: Position

    :attrib name: _sprite
    :attrib type: pygame.image.load()

    :attrib name: _width
    :attrib type: int

    :attrib name: _length
    :attrib type: int

    :attrib name: team
    :attrib type: Class

    Contains attributes of projectile
    """

    width = 2
    length = 4

    def __init__(
        self,
        position_x: int, position_y: int,
        speed: 'Speed',
        team,
        sprite: "pygame.image.load()"
    ) -> None:
        """
        Parameters:
        :param name: speed
        :param type: Speed

        :param name: position_x
        :param type: int

        :param name: position_y
        :param type: int

        :param name: team
        :param type: Class

        :param name: sprite
        :param type: pygame.image.load()

        inits an projectile
        """

        super().__init__(
            speed,
            position_x, position_y,
            sprite,
            Projectile.width, Projectile.length)
        self._team = team

    def team(self):
        """
        returns team of projectile
        """

        return self._team


class Shield(Entity):
    """
    Class Shield. Contains attributes:
    :attrib name: _position
    :attrib type: Position

    :attrib name: _sprite
    :attrib type: pygame.image.load()

    :attrib name: _health
    :attrib type: int

    :attrib name: _hp_start
    :attrib type: int

    Contains entities attributes
    """

    width = 60
    length = 30

    def __init__(self, position_x: int, position_y: int, health: int) -> None:
        """
        Parameters:
        :param name: position_x
        :param type: int

        :param name: position_y
        :param type: int

        :param name: health
        :param type: int

        inits a projectile
        """

        super().__init__(
            position_x, position_y,
            Shield.sprite_high,
            Shield.width, Shield.length
            )
        self._sprite = Shield.sprite_high
        self._health = health
        self._hp_start = health

    def update_sprite(self):
        """
        updates shield's sprite regarding its current hp
        """
        if self._health * 100 < self._hp_start * 60:
            if self._health * 100 < self._hp_start * 30:
                self._sprite = Shield.sprite_low
            else:
                self._sprite = Shield.sprite_mid
        else:
            pass

    def take_hit(self):
        """
        reduces shields hp by one, updates sprite

        returns True if shield has hp, False if does not
        """
        self._health -= 1
        if not self._health:
            return True
        self.update_sprite()
        return False
