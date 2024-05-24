import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Spaceship settings
spaceship_img = pygame.image.load("astronave.png")  # Add a spaceship image in the same directory
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))  # Scale the image to fit
spaceship_rect = spaceship_img.get_rect()
spaceship_rect.centerx = WIDTH // 2  # Start at the center horizontally
spaceship_rect.bottom = HEIGHT - 20  # Start closer to the bottom of the screen
spaceship_speed = 5

# Bullet settings
bullets = []
bullet_speed = 7

# Enemy settings
enemies = []
enemy_speed = 3
enemy_spawn_time = 1000  # in milliseconds

# Score and lives
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# Create custom events
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, enemy_spawn_time)

# Clock
clock = pygame.time.Clock()

def draw_window():
    screen.fill(WHITE)  # Change the background color to blue
    screen.blit(spaceship_img, spaceship_rect.topleft)
    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # Display score
    score_font = pygame.font.SysFont(None, 36)
    score_text = score_font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Display lives
    lives_text = score_font.render("Lives: " + str(lives), True, BLACK)
    screen.blit(lives_text, (WIDTH - 120, 10))
    
    pygame.display.flip()

def main():
    global score, lives
    run = True
    while run:
        clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == ADDENEMY:
                enemy = pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50)
                enemies.append(enemy)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_rect.left > 0:
            spaceship_rect.x -= spaceship_speed
        if keys[pygame.K_RIGHT] and spaceship_rect.right < WIDTH:
            spaceship_rect.x += spaceship_speed
        if keys[pygame.K_UP] and spaceship_rect.top > 0:
            spaceship_rect.y -= spaceship_speed
        if keys[pygame.K_DOWN] and spaceship_rect.bottom < HEIGHT:
            spaceship_rect.y += spaceship_speed
        if keys[pygame.K_SPACE]:
            bullet = pygame.Rect(spaceship_rect.centerx - 2, spaceship_rect.top, 5, 10)
            bullets.append(bullet)

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Move enemies
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.top > HEIGHT:
                enemies.remove(enemy)
                lives -= 1  # Deduct a life when an enemy passes through the bottom
                if lives <= 0:
                    run = False

        # Check collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1  # Increase the score when an enemy is destroyed

        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
