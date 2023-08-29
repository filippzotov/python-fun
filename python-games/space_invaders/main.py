import pygame

pygame.init()

WIDTH, HEIGHT = 400, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

FONT = pygame.font.SysFont("comicsans", 40)

FPS = 60

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 24


BULLET_SIZE = 2


class Alien:
    VEL = 1
    COLOR = GREEN

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.alive = True

    def draw(self):
        if self.alive:
            pygame.draw.rect(WIN, self.COLOR, self.rect)

    def move(self):
        self.rect.x += self.VEL
        self.y += self.VEL

    def kill(self):
        self.alive = False


class Bullet:
    VEL = 6
    COLOR = WHITE

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(WIN, self.COLOR, self.rect)

    def move(self):
        self.rect.y -= self.VEL
        self.y -= self.VEL

    def collision(self, alien):
        return self.rect.colliderect(alien)


class Player:
    COLOR = WHITE
    VEL = 3

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.bullets = []

    def draw(self):
        # pygame.draw.rect(WIN, self.COLOR, (self.x, self.y, self.width, self.height))
        # WIN.blit(self.rect, (self.rect.x, self.rect))
        pygame.draw.rect(WIN, self.COLOR, self.rect)

    def move(self, left=True):
        if left:
            # self.x -= self.VEL
            self.rect.x -= self.VEL
            self.x -= self.VEL
        else:
            # self.x += self.VEL
            self.rect.x += self.VEL
            self.x += self.VEL


def handle_player_movement(keys, player: Player):
    if keys[pygame.K_a] and player.x - 10 > 0:
        player.move(left=True)
    elif keys[pygame.K_d] and player.x + player.width + 10 < WIDTH:
        player.move(left=False)


def draw(player: Player, aliens):
    WIN.fill(BLACK)
    player.draw()
    for bullet in player.bullets:
        bullet.draw()
    for alien in aliens:
        alien.draw()
    pygame.display.update()


def handle_bullets(player: Player, aliens):
    for bullet in player.bullets:
        bullet.move()
        for alien in aliens:
            if bullet.collision(alien):
                alien.kill()
                player.bullets.remove(bullet)
        if bullet.y < 0:
            player.bullets.remove(bullet)


def handle_aliens(aliens):
    for alien in aliens:
        alien.move()


def main():
    run = True
    clock = pygame.time.Clock()

    player = Player(
        WIDTH // 2 - PLAYER_WIDTH // 2,
        HEIGHT - PLAYER_HEIGHT - 10,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )
    aliens = [Alien(10, 10, 20, 20)]
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(
                        player.x + player.width // 2, player.y, BULLET_SIZE, BULLET_SIZE
                    )
                    player.bullets.append(bullet)

        keys = pygame.key.get_pressed()

        handle_player_movement(keys, player)
        handle_aliens(aliens)
        handle_bullets(player, aliens)
        draw(player, aliens)

    pygame.quit()


if __name__ == "__main__":
    main()
