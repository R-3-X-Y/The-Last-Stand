import pygame
import sys
from menu import *
from enemies import *
#create game class
class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.running, self.playing = True, False
        #prepare dispay
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.DASH_KEY, self.SHOOT, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 500, 550
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        pygame.display.set_caption('Bullet Hell Warrior')
        #set font
        self.font_name = 'Bullet Hell 1.0/Fonts/joystix.monospace.ttf'
        #self.font_name = pygame.font.get_default_font()
        #set colors
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        #set sounds
        self.effect_volume = 100
        self.music_volume = 10
        self.select_sound = pygame.mixer.Sound('Bullet Hell 1.0/Sound Effects/menu_forward.wav')
        self.select_sound.set_volume(0.05)
        self.back_sound = pygame.mixer.Sound('Bullet Hell 1.0/Sound Effects/menu_backward.wav')
        self.back_sound.set_volume(0.05)
        self.fire_sound = pygame.mixer.Sound('Bullet Hell 1.0/Sound Effects/shoot.wav')
        self.fire_sound.set_volume(0.1)
        self.text_sound = pygame.mixer.Sound('Bullet Hell 1.0/Sound Effects/text.wav')
        self.text_sound.set_volume(0.1)
        self.music1 = pygame.mixer.music.load("Bullet Hell 1.0/Music/music1.wav")
        self.sound_effects = pygame.mixer.Channel(1)
        self.sound_effects.set_volume(self.effect_volume / 100)
        pygame.mixer.music.set_volume(self.music_volume / 100)
        pygame.mixer.music.play(-1, fade_ms = 1000)
        #load menus
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.volume = VolumeMenu(self)
        self.controls = ControlsMenu(self)
        self.credits = CreditsMenu(self)
        self.play_game = PlayGame(self)
        self.lose = DeathMenu(self)
        self.win = WinMenu(self)
        self.stats = StatsMenu(self)
        self.curr_enemy = GuideBook(self)
        self.curr_menu = self.main_menu
        #player stats for current enemy
        self.health_lost = 0
        self.shots_fired = 0
        self.shots_hit = 0
        #player stats for session
        self.total_health_lost = 0
        self.total_shots_fired = 0
        self.total_shots_hit = 0
        #player gameover
        self.player_died = False
    #check key presses
    def check_events(self):
        for event in pygame.event.get():
            #stop the program if the window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #check key downs
            if event.type == pygame.KEYDOWN:
                #quit game on escape key
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                    self.DOWN_KEY = True
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                    self.UP_KEY = True
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                    self.LEFT_KEY = True
                if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                    self.RIGHT_KEY = True
                if (event.key == pygame.K_SPACE):
                    self.DASH_KEY = True
            #check key ups
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                    self.DOWN_KEY = False
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                    self.UP_KEY = False
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                    self.LEFT_KEY = False
                if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                    self.RIGHT_KEY = False
            #fire bullets when mouse is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons_pressed = pygame.mouse.get_pressed()
                if buttons_pressed[0]:
                    self.SHOOT = True
    
    #reset keys
    def reset_keys(self):
        if self.playing:
            self.DASH_KEY, self.SHOOT, self.START_KEY, self.BACK_KEY = False, False, False, False
        else:
            self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.DASH_KEY, self.SHOOT, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False, False, False

    #draw text function
    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    
    #draw text but black function
    def draw_text_black(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)