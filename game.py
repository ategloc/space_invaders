from classes import Shield, Enemy, Player, Speed, Projectile, Entity
import pygame

spritesplaceholer = None


def check_if_hit(projectile: "Projectile", entity: "Entity"):
    proj = (
        projectile.position().x(), projectile.position().x() + projectile.width,
        projectile.position().y(), projectile.position().y() + projectile.length
    )
    target = (
        entity.position().x(), entity.position().x() + entity.width,
        entity.position().y(), entity.position().y() + entity.length
    )
    righter = None
    lefter = None
    lower = None
    higher = None
    if (proj[0] >= target[0]):
        righter = proj
        lefter = target
    else:
        righter = target
        lefter = proj
    if (proj[2] >= target[2]):
        lower = proj
        higher = target
    else:
        lower = target
        higher = proj
    mid_x = (righter[0] + lefter[1])/2
    mid_y = (lower[2] + higher[3])/2
    if (
        mid_x > target[0]
        and mid_x < target[1]
        and mid_y > target[2]
        and mid_y < target[3]
    ):
        return True
    return False


class Game():
    def __init__(self, win_resolution) -> None:
        self._width = win_resolution[0]
        self._length = win_resolution[1]
        self.entities = []
        self.enemies = []
        self.shields = []
        self.entity_hitable_by_player = []
        self.entity_hitable_by_enemy = []
        self.projectiles = []
        self.projectiles_team_enemy = []
        self.projectiles_team_player = []
        self.enemies_max_amount = 0
        self.since_last_enemy_move = 0
        self.ongoing = True
        self.result = None
        self.add_player(3, Speed(4, 0), pygame.image.load("playerv2.png"))
        for i in range(2):
            self.add_row_of_enemies(
                16 + i * 32, 16, 9, pygame.image.load("enemy2v2.png"))
        for i in range(2):
            self.add_row_of_enemies(
                32 + i * 32, 16, 9, pygame.image.load("enemy1v2.png"))

    def add_player(self, lifes, speed, sprite):
        self.player = Player(
            lifes,
            speed,
            (self._width//2), self._length - Player.length,
            sprite)
        self.entities.append(self.player)
        self.entity_hitable_by_enemy.append(self.player)

    def add_enemy(self, speed, pos_x, pos_y, sprite):
        curr_enemy = Enemy(speed, pos_x, pos_y, sprite)
        self.enemies.append(curr_enemy)
        self.entities.append(curr_enemy)
        self.enemies_max_amount += 1
        self.entity_hitable_by_player.append(curr_enemy)

    def add_shield(self, position, health):
        curr_shield = Shield(position, health)
        self.shields.append(curr_shield)
        self.entities.append(curr_shield)
        self.entity_hitable_by_player.append(curr_shield)
        self.entity_hitable_by_enemy.append(curr_shield)

    def player_shoot(self):
        curr_projectile = self.player.make_projectile()
        self.projectiles.append(curr_projectile)
        self.entities.append(curr_projectile)
        self.projectiles_team_player.append(curr_projectile)

    def enemy_shoot(self, enemy):
        curr_projectile = enemy.make_projectile()
        self.projectiles.append(curr_projectile)
        self.entities.append(curr_projectile)
        self.projectiles_team_enemy.append(curr_projectile)

    def update_position(self, entity):
        entity.position().update_position(entity.speed())

    def add_row_of_enemies(self, height, top_left_cord, amount, sprite):
        for i in range(amount):
            self.add_enemy(Speed(1, 0), top_left_cord, height, sprite)
            top_left_cord += Enemy.width*2

    def update_projectile_positions(self):
        for projectile in self.projectiles:
            self.update_position(projectile)
            if projectile.position().y < 0:
                self.remove_projectile(projectile)

    def update_enemy_positions(self):
        change_dir = 0
        if self.since_last_enemy_move == self.enemies_max_amount:
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
                    if enemy.position().y() + Enemy.length >= self.player.position().y():
                        self.ongoing = False
                        self.result = False
                Enemy.speed = Speed(Enemy.speed.right() * (-1), 0)
        else:
            self.since_last_enemy_move += 1

    def remove_projectile(self, projectile):
        self.projectiles.remove(projectile)
        self.entities.remove(projectile)
        if projectile.team() == Player:
            self.projectiles_team_player.remove(projectile)
        else:
            self.projectiles_team_enemy.remove(projectile)

    def remove_enemy(self, enemy):
        self.enemies.remove(enemy)
        self.entities.remove(enemy)
        self.entity_hitable_by_player.remove(enemy)

    def remove_shield(self, shield):
        self.shields.remove(shield)
        self.entities.remove(shield)
        self.entity_hitable_by_player.remove(shield)
        self.entity_hitable_by_enemy.remove(shield)

    def enemy_hit(self, enemy, projectile):
        self.remove_enemy(enemy)
        self.remove_projectile(projectile)

    def shield_hit(self, shield, projectile):
        self.remove_projectile(projectile)
        if shield.take_hit():
            self.remove_shield()

    def update_projectiles(self):
        for projectile in self.projectiles:
            hitable_entities = []
            hitable_projectiles = []
            if projectile.team() == Player:
                hitable_entities = self.entity_hitable_by_player
                hitable_projectiles = self.projectiles_team_player
            else:
                hitable_entities = self.entity_hitable_by_enemy
                hitable_projectiles = self.projectiles_team_enemy
            for entity in hitable_entities:
                if check_if_hit(projectile, entity):
                    pass