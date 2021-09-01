from math import degrees
import pygame
import sys
import random
from player import Play
from enemies import GuideBook

#create the default menu class
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

#create main menu
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.quitx, self.quity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    #display menu on screen
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('The Last Stand [ Demo ]', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.game.draw_text("Quit", 20, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()

    #move the selector
    def move_cursor(self):
        #down
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        #up
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    #check what option is selected
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
            elif self.state == 'Quit':
                pygame.quit()
                sys.exit()
            self.run_display = False

#create options menu
class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    #display menu on screen
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

    #check what option is selected
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

#create volume menu
class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    #display menu
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

#create controls menu
class ControlsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    
    #display menu
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

#create credits menu
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    #display menu
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
            self.game.draw_text('Art   R3XY', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 40)
            self.game.draw_text('Menu system is from a tutorial', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 70)
            self.game.draw_text('by Christial Duenas on Youtube', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 100)
            self.game.draw_text('Everything else   R3XY', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 130)
            self.blit_screen()

#create death menu
class DeathMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    #display menu
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('You Died', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('How Pathetic', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            self.blit_screen()

#create win menu
class WinMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    #display menu
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.credits
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('You Won GG', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.blit_screen()

#the game running class
class PlayGame(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.player = Play(game)
        self.enemy = GuideBook(game)
        self.game1 = game
    
    #display the game
    def display_menu(self):
        dialog = True
        dialog_stage = 0
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
                if self.game.SHOOT and not dialog:
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
            if dialog:
                dialog, dialog_stage = self.enemy.dialog(self.game, dialog_stage)
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
                            self.enemy.stage = 500
                        elif self.enemy.attack_type == 2:
                            self.enemy.stage = 350
                        elif self.enemy.attack_type == 3:
                            self.enemy.stage = 300
                    #attack 1
                    if self.enemy.attack_type == 1:
                        self.enemy.attack1(self.game1, self.enemy.stage)
                        self.enemy.stage -= 1
                        if self.enemy.stage <= 0:
                            self.enemy.attack_rotation = 0
                            self.enemy.stage = 0
                            self.enemy.attack_type = None
                            self.enemy.attack_cd = 100
                    #attack 2
                    elif self.enemy.attack_type == 2:
                        self.enemy.attack2(self.game1, self.enemy.stage)
                        self.enemy.stage -= 1
                        if self.enemy.stage <= 0:
                            self.enemy.attack_rotation = 0
                            self.enemy.stage = 0
                            self.enemy.attack_type = None
                            self.enemy.attack_cd = 300
                    #attack 3
                    elif self.enemy.attack_type == 3:
                        self.enemy.attack3(self.game, self.enemy.stage, self.player.player_rect.centerx, self.player.player_rect.centery)
                        self.enemy.stage -= 1
                        if self.enemy.stage <= 0:
                            self.enemy.attack_rotation = 0
                            self.enemy.stage = 0
                            self.enemy.attack_type = None
                            self.enemy.attack_cd = 200
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
        self.player.health = self.player.max_health
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
                self.player.health -= 1
                self.enemy.projectiles.remove(projectile)
                if self.player.health <= 0:
                    #change to game over screen
                    self.game.curr_menu = self.game.lose
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
                self.player.bullets.remove(projectile)
                if self.enemy.health <= 0:
                    #change to game over screen
                    self.game.curr_menu = self.game.win
                    self.gameover = True
            #check projectile lifetime
            elif projectile.lifetime <= 0:
                self.player.bullets.remove(projectile)
            if self.gameover:
                self.run_display = False
    










