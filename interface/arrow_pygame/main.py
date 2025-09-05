import pygame
from interface.arrow_pygame.game import Game

def main():
    pygame.init()
    try:
        Game().run()
    finally:
        pygame.quit()
