from random import choice

import pygame

from classes import Shield, Enemy, Player, Speed, Projectile, Entity
from model_io import write_to_json, read_from_json

spritesplaceholer = None


def check_if_hit(projectile: "Projectile", entity: "Entity"):
    """
    checks if a projectile is (at least partially)
    in an entity (Enemy, Shield, Player or Entity)
    """

    proj = (
        projectile.position().x(),
        projectile.position().x() + projectile.width,
        projectile.position().y(),
        projectile.position().y() + projectile.length
    )
    target = (
        entity.position().x(), entity.position().x() + entity.width,
        entity.position().y(), entity.position().y() + entity.length
    )

    if proj[0] >= target[0]:
        righter = proj
        lefter = target
    else:
        righter = target
        lefter = proj
    if proj[2] >= target[2]:
        lower = proj
        higher = target
    else:
        lower = target
        higher = proj
    mid_x = (righter[0] + lefter[1]) / 2
    mid_y = (lower[2] + higher[3]) / 2
    if (
            target[0] < mid_x < target[1]
            and target[2] < mid_y < target[3]
    ):
        return True
    return False


def load_sprites():
    """
    loads sprites needed for classes to run correctly
    """

    Shield.sprite_high = pygame.image.load("sprites/shieldv1green.png")
    Shield.sprite_mid = pygame.image.load("sprites/shieldv1yellow.png")
    Shield.sprite_low = pygame.image.load("sprites/shieldv1red.png")
    Enemy.projectile_sprite = pygame.image.load('sprites/bulletenemyv2.png')
    Player.projectile_sprite = pygame.image.load('sprites/bulletv2.png')


