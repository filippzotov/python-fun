import pygame
import random
import os

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
pygame.display.set_caption("First Game")

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT)
)


YELLOW_SPACEWHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)
YELLOW_SPACEWHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACEWHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90,
)
RED_SPACEWHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACEWHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACEWHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270,
)


def draw_window(red, yellow, red_bullets, yellow_bullets):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACEWHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACEWHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def yellow_handle_movment(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y + VEL > 0:  # UP
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:  # DOWN
        yellow.y += VEL


def red_handle_movment(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y + VEL > 0:  # UP
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():
    red = pygame.Rect(
        700,
        300,
        SPACESHIP_WIDTH,
        SPACESHIP_HEIGHT,
    )
    yellow = pygame.Rect(
        100,
        300,
        SPACESHIP_WIDTH,
        SPACESHIP_HEIGHT,
    )
    red_bullets = []
    yellow_bullets = []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
        key_pressed = pygame.key.get_pressed()
        yellow_handle_movment(key_pressed, yellow)
        red_handle_movment(key_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets)
    pygame.quit()


if __name__ == "__main__":
    main()