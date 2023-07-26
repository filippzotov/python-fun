import random


class Roulette:
    def __init__(self) -> None:
        self.wheel = (
            0,
            32,
            15,
            19,
            4,
            21,
            2,
            25,
            17,
            34,
            6,
            27,
            13,
            36,
            11,
            30,
            8,
            23,
            10,
            5,
            24,
            16,
            33,
            1,
            20,
            14,
            31,
            9,
            22,
            18,
            29,
            7,
            28,
            12,
            35,
            3,
            26,
        )
        self.wheel_len = len(self.wheel)
        self.bet_types = {
            "single": self.single_bet,
            "split": self.split_bet,
            "corner": self.croner_bet,
            "lowhigh": self.low_high_bet,
            "redblack": self.red_black_bet,
            "evenodd": self.even_odd_bet,
            "dozens": self.dozens_bet,
            "columns": self.columns_bet,
        }
        self.bet_wins = {
            "single": 35,
            "split": 17,
            "corner": 8,
            "lowhigh": 1,
            "redblack": 1,
            "evenodd": 1,
            "dozens": 2,
            "columns": 2,
        }

    def roll_wheel(self, bet_type, position):
        index = random.randint(0, self.wheel_len - 1)
        check_bet = self.bet_types[bet_type]
        if check_bet(index, position):
            return (self.bet_wins[bet_type], self.wheel[index])
        return (-1, self.wheel[index])

    def single_bet(self, index, number):
        if self.wheel[index] == number:
            return True
        return False

    def split_bet(self, index, numbers):
        if self.wheel[index] in numbers:
            return True
        return False

    def croner_bet(self, index, numbers):
        if self.wheel[index] in numbers:
            return True
        return False

    def low_high_bet(self, index, interval):
        if self.wheel[index] <= 18 and interval == "low":
            return True
        elif self.wheel[index] > 18 and interval == "high":
            return True
        return False

    def red_black_bet(self, index, color):
        if index % 2 == 0:
            win_color = "black"
            if index == 0:
                win_color = None
        else:
            win_color = "red"

        return color == win_color

    def even_odd_bet(self, index, even_odd):
        if self.wheel[index] % 2 == 0:
            win_side = "even"
        else:
            win_side = "odd"

        return even_odd == win_side

    def dozens_bet(self, index, dozen):
        number = self.wheel[index]
        if number < 12:
            win_dozen = "first"
        elif number < 24:
            win_dozen = "second"
        else:
            win_dozen = "third"

        return dozen == win_dozen

    def columns_bet(self, index, column):
        columns = {
            "first": [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
            "second": [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
            "third": [3, 6, 9, 12, 15, 21, 24, 27, 30, 33, 36],
        }
        number = self.wheel[index]
        win_col = None
        for col in columns:
            if number in columns[col]:
                win_col = col
                break
        return win_col == column
