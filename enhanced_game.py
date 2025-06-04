import pygame
import random
import sys
import os
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 50
GRAVITY = 0.6
JUMP_FORCE = -15
PROMPT_SPEED = 5
PROMPT_SPAWN_RATE = 60  # Frames between prompt spawns
GAME_SPEED_INCREASE = 0.0001  # How much to increase speed per frame
CLOUD_SPEED = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (135, 206, 235)
CLOUD_WHITE = (240, 240, 240)

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

# Try to load sounds
try:
    jump_sound = pygame.mixer.Sound(os.path.join('sounds', 'jump.wav'))
    good_collect_sound = pygame.mixer.Sound(os.path.join('sounds', 'good_collect.wav'))
    bad_collect_sound = pygame.mixer.Sound(os.path.join('sounds', 'bad_collect.wav'))
    game_over_sound = pygame.mixer.Sound(os.path.join('sounds', 'game_over.wav'))
except:
    print("Sound files not found. Game will run without sound.")
    jump_sound = None
    good_collect_sound = None
    bad_collect_sound = None
    game_over_sound = None

class Player:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = 100
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.vel_y = 0
        self.is_jumping = False
        self.color = BLUE
        self.animation_frame = 0
        self.animation_speed = 0.2
    
    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        # Check for ground collision
        if self.y > SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.is_jumping = False
        
        # Update animation frame
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 4:
            self.animation_frame = 0
    
    def jump(self):
        if not self.is_jumping:
            self.vel_y = JUMP_FORCE
            self.is_jumping = True
            if jump_sound:
                jump_sound.play()
    
    def draw(self, screen):
        # Draw player body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw face
        pygame.draw.circle(screen, WHITE, (self.x + 25, self.y + 20), 10)  # Left eye
        pygame.draw.circle(screen, WHITE, (self.x + 40, self.y + 20), 10)  # Right eye
        pygame.draw.circle(screen, BLACK, (self.x + 25, self.y + 20), 5)   # Left pupil
        pygame.draw.circle(screen, BLACK, (self.x + 40, self.y + 20), 5)   # Right pupil
        
        # Animated smile based on jumping state
        if self.is_jumping:
            pygame.draw.arc(screen, BLACK, (self.x + 15, self.y + 30, 30, 20), 0, 3.14, 3)  # Smile
        else:
            # Running animation for mouth
            mouth_offset = math.sin(self.animation_frame) * 5
            pygame.draw.arc(screen, BLACK, (self.x + 15, self.y + 30 + mouth_offset, 30, 20), 0, 3.14, 3)
        
        # Draw legs with running animation when on ground
        if not self.is_jumping:
            leg_offset = math.sin(self.animation_frame * 2) * 10
            # Left leg
            pygame.draw.line(screen, self.color, 
                            (self.x + 15, self.y + self.height),
                            (self.x + 15 - leg_offset, self.y + self.height + 15), 5)
            # Right leg
            pygame.draw.line(screen, self.color, 
                            (self.x + self.width - 15, self.y + self.height),
                            (self.x + self.width - 15 + leg_offset, self.y + self.height + 15), 5)
        else:
            # Jumping pose
            pygame.draw.line(screen, self.color, 
                            (self.x + 15, self.y + self.height),
                            (self.x, self.y + self.height + 10), 5)
            pygame.draw.line(screen, self.color, 
                            (self.x + self.width - 15, self.y + self.height),
                            (self.x + self.width, self.y + self.height + 10), 5)

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
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
        self.pulse_size = 0
        self.pulse_direction = 1
    
    def update(self, game_speed):
        self.x -= self.speed * game_speed
        self.rotation += self.rotation_speed
        
        # Pulsing effect
        self.pulse_size += 0.1 * self.pulse_direction
        if self.pulse_size > 1 or self.pulse_size < 0:
            self.pulse_direction *= -1
    
    def draw(self, screen):
        # Create a surface for the prompt
        prompt_surface = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
        
        # Draw the prompt on the surface
        pygame.draw.rect(prompt_surface, self.color, 
                        (5, 5, self.width + self.pulse_size, self.height + self.pulse_size))
        
        # Add text
        text = font_small.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=(self.width/2 + 5, self.height/2 + 5))
        prompt_surface.blit(text, text_rect)
        
        # Rotate the surface
        rotated_surface = pygame.transform.rotate(prompt_surface, self.rotation)
        rotated_rect = rotated_surface.get_rect(center=(self.x + self.width/2, self.y + self.height/2))
        
        # Draw the rotated surface
        screen.blit(rotated_surface, rotated_rect)

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(0, 100)
        self.y = random.randint(50, 200)
        self.speed = random.uniform(0.5, 1.5)
        self.width = random.randint(60, 120)
        self.height = random.randint(30, 60)
    
    def update(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(0, 100)
            self.y = random.randint(50, 200)
    
    def draw(self, screen):
        # Draw a fluffy cloud
        pygame.draw.ellipse(screen, CLOUD_WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, CLOUD_WHITE, (self.x + self.width * 0.2, self.y - self.height * 0.2, self.width * 0.6, self.height * 0.6))
        pygame.draw.ellipse(screen, CLOUD_WHITE, (self.x + self.width * 0.4, self.y + self.height * 0.1, self.width * 0.6, self.height * 0.6))

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(3, 8)
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-5, -1)
        self.gravity = 0.2
        self.life = 30  # frames
    
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity
        self.life -= 1
        self.size = max(0, self.size - 0.1)
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

