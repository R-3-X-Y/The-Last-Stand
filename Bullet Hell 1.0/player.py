import pygame
import math
from projectile import Projectile
from pygame.math import Vector2
#player class
class Player():
    def __init__(self, game):
        self.player_sprite = pygame.image.load('Bullet Hell 1.0/Sprites/player.png')
        self.game = game
        self.max_health = 5
        self.health = 5
        self.move = 1
        self.dashed_from = [0, 0]
        self.dashed_to = [0, 0]
        self.dash_cd = 0
        self.spawn_delay = 400
        self.attack_cd = 0
        self.bullet_speed = 10
        self.bullets = []
        self.x = 100
        self.y = 100
        self.player_rect = pygame.Rect(self.x, self.y, 10, 10)
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
    
    #fire a bullet at the mouse position
    def fire(self):
        self.game.sound_effects.play(self.game.fire_sound)
        x1, y1 = self.player_rect.center
        x2, y2 = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(y2-y1, x2-x1))
        vector = Vector2()
        vector.from_polar((self.bullet_speed, angle))
        self.bullets.append(Projectile(self.game, self.player_rect.centerx, self.player_rect.centery, vector[0], vector[1], 'Bullet Hell 1.0/Sprites/player_bullet.png', 20, 'paper'))
        self.game.shots_fired += 1
        self.game.total_shots_fired += 1
        






