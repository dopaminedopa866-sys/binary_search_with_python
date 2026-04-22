"""
NEON SURGE - A Futuristic Space Shooter Game
A stunning, high-performance arcade space game with cyberpunk aesthetics
"""

import pygame
import random
import math
from enum import Enum
from dataclasses import dataclass
from typing import List

# Initialize Pygame
pygame.init()

# ============================================================================
# CONSTANTS
# ============================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
GAME_TITLE = "NEON SURGE"

# Color Palette (Cyberpunk Neon)
class Colors:
    BLACK = (5, 5, 15)
    DARK_BLUE = (10, 20, 40)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    NEON_GREEN = (0, 255, 100)
    NEON_YELLOW = (255, 255, 0)
    NEON_PINK = (255, 20, 147)
    WHITE = (255, 255, 255)
    PURPLE = (138, 43, 226)

# ============================================================================
# PARTICLE SYSTEM
# ============================================================================

@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: int
    color: tuple
    size: int

class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []
    
    def emit(self, x, y, count=10, color=Colors.CYAN, speed=5):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            velocity = random.uniform(speed * 0.5, speed)
            self.particles.append(Particle(
                x=x,
                y=y,
                vx=math.cos(angle) * velocity,
                vy=math.sin(angle) * velocity,
                life=30,
                color=color,
                size=random.randint(1, 3)
            ))
    
    def update(self):
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.x += p.vx
            p.y += p.vy
            p.vy += 0.15  # Gravity
            p.life -= 1
    
    def draw(self, surface):
        for p in self.particles:
            alpha = max(0, p.life / 30)
            color = tuple(int(c * alpha) for c in p.color)
            pygame.draw.circle(surface, color, (int(p.x), int(p.y)), p.size)

# ============================================================================
# ENEMY SYSTEM
# ============================================================================

@dataclass
class Enemy:
    x: float
    y: float
    vx: float
    vy: float
    health: int
    size: int
    enemy_type: str  # "basic", "fast", "tank"
    angle: float = 0

class EnemyManager:
    def __init__(self):
        self.enemies: List[Enemy] = []
        self.wave = 1
        self.wave_timer = 0
        self.enemies_spawned = 0
    
    def spawn_wave(self):
        self.enemies_spawned = 0
        enemy_count = 3 + self.wave
        
        for _ in range(enemy_count):
            enemy_type = random.choice(["basic", "basic", "fast", "tank"])
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = -50
            
            if enemy_type == "basic":
                vx = random.uniform(-2, 2)
                vy = random.uniform(1.5, 2.5)
                health = 1
                size = 15
            elif enemy_type == "fast":
                vx = random.uniform(-3, 3)
                vy = random.uniform(2.5, 4)
                health = 1
                size = 12
            else:  # tank
                vx = random.uniform(-1, 1)
                vy = random.uniform(1, 1.5)
                health = 3
                size = 20
            
            self.enemies.append(Enemy(x, y, vx, vy, health, size, enemy_type))
            self.enemies_spawned += 1
    
    def update(self):
        self.enemies = [e for e in self.enemies if e.y < SCREEN_HEIGHT and e.health > 0]
        
        for enemy in self.enemies:
            enemy.x += enemy.vx
            enemy.y += enemy.vy
            enemy.angle += 3
        
        # Spawn new wave if all enemies defeated
        if len(self.enemies) == 0 and self.enemies_spawned > 0:
            self.wave += 1
            self.spawn_wave()
    
    def draw(self, surface, particles):
        for enemy in self.enemies:
            # Draw enemy based on type
            color = Colors.MAGENTA if enemy.enemy_type == "basic" else \
                    Colors.NEON_PINK if enemy.enemy_type == "fast" else Colors.CYAN
            
            # Draw main body
            pygame.draw.circle(surface, color, (int(enemy.x), int(enemy.y)), enemy.size)
            
            # Draw glow
            pygame.draw.circle(surface, color, (int(enemy.x), int(enemy.y)), enemy.size + 2, 1)
            
            # Draw rotating pattern
            angle_rad = math.radians(enemy.angle)
            for i in range(3):
                offset_x = math.cos(angle_rad + i * 2 * math.pi / 3) * enemy.size
                offset_y = math.sin(angle_rad + i * 2 * math.pi / 3) * enemy.size
                pygame.draw.line(surface, color, 
                               (int(enemy.x), int(enemy.y)),
                               (int(enemy.x + offset_x), int(enemy.y + offset_y)), 1)

