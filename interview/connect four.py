import random


class ConnectFour:
    def __init__(self, i, j) -> None:
        self.board = [[0 for _ in range(j)] for _ in range(i)]
        self.columns = len(self.board[0])
        self.rows = len(self.board)
        self.end = ""
        self.free_space = self.rows * self.columns
        self.column_height = [i - 1 for _ in range(j)]

    def turn(self, color, column):
        if self.column_height[column] == -1:
            return False
        self.board[self.column_height[column]][column] = color
        self.win_check(self.column_height[column], column, color)
        self.column_height[column] -= 1
        return True

    def win_check(self, row, column, color):
        cols = self.check_win_column(row, column, color)
        rows = self.check_win_row(row, column, color)
        d1 = self.check_win_diagonal1(row, column, color)
        d2 = self.check_win_diagonal2(row, column, color)
        if d1 or d2 or cols or rows:
            self.end = color

    def check_win_column(self, row, column, color):
        count = 3
        check_row = row + 1
        while check_row < self.rows:
            if self.board[check_row][column] == color:
                count -= 1
                check_row += 1
            else:
                break
        if count <= 0:
            return True
        return False

    def check_win_row(self, row, column, color):
        count = 3
        check_column = column - 1

        while check_column >= 0:
            if self.board[row][check_column] == color:
                count -= 1
                check_column -= 1
            else:
                break
        check_column = column + 1
        while check_column < self.columns:
            if self.board[row][check_column] == color:
                count -= 1
                check_column += 1
            else:
                break
        if count <= 0:
            return True
        return False

    def check_win_diagonal1(self, row, column, color):
        count = 3
        check_row = row - 1
        check_column = column - 1

        while check_row >= 0 and check_column >= 0:
            if self.board[check_row][check_column] == color:
                count -= 1
                check_row -= 1
                check_column -= 1
            else:
                break
        check_row = row + 1
        check_column = column + 1
        while check_row < self.rows and check_column < self.columns:
            if self.board[check_row][check_column] == color:
                count -= 1
                check_row += 1
                check_column += 1
            else:
                break
        if count <= 0:
            return True
        return False

    def check_win_diagonal2(self, row, column, color):
        count = 3
        check_row = row + 1
        check_column = column - 1

        while check_row < self.rows and check_column >= 0:
            if self.board[check_row][check_column] == color:
                count -= 1
                check_row += 1
                check_column -= 1
            else:
                break
        check_row = row - 1
        check_column = column + 1
        while check_row >= 0 and check_column < self.columns:
            if self.board[check_row][check_column] == color:
                count -= 1
                check_row -= 1
                check_column += 1
            else:
                break
        if count <= 0:
            return True
        return False

    def display(self):
        for line in self.board:
            print([i if i else "0" for i in line])


def make_random_turn(game, color):
    turn = random.randint(0, 6)
    while not game.turn(color, turn):
        turn = random.randint(0, 6)
    print(f"last turn {color}, column ", turn)
    game.display()


if __name__ == "__main__":
    rows = 6
    columns = 7
    game = ConnectFour(rows, columns)

    for i in range(rows * columns):
        color = "R" if i % 2 == 0 else "Y"
        make_random_turn(game, color)
        if game.end:
            print(f"{game.end} won!")
            break
        if not game.free_space:
            print("draw!")
            break
