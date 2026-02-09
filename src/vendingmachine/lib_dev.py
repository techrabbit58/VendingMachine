from functools import cache
from typing import Generator

from vendingmachine.conf import VALUES, BUTTONS, PRICES, COINS


def overpaid(price: int) -> dict[str, int]:
    coin, value = max_coin()
    coin_box = {coin: 0}
    amount = 0
    while amount <= price:
        coin_box[coin] += 1
        amount += value
    return coin_box


def max_coin() -> tuple[str, int]:
    value = max(VALUES)
    return get_coin_name_by_value(value), value


def button_and_price() -> Generator[tuple[str, int]]:
    for i, button in enumerate(BUTTONS):
        price = PRICES[i]
        yield button, price


@cache
def get_coin_name_by_value(value: int) -> str | None:
    coin = None
    for i, v in enumerate(VALUES):
        if v == value:
            coin = COINS[i]
            break
    return coin
