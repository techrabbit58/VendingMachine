import pytest

from .conf import COINS
from .lib_dev import overpaid, overpayable_product_selections


@pytest.mark.parametrize("coin", COINS)
def test_machine_shows_EXACT_CHANGE_ONLY_if_no_coins_of_any_kind(vending_machine, coin):
    v = vending_machine
    v.coin_box[coin] = 0
    v.reset_display()
    assert v.check_display() == "EXACT CHANGE ONLY"


@pytest.mark.parametrize("button, price", overpayable_product_selections())
def test_machine_does_not_sell_if_exact_change_and_change_not_possible(
        empty_coin_box_vending_machine, button, price):

    v = empty_coin_box_vending_machine
    assert v.check_display() == "EXACT CHANGE ONLY"
    assert not v.hopper, "vending machine hopper initially empty"

    coin_sequence = overpaid(price)
    for coin, count in coin_sequence.items():
        for _ in range(count):
            v.insert_coin(coin)

    v.select_product(button)
    assert v.selected_product is None

    coins_inserted = (coin for coin, count in coin_sequence.items() for _ in range(count))
    assert sorted(v.coin_return) == sorted(coins_inserted), "return coins if machine cannot give change"
    assert not v.hopper, "vending machine hopper empty if no sale"


# TODO: missing test: number of coins in buffer decreases due to giving change
