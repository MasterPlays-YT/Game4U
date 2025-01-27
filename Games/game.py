import pygame
import time
import random
import os

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Dodge")

BG = pygame.transform.scale(pygame.image.load(os.path.join('static', 'images', 'blockdodge', 'blockdodge.jpg')), (WIDTH, HEIGHT + 290))


PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)
BIG_FONT = pygame.font.SysFont("comicsans", 50)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "black")
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, "green", player)
    for star in stars:
        pygame.draw.rect(WIN, "black", star)
    pygame.display.update()

def main_menu():
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_text = BIG_FONT.render("~Block Dodge~", 1, "#003366")
        play_text = FONT.render("1) Press P to Play", 1, "#FF4500")
        quit_text = FONT.render("2) Press Q to Quit", 1, "#FF4500")

        WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, HEIGHT/3))
        WIN.blit(play_text, (WIDTH/2 - play_text.get_width()/2, HEIGHT/2))
        WIN.blit(quit_text, (WIDTH/2 - quit_text.get_width()/2, HEIGHT/2 + 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            return True
        if keys[pygame.K_q]:
            return False

def lost_menu():
    while True:
        WIN.blit(BG, (0, 0))
        lost_text = BIG_FONT.render("You Lost!", 1, "#FF6347")
        restart_text = FONT.render("1) Press R to Restart", 1, "#FF4500")
        quit_text = FONT.render("2) Press Q to Quit", 1, "#FF4500")

        WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/3))
        WIN.blit(restart_text, (WIDTH/2 - restart_text.get_width()/2, HEIGHT/2))
        WIN.blit(quit_text, (WIDTH/2 - quit_text.get_width()/2, HEIGHT/2 + 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            return True
        if keys[pygame.K_q]:
            return False

def main():
    if not main_menu():
        pygame.quit()
        return

    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            if not lost_menu():
                run = False
            else:
                main()
                return

        draw(player, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()

