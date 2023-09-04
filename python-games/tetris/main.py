import pygame
import random

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


def draw(field):
    WIN.fill(WHITE)
    for i, line in enumerate(field):
        for j, block in enumerate(line):
            if block:
                Block = pygame.Rect(
                    BLOCK_SIZE * j, BLOCK_SIZE * i, BLOCK_SIZE, BLOCK_SIZE
                )
                pygame.draw.rect(WIN, RED, Block)

    pygame.display.update()


class Block:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col


class Stick:
    def __init__(self, row, col) -> None:
        self.blocks = []
        for i in range(4):
            self.blocks.append(Block(row, col + i))


class Box:
    def __init__(self, row, col) -> None:
        self.blocks = []
        for i in range(2):
            self.blocks.append(Block(row, col + i))
        for i in range(2):
            self.blocks.append(Block(row + 1, col + i))


class Tshape:
    def __init__(self, row, col) -> None:
        self.blocks = []
        self.blocks.append(Block(row, col + 1))
        for i in range(3):
            self.blocks.append(Block(row + 1, col + i))


class Sleft:
    def __init__(self, row, col) -> None:
        self.blocks = []
        for i in range(2):
            self.blocks.append(Block(row, col + i))
        for i in range(2):
            self.blocks.append(Block(row + 1, col + i - 1))


class Sright:
    def __init__(self, row, col) -> None:
        self.blocks = []
        for i in range(2):
            self.blocks.append(Block(row, col + i))
        for i in range(2):
            self.blocks.append(Block(row + 1, col + i + 1))


class Lleft:
    def __init__(self, row, col) -> None:
        self.blocks = []
        for i in range(3):
            self.blocks.append(Block(row + i, col))
        self.blocks.append(Block(row + 2, col - 1))


class Lright:
    def __init__(self, row, col) -> None:
        self.blocks = []
        for i in range(3):
            self.blocks.append(Block(row + i, col))
        self.blocks.append(Block(row + 2, col + 1))


def handle_collision(field, new_figure):
    lowest_point_row = -1
    lowest_point_col = -1
    blocks_to_check = []
    for block in new_figure.blocks:
        if block.row > lowest_point_row:
            lowest_point_row = block.row
            blocks_to_check = [block]
        elif block.row == lowest_point_row:
            blocks_to_check.append(block)
    for block in blocks_to_check:
        if block.row + 1 >= FIELD_ROWS:
            return False
        if field[block.row + 1][block.col] != 0:
            return False

    return True


def move_figure(field, figure):
    if not handle_collision(field, figure):
        return False
    for block in figure.blocks[::-1]:
        field[block.row][block.col] = 0
        block.row += 1
        field[block.row][block.col] = 1
    return True


def check_lines(field):
    rows_to_remove = []
    i = FIELD_ROWS - 1
    while i >= 0:
        for j in range(len(field[i])):
            if field[i][j] == 0:
                break
        else:
            rows_to_remove.append(i)
        i -= 1

    for row in rows_to_remove:
        del field[row]

    for _ in range(len(rows_to_remove)):
        field.insert(0, [0 for i in range(FIELD_COLS)])


def move_figure_side(field, figure, direction):
    for block in figure.blocks:
        field[block.row][block.col] = 0
    for block in figure.blocks:
        block.col += direction
        field[block.row][block.col] = 1
    return True


def handle_figure_side_move(field, figure, direction):
    if direction == -1:
        side_point_row = FIELD_ROWS
        side_point_col = FIELD_COLS
        for block in figure.blocks:
            if block.col < side_point_col:
                side_point_row = block.row
                side_point_col = block.col
    else:
        side_point_row = -1
        side_point_col = -1
        for block in figure.blocks:
            if block.col > side_point_col:
                side_point_row = block.row
                side_point_col = block.col

    if side_point_col + direction >= FIELD_COLS or side_point_col + direction < 0:
        return True
    if field[side_point_row][side_point_col + direction] != 0:
        return True
    move_figure_side(field, figure, direction)
    return False


def main():
    run = True
    clock = pygame.time.Clock()
    fall_interval = 100
    last_fall_time = pygame.time.get_ticks()

    figures = {
        0: Stick,
        1: Box,
        2: Tshape,
        3: Sleft,
        4: Sright,
        5: Lleft,
        6: Lright,
    }

    figure_falling = True
    # figure = Block(0, 5)

    figure = figures[random.randint(0, 6)](0, 5)

    field = [[0 for i in range(FIELD_COLS)] for j in range(FIELD_ROWS)]

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    handle_figure_side_move(field, figure, -1)
                elif event.key == pygame.K_d:
                    handle_figure_side_move(field, figure, 1)
                elif event.key == pygame.K_w:
                    while True:
                        if not move_figure(field, figure):
                            figure_falling = False
                            check_lines(field)
                            break

        if not figure_falling:
            figure_falling = True
            # figure = Block(0, 5)
            figure = figures[random.randint(0, 6)](0, 5)

        keys = pygame.key.get_pressed()

        # handle_figure_movement(keys, field, figure)
        current_time = pygame.time.get_ticks()
        if current_time - last_fall_time > fall_interval:
            if not move_figure(field, figure):
                figure_falling = False
                check_lines(field)
            last_fall_time = current_time

        draw(field)

    main()


if __name__ == "__main__":
    main()
