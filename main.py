import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 50
GRAVITY = 0.6
JUMP_FORCE = -15
PROMPT_SPEED = 5
PROMPT_SPAWN_RATE = 60  # Frames between prompt spawns
GAME_SPEED_INCREASE = 0.0001  # How much to increase speed per frame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Prompt Runner")
clock = pygame.time.Clock()

# Load fonts
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

class Player:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = 100
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.vel_y = 0
        self.is_jumping = False
        self.color = BLUE
    
    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        # Check for ground collision
        if self.y > SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.is_jumping = False
    
    def jump(self):
        if not self.is_jumping:
            self.vel_y = JUMP_FORCE
            self.is_jumping = True
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Draw face
        pygame.draw.circle(screen, WHITE, (self.x + 25, self.y + 20), 10)  # Left eye
        pygame.draw.circle(screen, WHITE, (self.x + 40, self.y + 20), 10)  # Right eye
        pygame.draw.circle(screen, BLACK, (self.x + 25, self.y + 20), 5)   # Left pupil
        pygame.draw.circle(screen, BLACK, (self.x + 40, self.y + 20), 5)   # Right pupil
        pygame.draw.arc(screen, BLACK, (self.x + 15, self.y + 30, 30, 20), 0, 3.14, 3)  # Smile

class Prompt:
    def __init__(self, x, is_good):
        self.width = 80
        self.height = 40
        self.x = x
        self.y = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - 100)
        self.is_good = is_good
        self.color = GREEN if is_good else RED
        self.speed = PROMPT_SPEED
        self.text = random.choice(["Good!", "Nice!", "Great!"] if is_good else ["Bad!", "Wrong!", "Avoid!"])
    
    def update(self, game_speed):
        self.x -= self.speed * game_speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text = font_small.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.width/2, self.y + self.height/2))
        screen.blit(text, text_rect)

def check_collision(player, prompt):
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    prompt_rect = pygame.Rect(prompt.x, prompt.y, prompt.width, prompt.height)
    return player_rect.colliderect(prompt_rect)

def draw_ground():
    pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
    # Draw some ground details
    for i in range(0, SCREEN_WIDTH, 50):
        pygame.draw.line(screen, BLACK, (i, SCREEN_HEIGHT - GROUND_HEIGHT), 
                         (i + 25, SCREEN_HEIGHT - GROUND_HEIGHT), 2)

def show_menu():
    screen.fill(BLACK)
    
    title = font_large.render("PROMPT RUNNER", True, YELLOW)
    title_rect = title.get_rect(center=(SCREEN_WIDTH/2, 150))
    screen.blit(title, title_rect)
    
    instructions = [
        "Collect good prompts (green) and avoid bad prompts (red)",
        "Press SPACE to jump",
        "Press ENTER to start",
        "Press ESC to quit"
    ]
    
    for i, line in enumerate(instructions):
        text = font_small.render(line, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, 250 + i * 40))
        screen.blit(text, text_rect)
    
    pygame.display.flip()

def show_game_over(score):
    screen.fill(BLACK)
    
    game_over_text = font_large.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, 150))
    screen.blit(game_over_text, game_over_rect)
    
    score_text = font_medium.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, 250))
    screen.blit(score_text, score_rect)
    
    instructions = [
        "Press ENTER to play again",
        "Press ESC to quit"
    ]
    
    for i, line in enumerate(instructions):
        text = font_small.render(line, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, 350 + i * 40))
        screen.blit(text, text_rect)
    
    pygame.display.flip()

def main():
    game_state = MENU
    player = Player()
    prompts = []
    score = 0
    spawn_counter = 0
    game_speed = 1.0
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if game_state == MENU:
                    if event.key == pygame.K_RETURN:
                        game_state = PLAYING
                        player = Player()
                        prompts = []
                        score = 0
                        game_speed = 1.0
                
                elif game_state == PLAYING:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                
                elif game_state == GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        game_state = PLAYING
                        player = Player()
                        prompts = []
                        score = 0
                        game_speed = 1.0
        
        # Game state handling
        if game_state == MENU:
            show_menu()
        
        elif game_state == PLAYING:
            # Update game speed
            game_speed += GAME_SPEED_INCREASE
            
            # Update player
            player.update()
            
            # Spawn prompts
            spawn_counter += 1
            if spawn_counter >= PROMPT_SPAWN_RATE / game_speed:
                is_good = random.choice([True, False])
                prompts.append(Prompt(SCREEN_WIDTH, is_good))
                spawn_counter = 0
            
            # Update prompts
            for prompt in prompts[:]:
                prompt.update(game_speed)
                
                # Check for collisions
                if check_collision(player, prompt):
                    if prompt.is_good:
                        score += 10
                    else:
                        game_state = GAME_OVER
                    prompts.remove(prompt)
                
                # Remove prompts that are off-screen
                elif prompt.x + prompt.width < 0:
                    prompts.remove(prompt)
            
            # Drawing
            screen.fill(BLACK)
            
            # Draw score
            score_text = font_medium.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (20, 20))
            
            # Draw speed
            speed_text = font_small.render(f"Speed: {game_speed:.2f}x", True, WHITE)
            screen.blit(speed_text, (20, 70))
            
            # Draw game elements
            draw_ground()
            player.draw(screen)
            for prompt in prompts:
                prompt.draw(screen)
            
            pygame.display.flip()
        
        elif game_state == GAME_OVER:
            show_game_over(score)
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
