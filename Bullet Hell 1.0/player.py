import pygame

class Play():
    def __init__(self, game):
        self.player_sprite = pygame.image.load('Bullet Hell 1.0/Sprites/player.png')
        self.game = game
        self.max_health = 5
        self.health = 5
        self.lives = 3
        self.move = 0.1
        self.spawn_delay = 400
        self.attack_type = 0
        self.attack_cd = 0
        self.x = 100
        self.y = 100
        self.player_rect = pygame.Rect(self.x, self.y, 10, 10)
        self.mouseX, self.mouseY = pygame.mouse.get_pos()

    def count_downs(self):
        if self.attack_cd > 0:
            self.attack_cd -= 1
    
    def fire(self, attack_type):
        self.mouseX, self.mouseY = pygame.mouse.get_pos()




