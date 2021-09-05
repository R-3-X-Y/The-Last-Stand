from math import degrees
import pygame
import sys
import random
from player import Player
from enemies import GuideBook
from play import Gameplay

#create the default menu class
class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 110

    def draw_cursor(self):
        self.game.draw_text('>', 15, self.cursor_rect.x, self.cursor_rect.y)

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
            self.game.draw_text('The Last Stand [Demo]', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
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
            self.game.sound_effects.play(self.game.select_sound)
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
            self.game.sound_effects.play(self.game.back_sound)
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
            self.game.sound_effects.play(self.game.select_sound)
            if self.state == 'Controls':
                self.game.curr_menu = self.game.controls
            elif self.state == 'Volume':
                self.game.curr_menu = self.game.volume
            self.run_display = False

#create volume menu
class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Sound Effects'
        self.effect_volx, self.effect_voly = self.mid_w, self.mid_h + 20
        self.music_volx, self.music_voly = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.effect_volx + self.offset, self.effect_voly)

    #display menu on screen
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Volume Settings', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Sound Effects: " + str(self.game.effect_volume), 15, self.effect_volx, self.effect_voly)
            self.game.draw_text("Music: " + str(self.game.music_volume), 15, self.music_volx, self.music_voly)
            self.game.draw_text("Use left or right to change volume", 15, self.mid_w, self.mid_h + 60)
            self.draw_cursor()
            self.blit_screen()

    #check what option is selected
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.sound_effects.play(self.game.back_sound)
            self.game.curr_menu = self.game.options
            self.run_display = False
        elif self.game.DOWN_KEY or self.game.UP_KEY:
            if self.state == 'Sound Effects':
                self.state = 'Music'
                self.cursor_rect.midtop = (self.music_volx + self.offset, self.music_voly)
            elif self.state == 'Music':
                self.state = 'Sound Effects'
                self.cursor_rect.midtop = (self.effect_volx + self.offset, self.effect_voly)
        elif self.game.LEFT_KEY:
            if self.state == 'Sound Effects':
                if self.game.effect_volume >= 1:
                    self.game.effect_volume -= 1
            elif self.state == 'Music':
                if self.game.music_volume >= 1:
                    self.game.music_volume -= 1
        elif self.game.RIGHT_KEY:
            if self.state == 'Sound Effects':
                if self.game.effect_volume <= 99:
                    self.game.effect_volume += 1
            elif self.state == 'Music':
                if self.game.music_volume <= 99:
                    self.game.music_volume += 1
        self.game.sound_effects.set_volume(self.game.effect_volume / 100)
        pygame.mixer.music.set_volume(self.game.music_volume / 100)
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
                self.game.sound_effects.play(self.game.back_sound)
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Controls', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Movement: [WASD] or Arrow Keys', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('Shoot: Left Mouse Button', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            self.game.draw_text('Dash: [SPACEBAR]', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 50)
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
                self.game.sound_effects.play(self.game.back_sound)
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Programming: R3XY', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('Art: R3XY', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 40)
            self.game.draw_text('Menu system is from a tutorial', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 70)
            self.game.draw_text('by Christial Duenas on Youtube', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 100)
            self.game.draw_text('Music: DM Dokuro', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 130)
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
                self.game.sound_effects.play(self.game.select_sound)
                self.game.curr_menu = self.game.stats
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('You Died ;(', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('How Pathetic', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            text = "You Made It To " + self.game.curr_enemy.name
            self.game.draw_text(text, 10, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 80)
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
                self.game.sound_effects.play(self.game.select_sound)
                self.game.curr_menu = self.game.credits
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('You Won GG', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.blit_screen()
#create stats menu
class StatsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self, game)

    #display menu
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.sound_effects.play(self.game.select_sound)
                if self.game.player_died:
                    self.game.curr_menu = self.game.main_menu
                    self.game.curr_enemy = GuideBook(self.game)
                    self.game.reset_keys()
                    self.game.total_shots_fired = 0
                    self.game.total_shots_hit = 0
                    self.game.total_health_lost = 0
                    self.game.player_died = False
                elif self.game.curr_enemy.next_boss == None:
                    self.game.curr_menu = self.game.win
                    self.game.reset_keys()
                else:
                    self.game.curr_menu = self.game.play_game
                    self.game.playing = True
                    self.game.curr_enemy = self.game.curr_enemy.next_boss
                    
                self.game.shots_fired = 0
                self.game.shots_hit = 0
                self.game.health_lost = 0
                self.run_display = False
            else:
                self.game.display.fill(self.game.BLACK)
                if self.game.shots_fired != 0:
                    accuracy = round((self.game.shots_hit / self.game.shots_fired)*100)
                else:
                    accuracy = 0
                if self.game.total_shots_fired != 0:
                    total_accuracy = round((self.game.total_shots_hit / self.game.total_shots_fired)*100)
                else:
                    total_accuracy = 0

                self.game.draw_text("Last Battle:", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 70)
                self.game.draw_text("Shots Fired: " + str(self.game.shots_fired) + " Shots Hit: " + str(self.game.shots_hit), 10, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 40)
                self.game.draw_text("Accuracy: " + str(accuracy) + "%", 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
                self.game.draw_text("Damage Taken: " + str(self.game.health_lost), 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
                self.game.draw_text("This Game:", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
                self.game.draw_text("Total Shots Fired: " + str(self.game.total_shots_fired) + " Total Shots Hit: " + str(self.game.total_shots_hit), 10, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)
                self.game.draw_text("Total Accuracy: " + str(total_accuracy) + "%", 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 80)
                self.game.draw_text("Total Damage Taken: " + str(self.game.total_health_lost), 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 100)
                self.blit_screen()
#the game running class
class PlayGame(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.player = Player(game)
        self.enemy = GuideBook(game)
        self.playgame = Gameplay(game)
    #display the game
    def display_menu(self):
        self.playgame.play_game()
    










