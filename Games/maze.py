import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
FPS = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Runner')

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def generate_maze():
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    stack = [(random.randint(0, COLS-1), random.randint(0, ROWS-1))]
    maze[stack[-1][1]][stack[-1][0]] = 0
    
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in [UP, DOWN, LEFT, RIGHT]:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
                neighbors.append((dx, dy, nx, ny))
        
        if neighbors:
            dx, dy, nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[y + dy][x + dx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
    
    return maze

def draw_maze(maze):
    for y in range(ROWS):
        for x in range(COLS):
            color = BLACK if maze[y][x] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def is_collision(x, y, maze):
    if 0 <= x < COLS and 0 <= y < ROWS and maze[y][x] == 0:
        return False
    return True

def draw_space_background():
    screen.fill(BLACK)
    
    for _ in range(200):
        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, WHITE, (star_x, star_y), random.randint(1, 3))

def game(score):
    maze = generate_maze()
    player_x, player_y = 1, 1
    player_color = GREEN
    endpoint_x, endpoint_y = random.randint(0, COLS-1), random.randint(0, ROWS-1)
    while maze[endpoint_y][endpoint_x] == 1:
        endpoint_x, endpoint_y = random.randint(0, COLS-1), random.randint(0, ROWS-1)
    
    clock = pygame.time.Clock()
    
    while True:
        draw_space_background()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not is_collision(player_x - 1, player_y, maze):
                player_x -= 1
                score += 10
        if keys[pygame.K_RIGHT]:
            if not is_collision(player_x + 1, player_y, maze):
                player_x += 1
                score += 10
        if keys[pygame.K_UP]:
            if not is_collision(player_x, player_y - 1, maze):
                player_y -= 1
                score += 10
        if keys[pygame.K_DOWN]:
            if not is_collision(player_x, player_y + 1, maze):
                player_y += 1
                score += 10
        draw_maze(maze)
        pygame.draw.rect(screen, player_color, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (endpoint_x * CELL_SIZE, endpoint_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {score}", True, BLUE)
        screen.blit(score_text, (10, 10))
        
        if player_x == endpoint_x and player_y == endpoint_y:
            font = pygame.font.SysFont("Arial", 36)
            win_text = font.render("You Win!", True, BLUE)
            score_text = font.render(f"Score: {score}", True, BLUE)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2 - 20))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2 + 20))
            pygame.display.flip()
            pygame.time.wait(2000)
            return score
            
        pygame.display.flip()
        clock.tick(FPS)

def main():
    score = 0
    while True:
        score = game(score)

if __name__ == '__main__':
    main()