# ============================================================================
# PLAYER SYSTEM
# ============================================================================

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 12
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.angle = 0
        self.fire_cooldown = 0
    
    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        
        # Clamp to screen
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
        
        # Update rotation towards mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.angle = math.degrees(math.atan2(dy, dx))
        
        # Update cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
    
    def draw(self, surface):
        # Draw player ship
        angle_rad = math.radians(self.angle)
        
        # Main body
        pygame.draw.circle(surface, Colors.NEON_GREEN, (int(self.x), int(self.y)), self.size)
        
        # Glow effect
        pygame.draw.circle(surface, Colors.NEON_GREEN, (int(self.x), int(self.y)), self.size + 3, 1)
        
        # Direction indicator
        tip_x = self.x + math.cos(angle_rad) * (self.size + 8)
        tip_y = self.y + math.sin(angle_rad) * (self.size + 8)
        pygame.draw.line(surface, Colors.NEON_YELLOW, (int(self.x), int(self.y)), 
                        (int(tip_x), int(tip_y)), 2)
        
        # Side wings
        wing_angle = math.pi / 3
        wing_length = self.size + 5
        
        for offset in [-wing_angle, wing_angle]:
            wing_x = self.x + math.cos(angle_rad + offset) * wing_length
            wing_y = self.y + math.sin(angle_rad + offset) * wing_length
            pygame.draw.line(surface, Colors.CYAN, (int(self.x), int(self.y)), 
                            (int(wing_x), int(wing_y)), 1)
    
    def can_fire(self):
        return self.fire_cooldown <= 0
    
    def fire(self):
        self.fire_cooldown = 8
        angle_rad = math.radians(self.angle)
        return Bullet(
            self.x + math.cos(angle_rad) * 15,
            self.y + math.sin(angle_rad) * 15,
            math.cos(angle_rad) * 8,
            math.sin(angle_rad) * 8
        )

# ============================================================================
# BULLET SYSTEM
# ============================================================================

@dataclass
class Bullet:
    x: float
    y: float
    vx: float
    vy: float
    life: int = 120

class BulletManager:
    def __init__(self):
        self.bullets: List[Bullet] = []
    
    def add(self, bullet):
        self.bullets.append(bullet)
    
    def update(self):
        self.bullets = [b for b in self.bullets if b.life > 0 and 
                       0 <= b.x < SCREEN_WIDTH and 0 <= b.y < SCREEN_HEIGHT]
        
        for bullet in self.bullets:
            bullet.x += bullet.vx
            bullet.y += bullet.vy
            bullet.life -= 1
    
    def draw(self, surface):
        for bullet in self.bullets:
            pygame.draw.circle(surface, Colors.NEON_YELLOW, (int(bullet.x), int(bullet.y)), 3)
            pygame.draw.circle(surface, Colors.WHITE, (int(bullet.x), int(bullet.y)), 4, 1)

# ============================================================================
# GAME ENGINE
# ============================================================================

