import pytest

from .conf import COINS, EXACT_CHANGE_ONLY
from .lib import get_coin_value, coin_sum, add_coin_boxes
from .lib_dev import overpaid, overpayable_product_selections, fewest_coins_that_match_exact_amount


@pytest.mark.parametrize("coin", COINS)
def test_machine_shows_EXACT_CHANGE_ONLY_if_no_coins_of_any_kind(vending_machine, coin):
    v = vending_machine
    v.coin_box[coin] = 0
    v.reset_display()
    assert v.check_display() == EXACT_CHANGE_ONLY


@pytest.mark.parametrize("button, price", overpayable_product_selections())
def test_machine_does_not_sell_if_exact_change_and_change_not_possible(
        empty_coin_box_vending_machine, button, price):
    v = empty_coin_box_vending_machine
    assert v.check_display() == EXACT_CHANGE_ONLY
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


@pytest.mark.parametrize("button, price", overpayable_product_selections())
def test_machine_gives_change_from_coin_box(vending_machine, button, price):
    v = vending_machine
    assert not v.hopper, "vending machine hopper initially empty"
    assert not v.coin_return, "coin return initially empty"

    initial_coin_sum = coin_sum(add_coin_boxes(v.coin_box, v.coin_buffer))

    coin_sequence = overpaid(price)
    payment = 0
    for coin, count in coin_sequence.items():
        for _ in range(count):
            v.insert_coin(coin)
            payment += get_coin_value(coin)

    product = v.select_product(button)
    assert v.hopper == [product], "machine gave expected product"

    change = fewest_coins_that_match_exact_amount(payment - price)
    actual_change = sum(get_coin_value(coin) for coin in v.coin_return)
    expected_change = sum(get_coin_value(coin) for coin in change)
    assert actual_change == expected_change, "machine gave expected change"

    new_coin_sum = coin_sum(add_coin_boxes(v.coin_box, v.coin_buffer))
    assert coin_sum(v.coin_buffer) == 0, "coin buffer is empty after sale"
    assert new_coin_sum == initial_coin_sum + price, "payment taken, change given from coin box"
