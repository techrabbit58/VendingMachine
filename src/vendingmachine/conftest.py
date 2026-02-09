import pytest

from .vendingmachine import VendingMachine, restock_products, refill_money_box


@pytest.fixture
def vending_machine() -> VendingMachine:
    v = VendingMachine()
    restock_products(v, items_per_stock=1)
    refill_money_box(v, items_per_coin=1)
    return v


@pytest.fixture
def empty_vending_machine() -> VendingMachine:
    v = VendingMachine()
    refill_money_box(v, items_per_coin=1)
    return v


@pytest.fixture
def empty_coin_box_vending_machine() -> VendingMachine:
    v = VendingMachine()
    restock_products(v, items_per_stock=1)
    for coin in v.coin_box:
        v.coin_box[coin] = 0
    return v
