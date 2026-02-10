from functools import cache
from typing import Generator

from .conf import VALUES, BUTTONS, PRICES, COINS
from .lib import coin_by_descending_value, get_coin_value


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


def overpayable_product_selections() -> list[tuple[str, int]]:
    buttons_and_prices = []
    for button, price in button_and_price():
        if price > 0 and price % max_coin()[1] != 0:
            buttons_and_prices.append((button, price))
    return buttons_and_prices


def fewest_coins_that_match_exact_amount(remaining: int) -> Generator[str]:
    ordered_coins = coin_by_descending_value()
    coin = next(ordered_coins)
    value = get_coin_value(coin)
    while remaining > 0:
        if value <= remaining:
            yield coin
            remaining -= value
        else:
            coin = next(ordered_coins)
            value = get_coin_value(coin)


def valid_coins_and_values() -> Generator[tuple[str, int]]:
    for i, coin in enumerate(COINS):
        yield coin, VALUES[i]


def invalid_coins() -> Generator[str]:
    yield "quux"
    yield "$@µ"
