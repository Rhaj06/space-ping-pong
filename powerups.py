# space_pong/powerups.py
import math, pygame
from enums import PowerUpType
from settings import CYAN, GREEN, RED, PURPLE, GOLD, BLUE, WHITE, SCREEN_HEIGHT

class PowerUp:
    """Power-up items that appear during gameplay"""
    def __init__(self, x, y, power_type: PowerUpType):
        self.x = x
        self.y = y
        self.power_type = power_type
        self.size = 30
        self.lifetime = 300  # 5 seconds at 60 FPS
        self.float_offset = 0
        self.colors = {
            PowerUpType.SPEED_BOOST: CYAN,
            PowerUpType.PADDLE_GROW: GREEN,
            PowerUpType.PADDLE_SHRINK: RED,
            PowerUpType.MULTI_BALL: PURPLE,
            PowerUpType.SHIELD: GOLD,
            PowerUpType.FREEZE: BLUE
        }
    
    def update(self):
        self.lifetime -= 1
        self.float_offset += 0.1
        self.y += math.sin(self.float_offset) * 0.5
    
    def draw(self, screen):
        if self.lifetime > 0:
            color = self.colors.get(self.power_type, WHITE)
            # Draw power-up with pulsing effect
            pulse = abs(math.sin(self.float_offset * 2)) * 5 + self.size
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(pulse), 3)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size // 2)
    
    def is_alive(self):
        return self.lifetime > 0
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)