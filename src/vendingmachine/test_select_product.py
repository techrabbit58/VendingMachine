from collections import defaultdict
from collections.abc import Generator

import pytest

from .conf import SELECTIONS, PRICES, BUTTONS, ACCEPTABLE_COINS
from .vendingmachine import VendingMachine


@pytest.fixture
def vending_machine() -> VendingMachine:
    return VendingMachine()


def valid_selections() -> Generator[dict[str, str]]:
    yield from SELECTIONS.items()


def selections_and_prices() -> Generator[tuple[str, int]]:
    for button, product in SELECTIONS.items():
        price = PRICES[product]
        yield button, price


def invalid_selections():
    yield "D"
    yield "invalid"


def test_SELECTIONS_and_PRICES_must_match_with_length():
    assert len(SELECTIONS) == len(PRICES)


@pytest.mark.parametrize("button, product", valid_selections())
def test_select_products_by_button_press_on_idle_machine(vending_machine, button, product):
    v = vending_machine
    selected_product = v.select_product(button)
    assert selected_product == product


@pytest.mark.parametrize("button", invalid_selections())
def test_invalid_buttons_selects_None(vending_machine, button):
    v = vending_machine
    v.select_product(button)
    assert v.selected_product is None


@pytest.mark.parametrize("button, price", selections_and_prices())
def test_machine_displays_PRICE_for_selected_product(vending_machine, button, price):
    v = vending_machine
    v.select_product(button)
    assert v.check_display() == f"PRICE ${price / 100:.2f}"


@pytest.mark.parametrize("button, price", selections_and_prices())
def test_mch_no_coins_reverts_to_INSERT_COIN_if_display_checked_multiple(vending_machine, button, price):
    v = vending_machine
    v.select_product(button)
    assert v.selected_product is None
    assert v.check_display() == f"PRICE ${price / 100:.2f}"
    assert v.check_display() == "INSERT COIN"


@pytest.mark.parametrize("button, price", selections_and_prices())
def test_mch_with_small_amount_reverts_to_previous_if_display_checked_multiple(vending_machine, button, price):
    v = vending_machine
    v.current_amount = 1
    first_display = v.check_display()
    v.select_product(button)
    assert v.selected_product is None
    assert v.check_display() == f"PRICE ${price / 100:.2f}"
    assert v.check_display() == first_display


def test_machine_display_changes_for_subsequent_selections(vending_machine):
    v = vending_machine
    for button in BUTTONS:
        product = v.select_product(button)
        assert v.check_display() == f"PRICE ${PRICES[product] / 100:.2f}"
    assert v.check_display() == "INSERT COIN"


def fewest_coins_that_match_exact_price(remaining: int) -> Generator[str]:
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


@pytest.mark.parametrize("button, price", selections_and_prices())
def test_machine_dispenses_selected_product_if_enough_coins(vending_machine, button, price):
    v = vending_machine
    product = v.select_product(button)
    coins_in_sequence = fewest_coins_that_match_exact_price(price)
    coins_inserted = defaultdict(int)
    for coin in coins_in_sequence:
        coins_inserted[coin] += 1
        v.insert_coin(coin)
        v.select_product(button)
    assert v.check_display() == "THANK YOU"
    assert v.check_display() == "INSERT COIN"
    assert v.hopper == [product]
    assert v.current_amount == 0
    assert v.selected_product is None
    assert v.coin_box == coins_inserted
