from math import radians
import pygame
import random
import math
from pygame.math import Vector2
from projectile import Projectile

#create enemy 1
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
        self.move_to_x = self.x
        self.move_to_y = self.y
        self.stage = 0
        self.attack_rotation = 0
        self.attack_type = None
        self.boss_rect = pygame.Rect(self.x, self.y, self.enemy_sprite.get_width(), self.enemy_sprite.get_height())
        self.boss_rect.center = self.boss_rect.topleft
        self.x = self.boss_rect.left
        self.y = self.boss_rect.top
        #print(self.x, self.y)
    
    #enemy 1 dialog
    def dialog(self, game, dialog_stage):
        dialog = True
        next_text = dialog_stage
        if dialog_stage == 0:
            game.draw_text('Hello There Little Color', 15, self.boss_rect.centerx, self.boss_rect.bottom + 30)
            game.draw_text('[Click to Continue]', 15, self.boss_rect.centerx, self.boss_rect.bottom + 60)
        elif dialog_stage == 1:
            game.draw_text('I am here to guide you on', 15, self.boss_rect.centerx, self.boss_rect.bottom + 30)
            game.draw_text('your adventure', 15, self.boss_rect.centerx, self.boss_rect.bottom + 60)
        elif dialog_stage == 2:
            game.draw_text('There are two rules you should folow', 14, self.boss_rect.centerx, self.boss_rect.bottom + 30)
            game.draw_text('One is never touch anything', 15, self.boss_rect.centerx, self.boss_rect.bottom + 60)
        elif dialog_stage == 3:
            game.draw_text('The other is kill all that', 15, self.boss_rect.centerx, self.boss_rect.bottom + 30)
            game.draw_text('stands in your way', 15, self.boss_rect.centerx, self.boss_rect.bottom + 60)
        elif dialog_stage == 4:
            game.draw_text('This will be your first lesson', 15, self.boss_rect.centerx, self.boss_rect.bottom + 30)
            game.draw_text('[Click to start battle]', 15, self.boss_rect.centerx, self.boss_rect.bottom + 60)
        elif dialog_stage == 5:
            dialog = False
        else:
            dialog = True
        if game.SHOOT:
            next_text = dialog_stage + 1
        return dialog, next_text
    
    #enemy attack 1 
    def attack1(self, game, stage):
        
        if stage % 20 == 0:
            #fire a projectile in random direction
            self.projectiles.append(Projectile(game, self.boss_rect.centerx, self.boss_rect.centery, random.uniform(-2, 2), random.uniform(-2, 2), 'Bullet Hell 1.0/Sprites/paper.png', 1500, 'paper'))

    #enemy attack 2
    def attack2(self, game, stage):

        if stage % 100 == 0:
            #fire out projectiles in a circle
            for i in range(20):
                vector = Vector2()
                vector.from_polar((10, (i+1+self.attack_rotation)*18))
                self.projectiles.append(Projectile(game, self.boss_rect.centerx, self.boss_rect.centery, vector[0], vector[1], 'Bullet Hell 1.0/Sprites/paper.png', 1500, 'paper'))
            self.attack_rotation += 4.5
        if stage % 100 <= 50 and stage >= 100:
            #trace path of bullets to be fired
            for i in range(20):
                vector = Vector2()
                vector.from_polar((10, (i+1+self.attack_rotation)*18))
                pygame.draw.line(self.game.display, self.game.WHITE, [self.boss_rect.centerx, self.boss_rect.centery], [self.boss_rect.centerx + (vector[0]*300), self.boss_rect.centery + (vector[1]*300)], width = 2)
    
    #enemy attack 3
    def attack3(self, game, stage, playerx, playery):
        x1, y1 = self.boss_rect.center
        x2, y2 = playerx, playery
        angle = math.degrees(math.atan2(y2-y1, x2-x1))
        if stage % 100 == 0:
            #fire a spread of bullets at the player
            for i in range(5):
                vector = Vector2()
                vector.from_polar((5, angle - ((i-2)*20)))
                self.projectiles.append(Projectile(game, self.boss_rect.centerx, self.boss_rect.centery, vector[0], vector[1], 'Bullet Hell 1.0/Sprites/paper.png', 1500, 'paper'))
        


