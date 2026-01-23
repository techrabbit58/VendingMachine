import pytest

from .vendingmachine import VendingMachine, restock_all


@pytest.fixture
def vending_machine() -> VendingMachine:
    v = VendingMachine()
    restock_all(v, items_per_stock=1)
    return v


@pytest.fixture
def empty_vending_machine() -> VendingMachine:
    return VendingMachine()
