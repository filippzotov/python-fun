import copy
import random
from collections import Counter


class Hat:
    def __init__(self, **kwargs) -> None:
        self.d = kwargs
        self.contents = []
        for key in self.d:
            self.contents.extend([key] * self.d[key])

    def draw(self, number):
        answer = []
        while len(self.contents) and number:
            pick = random.choice(self.contents)
            answer.append(pick)
            del self.contents[self.contents.index(pick)]
            number -= 1
        return answer


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    count = 0
    for _ in range(num_experiments):
        hat_clone = copy.deepcopy(hat)
        draw_balls = hat_clone.draw(num_balls_drawn)
        d = Counter(draw_balls)
        for key in expected_balls:
            if d[key] < expected_balls[key]:
                break
        else:
            count += 1

    return count / num_experiments


h = Hat(red=5, blue=1, green=9)
print(experiment(h, {"blue": 1, "red": 1}, 10, 20000))