def check_collision(player, prompt):
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    prompt_rect = pygame.Rect(prompt.x, prompt.y, prompt.width, prompt.height)
    return player_rect.colliderect(prompt_rect)

def draw_ground():
    # Draw ground
    pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
    
    # Draw grass on top of ground
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, 5))
    
    # Draw some ground details
    for i in range(0, SCREEN_WIDTH, 50):
        # Dirt lines
        pygame.draw.line(screen, (80, 80, 80), (i, SCREEN_HEIGHT - GROUND_HEIGHT + 15), 
                         (i + 25, SCREEN_HEIGHT - GROUND_HEIGHT + 15), 2)
        
        # Random grass blades
        if random.random() > 0.7:
            grass_height = random.randint(5, 10)
            pygame.draw.line(screen, (0, 150, 0), 
                            (i + random.randint(0, 50), SCREEN_HEIGHT - GROUND_HEIGHT),
                            (i + random.randint(0, 50), SCREEN_HEIGHT - GROUND_HEIGHT - grass_height), 2)

def show_menu():
    screen.fill(LIGHT_BLUE)
    
    # Draw clouds
    for cloud in clouds:
        cloud.draw(screen)
    
    # Draw ground
    draw_ground()
    
    # Draw title with shadow
    title_shadow = font_large.render("PROMPT RUNNER", True, BLACK)
    title = font_large.render("PROMPT RUNNER", True, YELLOW)
    screen.blit(title_shadow, (SCREEN_WIDTH/2 - title.get_width()/2 + 3, 153))
    screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, 150))
    
    # Draw menu box
    menu_box = pygame.Rect(SCREEN_WIDTH/2 - 200, 220, 400, 200)
    pygame.draw.rect(screen, (50, 50, 50, 200), menu_box)
    pygame.draw.rect(screen, WHITE, menu_box, 3)
    
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
    
    # Draw animated character
    player = Player()
    player.x = SCREEN_WIDTH/2 - player.width/2
    player.y = SCREEN_HEIGHT - GROUND_HEIGHT - player.height - 50
    player.animation_frame = pygame.time.get_ticks() / 200  # Animate based on time
    player.draw(screen)
    
    pygame.display.flip()

def show_game_over(score):
    # Fade to black
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)
    for alpha in range(0, 200, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)
    
    if game_over_sound:
        game_over_sound.play()
    
    # Game over screen
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
    global clouds
    
    game_state = MENU
    player = Player()
    prompts = []
    particles = []
    clouds = [Cloud() for _ in range(5)]
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
                        particles = []
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
                        particles = []
                        score = 0
                        game_speed = 1.0
        
        # Update clouds in all game states
        for cloud in clouds:
            cloud.update()
        
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
                        if good_collect_sound:
                            good_collect_sound.play()
                        # Create particles for good prompts
                        for _ in range(15):
                            particles.append(Particle(prompt.x + prompt.width/2, 
                                                    prompt.y + prompt.height/2, 
                                                    GREEN))
                    else:
                        if bad_collect_sound:
                            bad_collect_sound.play()
                        # Create particles for bad prompts
                        for _ in range(15):
                            particles.append(Particle(prompt.x + prompt.width/2, 
                                                    prompt.y + prompt.height/2, 
                                                    RED))
                        game_state = GAME_OVER
                    prompts.remove(prompt)
                
                # Remove prompts that are off-screen
                elif prompt.x + prompt.width < 0:
                    prompts.remove(prompt)
            
            # Update particles
            for particle in particles[:]:
                particle.update()
                if particle.life <= 0:
                    particles.remove(particle)
            
            # Drawing
            screen.fill(LIGHT_BLUE)
            
            # Draw clouds
            for cloud in clouds:
                cloud.draw(screen)
            
            # Draw ground
            draw_ground()
            
            # Draw player
            player.draw(screen)
            
            # Draw prompts
            for prompt in prompts:
                prompt.draw(screen)
            
            # Draw particles
            for particle in particles:
                particle.draw(screen)
            
            # Draw score
            score_text = font_medium.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (20, 20))
            
            # Draw speed
            speed_text = font_small.render(f"Speed: {game_speed:.2f}x", True, BLACK)
            screen.blit(speed_text, (20, 70))
            
            pygame.display.flip()
        
        elif game_state == GAME_OVER:
            show_game_over(score)
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
