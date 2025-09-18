# space_pong/particles.py
import random, pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Particle:
    """Particle system for visual effects"""
    def __init__(self, x, y, color, velocity, lifetime=60):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
        self.lifetime -= 1
        
        # Fade out effect
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        self.color = (*self.color[:3], max(0, alpha))
    
    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
    
    def is_alive(self):
        return self.lifetime > 0

class Star:
    """Background stars for space theme"""
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.1, 1.0)
        self.size = random.randint(1, 3)
        self.brightness = random.randint(100, 255)
    
    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)