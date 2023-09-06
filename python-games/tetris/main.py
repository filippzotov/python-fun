import pygame
import random
import copy

pygame.init()

WIDTH, HEIGHT = 300, 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (0, 255, 255)
IDK = (50, 100, 0)

GRAY = (150, 150, 150)
DARK_GRAY = (58, 58, 58)

COLORS = {
    1: BLACK,
    2: GREEN,
    3: BLUE,
    4: RED,
    5: YELLOW,
    6: PURPLE,
    7: IDK,
}

RED = (255, 0, 0)
BLOCK_SIZE = 20
FPS = 60

FIELD_ROWS = 20
FIELD_COLS = 10

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


def draw(field):
    WIN.fill(WHITE)
    background = pygame.Rect(0, 0, BLOCK_SIZE * FIELD_COLS, BLOCK_SIZE * FIELD_ROWS)
    pygame.draw.rect(WIN, DARK_GRAY, background)
    for i, line in enumerate(field):
        for j, block in enumerate(line):
            if block:
                Block = pygame.Rect(
                    BLOCK_SIZE * j + 1,
                    BLOCK_SIZE * i + 1,
                    BLOCK_SIZE - 2,
                    BLOCK_SIZE - 2,
                )
                pygame.draw.rect(WIN, COLORS[block], Block)
            else:
                Block = pygame.Rect(
                    BLOCK_SIZE * j + 1,
                    BLOCK_SIZE * i + 1,
                    BLOCK_SIZE - 2,
                    BLOCK_SIZE - 2,
                )
                pygame.draw.rect(WIN, GRAY, Block)

    pygame.display.update()


class Block:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col


class Stick:
    COLOR = 1

    def __init__(self, row, col) -> None:
        self.blocks = []
        self.position = 0
        for i in range(4):
            self.blocks.append(Block(row, col + i))

    def rotate(self):
        row = self.blocks[0].row
        col = self.blocks[0].col
        self.blocks = []
        if self.position % 2 != 0:
            for i in range(4):
                self.blocks.append(Block(row, col + i))
        else:
            for i in range(4):
                self.blocks.append(Block(row + i, col))
        self.position = (self.position + 1) % 4


class Box:
    COLOR = 2

    def __init__(self, row, col) -> None:
        self.blocks = []
        self.position = 0
        for i in range(2):
            self.blocks.append(Block(row, col + i))
        for i in range(2):
            self.blocks.append(Block(row + 1, col + i))

    def rotate(self):
        self.position = (self.position + 1) % 4


class Tshape:
    COLOR = 3

    def __init__(self, row, col) -> None:
        self.blocks = []
        self.position = 0
        self.blocks.append(Block(row, col + 1))
        for i in range(3):
            self.blocks.append(Block(row + 1, col + i))

    def rotate(self):
        row = self.blocks[3].row
        col = self.blocks[3].col
        self.blocks = []
        if self.position == 0:
            self.blocks.append(Block(row, col + 1))
            for i in range(3):
                self.blocks.append(Block(row + i - 1, col))
        elif self.position == 1:
            self.blocks.append(Block(row + 1, col))
            for i in range(3):
                self.blocks.append(Block(row, col - 1 + i))
        elif self.position == 2:
            self.blocks.append(Block(row, col - 1))
            for i in range(3):
                self.blocks.append(Block(row - 1 + i, col))
        elif self.position == 3:
            self.blocks.append(Block(row - 1, col))
            for i in range(3):
                self.blocks.append(Block(row, col - 1 + i))
        self.position = (self.position + 1) % 4


class Sleft:
    COLOR = 4

    def __init__(self, row, col) -> None:
        self.blocks = []
        self.position = 0
        for i in range(2):
            self.blocks.append(Block(row, col + i))
        for i in range(2):
            self.blocks.append(Block(row + 1, col + i - 1))

    def rotate(self):
        row = self.blocks[0].row
        col = self.blocks[0].col
        self.blocks = []
        if self.position % 2 != 0:
            for i in range(2):
                self.blocks.append(Block(row, col + i))
            for i in range(2):
                self.blocks.append(Block(row + 1, col + i - 1))
        else:
            for i in range(2):
                self.blocks.append(Block(row + i, col))
            for i in range(2):
                self.blocks.append(Block(row + i + 1, col + 1))
        self.position = (self.position + 1) % 4


class Sright:
    COLOR = 5

    def __init__(self, row, col) -> None:
        self.blocks = []
        self.position = 0
        for i in range(2):
            self.blocks.append(Block(row, col + i))
        for i in range(2):
            self.blocks.append(Block(row + 1, col + i + 1))

    def rotate(self):
        row = self.blocks[0].row
        col = self.blocks[0].col
        self.blocks = []
        if self.position % 2 != 0:
            for i in range(2):
                self.blocks.append(Block(row, col + i))
            for i in range(2):
                self.blocks.append(Block(row + 1, col + i + 1))
        else:
            for i in range(2):
                self.blocks.append(Block(row + i, col))
            for i in range(2):
                self.blocks.append(Block(row + i - 1, col + 1))
        self.position = (self.position + 1) % 4


