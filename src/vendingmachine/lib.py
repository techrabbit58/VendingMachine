import queue
import sys
from collections import deque
from functools import cache
from typing import Generator

from .conf import ACCEPTABLE_COINS, SELECTIONS, PRICES


@cache
def check_coin(coin: str) -> int:
    return ACCEPTABLE_COINS.get(coin, 0)


@cache
def get_product_by_button(button: str) -> str | None:
    return SELECTIONS.get(button, None)


@cache
def get_price_by_product(product: str) -> int:
    return PRICES.get(product, 0)


def fewest_coins_that_match_exact_amount(remaining: int) -> Generator[str]:
    coin_by_descending_value = (coin for coin in sorted(ACCEPTABLE_COINS, reverse=True))
    coin = next(coin_by_descending_value)
    value = ACCEPTABLE_COINS[coin]
    while remaining > 0:
        if value <= remaining:
            yield coin
            remaining -= value
        else:
            coin = next(coin_by_descending_value)
            value = ACCEPTABLE_COINS[coin]


class FiFo[T]:
    def __init__(self, name: str, maxsize: int | None = None):
        self.name = name
        self._maxsize = maxsize
        self.queue = deque() if maxsize is None else deque(maxlen=maxsize)

    def qsize(self) -> int:
        return len(self.queue)

    @property
    def maxsize(self) -> int:
        length = self._maxsize
        return length if length is not None else sys.maxsize

    def put(self, item: T) -> None:
        if self.qsize() >= self.maxsize:
            raise queue.Full(f"Queue {self.name} is full")
        self.queue.append(item)

    def get(self) -> T:
        if self.qsize() == 0:
            raise queue.Empty(f"Queue {self.name} is empty")
        return self.queue.popleft()
