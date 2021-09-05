import pygame
import random
from player import Player
from enemies import GuideBook
#create actual game
class Gameplay():
    def __init__(self, game):
        self.game = game
        self.player = Player(game)
        
        pass
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()
    def play_game(self):
        self.enemy = self.game.curr_enemy
        self.enemy.isDialog = True
        self.enemy.dialogStage = 0
        clock = pygame.time.Clock()
        self.run_display = True
        self.gameover = False
        #while the game is running
        while self.run_display:
            
            #print(str(int(clock.get_fps())))
            #set game tick rate
            clock.tick(100)

            #check key presses
            self.game.check_events()

            #fill background
            self.game.display.fill([0, 0, 0])
            
            #prepare player health bar
            player_health_bar_outline = pygame.Rect(10, self.game.DISPLAY_H - 40, 200, 30)
            player_health_bar = pygame.Rect(player_health_bar_outline.left + 3, player_health_bar_outline.top + 3, ((200 / self.player.max_health) * self.player.health) - 6, player_health_bar_outline.height - 3)

            #prepare enemy health bar
            enemy_health_bar_outline = pygame.Rect(10, self.game.DISPLAY_H - 40, 200, 30)
            enemy_health_bar_outline.left = 280
            enemy_health_bar = pygame.Rect(enemy_health_bar_outline.left + 3, enemy_health_bar_outline.top + 3, ((200 / self.enemy.max_health) * self.enemy.health) - 6, enemy_health_bar_outline.height - 3)

            #position hit boxes
            self.player.player_rect.topleft = [self.player.x, self.player.y]
            self.enemy.boss_rect.topleft = [self.enemy.x, self.enemy.y]

            for projectile in self.enemy.projectiles:
                projectile.projectile_rect.topleft = [projectile.x, projectile.y]
            for projectile in self.player.bullets:
                projectile.projectile_rect.topleft = [projectile.x, projectile.y]
            
            #player spawn in effect
            if self.player.spawn_delay > 0:
                pygame.draw.circle(self.game.display, self.game.WHITE, [self.player.player_rect.centerx, self.player.player_rect.centery], self.player.spawn_delay / 4, width = 10)
                self.player.spawn_delay -= 20
            
            #player movement
            else:
                if (self.game.UP_KEY) and (self.player.player_rect.top > 0):
                    self.player.y -= self.player.move
                if (self.game.DOWN_KEY) and (self.player.player_rect.bottom < self.game.DISPLAY_H - 50):
                    self.player.y += self.player.move
                if (self.game.LEFT_KEY) and (self.player.player_rect.left > 0):
                    self.player.x -= self.player.move
                if (self.game.RIGHT_KEY) and (self.player.player_rect.right < self.game.DISPLAY_W):
                    self.player.x += self.player.move
                if self.game.SHOOT and not self.enemy.isDialog:
                    self.player.fire()
                if self.player.dash_cd <= 0:
                    #player dashing
                    if (self.game.DASH_KEY) and ((self.game.UP_KEY) or (self.game.DOWN_KEY) or (self.game.LEFT_KEY) or (self.game.RIGHT_KEY)):
                        self.player.dashed_from = [self.player.x + 5, self.player.y + 5]
                        if self.game.UP_KEY:
                            self.player.y -= 50
                        if self.game.DOWN_KEY:
                            self.player.y += 50
                        if self.game.LEFT_KEY:
                            self.player.x -= 50
                        if self.game.RIGHT_KEY:
                            self.player.x += 50
                        self.player.dashed_to = [self.player.x + 5, self.player.y + 5]
                        self.player.dash_cd = 300
                else:
                    #draw a temporary line after dashing
                    if self.player.dash_cd >= 250:
                        pygame.draw.line(self.game.display, self.game.WHITE, self.player.dashed_from, self.player.dashed_to, width = 1)
                    self.player.dash_cd -= 1
            #enemy dialog
            if self.enemy.isDialog:
                self.enemy.isDialog, self.enemy.dialogStage = self.enemy.dialog(self.game, self.enemy.dialogStage)
            #enemy attacks if not talking
            else:
                #check atack cooldown
                if self.enemy.attack_cd == 0:
                    #check that enemy is not attacking
                    if self.enemy.stage == 0:
                        #choose random attack
                        self.enemy.attack_type = random.randint(1, 3)
                        #setup attack
                        if self.enemy.attack_type == 1:
                            self.enemy.stage = self.enemy.attack1_durration
                        elif self.enemy.attack_type == 2:
                            self.enemy.stage = self.enemy.attack2_durration
                        elif self.enemy.attack_type == 3:
                            self.enemy.stage = self.enemy.attack3_durration
                    #attack 1
                    if self.enemy.attack_type == 1:
                        self.enemy.attack1(self.game, self.enemy.stage, self.player.player_rect.centerx, self.player.player_rect.centery)
                        self.enemy.stage -= 1
                        if self.enemy.stage <= 0:
                            self.enemy.attack_rotation = 0
                            self.enemy.stage = 0
                            self.enemy.attack_type = None
                            self.enemy.attack_cd = self.enemy.attack1_cd
                    #attack 2
                    elif self.enemy.attack_type == 2:
                        self.enemy.attack2(self.game, self.enemy.stage, self.player.player_rect.centerx, self.player.player_rect.centery)
                        self.enemy.stage -= 1
                        if self.enemy.stage <= 0:
                            self.enemy.attack_rotation = 0
                            self.enemy.stage = 0
                            self.enemy.attack_type = None
                            self.enemy.attack_cd = self.enemy.attack2_cd
                    #attack 3
                    elif self.enemy.attack_type == 3:
                        self.enemy.attack3(self.game, self.enemy.stage, self.player.player_rect.centerx, self.player.player_rect.centery)
                        self.enemy.stage -= 1
                        if self.enemy.stage <= 0:
                            self.enemy.attack_rotation = 0
                            self.enemy.stage = 0
                            self.enemy.attack_type = None
                            self.enemy.attack_cd = self.enemy.attack3_cd
                #decrease countdown if active
                else:
                    self.enemy.attack_cd -= 1
                    #move enemy
                    if self.enemy.x < self.enemy.move_to_x:
                        self.enemy.x += 1
                    elif self.enemy.x > self.enemy.move_to_x:
                        self.enemy.x -= 1
                    if self.enemy.y < self.enemy.move_to_y:
                        self.enemy.y += 1
                    elif self.enemy.y > self.enemy.move_to_y:
                        self.enemy.y -= 1
                #get new position to pathfind to
                if self.enemy.attack_cd % 200 == 0 and self.enemy.attack_cd > 0:
                    self.enemy.move_to_x = random.randint(100, self.game.DISPLAY_W - 100)
                    self.enemy.move_to_y = random.randint(100, self.game.DISPLAY_H - 100)
            #move projectiles
            self.move_projectiles()
            #display player
            self.game.display.blit(self.player.player_sprite, [self.player.x,self.player.y])
            #display projectiles and bullets
            for projectile in self.enemy.projectiles:
                self.game.display.blit(projectile.projectile_sprite, [projectile.x, projectile.y])
            for projectile in self.player.bullets:
                self.game.display.blit(projectile.projectile_sprite, [projectile.x, projectile.y])
            #display enemy
            self.game.display.blit(self.enemy.enemy_sprite, [self.enemy.x, self.enemy.y])
            #draw health bars
            pygame.draw.rect(self.game.display, self.game.WHITE, pygame.Rect(0, self.game.DISPLAY_H - 50, self.game.DISPLAY_W, 50))
            pygame.draw.rect(self.game.display, [255, 0, 0, 255], player_health_bar)
            pygame.draw.rect(self.game.display, self.game.BLACK, player_health_bar_outline, width = 5, border_radius = 5)
            pygame.draw.rect(self.game.display, [255, 255, 0], enemy_health_bar)
            pygame.draw.rect(self.game.display, self.game.BLACK, enemy_health_bar_outline, width = 5, border_radius = 5)
            self.game.draw_text_black('YOU', 10, player_health_bar_outline.centerx, player_health_bar_outline.centery)
            self.game.draw_text_black(self.enemy.name, 10, enemy_health_bar_outline.centerx, enemy_health_bar_outline.centery)
            #blit screen
            self.blit_screen()
        #set variables after game ends
        self.game.playing = False
        self.enemy.projectiles.clear()
        self.enemy.health = self.enemy.max_health
        self.enemy.x = 250
        self.enemy.y = 250
        self.player.bullets.clear()
        if self.player.health <= 0:
            self.player.health = self.player.max_health
        elif self.player.health < 5:
            self.player.health += 1
        self.player.x = 100
        self.player.y = 100

    #move projectiles
    def move_projectiles(self):
        #move enemy projectiles
        for projectile in self.enemy.projectiles:
            projectile.x += projectile.dx
            projectile.y += projectile.dy
            projectile.lifetime -= 1
            if projectile.projectile_rect.bottom < 0:
                self.enemy.projectiles.remove(projectile)
            elif projectile.projectile_rect.top > self.game.DISPLAY_H - 50:
                self.enemy.projectiles.remove(projectile)
            elif projectile.projectile_rect.right < 0:
                self.enemy.projectiles.remove(projectile)
            elif projectile.projectile_rect.left > self.game.DISPLAY_W:
                self.enemy.projectiles.remove(projectile)
            #check if player is hit
            if projectile.projectile_rect.colliderect(self.player.player_rect):
                if self.player.health > 0:
                    self.player.health -= 1
                    self.game.health_lost += 1
                    self.game.total_health_lost += 1
                self.enemy.projectiles.remove(projectile)
                if self.player.health <= 0:
                    #change to game over screen
                    self.game.curr_menu = self.game.lose
                    self.game.player_died = True
                    self.run_display = False
            #check projectile lifetime
            if projectile.lifetime <= 0:
                self.enemy.projectiles.remove(projectile)
        #move player bullets
        for projectile in self.player.bullets:
            projectile.x += projectile.dx
            projectile.y += projectile.dy
            projectile.lifetime -= 1
            if projectile.projectile_rect.bottom < 0:
                self.player.bullets.remove(projectile)
            elif projectile.projectile_rect.top > self.game.DISPLAY_H - 50:
                self.player.bullets.remove(projectile)
            elif projectile.projectile_rect.right < 0:
                self.player.bullets.remove(projectile)
            elif projectile.projectile_rect.left > self.game.DISPLAY_W:
                self.player.bullets.remove(projectile)
            #check if bullet hits enemy
            elif projectile.projectile_rect.colliderect(self.enemy.boss_rect):
                self.enemy.health -= 1
                self.game.shots_hit += 1
                self.game.total_shots_hit += 1
                self.player.bullets.remove(projectile)
                if self.enemy.health <= 0:
                    #change to game over screen
                    self.game.curr_menu = self.game.stats
                    self.gameover = True
            #check projectile lifetime
            elif projectile.lifetime <= 0:
                self.player.bullets.remove(projectile)
            if self.gameover:
                self.run_display = False