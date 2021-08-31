from math import radians
import pygame
import random
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
        self.attack_type = None
        self.boss_rect = pygame.Rect(self.x, self.y, self.enemy_sprite.get_width(), self.enemy_sprite.get_height())
        self.boss_rect.center = self.boss_rect.topleft
        self.x = self.boss_rect.left
        self.y = self.boss_rect.top
        #print(self.x, self.y)

    def count_downs(self):
        if self.attack_cd > 0:
            self.attack_cd -= 1
    
    def attack1(self,game, stage):
        
        if stage % 50 == 0:
            self.projectiles.append(Projectile(game, self.boss_rect.centerx, self.boss_rect.centery, random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 'Bullet Hell 1.0/Sprites/paper.png'))
