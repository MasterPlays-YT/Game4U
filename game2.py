import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Highway Havoc")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# Font for menu
font = pygame.font.SysFont('times new roman', 50)

# Game variables
car_width = 50
car_height = 100
car_x = width // 2 - car_width // 2
car_y = height - car_height - 10
car_speed = 6
obstacle_width = 50
obstacle_height = 100
obstacle_frequency = 30
score = 0
background_speed = 8

# Load images
car_img = pygame.image.load('car2.png')
car_img = pygame.transform.scale(car_img, (car_width, car_height))

enemy_cars = [
    {'image': pygame.image.load('enemycar.png'), 'speed': random.randint(5, 5)},
    {'image': pygame.image.load('enemycar2.png'), 'speed': random.randint(7, 10)},
    {'image': pygame.image.load('enemycar3.png'), 'speed': random.randint(6, 6)}
]

enemy_cars = [
    {'image': pygame.transform.scale(car['image'], (obstacle_width, obstacle_height)), 'speed': car['speed']}
    for car in enemy_cars
]

background_img = pygame.image.load('road_0.png')
background_img = pygame.transform.scale(background_img, (width, height + 100))

clock = pygame.time.Clock()

# Lanes
lanes = [120, 180, 250, 310, 370, 430, 500, 570, 650]


# Function to display the menu
def show_menu():
    while True:
        screen.fill(BLACK)
        title_text = font.render("Highway Havoc", True, BLUE)
        start_text = font.render("1) Press S to Start", True, WHITE)
        quit_text = font.render("2) Press Q to Quit", True, WHITE)

        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2))
        screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    main_game()  # Start the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def show_crash_message():
    while True:
        screen.fill(BLACK)
        crash_text = font.render("CRASHED!", True, RED)
        retry_text = font.render("1) Press R to Restart", True, WHITE)
        quit_text = font.render("2) Press Q to Quit", True, WHITE)

        screen.blit(crash_text, (width // 2 - crash_text.get_width() // 2, height // 3))
        screen.blit(retry_text, (width // 2 - retry_text.get_width() // 2, height // 2))
        screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()



def main_game():
    global car_x, score
    obstacles = []
    background_y = 0
    running = True

    while running:
        screen.fill(BLACK)

        # Draw background
        screen.blit(background_img, (0, background_y))
        screen.blit(background_img, (0, background_y - height))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < width - car_width:
            car_x += car_speed
        

        # Spawn obstacles
        if random.randint(1, obstacle_frequency) == 1:
            lane = random.choice(lanes)
            obstacle_x = lane
            obstacle_y = -obstacle_height
            car_type = random.choice(enemy_cars)
            enemy_car_img = car_type['image']
            obstacle_speed = car_type['speed']
            obstacles.append([obstacle_x, obstacle_y, enemy_car_img, obstacle_speed])

        # Move obstacles
        for obstacle in obstacles[:]:
            obstacle[1] += obstacle[3]
            if obstacle[1] > height:
                obstacles.remove(obstacle)
                score += 1

           # Collision detection
            if (
                car_x < obstacle[0] + obstacle_width and
                car_x + car_width > obstacle[0] and
                car_y < obstacle[1] + obstacle_height and
                car_y + car_height > obstacle[1]
            ):
                show_crash_message()


            # Draw enemy cars
            screen.blit(obstacle[2], (obstacle[0], obstacle[1]))

        # Draw player's car
        screen.blit(car_img, (car_x, car_y))

        # Scroll background
        background_y += background_speed
        if background_y >= height:
            background_y = 0

        # Draw score
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)



    


# Show menu before starting the game
show_menu()

# Start the game
main_game()