class Lleft:
    COLOR = 6

    def __init__(self, row, col) -> None:
        self.blocks = []
        self.position = 0
        for i in range(3):
            self.blocks.append(Block(row + i, col))
        self.blocks.append(Block(row + 2, col - 1))

    def rotate(self):
        row = self.blocks[1].row
        col = self.blocks[1].col
        self.blocks = []
        if self.position == 0:
            self.blocks.append(Block(row - 1, col))
            for i in range(3):
                self.blocks.append(Block(row, col + i))
        elif self.position == 1:
            self.blocks.append(Block(row, col + 1))
            for i in range(3):
                self.blocks.append(Block(row + i, col))
        elif self.position == 2:
            self.blocks.append(Block(row + 1, col))
            for i in range(3):
                self.blocks.append(Block(row, col - i))
        elif self.position == 3:
            self.blocks.append(Block(row, col - 1))
            for i in range(3):
                self.blocks.append(Block(row - i, col))
        self.position = (self.position + 1) % 4


class Lright:
    COLOR = 7

    def __init__(self, row, col) -> None:
        self.blocks = []
        self.position = 0
        for i in range(3):
            self.blocks.append(Block(row + i, col))
        self.blocks.append(Block(row + 2, col + 1))

    def rotate(self):
        row = self.blocks[1].row
        col = self.blocks[1].col
        self.blocks = []
        if self.position == 0:
            self.blocks.append(Block(row + 1, col))
            for i in range(3):
                self.blocks.append(Block(row, col + i))
        elif self.position == 1:
            self.blocks.append(Block(row, col - 1))
            for i in range(3):
                self.blocks.append(Block(row + i, col))
        elif self.position == 2:
            self.blocks.append(Block(row - 1, col))
            for i in range(3):
                self.blocks.append(Block(row, col - i))
        elif self.position == 3:
            self.blocks.append(Block(row, col + 1))
            for i in range(3):
                self.blocks.append(Block(row - i, col))
        self.position = (self.position + 1) % 4


def handle_collision(field, figure):
    blocks_of_firue = [(block.row, block.col) for block in figure.blocks]
    for block in figure.blocks:
        if (block.row + 1, block.col) not in blocks_of_firue:
            if block.row + 1 >= FIELD_ROWS:
                return False
            if field[block.row + 1][block.col] != 0:
                return False
    return True


def move_figure_down(field, figure):
    if not handle_collision(field, figure):
        return False
    for block in figure.blocks:
        field[block.row][block.col] = 0
    for block in figure.blocks:
        block.row += 1
        field[block.row][block.col] = figure.COLOR

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
        field[block.row][block.col] = figure.COLOR
    return True


def handle_figure_side_move(field, figure, direction):
    blocks_of_firue = [(block.row, block.col) for block in figure.blocks]
    for block in figure.blocks:
        if (block.row, block.col + direction) not in blocks_of_firue:
            if block.col + direction >= FIELD_COLS or block.col + direction < 0:
                return True
            if field[block.row][block.col + direction] != 0:
                return True
    move_figure_side(field, figure, direction)
    return False


def check_fit_figure(field, figure):
    for block in figure.blocks:
        if (
            block.row >= FIELD_ROWS
            or block.row < 0
            or block.col >= FIELD_COLS
            or block.col < 0
        ):
            return False

        if field[block.row][block.col] != 0:
            return False
    return True


def remove_add_figure(field, figure, remove=True):
    for block in figure.blocks:
        if remove:
            field[block.row][block.col] = 0
        else:
            field[block.row][block.col] = figure.COLOR


def rotate_figure(field, figure):
    old_figure = copy.deepcopy(figure)
    figure.rotate()
    remove_add_figure(field, old_figure)
    if not check_fit_figure(field, figure):
        for _ in range(3):
            figure.rotate()
    remove_add_figure(field, figure, remove=False)


def main():
    run = True
    clock = pygame.time.Clock()
    fall_interval = 300
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
    # figure = Lright(0, 5)
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
                elif event.key == pygame.K_SPACE:
                    while True:
                        if not move_figure_down(field, figure):
                            figure_falling = False
                            check_lines(field)
                            break

                elif event.key == pygame.K_w:
                    rotate_figure(field, figure)
                elif event.key == pygame.K_r:
                    run = False

        if not figure_falling:
            figure_falling = True
            # figure = Lright(0, 5)
            figure = figures[random.randint(0, 6)](0, 5)

        current_time = pygame.time.get_ticks()
        if current_time - last_fall_time > fall_interval:
            if not move_figure_down(field, figure):
                figure_falling = False
                check_lines(field)
            last_fall_time = current_time

        draw(field)

    main()


if __name__ == "__main__":
    main()
