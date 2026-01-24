from functools import cache
from operator import itemgetter
from typing import Generator

from .conf import COINS, VALUES, PRODUCTS, CURRENCY, PRICES, BUTTONS


@cache
def check_coin(coin: str) -> int:
    value = 0
    for i, c in enumerate(COINS):
        if c == coin:
            value = VALUES[i]
    return value


@cache
def get_product_by_button(button: str) -> str | None:
    product = None
    for i, b in enumerate(BUTTONS):
        if b == button:
            product = PRODUCTS[i]
            break
    return product


@cache
def get_price_by_product(product: str) -> int:
    price = 0
    for i, p in enumerate(PRODUCTS):
        if p == product:
            price = PRICES[i]
            break
    return price


@cache
def get_coin_value(coin: str) -> int:
    value = 0
    for i, c in enumerate(COINS):
        if c == coin:
            value = VALUES[i]
            break
    return value


@cache
def get_coin_name_by_value(value: int) -> str | None:
    coin = None
    for i, v in enumerate(VALUES):
        if v == value:
            coin = COINS[i]
            break
    return coin


def get_all_products() -> Generator[str]:
    yield from PRODUCTS


def get_acceptable_coins() -> Generator[str]:
    yield from COINS


def fewest_coins_that_match_exact_amount(remaining: int) -> Generator[str]:
    coin_by_descending_value = (item[0] for item in sorted(zip(COINS, VALUES), reverse=True, key=itemgetter(1)))
    coin = next(coin_by_descending_value)
    value = get_coin_value(coin)
    while remaining > 0:
        if value <= remaining:
            yield coin
            remaining -= value
        else:
            coin = next(coin_by_descending_value)
            value = get_coin_value(coin)


def coin_sum(coins: dict[str, int]) -> int:
    return sum(get_coin_value(coin) * count for coin, count in coins.items())


def get_currency() -> str:
    return CURRENCY
