# space_pong/game.py
import math, random, pygame
from enums import GameState, Difficulty, PowerUpType
from settings import *
from particles import Particle, Star
from powerups import PowerUp
from paddle import Paddle
from ball import Ball
from vector import Vector2D
from storage import load_high_scores, save_high_scores

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Ping Pong")
        self.clock = pygame.time.Clock()

        # Fonts (after pygame.init())
        try:
            self.font = pygame.font.Font("freesansbold.ttf", 32)
            self.title_font = pygame.font.Font("freesansbold.ttf", 84)
            self.small_font = pygame.font.Font("freesansbold.ttf", 20)
            self.menu_font = pygame.font.Font("freesansbold.ttf", 38)
        except:
            self.font = pygame.font.Font(None, 32)
            self.title_font = pygame.font.Font(None, 84)
            self.small_font = pygame.font.Font(None, 20)
            self.menu_font = pygame.font.Font(None, 32)

        # game state & objects (same as your file) ...
        self.state = GameState.MENU
        self.running = True
        self.game_mode = "vs_computer"
        self.difficulty = Difficulty.MEDIUM

        self.stars = [Star() for _ in range(100)]
        self.particles = []
        self.power_ups = []
        self.balls = []

        self.reset_game()
        self.player1_score = 0
        self.player2_score = 0
        self.high_scores = load_high_scores()

        self.power_up_timer = 0
        self.power_up_spawn_interval = 600
        self.screen_shake = 0
        self.freeze_timer = 0
        self.menu_time = 0
        self.menu_pulse = 0

    # reset_game, handle_events, handle_menu_input,
    # update, update_gameplay, update_power_ups, spawn_power_up,
    # apply_power_up, add_hit_effect, add_score_effect, add_power_up_effect,
    # draw, draw_menu, draw_game, draw_pause_overlay, draw_game_over,
    # draw_high_scores (but call save_high_scores(self.high_scores) where needed)

    def reset_game(self):
        """Reset game to initial state"""
        self.balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        # Player 1 is now RIGHT paddle, Player 2 is LEFT paddle
        self.paddle1 = Paddle(SCREEN_WIDTH - 45, SCREEN_HEIGHT // 2 - 50, True)  # Right paddle (Player 1)
        self.paddle2 = Paddle(30, SCREEN_HEIGHT // 2 - 50, 
                              self.game_mode == "vs_human")  # Left paddle (Player 2/Computer)
        self.power_ups.clear()
        self.particles.clear()
        self.player1_score = 0
        self.player2_score = 0
        self.power_up_timer = 0
        self.freeze_timer = 0
        self.screen_shake = 0
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    self.handle_menu_input(event.key)
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.HIGH_SCORES:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
    
    def handle_menu_input(self, key):
        """Handle menu navigation"""
        if key == pygame.K_1:
            self.game_mode = "vs_computer"
            self.reset_game()
            self.state = GameState.PLAYING
        elif key == pygame.K_2:
            self.game_mode = "vs_human"
            self.reset_game()
            self.state = GameState.PLAYING
        elif key == pygame.K_3:
            self.state = GameState.HIGH_SCORES
        elif key == pygame.K_e:
            self.difficulty = Difficulty.EASY
        elif key == pygame.K_m:
            self.difficulty = Difficulty.MEDIUM
        elif key == pygame.K_h:
            self.difficulty = Difficulty.HARD
        elif key == pygame.K_ESCAPE:
            self.running = False
    
    def update(self):
        """Update game state"""
        # Update background stars
        for star in self.stars:
            star.update()
        
        # Update particles
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()
        
        if self.state == GameState.MENU:
            self.menu_time += 1
            self.menu_pulse = abs(math.sin(self.menu_time * 0.05)) * 0.3 + 0.7
        elif self.state == GameState.PLAYING:
            self.update_gameplay()
        
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
    
    def update_gameplay(self):
        """Update gameplay elements"""
        keys = pygame.key.get_pressed()
        
        # Handle freeze effect
        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            return
        
        # Update paddle 1 (RIGHT paddle - Player 1) - Arrow Keys
        self.paddle1.update(keys)
        
        # Update paddle 2 (LEFT paddle) based on game mode
        if self.game_mode == "vs_human":
            # Player 2 controls (W/S keys) for LEFT paddle
            keys_p2 = {
                pygame.K_UP: keys[pygame.K_w],
                pygame.K_DOWN: keys[pygame.K_s]
            }
            self.paddle2.update(keys_p2)
        else:
            # Computer AI control for LEFT paddle
            self.paddle2.update(ball=self.balls[0] if self.balls else None, 
                              difficulty=self.difficulty)
        
        # Update balls
        for ball in self.balls[:]:
            ball.update()
            
            # Paddle collisions
            if ball.paddle_collision(self.paddle1.get_rect(), self.paddle1.get_center_y()):
                self.add_hit_effect(ball.x, ball.y)
            
            if ball.paddle_collision(self.paddle2.get_rect(), self.paddle2.get_center_y()):
                self.add_hit_effect(ball.x, ball.y)
            
            # Score when ball goes off screen
            # Left side (Player 2's goal) - Player 1 scores
            if ball.x < 0:
                self.player1_score += 1
                self.balls.remove(ball)
                self.add_score_effect()
                if len(self.balls) == 0:
                    self.balls.append(Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # Right side (Player 1's goal) - Player 2 scores
            elif ball.x > SCREEN_WIDTH:
                self.player2_score += 1
                self.balls.remove(ball)
                self.add_score_effect()
                if len(self.balls) == 0:
                    self.balls.append(Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Update power-ups
        self.update_power_ups()
        
        # Check for game over
        if self.player1_score >= 11 or self.player2_score >= 11:
            self.state = GameState.GAME_OVER
            self.save_high_score()
    
    def update_power_ups(self):
        """Update power-up system"""
        # Spawn new power-ups
        self.power_up_timer += 1
        if self.power_up_timer >= self.power_up_spawn_interval:
            self.spawn_power_up()
            self.power_up_timer = 0
        
        # Update existing power-ups
        self.power_ups = [p for p in self.power_ups if p.is_alive()]
        for power_up in self.power_ups:
            power_up.update()
            
            # Check collisions with balls
            for ball in self.balls:
                if power_up.get_rect().colliderect(ball.get_rect()):
                    self.apply_power_up(power_up.power_type, ball)
                    self.power_ups.remove(power_up)
                    self.add_power_up_effect(power_up.x, power_up.y)
                    break
    
    def spawn_power_up(self):
        """Spawn a random power-up"""
        x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4)
        y = random.randint(100, SCREEN_HEIGHT - 100)
        power_type = random.choice(list(PowerUpType))
        self.power_ups.append(PowerUp(x, y, power_type))
    
    def apply_power_up(self, power_type: PowerUpType, ball: Ball):
        """Apply power-up effect"""
        if power_type == PowerUpType.SPEED_BOOST:
            ball.speed_multiplier = 1.5
        elif power_type == PowerUpType.MULTI_BALL:
            if len(self.balls) < 3:
                new_ball = Ball(ball.x, ball.y)
                new_ball.velocity.y *= -1
                self.balls.append(new_ball)
        elif power_type == PowerUpType.FREEZE:
            self.freeze_timer = 120  # 2 seconds
        # Apply to appropriate paddle based on ball position
        elif power_type in [PowerUpType.PADDLE_GROW, PowerUpType.PADDLE_SHRINK, PowerUpType.SHIELD]:
            # Apply to nearest paddle
            if ball.x > SCREEN_WIDTH // 2:
                self.paddle1.apply_effect(power_type)  # Right paddle (Player 1)
            else:
                self.paddle2.apply_effect(power_type)  # Left paddle (Player 2/Computer)
    
    def add_hit_effect(self, x, y):
        """Add particle effect for ball hits"""
        for _ in range(10):
            velocity = Vector2D(
                random.uniform(-5, 5),
                random.uniform(-5, 5)
            )
            self.particles.append(Particle(x, y, CYAN, velocity))
        self.screen_shake = 5
    
    def add_score_effect(self):
        """Add effect for scoring"""
        self.screen_shake = 10
    
    def add_power_up_effect(self, x, y):
        """Add effect for power-up collection"""
        for _ in range(15):
            velocity = Vector2D(
                random.uniform(-8, 8),
                random.uniform(-8, 8)
            )
            self.particles.append(Particle(x, y, GOLD, velocity))
    
    def draw(self):
        """Main draw function"""
        # Screen shake effect
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw background stars
        for star in self.stars:
            star.draw(self.screen)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game(shake_x, shake_y)
        elif self.state == GameState.PAUSED:
            self.draw_game(shake_x, shake_y)
            self.draw_pause_overlay()
        elif self.state == GameState.GAME_OVER:
            self.draw_game(shake_x, shake_y)
            self.draw_game_over()
        elif self.state == GameState.HIGH_SCORES:
            self.draw_high_scores()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw colorful animated main menu"""
        # Animated background gradient effect
        for y in range(0, SCREEN_HEIGHT, 4):
            gradient_factor = (y / SCREEN_HEIGHT)
            color_r = int(20 + (30 * gradient_factor * self.menu_pulse))
            color_g = int(10 + (50 * gradient_factor))
            color_b = int(40 + (60 * gradient_factor))
            pygame.draw.rect(self.screen, (color_r, color_g, color_b), 
                           (0, y, SCREEN_WIDTH, 4))
        
        # Animated title with rainbow effect
        rainbow_colors = [
            (255, 100, 100),  # Red
            (255, 150, 0),    # Orange
            (255, 255, 0),    # Yellow
            (100, 255, 100),  # Green
            (100, 150, 255),  # Blue
            (150, 100, 255),  # Purple
            (255, 100, 255)   # Pink
        ]
        
        title_text = "SPACE PING PONG"
        title_x = SCREEN_WIDTH // 2 - 280
        
        for i, char in enumerate(title_text):
            if char != ' ':
                color_index = (i + int(self.menu_time * 0.1)) % len(rainbow_colors)
                color = rainbow_colors[color_index]
                # Add pulsing effect
                pulse_color = tuple(int(c * self.menu_pulse) for c in color)
                char_surface = self.title_font.render(char, True, pulse_color)
                self.screen.blit(char_surface, (title_x + i * 42, 100))
        
        # Glowing menu options with different colors
        menu_items = [
            ("1. Play vs Computer", CYAN, 280),
            ("2. Play vs Human", PURPLE, 340),
            ("3. High Scores", GOLD, 400),

            ("", WHITE, 450),  # Spacer
            (f"Difficulty: {self.difficulty.name}", GREEN, 480),
            ("(Press E/M/H to change)", WHITE, 510),
            ("", WHITE, 560),  # Spacer
            ("ESC. Quit", RED, 570)
            
        ]  
            # used if USE_OUTLINE is False
        for text, color, y in menu_items:
            if text:
                # Create glowing effect
                glow_surface = self.menu_font.render(text, True, color)
                glow_rect = glow_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
                
                # Draw glow effect (multiple layers)
                for offset in range(2,1):
                    glow_color = tuple(min(255, int(c * 0.3)) for c in color)
                    for dx in [-offset, 0, offset]:
                        for dy in [-offset, 0, offset]:
                            if dx != 0 or dy != 0:
                                self.screen.blit(glow_surface, (glow_rect.x + dx, glow_rect.y + dy))
                
                # Draw main text
                if text.startswith(("1.", "2.", "3.")):
                    # Make menu options pulse
                    pulse_color = tuple(int(c * (0.7 + 0.3 * self.menu_pulse)) for c in color)
                    main_surface = self.menu_font.render(text, True, pulse_color)
                else:
                    main_surface = self.menu_font.render(text, True, color)
                
                self.screen.blit(main_surface, glow_rect)
        
        # Animated control instructions with icons
        instructions = [
            "Player 1 (Right): Arrow Keys ↑↓",
            "Player 2 (Left): W/S Keys (Human vs Human)",
            "SPACE: Pause Game",
            "Collect Power-ups for Special Effects!"
        ]
        
        y = SCREEN_HEIGHT - 200
        for i, instruction in enumerate(instructions):
            color = [CYAN, PURPLE, GOLD, GREEN][i % 4]
            # Add slight animation to instructions
            wave_offset = math.sin(self.menu_time * 0.08 + i * 0.5) * 3
            
            text = self.small_font.render(instruction, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y + wave_offset))
            self.screen.blit(text, text_rect)
            y += 35
        
        # Floating particles for extra visual appeal
        if random.random() < 0.3:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            color = random.choice([CYAN, PURPLE, GOLD, PINK])
            velocity = Vector2D(random.uniform(-1, 1), random.uniform(-2, -0.5))
            self.particles.append(Particle(x, y, color, velocity, 120))
        
        # Update and draw menu particles
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()
            particle.draw(self.screen)
    
    def draw_game(self, shake_x=0, shake_y=0):
        """Draw game elements"""
        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.rect(self.screen, WHITE, 
                           (SCREEN_WIDTH // 2 - 2 + shake_x, y + shake_y, 4, 10))
        
        # Draw paddles
        self.paddle1.draw(self.screen)
        self.paddle2.draw(self.screen)
        
        # Draw balls
        for ball in self.balls:
            ball.draw(self.screen)
        
        # Draw power-ups
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw scores (Player 1 on right, Player 2 on left)
        score1 = self.font.render(str(self.player1_score), True, CYAN)  # Player 1 (Right paddle)
        score2 = self.font.render(str(self.player2_score), True, PINK)  # Player 2 (Left paddle)
        self.screen.blit(score2, (SCREEN_WIDTH // 2 - 50, 50))  # Player 2 score on left side of screen
        self.screen.blit(score1, (SCREEN_WIDTH // 2 + 30, 50))  # Player 1 score on right side of screen
        
        # Draw freeze overlay
        if self.freeze_timer > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 255, 50))
            self.screen.blit(overlay, (0, 0))
            
            freeze_text = self.font.render("FROZEN!", True, BLUE)
            freeze_rect = freeze_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(freeze_text, freeze_rect)
    
    def draw_pause_overlay(self):
        """Draw pause menu overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.title_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        continue_text = self.font.render("SPACE to continue, ESC to menu", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        winner = "PLAYER 1 WINS!" if self.player1_score > self.player2_score else "PLAYER 2 WINS!"
        winner_text = self.title_font.render(winner, True, GOLD)
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(winner_text, winner_rect)
        
        final_score = f"{self.player1_score} - {self.player2_score}"
        score_text = self.font.render(final_score, True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        continue_text = self.font.render("SPACE to play again, ESC to menu", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_high_scores(self):
        """Draw high scores screen"""
        title = self.title_font.render("HIGH SCORES", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        y = 250
        for i, score in enumerate(self.high_scores[:10]):
            score_text = f"{i+1}. {score['name']} - {score['score']}"
            text = self.font.render(score_text, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 40
        
        back_text = self.font.render("ESC to return to menu", True, WHITE)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(back_text, back_rect)
    
    def load_high_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists("high_scores.json"):
                with open("high_scores.json", "r") as f:
                    return json.load(f)
        except:
            pass
        
        # Default high scores
        return [
            {"name": "SPACE ACE", "score": 10},
            {"name": "COSMIC PLAYER", "score": 8},
            {"name": "STAR WARRIOR", "score": 6},
            {"name": "GALAXY HERO", "score": 4},
            {"name": "NEBULA NOVICE", "score": 2}
        ]

    def save_high_score(self):
        # matches your logic; now uses storage module
        winner_score = max(self.player1_score, self.player2_score)
        winner_name = "PLAYER 1" if self.player1_score > self.player2_score else "PLAYER 2"
        self.high_scores.append({"name": winner_name, "score": winner_score})
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]
        save_high_scores(self.high_scores)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
