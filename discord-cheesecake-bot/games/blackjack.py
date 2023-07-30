import random


class Blackjack:
    def __init__(self, n) -> None:
        self.deck = []
        for i in range(n):
            self.deck.extend(
                [
                    i + j
                    for i in [
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                        "j",
                        "q",
                        "k",
                    ]
                    for j in ["h", "s", "c", "d"]
                ]
            )

        random.shuffle(self.deck)
        self.players = {}

    def start_game(self, id):
        player_hand = [self.deck.pop(), self.deck.pop()]
        dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.players[id] = (player_hand, dealer_hand)
        if player_hand == 21 and dealer_hand == 21:
            return 0

        if dealer_hand == 21:
            return -1

        if player_hand == 21:
            return 1

        self.players[id] = (player_hand, dealer_hand)

    def take_card(self, id):
        self.players[id][0].append(self.deck.pop())
        new_hand = self.check_hand(self.players[id][0])
        # print(self.players[id][0])
        if new_hand > 21:
            return False
        if new_hand == 21:
            return self.end_game(id)

    def end_game(self, id):
        player_sum = self.check_hand(self.players[id][0])
        dealer_sum = self.check_hand(self.players[id][1])

        while dealer_sum < 17:
            self.players[id][1].append(self.deck.pop())
            dealer_sum = self.check_hand(self.players[id][1])
        if dealer_sum > 21:
            return True
        if dealer_sum == player_sum:
            return 0

        if dealer_sum > player_sum:
            return False
        return True

    def double():
        pass

    def transform_to_int(self, card):
        card = card[:-1]
        if card.isdigit():
            if card == "1":
                return 11
            else:
                return int(card)
        else:
            return 10

    def check_hand(self, hand):
        hand_sum = 0
        was_ace = 0
        for card in hand:
            card = self.transform_to_int(card)
            hand_sum += card
            if card == 11:
                was_ace += 1

            if hand_sum > 21:
                hand_sum -= was_ace * 10

        return hand_sum


# game = Blackjack(4)
# print(game.start_game(1))
# result = game.start_game(1)
# while True:
#     if result is not None:
#         print(result)
#         break
#     inp = input()
#     if inp == "take":
#         result = game.take_card(1)
#     if inp == "stop":
#         result = game.end_game(1)
#         print(result)
#         break