class Game:
    """
    Class Game. Contains attributes:
    :attrib name: _width
    :attrib type: int

    :attrib name: _length
    :attrib type: int

    :attrib name: gametick
    :attrib type: int

    :attrib name: entities
    :attrib type: list['Entity']

    :attrib name: enemies
    :attrib type: list['Enemy']

    :attrib name: shields
    :attrib type: list['Shield']

    :attrib name: projectiles
    :attrib type: list['Projectile']

    :attrib name: projectiles_team_enemy
    :attrib type: list['Projectile']

    :attrib name: projectiles_team_player
    :attrib type: list['Projectile']

    :attrib name: enemies_max_amount
    :attrib type: int

    :attrib name: since_last_enemy_move
    :attrib type: int

    :attrib name: score
    :attrib type: int

    :attrib name: ongoing
    :attrib type: bool

    :attrib name: result
    :attrib type: bool

    Contains game's data and crutial functions
    """

    def __init__(self, win_resolution) -> None:
        """
        Parameters:
        :param win_resolution: win_resolution
        :win_resolution type: tuple(int, int)

        initializes all lists and variables needed for class to work,
        spawns four rows of enemies and a row of shields
        """

        self.highscore = None
        self.player = None
        self._width = win_resolution[0]
        self._length = win_resolution[1]
        self.gametick = 0
        self.entities = []
        self.enemies = []
        self.shields = []
        self.projectiles = []
        self.projectiles_team_enemy = []
        self.projectiles_team_player = []
        self.enemies_max_amount = 0
        self.since_last_enemy_move = 0
        self.score = 0
        self.ongoing = True
        self.result = None
        self.get_highscore()
        self.add_player(
            lifes=3,
            speed=Speed(4, 0),
            sprite=pygame.image.load("sprites/playerv2.png"),
            shoot_cooldown=50
        )
        load_sprites()

        for i in range(2):
            self.add_row_of_enemies(
                height=16 + i * 32,
                top_left_cord_x=16,
                amount=9,
                gap=16,
                sprite=pygame.image.load("sprites/enemy2v2.png"),
                shoot_cooldown=80
            )
        for i in range(2):
            self.add_row_of_enemies(
                height=32 + i * 32,
                top_left_cord_x=16,
                amount=9,
                gap=16,
                sprite=pygame.image.load("sprites/enemy1v2.png"),
                shoot_cooldown=80
            )
        self.add_row_of_shields(
            height=self._length - 120,
            top_left_cord=30,
            amount=3,
            gap=40,
            health=15
        )

    def add_player(self, lifes, speed, sprite, shoot_cooldown):
        """
        adds an instance of Player to entities list
        """

        self.player = Player(
            lifes,
            speed,
            self._width // 2,
            self._length - Player.length,
            sprite,
            shoot_cooldown)
        self.entities.append(self.player)

    def add_enemy(self, speed, pos_x, pos_y, sprite, shoot_cooldown):
        """
        adds an instance of Enemy to entities and enemies lists
        """

        curr_enemy = Enemy(
            speed,
            pos_x,
            pos_y,
            sprite,
            shoot_cooldown)
        self.enemies.append(curr_enemy)
        self.entities.append(curr_enemy)
        self.enemies_max_amount += 1

    def add_shield(self, pos_x, pos_y, health):
        """
        adds an instance of Shield to enitities and shields lists
        """

        curr_shield = Shield(pos_x, pos_y, health)
        self.shields.append(curr_shield)
        self.entities.append(curr_shield)

    def player_shoot(self):
        """
        makes player shoot if he is allowed to
        """

        if self.player.can_shoot(self.gametick):
            curr_projectile = self.player.make_projectile()
            self.projectiles.append(curr_projectile)
            self.entities.append(curr_projectile)
            self.projectiles_team_player.append(curr_projectile)

    def enemy_shoot(self, enemy: 'Enemy'):
        """
        makes an enemy shoot if it is allowed to
        """

        if enemy.can_shoot(self.gametick):
            curr_projectile = enemy.make_projectile()
            self.projectiles.append(curr_projectile)
            self.entities.append(curr_projectile)
            self.projectiles_team_enemy.append(curr_projectile)

    @staticmethod
    def update_position(entity):
        """
        updates position of an entity
        """

        entity.position().update_position(entity.speed())

    def add_row_of_enemies(
            self,
            height,
            top_left_cord_x,
            amount,
            gap,
            sprite,
            shoot_cooldown
    ):
        """
        adds a row of enemies
        """

        for i in range(amount):
            self.add_enemy(
                Speed(4, 0),
                top_left_cord_x,
                height, sprite,
                shoot_cooldown)
            top_left_cord_x += gap + Enemy.width

    def add_row_of_shields(self, height, top_left_cord, amount, gap, health):
        """
        adds a row of shields
        """

        for i in range(amount):
            self.add_shield(top_left_cord, height, health)
            top_left_cord += gap + Shield.width

    def update_projectile_position(self, projectile):
        """
        updates position of projectiles - deletes if out of screen
        """

        self.update_position(projectile)
        if projectile.position().y() < 0:
            self.score -= 10
            self.remove_projectile(projectile)
        elif projectile.position().y() > self._length:
            self.remove_projectile(projectile)

    def update_enemy_positions(self):
        """
        updates position of enemies - to a side, if a side is hit,
        enemies go down and change direction

        if enemies go to player, ongoing status is changed
        """

        change_dir = 0
        if self.since_last_enemy_move >= len(self.enemies):
            self.since_last_enemy_move = 0
            for enemy in self.enemies:
                # print(enemy.position().x())
                enemy.position().update_position(Enemy.speed)
                if (
                        (enemy.position().x() + enemy.width == self._width)
                        or
                        (enemy.position().x() == 0)
                ):
                    # print(enemy.position().x() + enemy.width)
                    # print(enemy.width)
                    change_dir = True
            if change_dir:
                for enemy in self.enemies:
                    enemy.position().update_position(Speed(0, Enemy.length))
                    if enemy.position().y() + Enemy.length \
                            >= self.player.position().y():
                        self.ongoing = False
                        self.result = False
                Enemy.speed = Speed(Enemy.speed.right() * (-1), 0)
            self.enemies_shoot()
        else:
            self.since_last_enemy_move += 1

    def remove_projectile(self, projectile):
        """
        removes a projectile from every place it is
        """

        self.projectiles.remove(projectile)
        self.entities.remove(projectile)
        if projectile.team() == Player:
            self.projectiles_team_player.remove(projectile)
        else:
            self.projectiles_team_enemy.remove(projectile)

    def remove_enemy(self, enemy):
        """
        removes an enemy from every list it is in
        """

        self.enemies.remove(enemy)
        self.entities.remove(enemy)

    def remove_shield(self, shield):
        """
        removes a shield from every list it is in
        """

        self.shields.remove(shield)
        self.entities.remove(shield)

    def enemy_hit(self, enemy, projectile):
        """
        manages enemy and projectile if they are inside eachother
        """

        self.remove_enemy(enemy)
        self.remove_projectile(projectile)
        self.score += 100

    def shield_hit(self, shield, projectile):
        """
        manages shield and projectile if they are in eachother
        """

        self.remove_projectile(projectile)
        if shield.take_hit():
            self.remove_shield(shield)

    def player_hit(self, projectile):
        """
        manages player and projectile if they are in each other
        """

        self.remove_projectile(projectile)
        self.player._lifes -= 1
        self.score -= 1000

    def update_projectiles(self):
        """
        manages projectiles - moves and checks if hit
        """

        for projectile in self.projectiles:

            if projectile.team() == Player:
                hitable_projectiles = self.projectiles_team_enemy
                for enemy in self.enemies:
                    if check_if_hit(projectile, enemy):
                        self.enemy_hit(enemy, projectile)

            else:
                hitable_projectiles = self.projectiles_team_player

                if check_if_hit(projectile, self.player):
                    self.player_hit(projectile)

            for opposing_projectile in hitable_projectiles:
                if check_if_hit(projectile, opposing_projectile):
                    self.remove_projectile(projectile)
                    self.remove_projectile(opposing_projectile)

            for shield in self.shields:
                if check_if_hit(projectile, shield):
                    self.shield_hit(shield, projectile)

            self.update_projectile_position(projectile)

    def update_game_status(self):
        """
        checks if player is alive and any enemy lives
        """

        if len(self.enemies) == 0:
            self.score += 1000
            self.ongoing = False
            self.result = True
            return True

        if self.player.lifes() < 1:
            self.ongoing = False
            self.result = False
            return True

        return False

    def enemies_shoot(self):
        """
        makes one of enemies shoot - if is able to
        """

        shooting_enemy = choice(self.enemies)
        self.enemy_shoot(shooting_enemy)

    def score_calc(self):
        """
        reduces score after some time
        """

        if self.gametick % 1000 == 0:
            self.score -= self.gametick // 1000

    def get_highscore(self):
        """
        gets highscore from highscore.json file
        """

        try:
            path = open('highscore.json', 'r')
            list_with_score = read_from_json(path)
            self.highscore = list_with_score[0].get('highscore', 0)
        except OSError:
            path = open('highscore.json', 'w')
            write_to_json(path, 0)
            self.highscore = 0

    def save_potential_highscore(self):
        """
        saves a current score as a highscore if its higher into highscore.json
        """

        if self.score > self.highscore:
            path = open('highscore.json', 'w')
            write_to_json(path, self.score)
