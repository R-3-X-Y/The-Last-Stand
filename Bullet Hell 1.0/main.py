import pygame
from game import Game
from player import Play
from sprite import Sprite

g = Game()

p = Play(g)

while g.running:
    g.curr_menu.display_menu()
