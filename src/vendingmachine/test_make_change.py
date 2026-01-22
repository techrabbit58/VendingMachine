import pytest

from .conf import BUTTONS, PRICE_POINTS, ACCEPTABLE_COINS
from .lib import fewest_coins_that_match_exact_amount, coin_sum


def overpaid(price: int) -> list[str]:
    coin, value = max(ACCEPTABLE_COINS.items(), key=lambda x: x[1])
    coin_sequence = []
    amount = 0
    while amount <= price:
        coin_sequence.append(coin)
        amount += value
    return coin_sequence


@pytest.mark.parametrize("button, price", zip(BUTTONS, PRICE_POINTS))
def test_machine_returns_correct_change_on_sale(vending_machine, button, price):
    v = vending_machine
    coin_sequence = overpaid(price)
    change = list(fewest_coins_that_match_exact_amount(coin_sum(coin_sequence) - price))
    assert len(change) > 0
    for coin in coin_sequence:
        v.insert_coin(coin)
    product = v.select_product(button)
    assert v.hopper == [product]
    assert len(v.coin_buffer) == 0
    assert v.coin_return == change
