from math import radians
import pygame
import random
import math
from pygame.math import Vector2
from projectile import Projectile


class GuideBook():
    def __init__(self, game):
        self.enemy_sprite = pygame.image.load('Bullet Hell 1.0/Sprites/guide_book.png')
        self.name = "The Guide Book"
        self.game = game
        self.projectiles = []
        self.max_health = 100
        self.health = 100
        self.move = 0.5
        self.spawn_delay = 400
        self.attack_cd = 0
        self.x = 250
        self.y = 250
        self.stage = 0
        self.attack_rotation = 0
        self.attack_type = None
        self.boss_rect = pygame.Rect(self.x, self.y, self.enemy_sprite.get_width(), self.enemy_sprite.get_height())
        self.boss_rect.center = self.boss_rect.topleft
        self.x = self.boss_rect.left
        self.y = self.boss_rect.top
        #print(self.x, self.y)

    def count_downs(self):
        if self.attack_cd > 0:
            self.attack_cd -= 1
    
    def attack1(self, game, stage):
        
        if stage % 20 == 0:
            self.projectiles.append(Projectile(game, self.boss_rect.centerx, self.boss_rect.centery, random.uniform(-2, 2), random.uniform(-2, 2), 'Bullet Hell 1.0/Sprites/paper.png', 1500))

    def attack2(self, game, stage):

        if stage % 100 == 0:
            for i in range(20):
                vector = Vector2()
                vector.from_polar((10, (i+1+self.attack_rotation)*18))
                self.projectiles.append(Projectile(game, self.boss_rect.centerx, self.boss_rect.centery, vector[0], vector[1], 'Bullet Hell 1.0/Sprites/paper.png', 1500))
            self.attack_rotation += 4.5
    
    def attack3(self, game, stage, playerx, playery):
        x1, y1 = self.boss_rect.center
        x2, y2 = playerx, playery
        angle = math.degrees(math.atan2(y2-y1, x2-x1))
        if stage % 100 == 0:
            for i in range(5):
                vector = Vector2()
                vector.from_polar((5, angle - ((i-2)*20)))
                self.projectiles.append(Projectile(game, self.boss_rect.centerx, self.boss_rect.centery, vector[0], vector[1], 'Bullet Hell 1.0/Sprites/paper.png', 1500))
        


