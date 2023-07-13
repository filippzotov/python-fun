import random


class ConnectFour:
    def __init__(self, i, j) -> None:
        self.board = [[0 for _ in range(j)] for _ in range(i)]
        self.columns = len(self.board[0])
        self.rows = len(self.board)
        self.end = ""
        self.free_space = self.rows * self.columns

    def turn(self, color, column):
        for i in range(len(self.board)):
            if self.board[i][column] != 0:
                if i != 0:
                    self.board[i - 1][column] = color
                    self.free_space -= 1
                    self.win_check(i - 1, column, color)
                    return True
                else:
                    return False
        self.board[len(self.board) - 1][column] = color
        self.win_check(len(self.board) - 1, column, color)
        self.free_space -= 1
        return True

    def win_check(self, i, j, color):
        cols = self.check_win_column(i, j, color)
        rows = self.check_win_row(i, j, color)
        d1 = self.check_win_diagonal1(i, j, color)
        d2 = self.check_win_diagonal2(i, j, color)
        if d1 or d2 or cols or rows:
            self.end = color

    def check_win_column(self, i, j, color):
        count = 4
        while i < self.rows:
            if self.board[i][j] == color:
                count -= 1
                i += 1
            else:
                break
        if count <= 0:
            return True
        return False

    def check_win_row(self, i, j, color):
        count = 3
        start = j - 1

        while start >= 0:
            if self.board[i][start] == color:
                count -= 1
                start -= 1
            else:
                break
        start = j + 1
        while start < self.columns:
            if self.board[i][start] == color:
                count -= 1
                start += 1
            else:
                break
        if count <= 0:
            return True
        return False

    def check_win_diagonal1(self, i, j, color):
        count = 3
        start1 = i - 1
        start2 = j - 1

        while start1 >= 0 and start2 >= 0:
            if self.board[start1][start2] == color:
                count -= 1
                start1 -= 1
                start2 -= 1
            else:
                break
        start1 = i + 1
        start2 = j + 1
        while start1 < self.rows and start2 < self.columns:
            if self.board[start1][start2] == color:
                count -= 1
                start1 += 1
                start2 += 1
            else:
                break
        if count <= 0:
            return True
        return False

    def check_win_diagonal2(self, i, j, color):
        count = 3
        start1 = i + 1
        start2 = j - 1

        while start1 < self.rows and start2 >= 0:
            if self.board[start1][start2] == color:
                count -= 1
                start1 += 1
                start2 -= 1
            else:
                break
        start1 = i - 1
        start2 = j + 1
        while start1 >= 0 and start2 < self.columns:
            if self.board[start1][start2] == color:
                count -= 1
                start1 -= 1
                start2 += 1
            else:
                break
        if count <= 0:
            return True
        return False

    def display(self):
        for line in self.board:
            print([i if i else "0" for i in line])


if __name__ == "__main__":
    game = ConnectFour(6, 7)

    RED_TURN = True
    while True:
        if RED_TURN:
            turn = random.randint(0, 6)
            while not game.turn("R", turn):
                turn = random.randint(0, 6)
            RED_TURN = False
            print("last turn R, column ", turn)
        else:
            turn = random.randint(0, 6)
            while not game.turn("Y", turn):
                turn = random.randint(0, 6)
            RED_TURN = True
            print("last turn Y, column ", turn)

        game.display()
        print()
        if not game.free_space:
            print("draw!")
            break
        if game.end:
            print(f"{game.end} won!")
            break
