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

ALIEN_VEL = 1
ALIENS_IN_LINE = 7
ALIEN_LINES = 4
ALIEN_COUNT = ALIENS_IN_LINE * ALIEN_LINES

ALIEN_KILLED = pygame.USEREVENT + 1
PLAYER_LOST = pygame.USEREVENT + 2


class Alien:
    VEL = ALIEN_VEL
    COLOR = GREEN

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.alive = True
        self.left = False

    def draw(self):
        if self.alive:
            pygame.draw.rect(WIN, self.COLOR, self.rect)

    def move(self):
        if self.left:
            self.rect.x -= self.VEL
            self.x -= self.VEL
        else:
            self.rect.x += self.VEL
            self.x += self.VEL

    def move_down(self):
        self.rect.y += 40
        self.y += 40

    def change_direction(self, left=False):
        self.left = left

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
        pygame.draw.rect(WIN, self.COLOR, self.rect)

    def move(self, left):
        if left:
            self.rect.x -= self.VEL
            self.x -= self.VEL
        else:
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
    for alien_line in aliens:
        for alien in alien_line:
            alien.draw()
    pygame.display.update()


def handle_bullets(player: Player, aliens):
    for bullet in player.bullets:
        bullet.move()
        count_aliens = 0
        for i, alien_line in enumerate(aliens):
            for alien in alien_line:
                if not alien.alive:
                    continue
                count_aliens += 1
                if bullet.collision(alien):
                    alien.kill()
                    pygame.event.post(pygame.event.Event(ALIEN_KILLED))
                    player.bullets.remove(bullet)
        if bullet.y < 0:
            player.bullets.remove(bullet)


def handle_aliens_movement(aliens):
    for alien_line in aliens:
        if not alien_line:
            continue
        if alien_line[-1].x > WIDTH - 15 - alien_line[-1].width:
            for alien in alien_line:
                alien.change_direction(left=True)
                alien.move_down()
        elif alien_line[0].x < 15:
            for alien in alien_line:
                alien.change_direction(left=False)
                alien.move_down()

        for alien in alien_line:
            alien.move()
            if alien.alive and alien.y > HEIGHT - alien.height - 40:
                pygame.event.post(pygame.event.Event(PLAYER_LOST))


def end_game(text):
    win_text = FONT.render(text, 1, WHITE)
    WIN.blit(
        win_text,
        (
            WIDTH // 2 - win_text.get_width() // 2,
            HEIGHT // 2 - win_text.get_height() // 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    run = True
    clock = pygame.time.Clock()
    game_ended = False
    Alien.VEL = ALIEN_VEL
    aliens_left = ALIEN_COUNT
    player = Player(
        WIDTH // 2 - PLAYER_WIDTH // 2,
        HEIGHT - PLAYER_HEIGHT - 10,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )
    aliens_in_line_left = ALIENS_IN_LINE * 2
    aliens = [
        [Alien(40 * i, 40 * j, 20, 20) for i in range(1, ALIENS_IN_LINE + 1)]
        for j in range(1, ALIEN_LINES + 1)
    ]
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(
                        player.x + player.width // 2, player.y, BULLET_SIZE, BULLET_SIZE
                    )
                    player.bullets.append(bullet)

            if event.type == ALIEN_KILLED:
                aliens_left -= 1
                aliens_in_line_left -= 1
                if not aliens_in_line_left:
                    Alien.VEL += 1
                    aliens_in_line_left = ALIENS_IN_LINE * 2
                if not aliens_left:
                    end_text = "You've won!"
                    game_ended = True
            if event.type == PLAYER_LOST:
                end_text = "You lost!"
                game_ended = True

        keys = pygame.key.get_pressed()

        handle_player_movement(keys, player)
        handle_aliens_movement(aliens)
        handle_bullets(player, aliens)
        draw(player, aliens)

        if game_ended:
            end_game(end_text)
            break

    main()


if __name__ == "__main__":
    main()
