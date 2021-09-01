import pygame
from game import Game
from player import Play

g = Game()

p = Play(g)

while g.running:
    g.curr_menu.display_menu()