class GameEngine:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        self.enemies = EnemyManager()
        self.bullets = BulletManager()
        self.particles = ParticleSystem()
        
        self.score = 0
        self.wave_just_started = True
        self.game_state = "playing"  # "playing", "game_over"
    
    def draw_background(self):
        self.screen.fill(Colors.BLACK)
        
        # Draw grid
        grid_size = 40
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(self.screen, (20, 40, 80), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(self.screen, (20, 40, 80), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw border
        pygame.draw.rect(self.screen, Colors.CYAN, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2)
    
    def check_collisions(self):
        # Bullet-Enemy collisions
        for bullet in self.bullets.bullets[:]:
            for enemy in self.enemies.enemies[:]:
                dist = math.sqrt((bullet.x - enemy.x)**2 + (bullet.y - enemy.y)**2)
                if dist < enemy.size + 3:
                    enemy.health -= 1
                    self.bullets.bullets.remove(bullet)
                    self.particles.emit(bullet.x, bullet.y, 20, Colors.NEON_YELLOW, 4)
                    
                    if enemy.health <= 0:
                        self.score += 10 if enemy.enemy_type == "basic" else \
                                    15 if enemy.enemy_type == "fast" else 25
                        self.particles.emit(enemy.x, enemy.y, 30, Colors.MAGENTA, 6)
                    break
        
        # Enemy-Player collisions
        for enemy in self.enemies.enemies:
            dist = math.sqrt((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)
            if dist < enemy.size + self.player.size:
                self.player.health -= 0.5
                self.particles.emit(self.player.x, self.player.y, 10, Colors.CYAN, 3)
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r and self.game_state == "game_over":
                    self.__init__()  # Restart game
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        # Continuous fire with left mouse button
        if pygame.mouse.get_pressed()[0] and self.player.can_fire():
            bullet = self.player.fire()
            self.bullets.add(bullet)
            self.particles.emit(self.player.x, self.player.y, 5, Colors.NEON_YELLOW, 2)
        
        return True
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.enemies.update()
        self.bullets.update()
        self.particles.update()
        self.check_collisions()
        
        if self.player.health <= 0:
            self.game_state = "game_over"
        
        # Spawn first wave
        if self.wave_just_started and len(self.enemies.enemies) == 0:
            self.enemies.spawn_wave()
            self.wave_just_started = False
    
    def draw_ui(self):
        # Score
        score_text = self.font_medium.render(f"SCORE: {self.score}", True, Colors.NEON_YELLOW)
        self.screen.blit(score_text, (20, 20))
        
        # Wave
        wave_text = self.font_medium.render(f"WAVE: {self.enemies.wave}", True, Colors.CYAN)
        self.screen.blit(wave_text, (SCREEN_WIDTH - 250, 20))
        
        # Health bar
        bar_width = 300
        bar_height = 20
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 30
        
        # Background
        pygame.draw.rect(self.screen, Colors.DARK_BLUE, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, Colors.CYAN, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Health fill
        health_percentage = max(0, self.player.health / self.player.max_health)
        health_color = Colors.NEON_GREEN if health_percentage > 0.3 else Colors.NEON_YELLOW if health_percentage > 0.1 else Colors.MAGENTA
        pygame.draw.rect(self.screen, health_color, (bar_x + 2, bar_y + 2, 
                                                      int((bar_width - 4) * health_percentage), 
                                                      bar_height - 4))
        
        # Health text
        health_text = self.font_small.render(f"HEALTH: {max(0, int(self.player.health))}/{int(self.player.max_health)}", 
                                            True, health_color)
        self.screen.blit(health_text, (bar_x + 10, bar_y + 35))
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(Colors.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, Colors.MAGENTA)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, text_rect)
        
        # Final score
        final_score_text = self.font_medium.render(f"FINAL SCORE: {self.score}", True, Colors.NEON_YELLOW)
        text_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(final_score_text, text_rect)
        
        # Wave reached
        wave_text = self.font_small.render(f"Wave Reached: {self.enemies.wave}", True, Colors.CYAN)
        text_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(wave_text, text_rect)
        
        # Restart instruction
        restart_text = self.font_small.render("Press R to restart or ESC to quit", True, Colors.WHITE)
        text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(restart_text, text_rect)
    
    def draw(self):
        self.draw_background()
        
        if self.game_state == "playing":
            self.enemies.draw(self.screen, self.particles)
            self.bullets.draw(self.screen)
            self.player.draw(self.screen)
            self.particles.draw(self.screen)
            self.draw_ui()
        else:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    game = GameEngine()
    game.run()
