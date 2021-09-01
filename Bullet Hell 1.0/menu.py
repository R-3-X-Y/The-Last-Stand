import pygame
import sys
import random
from player import Play
from enemies import GuideBook
from projectile import Projectile


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('The Last Stand', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                self.game.curr_menu = self.game.play_game
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            if self.state == 'Controls':
                self.game.curr_menu = self.game.controls
            elif self.state == 'Volume':
                self.game.curr_menu = self.game.volume
            self.run_display = False

class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Volume', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Coming Soon', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()

class ControlsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Controls', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Movement   [WASD] or Arrow Keys', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('Shoot   Left Mouse Button', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            self.game.draw_text('Dash   [SPACEBAR]', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 50)
            self.blit_screen()

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Programming   R3XY', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()



class PlayGame(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.player = Play(game)
        self.enemy = GuideBook(game)
        self.game1 = game
    def show_health(self):
        pass
    def display_menu(self):
        self.game.playing = True
        dialog = True
        dialog_stage = 0
        clock = pygame.time.Clock()
        self.run_display = True
        self.gameover = False
        while self.run_display:
            
            #print(str(int(clock.get_fps())))
            
            clock.tick(100)

            self.game.check_events()
            self.game.display.fill([0, 0, 0])
            pygame.draw.rect(self.game.display, self.game.WHITE, pygame.Rect(0, self.game.DISPLAY_H - 50, self.game.DISPLAY_W, 50))
            
            player_health_bar_outline = pygame.Rect(10, self.game.DISPLAY_H - 40, 200, 30)
            
            player_health_bar = pygame.Rect(player_health_bar_outline.left + 3, player_health_bar_outline.top + 3, ((200 / self.player.max_health) * self.player.health) - 6, player_health_bar_outline.height - 3)
            
            pygame.draw.rect(self.game.display, [255, 0, 0, 255], player_health_bar)
            pygame.draw.rect(self.game.display, self.game.BLACK, player_health_bar_outline, width = 5, border_radius = 5)
            self.game.draw_text_black('YOU', 10, player_health_bar_outline.centerx, player_health_bar_outline.centery)

            enemy_health_bar_outline = player_health_bar_outline
            enemy_health_bar_outline.left = 280

            enemy_health_bar = pygame.Rect(enemy_health_bar_outline.left + 3, enemy_health_bar_outline.top + 3, ((200 / self.enemy.max_health) * self.enemy.health) - 6, enemy_health_bar_outline.height - 3)

            pygame.draw.rect(self.game.display, [255, 255, 0], enemy_health_bar)
            pygame.draw.rect(self.game.display, self.game.BLACK, enemy_health_bar_outline, width = 5, border_radius = 5)
            self.game.draw_text_black(self.enemy.name, 10, enemy_health_bar_outline.centerx, enemy_health_bar_outline.centery)

            self.player.player_rect.topleft = [self.player.x, self.player.y]
            
            for projectile in self.enemy.projectiles:
                projectile.projectile_rect.topleft = [projectile.x, projectile.y]
            for projectile in self.player.bullets:
                projectile.projectile_rect.topleft = [projectile.x, projectile.y]
            if self.player.spawn_delay > 0:
                pygame.draw.circle(self.game.display, self.game.WHITE, [self.player.player_rect.centerx, self.player.player_rect.centery], self.player.spawn_delay / 4, width = 10)
                self.player.spawn_delay -= 20
            else:
                if (self.game.UP_KEY) and (self.player.player_rect.top > 0):
                    self.player.y -= self.player.move
                if (self.game.DOWN_KEY) and (self.player.player_rect.bottom < self.game.DISPLAY_H - 50):
                    self.player.y += self.player.move
                if (self.game.LEFT_KEY) and (self.player.player_rect.left > 0):
                    self.player.x -= self.player.move
                if (self.game.RIGHT_KEY) and (self.player.player_rect.right < self.game.DISPLAY_W):
                    self.player.x += self.player.move
                if self.game.SHOOT and not dialog:
                    self.player.fire()
            if dialog:
                if dialog_stage == 0:
                    self.game.draw_text('Hello There Little Color', 15, self.enemy.boss_rect.centerx, self.enemy.boss_rect.bottom + 30)
                    self.game.draw_text('[Click to Continue]', 15, self.enemy.boss_rect.centerx, self.enemy.boss_rect.bottom + 60)
                elif dialog_stage == 1:
                    self.game.draw_text('I am here to guide you on', 15, self.enemy.boss_rect.centerx, self.enemy.boss_rect.bottom + 30)
                    self.game.draw_text('your adventure', 15, self.enemy.boss_rect.centerx, self.enemy.boss_rect.bottom + 60)
                elif dialog_stage == 2:
                    self.game.draw_text('There are two rules you should folow', 14, self.enemy.boss_rect.centerx, self.enemy.boss_rect.bottom + 30)
                    self.game.draw_text('One is never touch anything', 15, self.enemy.boss_rect.centerx, self.enemy.boss_rect.bottom + 60)
                elif dialog_stage == 3:
                    self.game.draw_text('The other is kill all that', 15, self.enemy.boss_rect.centerx, self.enemy.boss_rect.bottom + 30)
                    self.game.draw_text('stands in your way', 15, self.enemy.boss_rect.centerx, self.enemy.boss_rect.bottom + 60)
                elif dialog_stage == 4:
                    self.game.draw_text('This will be your first lesson', 15, self.enemy.boss_rect.centerx, self.enemy.boss_rect.bottom + 30)
                    self.game.draw_text('[Click to start battle]', 15, self.enemy.boss_rect.centerx, self.enemy.boss_rect.bottom + 60)
                elif dialog_stage == 5:
                    dialog = False
                if self.game.SHOOT:
                    dialog_stage += 1
            else:
                if self.enemy.attack_cd == 0:
                    if self.enemy.stage == 0:
                        self.enemy.attack_type = random.randint(1, 3)
                        if self.enemy.attack_type == 1:
                            self.enemy.stage = 500
                        elif self.enemy.attack_type == 2:
                            self.enemy.stage = 300
                        elif self.enemy.attack_type == 3:
                            self.enemy.stage = 300
                    if self.enemy.attack_type == 1:
                        self.enemy.attack1(self.game1, self.enemy.stage)
                        self.enemy.stage -= 1
                        if self.enemy.stage <= 0:
                            self.enemy.attack_rotation = 0
                            self.enemy.stage = 0
                            self.enemy.attack_type = None
                            self.enemy.attack_cd = 100
                    elif self.enemy.attack_type == 2:
                        self.enemy.attack2(self.game1, self.enemy.stage)
                        self.enemy.stage -= 1
                        if self.enemy.stage <= 0:
                            self.enemy.attack_rotation = 0
                            self.enemy.stage = 0
                            self.enemy.attack_type = None
                            self.enemy.attack_cd = 300
                    elif self.enemy.attack_type == 3:
                        self.enemy.attack3(self.game, self.enemy.stage, self.player.player_rect.centerx, self.player.player_rect.centery)
                        self.enemy.stage -= 1
                        if self.enemy.stage <= 0:
                            self.enemy.attack_rotation = 0
                            self.enemy.stage = 0
                            self.enemy.attack_type = None
                            self.enemy.attack_cd = 200
                else:
                    self.enemy.attack_cd -= 1
            self.move_projectiles()
            self.game.display.blit(self.player.player_sprite, [self.player.x,self.player.y])
            for projectile in self.enemy.projectiles:
                self.game.display.blit(projectile.projectile_sprite, [projectile.x, projectile.y])
            for projectile in self.player.bullets:
                self.game.display.blit(projectile.projectile_sprite, [projectile.x, projectile.y])
            self.game.display.blit(self.enemy.enemy_sprite, [self.enemy.x, self.enemy.y])
            self.blit_screen()
        self.game.playing = False
        self.enemy.projectiles.clear()
        self.enemy.health = self.enemy.max_health
        self.player.bullets.clear()
        self.player.health = self.player.max_health

    def move_projectiles(self):
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
            if projectile.projectile_rect.colliderect(self.player.player_rect):
                self.player.health -= 1
                self.enemy.projectiles.remove(projectile)
                if self.player.health <= 0:
                    #change to game over screen
                    pygame.quit()
                    sys.exit()
                    pass
            if projectile.lifetime <= 0:
                self.enemy.projectiles.remove(projectile)
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
            elif projectile.projectile_rect.colliderect(self.enemy.boss_rect):
                self.enemy.health -= 1
                self.player.bullets.remove(projectile)
                if self.enemy.health <= 0:
                    self.game.curr_menu = self.game.main_menu
                    self.gameover = True
            elif projectile.lifetime <= 0:
                self.player.bullets.remove(projectile)
            if self.gameover:
                #change to game over screen
                self.game.playing = False
                self.run_display = False
    










