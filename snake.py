import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load sound effects
eat_sound = pygame.mixer.Sound('eating_sound.mp3')  # Add your path to the sound file
game_over_sound = pygame.mixer.Sound('game_over_sound.wav')

# Set up the display
window_size = (600, 400)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Snake")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the Snake
snake_size = 20  # Size of each segment
snake_body = [(300, 200)]  # A list to store the Snake's body positions (starts with 1 block)
direction = 'RIGHT'  # Initial direction

# Set up the food
def reposition_food():
    return (random.randint(0, (window_size[0] // snake_size - 1)) * snake_size,
            random.randint(0, (window_size[1] // snake_size - 1)) * snake_size)

food_x, food_y = reposition_food()

# Set up the game clock
clock = pygame.time.Clock()
move_delay = 150  # Snake moves every 150 milliseconds
last_move_time = pygame.time.get_ticks()

score = 0
high_score = 0

font = pygame.font.Font(None, 36)

# Function to read high score from a file
def read_high_score():
    try:
        with open('highscore.txt', 'r') as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0  # Return 0 if the file does not exist or contains invalid data

# Function to write high score to a file
def write_high_score(score):
    with open('highscore.txt', 'w') as file:
        file.write(str(score))

high_score = read_high_score()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses and change the direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and direction != 'RIGHT':
        direction = 'LEFT'
    if keys[pygame.K_RIGHT] and direction != 'LEFT':
        direction = 'RIGHT'
    if keys[pygame.K_UP] and direction != 'DOWN':
        direction = 'UP'
    if keys[pygame.K_DOWN] and direction != 'UP':
        direction = 'DOWN'

    # Move the Snake at regular intervals
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - last_move_time

    if elapsed_time > move_delay:
        head_x, head_y = snake_body[0]  # Get the current position of the Snake's head

        # Move the head in the chosen direction
        if direction == 'LEFT':
            head_x -= snake_size
        elif direction == 'RIGHT':
            head_x += snake_size
        elif direction == 'UP':
            head_y -= snake_size
        elif direction == 'DOWN':
            head_y += snake_size

        # Check for self-collision before updating the snake body
        if (head_x, head_y) in snake_body:
            write_high_score(high_score)
            game_over_sound.play()
            pygame.time.wait(2000)
            running = False

        # Add the new head position to the front of the snake body
        snake_body = [(head_x, head_y)] + snake_body

        # Check if the Snake eats the food
        if head_x == food_x and head_y == food_y:
            eat_sound.play()
            score += 1
            high_score = max(score, high_score)
            food_x, food_y = reposition_food()  # Reposition food
        else:
            # If no food is eaten, remove the last segment to maintain size
            snake_body.pop()

        # Boundary checking to end the game if the Snake goes out of bounds
        if (head_x < 0 or head_x >= window_size[0] or
            head_y < 0 or head_y >= window_size[1]):
            write_high_score(high_score)
            game_over_sound.play()
            pygame.time.wait(2000)
            running = False

        last_move_time = current_time  # Update the time of the last movement

    # Fill the screen with black
    window.fill(BLACK)

    # Draw the Snake
    for segment in snake_body:
        pygame.draw.rect(window, GREEN, (segment[0], segment[1], snake_size, snake_size))

    # Draw the food
    pygame.draw.rect(window, RED, (food_x, food_y, snake_size, snake_size))

    # Render score and high score
    score_text = font.render(f"Score: {score}  High Score: {high_score}", True, WHITE)
    window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)  # Set to 60 FPS for smoother movement

# Quit Pygame
pygame.quit()
sys.exit()