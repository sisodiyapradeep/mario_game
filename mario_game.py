import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
MARIO_SIZE = 40
ENEMY_SIZE = 30
JUMP_SPEED = 15
GRAVITY = 0.8
MOVE_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.on_ground = False
        self.size = MARIO_SIZE
        
    def update(self, keys):
        # Horizontal movement
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.size:
            self.x += MOVE_SPEED
            
        # Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -JUMP_SPEED
            self.on_ground = False
            
        # Apply gravity
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        # Ground collision
        if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.size
            self.vel_y = 0
            self.on_ground = True
            
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))
        # Simple face
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + 10), 3)
        pygame.draw.circle(screen, BLACK, (self.x + 30, self.y + 10), 3)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = -1
        self.size = ENEMY_SIZE
        
    def update(self):
        self.x += self.direction * 2
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.size:
            self.direction *= -1
            
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.size, self.size))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mario Game - Press R to restart")
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        
    def reset_game(self):
        self.mario = Mario(50, SCREEN_HEIGHT - GROUND_HEIGHT - MARIO_SIZE)
        self.enemies = [
            Enemy(400, SCREEN_HEIGHT - GROUND_HEIGHT - ENEMY_SIZE),
            Enemy(650, SCREEN_HEIGHT - GROUND_HEIGHT - ENEMY_SIZE)
        ]
        self.score = 0
        self.game_over = False
        
    def check_collisions(self):
        mario_rect = pygame.Rect(self.mario.x + 5, self.mario.y + 5, self.mario.size - 10, self.mario.size - 10)
        for enemy in self.enemies[:]:
            enemy_rect = pygame.Rect(enemy.x + 3, enemy.y + 3, enemy.size - 6, enemy.size - 6)
            if mario_rect.colliderect(enemy_rect):
                # Mario jumps on enemy (must be falling and above enemy)
                if self.mario.vel_y > 0 and self.mario.y < enemy.y - 10:
                    self.enemies.remove(enemy)
                    self.score += 100
                    self.mario.vel_y = -JUMP_SPEED // 2
                    # Spawn new enemy
                    import random
                    new_x = random.randint(200, SCREEN_WIDTH - 200)
                    self.enemies.append(Enemy(new_x, SCREEN_HEIGHT - GROUND_HEIGHT - ENEMY_SIZE))
                else:
                    return True  # Game over
        return False
        
    def draw(self):
        # Sky
        self.screen.fill(BLUE)
        
        # Ground
        pygame.draw.rect(self.screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        
        # Game objects
        self.mario.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # Score and instructions
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press R to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    
            keys = pygame.key.get_pressed()
            
            if not self.game_over:
                # Update game objects
                self.mario.update(keys)
                for enemy in self.enemies:
                    enemy.update()
                    
                # Check collisions
                if self.check_collisions():
                    self.game_over = True
                
            self.draw()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()