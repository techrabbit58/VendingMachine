import itertools

import pytest

from .conf import CURRENCY, COINS, INSERT_COIN
from .conftest import vending_machine
from .lib import coin_sum
from .lib_dev import valid_coins_and_values, invalid_coins


@pytest.mark.parametrize("actual_coin, expected_result", valid_coins_and_values())
def test_vending_machine_accepts_valid_coins(vending_machine, actual_coin, expected_result):
    v = vending_machine
    v.insert_coin(actual_coin)
    assert len(v.coin_buffer) > 0 and v.coin_buffer[actual_coin] == 1


@pytest.mark.parametrize("actual_coin", invalid_coins())
def test_vending_machine_rejects_invalid_coins(vending_machine, actual_coin):
    v = vending_machine
    v.insert_coin(actual_coin)
    assert len(v.coin_return) > 0 and v.coin_return[0] == actual_coin


@pytest.mark.parametrize("coins", itertools.permutations(COINS))
def test_vending_machine_accumulates_inserted_coin_values(vending_machine, coins):
    for coin in coins:
        vending_machine.insert_coin(coin)
    assert vending_machine.current_amount == coin_sum(vending_machine.coin_buffer)


def test_idle_vending_machine_displays_INSERT_COIN(vending_machine):
    v = vending_machine
    assert v.current_amount == 0 and v.display == INSERT_COIN


@pytest.mark.parametrize("actual_coin, expected_result", valid_coins_and_values())
def test_insert_valid_coin_updates_display(vending_machine, actual_coin, expected_result):
    v = vending_machine
    assert v.check_display() == INSERT_COIN
    v.insert_coin(actual_coin)
    assert v.check_display() == f"{CURRENCY}{expected_result / 100:.2f}"


@pytest.mark.parametrize("first_coin, second_coin", [
    (None, "penny"),
    ("penny", "penny"),
    ("dime", "penny"),
])
def test_invalid_coin_return_does_no_change_state(vending_machine, first_coin, second_coin):
    v = vending_machine
    if first_coin is not None:
        v.insert_coin(first_coin)
    old_state = v.current_amount, v.check_display()
    v.insert_coin(second_coin)
    assert (v.current_amount, v.check_display()) == old_state and len(v.coin_return) > 0
