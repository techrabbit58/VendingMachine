import pytest

from .conf import BUTTONS, CURRENCY
from .lib import (
    get_price_by_product, get_product_by_button,
    fewest_coins_that_match_exact_amount
)


@pytest.mark.parametrize("button", BUTTONS)
def test_machine_tells_SOLD_OUT_if_selected_product_not_in_stock(empty_vending_machine, button):
    v = empty_vending_machine
    v.select_product(button)
    assert v.check_display() == "SOLD OUT"
    assert v.check_display() == "INSERT COIN"


@pytest.mark.parametrize("button", BUTTONS)
def test_machine_with_coins_tells_SOLD_OUT_if_selected_product_not_in_stock(empty_vending_machine, button):
    product = get_product_by_button(button)
    price = get_price_by_product(product)
    v = empty_vending_machine
    for coin in fewest_coins_that_match_exact_amount(price):
        v.insert_coin(coin)
    v.select_product(button)
    assert v.check_display() == "SOLD OUT"
    assert v.check_display() == f"{CURRENCY}{price / 100:.2f}"


@pytest.mark.parametrize("button1, button2", zip(BUTTONS, BUTTONS[1:] + BUTTONS[:1]))
def test_machine_allows_alternate_choice_if_out_of_stock(empty_vending_machine, button1, button2):
    v = empty_vending_machine
    v.stock[get_product_by_button(button1)] = 0
    v.stock[get_product_by_button(button2)] = 1
    v.select_product(button1)
    assert v.check_display() == "SOLD OUT"
    product = v.select_product(button2)
    price = get_price_by_product(product)
    assert v.check_display() == f"PRICE {CURRENCY}{price / 100:.2f}"


@pytest.mark.parametrize("button", BUTTONS)
def test_selling_a_product_reduces_stock(empty_vending_machine, button):
    v = empty_vending_machine
    product = get_product_by_button(button)
    price = get_price_by_product(product)
    v.stock[product] = 1
    for coin in fewest_coins_that_match_exact_amount(price):
        v.insert_coin(coin)
    v.select_product(button)
    assert v.hopper == [product]
    assert v.stock[product] == 0
