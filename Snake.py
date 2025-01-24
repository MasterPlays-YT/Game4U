import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
CELL_SIZE = 25

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SnakeXenzia")

# Clock for controlling frame rate
clock = pygame.time.Clock()

def show_menu(options, title):
    font = pygame.font.SysFont('times new roman', 50)
    option_font = pygame.font.SysFont('times new roman', 35)
    title_surface = font.render(title, True, WHITE)
    selected_index = 0

    while True:
        screen.fill(BLACK)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_surface, title_rect)

        for i, option in enumerate(options):
            color = YELLOW if i == selected_index else WHITE
            option_surface = option_font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
            screen.blit(option_surface, option_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected_index]

# Display start menu
menu_choice = show_menu(["START NEW GAME", "QUIT"], "SnakeXenzia")
if menu_choice == "QUIT":
    pygame.quit()
    sys.exit()

# Snake and Food Initialization
snake = [(WIDTH // 2, HEIGHT // 2)]  # Snake starts in the center
direction = "RIGHT"
change_to = direction

food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
        random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

# Invincible Mode Initialization
invincible_food = None
invincible_mode = False
invincible_timer = 0
INVINCIBLE_DURATION = 7000  # Invincible mode lasts for 7000 milliseconds

score = 0
speed = 15

# Game Over Function
def game_over():
    while True:
        font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = font.render(f'Game Over! Your Score: {score}', True, WHITE)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (WIDTH / 2, HEIGHT / 4)
        screen.fill(BLACK)
        screen.blit(game_over_surface, game_over_rect)

        menu_choice = show_menu(["START NEW GAME", "QUIT"], "Game Over")
        if menu_choice == "QUIT":
            pygame.quit()
            sys.exit()
        elif menu_choice == "START NEW GAME":
            main_game()

# Main Game Function
def main_game():
    global snake, direction, change_to, food, invincible_food, invincible_mode, invincible_timer, score, speed

    # Reinitialize game variables
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = "RIGHT"
    change_to = direction

    food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    invincible_food = None
    invincible_mode = False
    invincible_timer = 0
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Control snake direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"

        # Update the direction of the snake
        direction = change_to

        # Update snake position
        x, y = snake[0]
        if direction == "UP":
            y -= CELL_SIZE
        elif direction == "DOWN":
            y += CELL_SIZE
        elif direction == "LEFT":
            x -= CELL_SIZE
        elif direction == "RIGHT":
            x += CELL_SIZE

        # Implement edge looping
        x %= WIDTH
        y %= HEIGHT

        # Add new position to snake
        new_head = (x, y)
        snake.insert(0, new_head)

        # Check for collisions with itself
        if not invincible_mode and new_head in snake[1:]:
            game_over()

        # Check if the snake eats normal food
        if new_head == food:
            score += 10
            food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                    random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
            # 10% chance to spawn invincible food
            if random.randint(1, 20) == 1 and invincible_food is None:
                invincible_food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                                random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        else:
            snake.pop()

        # Check if the snake eats invincible food
        if invincible_food and new_head == invincible_food:
            invincible_mode = True
            invincible_timer = pygame.time.get_ticks()
            invincible_food = None

        # Check if invincible mode should end
        if invincible_mode and pygame.time.get_ticks() - invincible_timer > INVINCIBLE_DURATION:
            invincible_mode = False

        # Draw everything
        screen.fill(BLACK)

        # Draw snake
        for segment in snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Draw normal food
        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

        # Draw invincible food
        if invincible_food:
            pygame.draw.rect(screen, WHITE, pygame.Rect(invincible_food[0], invincible_food[1], CELL_SIZE, CELL_SIZE))

        # Display score
        font = pygame.font.SysFont('times new roman', 20)
        score_surface = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_surface, (10, 10))

        # Display invincible mode status
        if invincible_mode:
            invincible_surface = font.render('Invincible Mode On', True, WHITE)
            screen.blit(invincible_surface, (WIDTH - 200, 10))

        pygame.display.flip()

        # Control game speed
        clock.tick(speed)

# Start the main game loop
main_game()