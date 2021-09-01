import pygame

#projectile class
class Projectile():
    def __init__(self, game, x, y, velx, vely, image, lifetime, name):
        self.game = game
        self.lifetime = lifetime
        self.projectile_sprite = pygame.image.load(image)
        self.dx = velx
        self.dy = vely
        self.attack_cd = 0
        self.x = x
        self.y = y
        self.projectile_rect = pygame.Rect(self.x, self.y, self.projectile_sprite.get_width(), self.projectile_sprite.get_height())