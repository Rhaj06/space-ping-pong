# space_pong/enums.py
from enum import Enum

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    HIGH_SCORES = 5

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class PowerUpType(Enum):
    SPEED_BOOST = 1
    PADDLE_GROW = 2
    PADDLE_SHRINK = 3
    MULTI_BALL = 4
    SHIELD = 5
    FREEZE = 6
