import pygame
import sys
import random
from random import randint


pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
FPS = 60
WHITE = (255, 255, 255)
collision_sound = pygame.mixer.Sound("audio/crash-6711.mp3")
level_sound = pygame.mixer.Sound("audio/level.mp3")
pygame.mixer.music.load("audio/bg.mp3")
pygame.mixer.music.play(-1)
won_sound = pygame.mixer.Sound("audio/won.mp3")
bg_image = pygame.image.load("img/bg.png")



bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Maze Game")

def generate_maze():
   
    return [[0 for _ in range(WIDTH // CELL_SIZE)] for _ in range(HEIGHT // CELL_SIZE)]

# Initialize the player character 
player_image = pygame.image.load("img/movingcar.png") 
player_image = pygame.transform.scale(player_image, (CELL_SIZE, CELL_SIZE))
player_rect = player_image.get_rect()
rotation_angle = 0 


home_image = pygame.image.load("img/home.png") 
home_image = pygame.transform.scale(home_image, (CELL_SIZE, CELL_SIZE))

grid = generate_maze()

# Find the start and end positions
start = (0, 0)
end = (len(grid[0]) - 1, len(grid) - 1)

# Initialize the moving lines
lines = []
line_speed = 0.1
line_count = 1
current_level = 0

def generate_lines():
    return [
        (random.randint(50, WIDTH), line_speed, random.randint(7, 15), (255, 255, 255))  # Change the color to white
        for _ in range(line_count)
    ]

lines = generate_lines()

#game
clock = pygame.time.Clock()
running = True
won = False
game_over = False
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not won and not game_over:

        if keys[pygame.K_LEFT]:
            rotation_angle = 90  
            player_rect.move_ip(-5, 0)
        elif keys[pygame.K_RIGHT]:
            rotation_angle = -90 
            player_rect.move_ip(5, 0)

        if keys[pygame.K_UP] and player_rect.top > 0:
            rotation_angle = 180
            player_rect.move_ip(0, -5)
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            rotation_angle = 180
            player_rect.move_ip(0, 5)

        rotated_player = pygame.transform.rotate(player_image, rotation_angle)
        rotated_rect = rotated_player.get_rect(center=player_rect.center)
        player_rect = rotated_rect

        for i, line_data in enumerate(lines):
            line_x, line_speed, line_width, _ = line_data
            line_x += line_speed
            if line_x > WIDTH:
                line_x = 0
                line_speed = random.uniform(0, 3)  
                line_width = random.randint(5, 10) 
                lines[i] = (line_x, line_speed, line_width, (0, 0, 0))

            if player_rect.colliderect(pygame.Rect(line_x, random.randint(0, HEIGHT - line_width), line_width, line_width)):
                game_over = True
                current_level = 0  # Reset the level to 0
                collision_sound.play()

   
    if current_level == 2:
       
        
        random_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        screen.fill(random_color)
        # Add more moving lines at random points
        additional_lines = generate_lines()
        lines.extend(additional_lines)
        line_speed += 1  # Increase line speed after winning level 2
    else:
        screen.blit(bg_image, (0, 0))

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    screen.blit(rotated_player, player_rect)

    screen.blit(home_image, pygame.Rect(end[0] * CELL_SIZE, end[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for line_data in lines:
        line_x, _, line_width, line_color = line_data
        pygame.draw.rect(screen, line_color, pygame.Rect(line_x, random.randint(0, HEIGHT - line_width), line_width, line_width))

    if player_rect.colliderect(pygame.Rect(end[0] * CELL_SIZE, end[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)):
        won = True
       
        level_sound.play()
        current_level += 1  # Increase the level
        if current_level >= 2:
            pygame.mixer.music.pause()
            won_sound.play()
           
            random_color = (randint(0, 255), randint(0, 255), randint(0, 255))
            screen.fill(random_color)

            # Add more moving lines at random points
            additional_lines = generate_lines()
            lines.extend(additional_lines)
            text = font.render("You Won", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            small_font = pygame.font.Font(None, 24)
            text2 = small_font.render("Developed By Nadeesha", True, (0, 0, 0))
            text_rect2 = text2.get_rect(bottomleft=(0, HEIGHT))
            screen.blit(text2, text_rect2)
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.mixer.music.unpause()
            current_level = 0 
            line_speed = 2  
        else:
            text = font.render(f"Level: {current_level}", True, (255, 255, 255))
            text_rect = text.get_rect(topleft=(10, 10))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(2000)  
        # Reset the game
        player_rect.topleft = (0, 0)
        won = False
        game_over = False

    # Check for game over
    if game_over:
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000) 
        # Reset the game
        player_rect.topleft = (0, 0)
        won = False
        game_over = False
        current_level = 0
        lines = generate_lines()
        line_speed = 2  # Reset line speed

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
