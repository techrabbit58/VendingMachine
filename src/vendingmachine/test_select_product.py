from collections.abc import Generator

import pytest

from .conf import BUTTONS, CURRENCY, PRODUCTS
from .lib import get_price_by_product, coin_sum, get_product_by_button
from .lib_dev import button_and_price, fewest_coins_that_match_exact_amount


def valid_selections() -> Generator[tuple[str, str]]:
    for i, button in enumerate(BUTTONS):
        yield button, PRODUCTS[i]


def invalid_selections():
    yield "D"
    yield "invalid"


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


@pytest.mark.parametrize("button, price", button_and_price())
def test_machine_displays_PRICE_for_selected_product(vending_machine, button, price):
    v = vending_machine
    v.select_product(button)
    assert v.check_display() == f"PRICE {CURRENCY}{price / 100:.2f}"


@pytest.mark.parametrize("button, price", button_and_price())
def test_mch_no_coins_reverts_to_INSERT_COIN_if_display_checked_multiple(vending_machine, button, price):
    v = vending_machine
    v.select_product(button)
    assert v.selected_product is None
    assert v.check_display() == f"PRICE {CURRENCY}{price / 100:.2f}"
    assert v.check_display() == "INSERT COIN"


@pytest.mark.parametrize("button, price", button_and_price())
def test_mch_with_small_amount_reverts_to_previous_if_display_checked_multiple(vending_machine, button, price):
    v = vending_machine
    v.current_amount = 1
    first_display = v.check_display()
    v.select_product(button)
    assert v.selected_product is None
    assert v.check_display() == f"PRICE {CURRENCY}{price / 100:.2f}"
    assert v.check_display() == first_display


def test_machine_display_changes_for_subsequent_selections(vending_machine):
    v = vending_machine
    for button in BUTTONS:
        product = v.select_product(button)
        assert v.check_display() == f"PRICE {CURRENCY}{get_price_by_product(product) / 100:.2f}"
    assert v.check_display() == "INSERT COIN"


@pytest.mark.parametrize("button, price", button_and_price())
def test_machine_dispenses_selected_product_if_enough_coins(vending_machine, button, price):
    v = vending_machine
    product = v.select_product(button)
    coin_sequence = fewest_coins_that_match_exact_amount(price)
    for coin in coin_sequence:
        v.insert_coin(coin)
        v.select_product(button)
    assert v.check_display() == "THANK YOU"
    assert v.hopper == [product]


@pytest.mark.parametrize("button, price", button_and_price())
def test_machine_stores_payment_and_is_ready_for_next_after_selling(vending_machine, button, price):
    v = vending_machine
    coin_sequence = fewest_coins_that_match_exact_amount(price)
    for coin in coin_sequence:
        v.insert_coin(coin)
    v.select_product(button)
    v.check_display()
    assert v.check_display() == "INSERT COIN"
    assert v.selected_product is None
    assert v.current_amount == 0
    assert coin_sum(v.coin_buffer) == 0


@pytest.mark.parametrize("button, price", button_and_price())
def test_machine_has_one_less_product_after_selling(vending_machine, button, price):
    v = vending_machine
    product = get_product_by_button(button)
    initial_stock = v.stock[product]
    coin_sequence = fewest_coins_that_match_exact_amount(price)
    for coin in coin_sequence:
        v.insert_coin(coin)
    v.select_product(button)
    assert v.stock[product] == initial_stock - 1, "one less product on stock after sale"
