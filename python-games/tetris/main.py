import pygame

pygame.init()

WIDTH, HEIGHT = 300, 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLOCK_SIZE = 20
FPS = 60

FIELD_ROWS = 20
FIELD_COLS = 10

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


# class Figure:
#     COLOR = RED

#     def __init__(self, x, y, width, height) -> None:
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.rect = pygame.Rect(x, y, width, height)

#     def draw(self):
#         pygame.draw.rect(WIN, self.COLOR, self.rect)

#     def move(self):
#         self.y += self.height
#         self.rect.y += self.height


def draw(field):
    WIN.fill(WHITE)
    # figure.draw()
    for i, line in enumerate(field):
        for j, block in enumerate(line):
            if block:
                Block = pygame.Rect(
                    BLOCK_SIZE * j, BLOCK_SIZE * i, BLOCK_SIZE, BLOCK_SIZE
                )
                pygame.draw.rect(WIN, RED, Block)

    pygame.display.update()


class ff:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col


def handle_collision(field, new_figure):
    if new_figure.row >= FIELD_ROWS or new_figure.col >= FIELD_COLS:
        return True
    if field[new_figure.row][new_figure.col] != 0:
        return True

    return False


def move_figure(field, figure):
    start_row, start_col = figure.row, figure.col
    field[figure.row][figure.col] = 0
    figure.row += 1
    if not handle_collision(field, figure):
        field[figure.row][figure.col] = 1
        return True

    field[start_row][start_col] = 1

    return False


def handle_figure_movement(keys, field, figure: ff):
    if keys[pygame.K_a]:
        field[figure.row][figure.col] = 0
        figure.col -= 1
        field[figure.row][figure.col] = 1
    elif keys[pygame.K_d]:
        field[figure.row][figure.col] = 0
        figure.col += 1
        field[figure.row][figure.col] = 1


def main():
    run = True
    clock = pygame.time.Clock()
    fall_interval = 100
    last_fall_time = pygame.time.get_ticks()

    figure_falling = True
    figure = ff(0, 5)
    field = [[0 for i in range(FIELD_COLS)] for j in range(FIELD_ROWS)]

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    field[figure.row][figure.col] = 0
                    figure.col -= 1
                    field[figure.row][figure.col] = 1
                elif event.key == pygame.K_d:
                    field[figure.row][figure.col] = 0
                    figure.col += 1
                    field[figure.row][figure.col] = 1

        if not figure_falling:
            figure_falling = True
            figure = ff(0, 5)

        keys = pygame.key.get_pressed()
        pygame.key
        # handle_figure_movement(keys, field, figure)

        current_time = pygame.time.get_ticks()
        if current_time - last_fall_time > fall_interval:
            if not move_figure(field, figure):
                figure_falling = False
            last_fall_time = current_time

        draw(field)

    main()


if __name__ == "__main__":
    main()
