import pytest

from .conf import SELECTIONS, PRICES, ACCEPTABLE_COINS
from .lib import fewest_coins_that_match_exact_amount


def test_SELECTIONS_and_PRICES_must_match_in_length():
    assert len(SELECTIONS) == len(PRICES)


@pytest.mark.parametrize("price", PRICES.values())
def test_every_product_price_must_be_put_together_from_acceptable_coins(price):
    coin_sequence = fewest_coins_that_match_exact_amount(price)
    coin_sum = sum(ACCEPTABLE_COINS[coin] for coin in coin_sequence)
    assert coin_sum == price
