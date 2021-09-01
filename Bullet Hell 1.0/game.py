import pygame
import sys
from menu import *


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.DASH_KEY, self.SHOOT, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 500, 550
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        pygame.display.set_caption('Bullet Hell Warrior')
        self.font_name = 'Bullet Hell 1.0/Fonts/8-BIT WONDER.TTF'
        #self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.volume = VolumeMenu(self)
        self.controls = ControlsMenu(self)
        self.credits = CreditsMenu(self)
        self.play_game = PlayGame(self)
        self.curr_menu = self.main_menu
        

    



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
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
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                    self.DOWN_KEY = False
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                    self.UP_KEY = False
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                    self.LEFT_KEY = False
                if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                    self.RIGHT_KEY = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons_pressed = pygame.mouse.get_pressed()
                if buttons_pressed[0]:
                    self.SHOOT = True

    def reset_keys(self):
        if self.playing:
            self.DASH_KEY, self.SHOOT, self.START_KEY, self.BACK_KEY = False, False, False, False
        else:
            self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.DASH_KEY, self.SHOOT, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    
    def draw_text_black(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)





