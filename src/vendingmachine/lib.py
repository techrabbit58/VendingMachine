from functools import cache
from operator import itemgetter
from typing import Generator

from .conf import COINS, VALUES, PRODUCTS, CURRENCY, PRICES, BUTTONS

type CoinBox = dict[str, int]


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


def get_all_products() -> Generator[str]:
    yield from PRODUCTS


def get_acceptable_coins() -> Generator[str]:
    yield from COINS


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


def coin_by_descending_value() -> Generator[str]:
    return (item[0] for item in sorted(zip(COINS, VALUES), reverse=True, key=itemgetter(1)))


def coin_sum(coins: CoinBox) -> int:
    return sum(get_coin_value(coin) * count for coin, count in coins.items())


def get_currency() -> str:
    return CURRENCY


def add_coin_boxes(this: CoinBox, other: CoinBox) -> CoinBox:
    new_box = this.copy()
    for coin in new_box:
        new_box[coin] += other.get(coin, 0)
    return new_box
