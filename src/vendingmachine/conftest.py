import pytest

from .vendingmachine import VendingMachine


@pytest.fixture
def vending_machine() -> VendingMachine:
    return VendingMachine()
