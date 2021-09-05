import pygame
from game import Game
from player import Player

g = Game()

p = Player(g)

while g.running:
    g.curr_menu.display_menu()