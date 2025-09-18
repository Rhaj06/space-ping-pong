# space_pong/ball.py
import random, pygame
from vector import Vector2D
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, CYAN

class Ball:
    """Game ball with realistic physics"""
    def __init__(self, x, y, speed=8):
        self.x = x
        self.y = y
        self.base_speed = speed
        self.velocity = Vector2D(speed * random.choice([-1, 1]), speed * random.uniform(-0.5, 0.5))
        self.size = 8
        self.trail = []
        self.speed_multiplier = 1.0
        
    def update(self):
        # Update position
        self.x += self.velocity.x * self.speed_multiplier
        self.y += self.velocity.y * self.speed_multiplier
        
        # Add to trail for visual effect
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
        
        # Wall collision (top and bottom)
        if self.y <= self.size or self.y >= SCREEN_HEIGHT - self.size:
            self.velocity.y *= -1
            self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
    
    def paddle_collision(self, paddle_rect, paddle_center_y):
        """Handle collision with paddle"""
        ball_rect = self.get_rect()
        if ball_rect.colliderect(paddle_rect):
            # Calculate hit position relative to paddle center
            hit_pos = (self.y - paddle_center_y) / (paddle_rect.height / 2)
            hit_pos = max(-1, min(1, hit_pos))  # Clamp between -1 and 1
            
            # Reverse horizontal direction
            self.velocity.x *= -1
            
            # Adjust vertical velocity based on hit position
            self.velocity.y = hit_pos * self.base_speed * 0.75
            
            # Increase speed slightly for more exciting gameplay
            current_speed = self.velocity.magnitude()
            if current_speed < self.base_speed * 2:
                speed_increase = 1.05
                self.velocity = self.velocity * speed_increase
            
            # Move ball away from paddle to prevent sticking
            if paddle_rect.centerx < SCREEN_WIDTH // 2:  # Left paddle
                self.x = paddle_rect.right + self.size
            else:  # Right paddle
                self.x = paddle_rect.left - self.size
            
            return True
        return False
    
    def reset_position(self, direction=None):
        """Reset ball to center with optional direction"""
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        speed = self.base_speed
        
        if direction is None:
            direction = random.choice([-1, 1])
        
        self.velocity = Vector2D(speed * direction, speed * random.uniform(-0.5, 0.5))
        self.speed_multiplier = 1.0
        self.trail.clear()
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
    
    def draw(self, screen):
        # Draw trail
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)) * 0.3)
            trail_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            trail_surface.fill((*CYAN, alpha))
            screen.blit(trail_surface, (trail_x - self.size//2, trail_y - self.size//2))
        
        # Draw ball
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, CYAN, (int(self.x), int(self.y)), self.size, 2)