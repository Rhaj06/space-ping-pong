# space_pong/paddle.py
import random, pygame
from enums import Difficulty, PowerUpType
from settings import SCREEN_HEIGHT, WHITE, GREEN, RED, GOLD


class Paddle:
    """Player paddle with enhanced features"""
    def __init__(self, x, y, is_player=True):
        self.x = x
        self.y = y
        self.width = 15
        self.base_height = 100
        self.height = self.base_height
        self.speed = 8
        self.is_player = is_player
        self.effects = {}  # Store active effects
        self.shield_active = False
        self.shield_duration = 0
        
    def update(self, keys=None, ball=None, difficulty=Difficulty.MEDIUM):
        # Update effects
        for effect_type in list(self.effects.keys()):
            self.effects[effect_type] -= 1
            if self.effects[effect_type] <= 0:
                self.remove_effect(effect_type)
        
        # Update shield
        if self.shield_duration > 0:
            self.shield_duration -= 1
            if self.shield_duration <= 0:
                self.shield_active = False
        
        # Player movement
        if self.is_player and keys:
            if keys[pygame.K_UP] and self.y > 0:
                self.y -= self.speed
            if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
                self.y += self.speed
        
        # AI movement
        elif not self.is_player and ball:
            self.ai_move(ball, difficulty)
        
        # Keep paddle within screen bounds
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
    
    def ai_move(self, ball, difficulty):
        """AI paddle movement with difficulty scaling"""
        target_y = ball.y - self.height // 2
        
        # Difficulty adjustments
        if difficulty == Difficulty.EASY:
            speed_factor = 0.2
            prediction_error = random.randint(-30, 30)
        elif difficulty == Difficulty.MEDIUM:
            speed_factor = 0.5
            prediction_error = random.randint(-15, 15)
        else:  # HARD
            speed_factor = 1.0
            prediction_error = random.randint(-5, 5)
        
        target_y += prediction_error
        
        # Move towards target
        if abs(target_y - self.y) > 5:
            if target_y > self.y:
                self.y += self.speed * speed_factor
            else:
                self.y -= self.speed * speed_factor
    
    def apply_effect(self, effect_type: PowerUpType, duration=300):
        """Apply power-up effect to paddle"""
        self.effects[effect_type] = duration
        
        if effect_type == PowerUpType.PADDLE_GROW:
            self.height = min(self.base_height * 1.5, 150)
        elif effect_type == PowerUpType.PADDLE_SHRINK:
            self.height = max(self.base_height * 0.5, 50)
        elif effect_type == PowerUpType.SHIELD:
            self.shield_active = True
            self.shield_duration = duration
    
    def remove_effect(self, effect_type: PowerUpType):
        """Remove power-up effect"""
        if effect_type in self.effects:
            del self.effects[effect_type]
            
        if effect_type in [PowerUpType.PADDLE_GROW, PowerUpType.PADDLE_SHRINK]:
            self.height = self.base_height
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_center_y(self):
        return self.y + self.height // 2
    
    def draw(self, screen):
        # Draw paddle
        color = WHITE
        if PowerUpType.PADDLE_GROW in self.effects:
            color = GREEN
        elif PowerUpType.PADDLE_SHRINK in self.effects:
            color = RED
            
        pygame.draw.rect(screen, color, self.get_rect())
        
        # Draw shield effect
        if self.shield_active:
            shield_rect = pygame.Rect(self.x - 5, self.y - 5, self.width + 10, self.height + 10)
            pygame.draw.rect(screen, GOLD, shield_rect, 3)