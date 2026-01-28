import pytest

from .conf import COINS


@pytest.mark.parametrize("coin", COINS)
def test_machine_shows_EXACT_CHANGE_ONLY_if_no_coins_of_any_kind(vending_machine, coin):
    v = vending_machine
    v.coin_box[coin] = 0
    v.reset_display()
    assert v.check_display() == "EXACT CHANGE ONLY"


def test_machine_does_not_sell_if_exact_change_and_change_not_possible():
    ...
