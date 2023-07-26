import pytest

from roulette import Roulette


@pytest.fixture()
def game():
    roulette = Roulette()
    return roulette


def test_single_bet_win(game):
    assert game.single_bet(0, 0) == True


def test_single_bet_lose(game):
    assert game.single_bet(1, 1) == False


def test_split_bet_win(game):
    assert game.split_bet(23, [1, 2]) == True


def test_split_bet_lose(game):
    assert game.split_bet(1, [1, 2]) == False


def test_croner_bet_win(game):
    assert game.croner_bet(23, [1, 2, 4, 5]) == True


def test_croner_bet_lose(game):
    assert game.croner_bet(1, [1, 2, 4, 5]) == False


def test_low_high_bet_win_low(game):
    assert game.low_high_bet(4, "low") == True


def test_low_high_bet_win_high(game):
    assert game.low_high_bet(1, "high") == True


def test_low_high_bet_lose_low(game):
    assert game.low_high_bet(4, "high") == False


def test_low_high_bet_lose_high(game):
    assert game.low_high_bet(1, "low") == False


def test_red_black_bet_win(game):
    assert game.red_black_bet(1, "red") == True


def test_red_black_bet_lose(game):
    assert game.red_black_bet(1, "black") == False


def test_even_odd_bet_win(game):
    assert game.even_odd_bet(1, "even") == True


def test_even_odd_bet_lose(game):
    assert game.even_odd_bet(2, "even") == False


def test_dozens_bet_win(game):
    assert game.dozens_bet(9, "third") == True


def test_dozens_bet_lose(game):
    assert game.dozens_bet(0, "third") == False


def test_columns_bet_win(game):
    assert game.columns_bet(1, "second") == True


def test_columns_bet_lose(game):
    assert game.columns_bet(0, "third") == False
