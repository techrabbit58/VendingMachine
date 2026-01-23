from functools import cache
from typing import Generator

from .conf import ACCEPTABLE_COINS, SELECTIONS, PRICES, PRODUCTS, CURRENCY


@cache
def check_coin(coin: str) -> int:
    return ACCEPTABLE_COINS.get(coin, 0)


@cache
def get_product_by_button(button: str) -> str | None:
    return SELECTIONS.get(button, None)


@cache
def get_price_by_product(product: str) -> int:
    return PRICES.get(product, 0)


def get_all_products() -> Generator[str]:
    yield from PRODUCTS


def fewest_coins_that_match_exact_amount(remaining: int) -> Generator[str]:
    coin_by_descending_value = (coin[0] for coin in sorted(ACCEPTABLE_COINS.items(), reverse=True, key=lambda x: x[1]))
    coin = next(coin_by_descending_value)
    value = ACCEPTABLE_COINS[coin]
    while remaining > 0:
        if value <= remaining:
            yield coin
            remaining -= value
        else:
            coin = next(coin_by_descending_value)
            value = ACCEPTABLE_COINS[coin]


def coin_sum(coins: list[str]) -> int:
    return sum(ACCEPTABLE_COINS[coin] for coin in coins)


def get_currency() -> str:
    return CURRENCY
