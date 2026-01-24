import pytest

from .conf import BUTTONS, PRICES, VALUES
from .lib import fewest_coins_that_match_exact_amount, coin_sum, get_coin_name_by_value


def overpaid(price: int) -> dict[str, int]:
    value = max(VALUES)
    coin = get_coin_name_by_value(value)
    coin_sequence = {coin: 0}
    amount = 0
    while amount <= price:
        coin_sequence[coin] += 1
        amount += value
    return coin_sequence


@pytest.mark.parametrize("button, price", zip(BUTTONS, PRICES))
def test_machine_returns_correct_change_on_sale(vending_machine, button, price):
    v = vending_machine
    coin_sequence = overpaid(price)
    change = list(fewest_coins_that_match_exact_amount(coin_sum(coin_sequence) - price))
    assert len(change) > 0
    for coin, count in coin_sequence.items():
        for _ in range(count):
            v.insert_coin(coin)
    product = v.select_product(button)
    assert v.hopper == [product]
    assert coin_sum(v.coin_buffer) == 0
    assert v.coin_return == change
