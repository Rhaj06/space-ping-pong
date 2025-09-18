# space_pong/main.py
import pygame
from game import Game

def main():
    pygame.init()  # must be called before fonts/timers/mixer
    try:
        Game().run()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
