import random


class SlotLine:
    def __init__(self) -> None:
        self.line = ["🥜", "🧋", "🍆", "🍒", "🍰"]
        random.shuffle(self.line)

    def roll(self):
        choice = random.randint(0, len(self.line) - 1)
        return [
            self.line[choice - 1],
            self.line[choice],
            self.line[(choice + 1) % len(self.line)],
        ]


class SlotMachine:
    def __init__(self) -> None:
        self.machine = [
            SlotLine(),
            SlotLine(),
            SlotLine(),
        ]
        self.prize = {
            "🥜": 10,
            "🧋": 15,
            "🍆": 20,
            "🍒": 30,
            "🍰": 50,
            "": 0,
        }

    def roll_machine(self):
        roll_results = []
        win_prize = 1
        for line in self.machine:
            roll_results.append(line.roll())

        slot_view = []

        for line in zip(*roll_results):
            letter = random.choice(["🥜", "🧋", "🍆", "🍒", "🍰"])
            if random.random() < 0.15:
                slot_view.append([letter, letter, letter])
            else:
                slot_view.append(line)

            if len(set(slot_view[-1])) == 1:
                win_prize *= self.prize[slot_view[-1][0]]
        return (win_prize, slot_view)

    # def win_roll_machine(self):


# game = SlotMachine()
# print(game.roll_machine())
